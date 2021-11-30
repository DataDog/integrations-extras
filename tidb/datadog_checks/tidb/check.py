from copy import deepcopy

from datadog_checks.base import OpenMetricsBaseCheck

from .metrics import TIDB_METRICS, TIFLASH_METRICS, TIKV_METRICS
from .utils import build_check


# A check object is mapped to a single instance in integration config.
class TiDBCheck(OpenMetricsBaseCheck):
    def __init__(self, name, init_config, instances=None):

        # Expand tidb check instance to openmetrics check instance
        openmetrics_instance = deepcopy(instances[0])

        build_check("tidb", openmetrics_instance)
        build_check("pd", openmetrics_instance)
        build_check("tikv", openmetrics_instance)
        build_check("tiflash", openmetrics_instance)
        build_check("tiflash_proxy", openmetrics_instance)
        build_check("ticdc", openmetrics_instance)
        build_check("dm_master", openmetrics_instance)
        build_check("dm_worker", openmetrics_instance)
        build_check("pump", openmetrics_instance)

        default_instances = {
            'tidb_cluster': build_check(
                "pd",
                {
                    'pd_metric_url': 'http://localhost:2379/metrics',
                    'metrics': TIDB_METRICS + TIFLASH_METRICS + TIKV_METRICS,
                },
            )
        }

        super(TiDBCheck, self).__init__(
            name,
            init_config,
            [openmetrics_instance],
            default_instances=default_instances,
            default_namespace="tidb_cluster",
        )
