import requests

from datadog_checks.base import AgentCheck, ConfigurationError


class PhpApcuCheck(AgentCheck):
    def check(self, instance):
        url = instance.get('url')
        if not url:
            raise ConfigurationError('require url.')

        self.log.debug('apcu check url[%s]', url)

        try:
            response = requests.get(url)
            response.raise_for_status()
        except Exception as e:
            self.service_check('php_apcu.can_collect', self.CRITICAL, message=str(e))
        else:
            self.service_check('php_apcu.can_collect', self.OK)
            for line in response.iter_lines(decode_unicode=True):
                values = line.split(' ')
                if len(values) == 2:
                    metric, value = values
                    try:
                        value = float(value)
                    except ValueError:
                        continue
                    self.gauge(metric, value)
