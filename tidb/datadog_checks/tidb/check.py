from copy import deepcopy

from datadog_checks.base import ConfigurationError, OpenMetricsBaseCheck

from .instances import DEFAULT_INSTANCES


class TiDBCheck(OpenMetricsBaseCheck):
    DEFAULT_METRIC_LIMIT = 0

    def __init__(self, name, init_config, instances=None):

        # A tidb check instance represents a standalone tidb cluster.
        # There may be several components in the tidb cluster, such as tikv, tidb, pd, ticdc, etc.
        # Each component maps to a openmetrics check instance.
        #
        # expand tidb check instances to openmetrics check instances
        openmetrics_instances = []
        for i, instance in enumerate(instances):

            def _required_instance(component):
                new_instance = deepcopy(instance)
                url = new_instance.get(component + "_metric_url")
                if url is None:
                    raise ConfigurationError("`" + component + "_metric_url` parameter is required.")
                customized_metrics = new_instance.get(component + "_customized_metrics")
                new_instance.update({
                    'prometheus_url': url,
                    'namespace': component,
                    'metrics': customized_metrics
                })
                openmetrics_instances.append(new_instance)

            def _optional_instance(component):
                new_instance = deepcopy(instance)
                url = new_instance.get(component + "_metric_url")
                if url is not None:
                    customized_metrics = new_instance.get(component + "_customized_metrics")
                    new_instance.update({
                        'prometheus_url': url,
                        'namespace': component,
                        'metrics': customized_metrics
                    })
                    openmetrics_instances.append(new_instance)

            # required
            _required_instance("tidb")
            _required_instance("pd")
            _required_instance("tikv")

            # optional
            _optional_instance("tiflash")
            _optional_instance("tiflash_proxy")
            _optional_instance("ticdc")
            _optional_instance("dm_master")
            _optional_instance("dm_worker")
            _optional_instance("pump")

        # For the usage of instances and namespace,
        # see datadog_`checks.base.checks.openmetrics.mixins.OpenMetricsScraperMixin.create_scraper_configuration`
        super(TiDBCheck, self).__init__(
            name, init_config, instances, default_instances=DEFAULT_INSTANCES)
