import simplejson as json
from six.moves.urllib.parse import urlparse

from datadog_checks.base import AgentCheck, ConfigurationError

METRICS = [
    ('backlog', 'backlog', AgentCheck.gauge),
    ('booted_workers', 'booted_workers', AgentCheck.gauge),
    ('max_threads', 'max_threads', AgentCheck.gauge),
    ('pool_capacity', 'pool_capacity', AgentCheck.gauge),
    ('requests_count', 'requests_count', AgentCheck.gauge),
    ('running', 'running', AgentCheck.gauge),
    ('workers', 'workers', AgentCheck.gauge),
]


class PumaCheck(AgentCheck):
    def check(self, instance):
        control_url = instance.get('control_url')
        if control_url is None:
            raise ConfigurationError('Puma instance missing "control_url" value')

        tags = instance.get('tags', [])
        response, content_type, version = self._perform_service_check(instance, control_url)
        metrics = self._extract_metrics(response)

        for (key, name, reporter) in METRICS:
            reporter(self, 'puma.{}'.format(name), metrics[key], tags)

    def _extract_metrics(self, response):
        metrics = {
            'backlog': 0,
            'booted_workers': 0,
            'max_threads': 0,
            'pool_capacity': 0,
            'requests_count': 0,
            'running': 0,
            'workers': 0,
        }

        if 'workers' in response:  # Puma is clustered
            metrics['booted_workers'] = int(response.get('booted_workers', 0))
            metrics['workers'] = int(response.get('workers', 0))

            for worker in response['worker_status']:
                last_status = worker.get('last_status')
                metrics['backlog'] += int(last_status.get('backlog', 0))
                metrics['max_threads'] += int(last_status.get('max_threads', 0))
                metrics['pool_capacity'] += int(last_status.get('pool_capacity', 0))
                metrics['requests_count'] += int(last_status.get('requests_count', 0))
                metrics['running'] += int(last_status.get('running', 0))

        else:  # Puma is not clustered
            metrics['backlog'] = int(response.get('backlog', 0))
            metrics['max_threads'] = int(response.get('max_threads', 0))
            metrics['pool_capacity'] = int(response.get('pool_capacity', 0))
            metrics['running'] = int(response.get('running', 0))

        return metrics

    def _perform_service_check(self, instance, url):
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        port = parsed_url.port or 80
        tags = instance.get('tags', [])
        service_check_name = 'puma.connection'
        service_check_tags = ['host:%s' % host, 'port:%s' % port] + tags

        try:
            self.log.debug("Querying URL: %s", url)
            request = self._perform_request(url)
        except Exception:
            self.service_check(service_check_name, AgentCheck.CRITICAL, tags=service_check_tags)
            raise
        else:
            self.service_check(service_check_name, AgentCheck.OK, tags=service_check_tags)

        body = json.loads(request.content)
        return body, request.headers.get('content-type', 'text/plain'), request.headers.get('server')

    def _perform_request(self, url):
        request = self.http.get(url)
        request.raise_for_status()
        return request
