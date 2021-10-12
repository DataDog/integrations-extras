from copy import deepcopy

from datadog_checks.base import ConfigurationError, OpenMetricsBaseCheck

from .metrics import DM_METRICS, PD_METRICS, PUMP_METRICS, TICDC_METRICS, TIDB_METRICS, TIFLASH_METRICS, TIKV_METRICS


class TiDBCheck(OpenMetricsBaseCheck):
    __NAMESPACE__ = "tidb_cluster"

    def __init__(self, name, init_config, instances=None):

        # A tidb check instance represents a standalone tidb cluster.
        # There may be several components in the tidb cluster, such as tikv, tidb, pd, ticdc, etc.
        # Each component maps to a openmetrics check instance.
        #
        # expand tidb check instances to openmetrics check instances
        openmetrics_instances = []
        for _, instance in enumerate(instances):

            def _required_instance(component):
                new_instance = deepcopy(instance)
                url = new_instance.get(component + "_metric_url")
                if url is None:
                    raise ConfigurationError("`" + component + "_metric_url` parameter is required.")
                customized_metrics = new_instance.get(component + "_customized_metrics", [])
                new_instance.update({'prometheus_url': url, 'namespace': component, 'metrics': customized_metrics})
                openmetrics_instances.append(new_instance)

            def _optional_instance(component):
                new_instance = deepcopy(instance)
                url = new_instance.get(component + "_metric_url")
                if url is not None:
                    customized_metrics = new_instance.get(component + "_customized_metrics", [])
                    new_instance.update({'prometheus_url': url, 'namespace': component, 'metrics': customized_metrics})
                    openmetrics_instances.append(new_instance)

            # required
            _required_instance("tidb")
            _required_instance("pd")
            _required_instance("tikv")

            # optional
            _optional_instance("tiflash")
            _optional_instance("ticdc")
            _optional_instance("dm_master")
            _optional_instance("dm_worker")
            _optional_instance("pump")

        default_instances = {
            'pd': {
                'prometheus_url': 'http://localhost:2379/metrics',
                'namespace': "pd",
                'metrics': [PD_METRICS],
            },
            'tidb': {
                'prometheus_url': 'http://localhost:10080/metrics',
                'namespace': "tidb",
                'metrics': [TIDB_METRICS],
            },
            'tikv': {
                'prometheus_url': 'http://localhost:20180/metrics',
                'namespace': "tikv",
                'metrics': [TIKV_METRICS],
            },
            'tiflash': {
                'prometheus_url': 'http://localhost:8234/metrics',
                'namespace': "tiflash",
                'metrics': [TIFLASH_METRICS],
            },
            'ticdc': {
                'prometheus_url': 'http://localhost:8301/metrics',
                'namespace': "ticdc",
                'metrics': [TICDC_METRICS],
            },
            'dm_master': {
                'prometheus_url': 'http://localhost:8261/metrics',
                'namespace': "dm_master",
                'metrics': [DM_METRICS],
            },
            'dm_worker': {
                'prometheus_url': 'http://localhost:8262/metrics',
                'namespace': "dm_worker",
                'metrics': [DM_METRICS],
            },
            'pump': {
                'prometheus_url': 'http://localhost:8250/metrics',
                'namespace': "pump",
                'metrics': [PUMP_METRICS],
            },
        }

        # For the usage of instances and namespace,
        # see datadog_`checks.base.checks.openmetrics.mixins.OpenMetricsScraperMixin.create_scraper_configuration`
        super(TiDBCheck, self).__init__(name, init_config, openmetrics_instances, default_instances=default_instances)
