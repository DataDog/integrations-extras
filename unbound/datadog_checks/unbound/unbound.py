import os
import re


from datadog_checks.checks import AgentCheck
from datadog_checks.utils.subprocess_output import get_subprocess_output


EVENT_TYPE = 'unbound'


class UnboundCheck(AgentCheck):
    # Stats info https://unbound.net/documentation/unbound-control.html

    UNBOUND_CTL = ['unbound-control', 'stats']

    def __init__(self, name, init_config, agentConfig, instances=None):
        if instances is not None and len(instances) > 1:
            raise ConfigurationError('Disk check only supports one configured instance.')
        AgentCheck.__init__(self, name, init_config, agentConfig, instances=instances)

        self.host = instances[0].get('host')
        self.tags = instances[0].get('tags', [])

    def check(self, instance):

        """
        Example of unbound stats outpout:
        total.num.queries=12
        mem.cache.rrset=0
        num.query.type.A=4
        unwanted.queries=3
        ...
        """

        test_sudo = os.system('setsid sudo -l < /dev/null')
        if test_sudo != 0:
            raise Exception('The dd-agent user does not have sudo access')
        else:
            self.UNBOUND_CTL = self.UNBOUND_CTL.insert(0, "sudo")
            try:
                ub_out, _, _ = get_subprocess_output(self.UNBOUND_CTL + ['-s', self.host], self.log)
                self.log.debug(ub_out)
            except Exception as e:
                raise Exception("Unable to get unbound stats: {}".format(str(e)))

            # [(u'thread0.num.queries', u'12'), (u'thread0.num.queries_ip_ratelimited', u'45')...]
            data = re.findall(r'(\S+)=(.*\d)', ub_out)

            for stat in data:
                if 'histogram' in stat[0]:  # dont send histogram metrics
                    self.log.debug('unbound.{}:{}'.format(stat[0], stat[1]))
                else:
                    if ['num.', 'unwanted'] in stat[0]:
                        self.rate('unbound.{}'.format(stat[0]), float(stat[1]), tags=self.tags)
                    elif 'time.' in stat[0]:
                        self.gauge('unbound.{}'.format(stat[0]), float(stat[1]), tags=self.tags)
                    else:
                        self.gauge('unbound.{}'.format(stat[0]), float(stat[1]), tags=self.tags)
