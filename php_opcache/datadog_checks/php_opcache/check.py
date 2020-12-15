from datadog_checks.base import AgentCheck, ConfigurationError


class PhpOpcacheCheck(AgentCheck):
    def check(self, instance):
        url = instance.get('url')
        if not url:
            raise ConfigurationError('The `url` must be specified')

        self.log.debug('opcache check url[%s]', url)

        try:
            response = self.http.get(url)
            response.raise_for_status()
        except Exception as e:
            self.service_check('php_opcache .can_connect', self.CRITICAL, message=str(e))
        else:
            self.service_check('php_opcache.can_connect', self.OK)
            for line in response.iter_lines(decode_unicode=True):
                values = line.split(' ')
                if len(values) == 2:
                    metric, value = values
                    try:
                        value = float(value)
                    except ValueError:
                        continue
                    self.gauge(metric, value)
                else:
                    self.log.debug("Unexpected response: %s", values)
