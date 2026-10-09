import re
import shlex
from collections import namedtuple
from typing import Any  # noqa: F401

from datadog_checks.base import AgentCheck, is_affirmative
from datadog_checks.base.utils.subprocess_output import get_subprocess_output

DEFAULT_EXIM_PATH = '/usr/sbin/exim'
DEFAULT_EXIQSUMM_PATH = '/usr/sbin/exiqsumm'


class EximCheck(AgentCheck):
    # This will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = 'exim'

    SERVICE_CHECK_NAME = 'returns.output'

    def __init__(self, name, init_config, instances):
        super(EximCheck, self).__init__(name, init_config, instances)

    def check(self, _):
        # type: (Any) -> None

        config = self._get_config()

        tags = config['tags']
        try:
            queue_stats = self._get_queue_stats()
            for queue in queue_stats:
                self.gauge('queue.count', int(queue.Count), tags=tags + [f'domain:{queue.Domain}'])
                self.gauge('queue.volume', self.parse_size(queue.Volume), tags=tags + [f'domain:{queue.Domain}'])
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.OK, tags)
        except Exception as e:
            self.log.warning("Cannot get exim queue info: %s", e)
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.CRITICAL, tags, message=str(e))

    def _get_config(self):
        tags = self.instance.get('tags', [])
        instance_config = {
            'tags': tags,
            'exim_path': self.instance.get('exim_path', DEFAULT_EXIM_PATH),
            'exiqsumm_path': self.instance.get('exiqsumm_path', DEFAULT_EXIQSUMM_PATH),
            'use_sudo': is_affirmative(self.instance.get('use_sudo', False)),
        }
        return instance_config

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
        """
        config = self._get_config()
        exim_command = f'{shlex.quote(config["exim_path"])} -bp'
        if config['use_sudo']:
            exim_command = f'sudo -n {exim_command}'
        exiqsumm_command = shlex.quote(config['exiqsumm_path'])
        script = f'out=$({exim_command}) || exit $?; printf \'%s\\n\' "$out" | {exiqsumm_command}'
        return ['/bin/sh', '-c', script]

    def _get_queue_stats(self):
        command = self._build_command()
        # exiqsumm always prints a header and a TOTAL row, so empty output means the pipeline
        # itself did not run and must be treated as a failure.
        output, err, returncode = get_subprocess_output(command, self.log, raise_on_empty_output=True)
        if returncode != 0:
            raise Exception(
                'Command `{}` exited with status {}: {}'.format(command[2], returncode, (err or '').strip())
            )

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
        for line in filter(None, output.splitlines()):
            if '----' in line:
                continue
            if not header:
                header = line.split()
                queue = namedtuple('Queue', header)
                continue
            line_contents = line.split()
            if line_contents:
                data.append(queue(*line_contents))
        return data

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
