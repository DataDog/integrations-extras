from six.moves.urllib.parse import urlparse

from datadog_checks.base import AgentCheck, ConfigurationError


class PhpApcuCheck(AgentCheck):
    def check(self, instance):
        url = instance.get('url')
        if not url:
            raise ConfigurationError('The `url` must be specified')

        tags = instance.get('tags', [])
        # https://github.com/DataDog/integrations-core/blob/master/apache/datadog_checks/apache/apache.py#L53
        parsed_url = urlparse(url)
        server_host = parsed_url.hostname
        server_port = parsed_url.port or 80
        service_check_tags = ['host:%s' % server_host, 'port:%s' % server_port] + tags

        self.log.debug('apcu check url[%s]', url)

        try:
            response = self.http.get(url)
            response.raise_for_status()
        except Exception as e:
            self.service_check('php_apcu.can_connect', self.CRITICAL, tags=service_check_tags, message=str(e))
        else:
            self.service_check('php_apcu.can_connect', self.OK)
            for line in response.iter_lines(decode_unicode=True):
                values = line.split(' ')
                if len(values) == 2:
                    metric, value = values
                    try:
                        value = float(value)
                    except ValueError:
                        continue
                    self.gauge(metric, value, tags=tags)
                else:
                    self.log.debug("Unexpected response: %s", values)
