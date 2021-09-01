from typing import Any

from datadog_checks.base import ConfigurationError, OpenMetricsBaseCheck

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

    def check(self, instance):
        endpoint = instance.get('prometheus_url')
        if endpoint is None:
            raise ConfigurationError("Unable to find prometheus_url in config file.")
        config = self.create_scraper_configuration(instance)
        self.process(config)
        pass
