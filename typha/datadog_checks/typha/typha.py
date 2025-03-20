# (C) Datadog, Inc. 2020
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from datadog_checks.base import ConfigurationError, OpenMetricsBaseCheck

from .metrics import METRIC_MAP


class TyphaCheck(OpenMetricsBaseCheck):
    DEFAULT_METRIC_LIMIT = 0

    def __init__(self, name, init_config, instances=None):
        default_instances = {
            'typha': {
                'metrics': [METRIC_MAP],
                'send_distribution_sums_as_monotonic': 'true',
                'send_distribution_counts_as_monotonic': 'true',
            }
        }

        super(TyphaCheck, self).__init__(
            name, init_config, instances, default_instances=default_instances, default_namespace='typha'
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

        super(TyphaCheck, self).check(instance)
