import re
import shlex
import shutil
from collections import namedtuple

from datadog_checks.base import AgentCheck, ConfigurationError, is_affirmative
from datadog_checks.base.utils.subprocess_output import get_subprocess_output

# Printed between the summaries in the command output; never part of exiqsumm output itself.
# Each extra summary separates one kind of message into `<domain> (x)` rows: -f frozen, -b bounces.
SEPARATED_SUMMARIES = (('frozen', '-f', '@@exiqsumm-f@@'), ('bounce', '-b', '@@exiqsumm-b@@'))
DEFAULT_EXIM_PATH = '/usr/sbin/exim'
DEFAULT_EXIQSUMM_PATH = '/usr/sbin/exiqsumm'
# systemd unit names probed when `service_name` is not set: Debian/Ubuntu, then Red Hat based systems.
DEFAULT_SERVICE_NAMES = ('exim4', 'exim')
# Domains beyond `max_domains` (ordered by queued recipients) are aggregated under this tag value.
DEFAULT_MAX_DOMAINS = 100
OTHER_DOMAIN = 'other'
TOTAL_DOMAIN = 'TOTAL'
# Exim versions have two parts (4.97) and sometimes a third (4.94.2), which semver would reject.
VERSION_PATTERN = r'^(?P<major>\d+)\.(?P<minor>\d+)(?:\.(?P<patch>\d+))?$'


