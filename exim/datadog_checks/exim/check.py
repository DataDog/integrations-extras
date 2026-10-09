import re
import shlex
import shutil
from collections import namedtuple
from typing import Any  # noqa: F401

from datadog_checks.base import AgentCheck, is_affirmative
from datadog_checks.base.utils.subprocess_output import get_subprocess_output

# Printed between the plain and the `exiqsumm -f` summary; never part of exiqsumm output.
FROZEN_SUMMARY_MARKER = '@@exiqsumm-f@@'
DEFAULT_EXIM_PATH = '/usr/sbin/exim'
DEFAULT_EXIQSUMM_PATH = '/usr/sbin/exiqsumm'
# systemd unit names probed when `service_name` is not set: Debian/Ubuntu, then Red Hat based systems.
DEFAULT_SERVICE_NAMES = ('exim4', 'exim')


class EximCheck(AgentCheck):
    # This will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = 'exim'

    SERVICE_CHECK_NAME = 'returns.output'
    SERVICE_RUNNING_CHECK_NAME = 'service.running'

    def __init__(self, name, init_config, instances):
        super(EximCheck, self).__init__(name, init_config, instances)

    def check(self, _):
        # type: (Any) -> None

        config = self._get_config()

        tags = config['tags']
        try:
            queue_stats, frozen_stats = self._get_queue_summaries()
            frozen_counts = self._get_frozen_counts(queue_stats, frozen_stats)
            for queue in queue_stats:
                if frozen_counts is not None:
                    self.gauge(
                        'queue.frozen.count', frozen_counts.get(queue.Domain, 0), tags=tags + [f'domain:{queue.Domain}']
                    )
                self.gauge('queue.count', int(queue.Count), tags=tags + [f'domain:{queue.Domain}'])
                self.gauge('queue.volume', self.parse_size(queue.Volume), tags=tags + [f'domain:{queue.Domain}'])
                oldest_age = self.parse_age(queue.Oldest)
                if oldest_age is None:
                    self.log.debug('Cannot parse the Oldest value %r for domain %s', queue.Oldest, queue.Domain)
                else:
                    self.gauge('queue.oldest_age', oldest_age, tags=tags + [f'domain:{queue.Domain}'])
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.OK, tags)
        except Exception as e:
            self.log.warning("Cannot get exim queue info: %s", e)
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.CRITICAL, tags, message=str(e))

        self._check_service_running(tags, config['service_name'])

    def _get_config(self):
        tags = self.instance.get('tags', [])
        instance_config = {
            'tags': tags,
            'exim_path': self.instance.get('exim_path', DEFAULT_EXIM_PATH),
            'exiqsumm_path': self.instance.get('exiqsumm_path', DEFAULT_EXIQSUMM_PATH),
            'use_sudo': is_affirmative(self.instance.get('use_sudo', False)),
            'service_name': self.instance.get('service_name') or None,
        }
        return instance_config

    def _check_service_running(self, tags, service_name):
        """
        Submit `exim.service.running` based on the state of the Exim systemd unit.

        Any error results in UNKNOWN and never affects the queue metrics collected before.
        """
        try:
            status, message = self._get_service_status(service_name)
        except Exception as e:
            status, message = AgentCheck.UNKNOWN, 'Cannot determine the state of the Exim service: {}'.format(e)
        if status != AgentCheck.OK:
            self.log.warning(message)
        self.service_check(
            self.SERVICE_RUNNING_CHECK_NAME, status, tags, message=message if status != AgentCheck.OK else None
        )

    def _get_service_status(self, service_name):
        """
        Return the service check status and message for the Exim systemd unit.

        `systemctl show` is used instead of `systemctl is-active`, which reports a stopped unit and a
        nonexistent unit the same way. A unit whose LoadState is `not-found` does not exist, so the next
        candidate is tried.
        """
        systemctl = shutil.which('systemctl')
        if systemctl is None:
            return AgentCheck.UNKNOWN, '`systemctl` was not found; this service check requires systemd'

        candidates = [service_name] if service_name else list(DEFAULT_SERVICE_NAMES)
        for unit in candidates:
            command = [systemctl, 'show', '-p', 'LoadState,ActiveState', unit]
            output, err, returncode = get_subprocess_output(command, self.log, raise_on_empty_output=False)
            if returncode != 0:
                return AgentCheck.UNKNOWN, 'Command `{}` exited with status {}: {}'.format(
                    ' '.join(command), returncode, (err or '').strip()
                )

            properties = dict(line.split('=', 1) for line in (output or '').splitlines() if '=' in line)
            load_state = properties.get('LoadState')
            active_state = properties.get('ActiveState')
            if not load_state or not active_state:
                return AgentCheck.UNKNOWN, 'Unexpected output from `{}`: {!r}'.format(' '.join(command), output)
            if load_state == 'not-found':
                continue
            if active_state == 'active':
                return AgentCheck.OK, None
            return AgentCheck.CRITICAL, 'Exim unit `{}` is {} (LoadState={})'.format(unit, active_state, load_state)

        return AgentCheck.UNKNOWN, 'No Exim systemd unit found (tried: {}); set `service_name` to the unit name'.format(
            ', '.join(candidates)
        )

    def _build_command(self):
        """
        Build the argv used to collect the queue summary.

        `exiqsumm` only reads `exim -bp` output from stdin, so the two commands have to be
        connected with a pipe, which requires a shell. The exit status of a plain pipeline is
        the status of its last command, so a failing `exim -bp` (for example a permission
        error when `queue_list_requires_admin` is enabled) would be masked by a successful
        `exiqsumm` run that prints an empty summary. The script therefore captures the output
        of `exim -bp` first and exits with its status when it fails. `set -o pipefail` is not
        used because it is not available in every `/bin/sh` (for example dash).

        `sudo -n` makes sudo fail immediately instead of prompting for a password when no
        matching NOPASSWD rule exists; its error message ends up in the service check.

        The captured output is summarized twice: as is, and with `exiqsumm -f`, which moves
        recipients of frozen messages to separate `<domain> (f)` rows. Both summaries come from
        a single `exim -bp` run, so the spool is only scanned once.
        """
        config = self._get_config()
        exim_command = f'{shlex.quote(config["exim_path"])} -bp'
        if config['use_sudo']:
            exim_command = f'sudo -n {exim_command}'
        exiqsumm_command = shlex.quote(config['exiqsumm_path'])
        script = (
            f'out=$({exim_command}) || exit $?; '
            f'printf \'%s\\n\' "$out" | {exiqsumm_command} && '
            f'echo {FROZEN_SUMMARY_MARKER} && '
            f'printf \'%s\\n\' "$out" | {exiqsumm_command} -f'
        )
        return ['/bin/sh', '-c', script]

    def _get_queue_stats(self):
        return self._get_queue_summaries()[0]

    def _get_queue_summaries(self):
        """
        Run the command and return the rows of the plain summary and of the `exiqsumm -f`
        summary. The latter is None when the output does not contain it.
        """
        command = self._build_command()
        # exiqsumm always prints a header and a TOTAL row, so empty output means the pipeline
        # itself did not run and must be treated as a failure.
        output, err, returncode = get_subprocess_output(command, self.log, raise_on_empty_output=True)
        if returncode != 0:
            raise Exception(
                'Command `{}` exited with status {}: {}'.format(command[2], returncode, (err or '').strip())
            )

        lines = output.splitlines()
        if FROZEN_SUMMARY_MARKER in lines:
            index = lines.index(FROZEN_SUMMARY_MARKER)
            return self._parse_summary(lines[:index]), self._parse_summary(lines[index + 1 :])
        return self._parse_summary(lines), None

    @staticmethod
    def _parse_summary(lines):
        # sample output
        '''
        Count  Volume  Oldest  Newest  Domain
        -----  ------  ------  ------  ------
           11   495KB     14h     14h  gmail.com
           20   900KB     14h     14h  homtail.com
          154  6930KB     14h     14h  yahoo.com
        '''
        header = []
        data = []
        for line in filter(None, lines):
            if '----' in line:
                continue
            if not header:
                header = line.split()
                queue = namedtuple('Queue', header)
                continue
            # The last column can contain a space with `exiqsumm -f`, for example `gmail.com (f)`.
            line_contents = line.split(None, len(header) - 1)
            if line_contents:
                data.append(queue(*line_contents))
        return data

    def _get_frozen_counts(self, queue_stats, frozen_stats):
        """
        Return the number of recipients of frozen messages per domain, including TOTAL.

        `exiqsumm -f` splits each domain into a `<domain>` row for recipients of messages that
        are not frozen and a `<domain> (f)` row for frozen ones. The frozen count is derived as
        the plain count minus the not-frozen count instead of reading the `(f)` rows, because
        exiqsumm truncates the domain column to 80 characters, which cuts the ` (f)` suffix off
        domains longer than 76 characters. The derivation stays exact up to 78 characters;
        beyond that both rows collapse into one and the frozen count can only be too low.
        """
        if frozen_stats is None:
            self.log.warning('The `exiqsumm -f` summary is missing from the output, skipping exim.queue.frozen.count')
            return None

        not_frozen = {}
        for row in frozen_stats:
            not_frozen[row.Domain] = not_frozen.get(row.Domain, 0) + int(row.Count)

        counts = {}
        for row in queue_stats:
            if row.Domain != 'TOTAL':
                counts[row.Domain] = max(0, int(row.Count) - not_frozen.get(row.Domain, 0))
        counts['TOTAL'] = sum(counts.values())
        return counts

    @staticmethod
    def parse_size(size_string):
        """
        Convert a Volume value printed by exiqsumm to bytes.

        exiqsumm prints plain bytes below 10000 and otherwise rounds to KB or MB using
        1024-based units (see `print_volume_rounded` in exiqsumm).
        """
        match = re.match(r"([0-9]+)([a-z]+)", size_string, re.I)
        if match:
            number, unit = match.groups()
        else:
            number, unit = size_string, 'B'
        units = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3, "TB": 1024**4}
        return int(float(number) * units[unit.upper()])

    @staticmethod
    def parse_age(age_string):
        """
        Convert an Oldest/Newest value printed by exiqsumm to seconds, or return None.

        exiqsumm copies the age from `exim -bp`, which prints whole minutes up to 90 minutes,
        rounded hours up to 72 hours and rounded days beyond that (for example `5m`, `14h`, `4d`,
        `100d`). On an empty queue exiqsumm prints `0m` as the oldest and `0000d` as the newest
        age. Seconds and weeks are never printed but are accepted for robustness.
        """
        match = re.match(r'^(\d+)([smhdw])$', (age_string or '').strip())
        if not match:
            return None
        number, unit = match.groups()
        units = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400, 'w': 604800}
        return int(number) * units[unit]
