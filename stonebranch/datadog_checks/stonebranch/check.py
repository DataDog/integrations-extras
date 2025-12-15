from datadog_checks.base import OpenMetricsBaseCheckV2


class StonebranchCheck(OpenMetricsBaseCheckV2):
    __NAMESPACE__ = "stonebranch"

    def __init__(self, name, init_config, instances):
        super().__init__(name, init_config, instances)

        # Optional: define a mapping (Prometheus name -> Datadog name without namespace).
        # If you prefer, you can skip this and just configure `metrics:` in YAML.
        self.metrics_map = {
            # "prom_metric_name": "datadog_metric_name",
            # "stonebranch_jobs_total": "jobs.total",
        }

    def get_default_config(self):
        # Minimal defaults; instance-level YAML will override/extend as needed.
        return {
            # If you use metrics_map, you can default to those keys.
            "metrics": list(self.metrics_map.keys()) if self.metrics_map else [],
        }