class EximCheck(AgentCheck):
    # This will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = 'exim'

    SERVICE_CHECK_NAME = 'returns.output'
    SERVICE_RUNNING_CHECK_NAME = 'service.running'

    def check(self, _):
        config = self._get_config()

        tags = config['tags']
        try:
            queue_stats, separated_stats = self._get_queue_summaries()
            separated_counts = {
                kind: self._get_separated_counts(queue_stats, separated_stats.get(kind), kind)
                for kind, _, _ in self._enabled_summaries(config)
            }
            rows = self._collect_rows(queue_stats, separated_counts)
            self.gauge('queue.domains', sum(1 for row in rows if row['domain'] != TOTAL_DOMAIN), tags=tags)
            if config['collect_domain_metrics']:
                rows = self._limit_domains(rows, config['max_domains'])
            else:
                # Only the TOTAL row: a fixed number of time series regardless of the queue contents.
                rows = [row for row in rows if row['domain'] == TOTAL_DOMAIN]
            for row in rows:
                domain_tags = tags + [f"domain:{row['domain']}"]
                self.gauge('queue.count', row['count'], tags=domain_tags)
                self.gauge('queue.volume', row['volume'], tags=domain_tags)
                if config['collect_oldest_age'] and row['oldest_age'] is not None:
                    self.gauge('queue.oldest_age', row['oldest_age'], tags=domain_tags)
                for kind, value in row['separated'].items():
                    self.gauge(f'queue.{kind}.count', value, tags=domain_tags)
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.OK, tags)
        except Exception as e:
            self.log.warning("Cannot get exim queue info: %s", e)
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.CRITICAL, tags, message=str(e))

        if config['collect_service_running']:
            self._check_service_running(tags, config['service_name'])
        if config['collect_version_metadata']:
            self._collect_version(config['exim_path'])

    def _get_config(self):
        tags = self.instance.get('tags', [])
        instance_config = {
            'tags': tags,
            'exim_path': self.instance.get('exim_path', DEFAULT_EXIM_PATH),
            'exiqsumm_path': self.instance.get('exiqsumm_path', DEFAULT_EXIQSUMM_PATH),
            'use_sudo': is_affirmative(self.instance.get('use_sudo', False)),
            'service_name': self.instance.get('service_name') or None,
            'max_domains': int(self.instance.get('max_domains', DEFAULT_MAX_DOMAINS)),
            # Feature toggles; a disabled feature also skips the work behind it.
            'collect_domain_metrics': is_affirmative(self.instance.get('collect_domain_metrics', True)),
            'collect_oldest_age': is_affirmative(self.instance.get('collect_oldest_age', True)),
            'collect_frozen_count': is_affirmative(self.instance.get('collect_frozen_count', True)),
            'collect_bounce_count': is_affirmative(self.instance.get('collect_bounce_count', True)),
            'collect_service_running': is_affirmative(self.instance.get('collect_service_running', True)),
            'collect_version_metadata': is_affirmative(self.instance.get('collect_version_metadata', True)),
        }
        if instance_config['max_domains'] < 0:
            raise ConfigurationError('`max_domains` must be 0 (no limit) or a positive number')
        return instance_config

    def _enabled_summaries(self, config):
        return [item for item in SEPARATED_SUMMARIES if config[f'collect_{item[0]}_count']]

    def _collect_rows(self, queue_stats, separated_counts):
        """
        Turn the exiqsumm rows into dicts with parsed values: count, volume in bytes, oldest age in
        seconds (None when unparseable) and the separated counts (frozen, bounce) that are available.
        """
        rows = []
        for queue in queue_stats:
            oldest_age = self.parse_age(queue.Oldest)
            if oldest_age is None:
                self.log.debug('Cannot parse the Oldest value %r for domain %s', queue.Oldest, queue.Domain)
            rows.append(
                {
                    'domain': queue.Domain,
                    'count': int(queue.Count),
                    'volume': self.parse_size(queue.Volume),
                    'oldest_age': oldest_age,
                    'separated': {
                        kind: counts.get(queue.Domain, 0)
                        for kind, counts in separated_counts.items()
                        if counts is not None
                    },
                }
            )
        return rows

    @staticmethod
    def _limit_domains(rows, max_domains):
        """
        Keep the `max_domains` domains with the most queued recipients and aggregate the rest into
        one `other` row, so the number of `domain` tag values (and therefore of time series) stays
        bounded on relays that queue mail for many domains. TOTAL is passed through unchanged and
        0 disables the limit.
        """
        total = [row for row in rows if row['domain'] == TOTAL_DOMAIN]
        domains = sorted(
            (row for row in rows if row['domain'] != TOTAL_DOMAIN), key=lambda r: (-r['count'], r['domain'])
        )
        if not max_domains or len(domains) <= max_domains:
            return domains + total

        kept, rest = domains[:max_domains], domains[max_domains:]
        ages = [row['oldest_age'] for row in rest if row['oldest_age'] is not None]
        other = {
            'domain': OTHER_DOMAIN,
            'count': sum(row['count'] for row in rest),
            'volume': sum(row['volume'] for row in rest),
            'oldest_age': max(ages) if ages else None,
            'separated': {kind: sum(row['separated'].get(kind, 0) for row in rest) for kind in rest[0]['separated']},
        }
        return kept + [other] + total

    def _collect_version(self, exim_path):
        """
        Submit the Exim version as check metadata. `exim -bV` needs no privileges; its first line
        reads `Exim version 4.97 #2 built 22-Sep-2026 18:24:17`.
        """
        try:
            output, err, returncode = get_subprocess_output([exim_path, '-bV'], self.log, raise_on_empty_output=False)
            match = re.search(r'^Exim version (\d+(?:\.\d+)+)', output or '', re.M)
            if returncode != 0 or not match:
                self.log.debug('Cannot determine the Exim version (status %s): %r %r', returncode, output, err)
                return
            self.set_metadata('version', match.group(1), scheme='regex', pattern=VERSION_PATTERN)
        except Exception as e:
            self.log.debug('Cannot determine the Exim version: %s', e)

    def _check_service_running(self, tags, service_name):
        """
        Submit `exim.service.running` based on the state of the Exim systemd unit.

        Any error results in UNKNOWN and never affects the queue metrics collected before.
        """
        try:
            status, message = self._get_service_status(service_name)
        except Exception as e:
            status, message = AgentCheck.UNKNOWN, 'Cannot determine the state of the Exim service: {}'.format(e)
        if status == AgentCheck.CRITICAL:
            self.log.warning(message)
        elif status == AgentCheck.UNKNOWN:
            # Expected on hosts without systemd (the status already says so), so do not warn on every run.
            self.log.debug(message)
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

    def _command_parts(self):
        config = self._get_config()
        exim_command = f'{shlex.quote(config["exim_path"])} -bp'
        if config['use_sudo']:
            exim_command = f'sudo -n {exim_command}'
        return exim_command, shlex.quote(config['exiqsumm_path'])

    def _command_description(self):
        # Short form for log and service check messages; the full script is in _build_command().
        return ' | '.join(self._command_parts())

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

        The captured output is summarized several times: as is, with `exiqsumm -f`, which moves
        recipients of frozen messages to separate `<domain> (f)` rows, and with `exiqsumm -b`,
        which does the same for bounce messages as `<domain> (b)` rows. All summaries come from
        a single `exim -bp` run, so the spool is only scanned once.
        """
        config = self._get_config()
        exim_command, exiqsumm_command = self._command_parts()
        script = f'out=$({exim_command}) || exit $?; printf \'%s\\n\' "$out" | {exiqsumm_command}'
        for _, option, marker in self._enabled_summaries(config):
            script += f' && echo {marker} && printf \'%s\\n\' "$out" | {exiqsumm_command} {option}'
        return ['/bin/sh', '-c', script]

    def _get_queue_stats(self):
        return self._get_queue_summaries()[0]

    def _get_queue_summaries(self):
        """
        Run the command and return the rows of the plain summary and a dict with the rows of each
        separated summary by kind (`frozen`, `bounce`). A kind is missing when its summary is not
        in the output.
        """
        command = self._build_command()
        # raise_on_empty_output is False on purpose: on the Agent the error it raises never carries
        # stderr, so the reason (for example `sudo: a password is required`) would be lost. Empty
        # output is still a failure, because exiqsumm always prints a header and a TOTAL row.
        output, err, returncode = get_subprocess_output(command, self.log, raise_on_empty_output=False)
        err = (err or '').strip()
        description = self._command_description()
        if returncode != 0:
            raise Exception('`{}` exited with status {}: {}'.format(description, returncode, err))
        if not output:
            raise Exception('`{}` produced no output{}'.format(description, ': ' + err if err else ''))

        sections = {None: []}
        current = None
        markers = {marker: kind for kind, _, marker in SEPARATED_SUMMARIES}
        for line in output.splitlines():
            if line in markers:
                current = markers[line]
                sections[current] = []
            else:
                sections[current].append(line)
        separated = {kind: self._parse_summary(lines) for kind, lines in sections.items() if kind is not None}
        return self._parse_summary(sections[None]), separated

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

    def _get_separated_counts(self, queue_stats, separated_stats, kind):
        """
        Return the number of recipients of frozen (or bounce) messages per domain, including TOTAL.

        `exiqsumm -f` (or `-b`) splits each domain into a `<domain>` row for recipients of messages
        that are not frozen (not bounces) and a `<domain> (f)` (`<domain> (b)`) row for the others.
        The count is derived as the plain count minus the `<domain>` row instead of reading the
        suffixed rows, because exiqsumm truncates the domain column to 80 characters, which cuts
        the suffix off domains longer than 76 characters. The derivation stays exact up to 78
        characters; beyond that both rows collapse into one and the count can only be too low.
        """
        if separated_stats is None:
            self.log.warning(
                'The `exiqsumm` %s summary is missing from the output, skipping exim.queue.%s.count', kind, kind
            )
            return None

        plain = {}
        for row in separated_stats:
            plain[row.Domain] = plain.get(row.Domain, 0) + int(row.Count)

        counts = {}
        for row in queue_stats:
            if row.Domain != TOTAL_DOMAIN:
                counts[row.Domain] = max(0, int(row.Count) - plain.get(row.Domain, 0))
        counts[TOTAL_DOMAIN] = sum(counts.values())
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
