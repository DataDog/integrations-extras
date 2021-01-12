# (C) Datadog, Inc. 2020
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from datadog_checks.base import ConfigurationError, OpenMetricsBaseCheck

from .metrics import METRIC_MAP


class GatekeeperCheck(OpenMetricsBaseCheck):
    DEFAULT_METRIC_LIMIT = 0

    def __init__(self, name, init_config, instances=None):
        default_instances = {
            'gatekeeper': {
                'metrics': [METRIC_MAP],
                'send_distribution_sums_as_monotonic': 'true',
                'send_distribution_counts_as_monotonic': 'true',
            }
        }

        super(GatekeeperCheck, self).__init__(
            name, init_config, instances, default_instances=default_instances, default_namespace='gatekeeper'
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
        gatekeeper_url = instance.get("gatekeeper_health_endpoint")
        if gatekeeper_url is None:
            raise ConfigurationError("Each instance must have a url to the gatekeeper health endpoint")

        prometheus_url = instance.get("prometheus_url")
        if prometheus_url is None:
            raise ConfigurationError("Each instance must have a url to the metrics endpoint")

        health_url = gatekeeper_url + "/healthz"

        # General service health
        self._http_check(health_url, 'gatekeeper.health')

        super(GatekeeperCheck, self).check(instance)
