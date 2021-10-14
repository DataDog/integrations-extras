from copy import deepcopy

from datadog_checks.base import OpenMetricsBaseCheck

from .metrics import (
    DM_METRICS,
    LABEL_MAPPERS,
    PD_METRICS,
    PUMP_METRICS,
    TICDC_METRICS,
    TIDB_METRICS,
    TIFLASH_METRICS,
    TIKV_METRICS,
)


class TiDBCheck(OpenMetricsBaseCheck):
    def __init__(self, name, init_config, instances=None):

        # A tidb check instance represents a standalone tidb cluster.
        # There may be several components in the tidb cluster, such as tikv, tidb, pd, ticdc, etc.
        # Each component maps to a openmetrics check instance.
        #
        # expand tidb check instances to openmetrics check instances
        openmetrics_instances = []
        for _, instance in enumerate(instances):

            def _build_instance(component):
                new_instance = deepcopy(instance)
                new_instance.update(
                    {
                        'namespace': "tidb_cluster",
                        'labels_mapper': LABEL_MAPPERS,
                        'tags': ['tidb_cluster_component:' + component],
                    }
                )
                url = new_instance.get(component + "_metric_url")
                if url is not None:
                    new_instance.update({'prometheus_url': url})
                    openmetrics_instances.append(new_instance)

            _build_instance("tidb")
            _build_instance("pd")
            _build_instance("tikv")
            _build_instance("tiflash")
            _build_instance("tiflash_proxy")
            _build_instance("ticdc")
            _build_instance("dm_master")
            _build_instance("dm_worker")
            _build_instance("pump")

        default_instances = {
            'tidb_cluster': {
                'prometheus_url': 'http://localhost:2379/metrics',
                'namespace': "tidb_cluster",
                'metrics': DM_METRICS
                + PD_METRICS
                + PUMP_METRICS
                + TICDC_METRICS
                + TIDB_METRICS
                + TIFLASH_METRICS
                + TIKV_METRICS,
            },
        }

        # For the usage of instances and namespace,
        # see datadog_`checks.base.checks.openmetrics.mixins.OpenMetricsScraperMixin.create_scraper_configuration`
        super(TiDBCheck, self).__init__(name, init_config, openmetrics_instances, default_instances=default_instances)
