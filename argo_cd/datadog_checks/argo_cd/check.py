from datadog_checks.base import ConfigurationError, OpenMetricsBaseCheck

from .metrics import APPLICATION_METRICS

class ArgoCdCheck(OpenMetricsBaseCheck):
    """
    Collect Argocd metrics from Prometheus endpoint
    """
    def __init__(self, name, init_config, instances=None):
        instance = instances[0]
        endpoint = instance.get('prometheus_url')
        if endpoint is None:
            raise ConfigurationError("Unable to find prometheus url in config file.")

        instance.update(
            {
                'prometheus_url': endpoint,
                'namespace': 'argocd',
                'metrics': [APPLICATION_METRICS],

            }
        )

        super(ArgoCdCheck, self).__init__(name, init_config, [instance])

# (C) Datadog, Inc. 2019-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)