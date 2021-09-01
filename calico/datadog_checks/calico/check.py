from typing import Any

from datadog_checks.base import ConfigurationError, OpenMetricsBaseCheckV2

class CalicoCheck(OpenMetricsBaseCheckV2):
    def __init__(self, name, init_config, instances=None):
        METRICS_MAP = {'felix_active_local_endpoints': 'felix_active_local_endpoints'}

        super(CalicoCheck, self).__init__(
            name,
            init_config,
            instances,
            default_instances={
                'calico-felix': {
                    'prometheus_url': 'http://localhost:9091/metrics',
                    'namespace': 'kube-system',
                    'metrics': [METRICS_MAP],
                }
            },
            default_namespace='kube-system',
        )

