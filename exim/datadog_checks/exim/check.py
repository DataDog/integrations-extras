import re
from collections import namedtuple
from typing import Any

from datadog_checks.base import AgentCheck
from datadog_checks.base.utils.subprocess_output import get_subprocess_output


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
            self.log.info("Cannot get exim queue info: %s", e)
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.CRITICAL, tags, message=str(e))

    def _get_config(self):
        tags = self.instance.get('tags', [])
        instance_config = {
            'tags': tags,
        }
        return instance_config

    def _get_queue_stats(self):

        command = ['exim -bp', '|', 'exiqsumm']
        output, _, _ = get_subprocess_output(command, self.log, False)

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
        match = re.match(r"([0-9]+)([a-z]+)", size_string, re.I)
        if match:
            number, unit = match.groups()
        else:
            number, unit = size_string, 'B'
        units = {"B": 1, "KB": 10**3, "MB": 10**6, "GB": 10**9, "TB": 10**12}
        return int(float(number) * units[unit])
