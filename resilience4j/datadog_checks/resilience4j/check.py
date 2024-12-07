from datadog_checks.base import OpenMetricsBaseCheck, ConfigurationError

from .metrics import METRIC_MAP


class Resilience4jCheck(OpenMetricsBaseCheck):
    DEFAULT_METRIC_LIMIT = 0

    def __init__(self, name, init_config, instances):
        default_instances = {
            'resilience4j': {
                'metrics': [METRIC_MAP],
                'send_distribution_sums_as_monotonic': 'true',
                'send_distribution_counts_as_monotonic': 'true',
            }
        }

        super(Resilience4jCheck, self).__init__(
            name, init_config, instances, default_instances=default_instances, default_namespace='resilience4j'
        )

    def _http_check(self, url, check_name):
        try:
            response = self.http.get(url)
            response.raise_for_status()
        except Exception as e:
            self.service_check(check_name, self.CRITICAL, message=str(e))
        else:
            if response.status_code == 200:
                self.service_check(check_name, self.OK)
            else:
                self.service_check(check_name, self.WARNING)

    def check(self, instance):
        prometheus_url = instance.get("prometheus_url")
        if prometheus_url is None:
            raise ConfigurationError("Each instance must have a url to the metrics endpoint")

        super(Resilience4jCheck, self).check(instance)