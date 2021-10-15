from copy import deepcopy

from datadog_checks.base import OpenMetricsBaseCheck
from datadog_checks.base.utils.tagging import GENERIC_TAGS

from .metrics import DM_METRICS, PD_METRICS, PUMP_METRICS, TICDC_METRICS, TIDB_METRICS, TIFLASH_METRICS, TIKV_METRICS


# A check object is mapped to a single instance in integration config.
class TiDBCheck(OpenMetricsBaseCheck):
    def __init__(self, name, init_config, instances=None):

        # Expand tidb check instance to openmetrics check instance
        openmetrics_instance = deepcopy(instances[0])

        _build_check("tidb", openmetrics_instance)
        _build_check("pd", openmetrics_instance)
        _build_check("tikv", openmetrics_instance)
        _build_check("tiflash", openmetrics_instance)
        _build_check("tiflash_proxy", openmetrics_instance)
        _build_check("ticdc", openmetrics_instance)
        _build_check("dm_master", openmetrics_instance)
        _build_check("dm_worker", openmetrics_instance)
        _build_check("pump", openmetrics_instance)

        default_instances = {
            'tidb_cluster': _build_check(
                "pd",
                {
                    'pd_metric_url': 'http://localhost:2379/metrics',
                    'metrics': DM_METRICS
                    + PD_METRICS
                    + PUMP_METRICS
                    + TICDC_METRICS
                    + TIDB_METRICS
                    + TIFLASH_METRICS
                    + TIKV_METRICS,
                },
            )
        }

        super(TiDBCheck, self).__init__(name, init_config, [openmetrics_instance], default_instances=default_instances)


def _build_check(component, instance):
    url = instance.get(component + "_metric_url")
    if url is not None:
        instance.update(
            {
                'prometheus_url': url,
                'namespace': "tidb_cluster",
                'labels_mapper': _labels_mapper(),
                'tags': ['tidb_cluster_component:' + component],
            }
        )
    return instance


def _labels_mapper():
    m = {}
    for label in GENERIC_TAGS:
        m.update({label: label + '_in_app'})
    return m
