# (C) Datadog, Inc. 2020
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from datadog_checks.base import ConfigurationError, OpenMetricsBaseCheck

from .metrics import METRIC_MAP


class OpenPolicyAgentCheck(OpenMetricsBaseCheck):
    DEFAULT_METRIC_LIMIT = 0

    def __init__(self, name, init_config, instances=None):
        default_instances = {
            'open_policy_agent': {
                'metrics': [METRIC_MAP],
                'send_distribution_sums_as_monotonic': 'true',
                'send_distribution_counts_as_monotonic': 'true',
            }
        }

        super(OpenPolicyAgentCheck, self).__init__(
            name, init_config, instances, default_instances=default_instances, default_namespace='open_policy_agent'
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

    def _get_policies(self, opa_url):
        policies_url = opa_url + "/v1/policies"
        try:
            response = self.http.get(policies_url)
            policies = response.json()
        except Exception:
            self.log.warning("The policies endpoint is not available")
        else:
            self.gauge('open_policy_agent.policies', len(policies['result']), tags=[])

    def check(self, instance):
        opa_url = instance.get("opa_url")
        if opa_url is None:
            raise ConfigurationError("Each instance must have a url to the open policy agent service")

        prometheus_url = instance.get("prometheus_url")
        if prometheus_url is None:
            raise ConfigurationError("Each instance must have a url to the prometheus endpoint")

        health_url = opa_url + "/health"
        plugins_url = health_url + "?plugins"
        bundles_url = health_url + "?bundles"

        # General service health
        self._http_check(health_url, 'open_policy_agent.health')
        # Bundles activation status
        self._http_check(bundles_url, 'open_policy_agent.bundles_health')
        # Plugins status
        self._http_check(plugins_url, 'open_policy_agent.plugins_health')

        self._get_policies(opa_url)

        super(OpenPolicyAgentCheck, self).check(instance)
