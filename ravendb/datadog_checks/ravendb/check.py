from datadog_checks.base import OpenMetricsBaseCheckV2

from .metrics import METRIC_MAP


class RavendbCheck(OpenMetricsBaseCheckV2):
    __NAMESPACE__ = 'ravendb'
    DEFAULT_METRIC_LIMIT = 0

    def __init__(self, name, init_config, instances):
        super(RavendbCheck, self).__init__(name, init_config, instances)

        endpoint = self.instance.get("openmetrics_endpoint")
        if not endpoint:
            return

        enable_database_metrics = bool(self.instance.get("enable_database_metrics", False))
        enable_index_metrics = bool(self.instance.get("enable_index_metrics", False))
        enable_collection_metrics = bool(self.instance.get("enable_collection_metrics", False))
        include_gc_metrics = bool(self.instance.get("enable_gc_metrics", False))

        params = []
        if not enable_database_metrics:
            params.append("skipDatabasesMetrics=true")
        if not enable_index_metrics:
            params.append("skipIndexesMetrics=true")
        if not enable_collection_metrics:
            params.append("skipCollectionsMetrics=true")
        if include_gc_metrics:
            params.append("includeGcMetrics=true")

        if params:
            for p in params:
                if p in endpoint:
                    continue
                endpoint += ("&" if "?" in endpoint else "?") + p

            self.instance["openmetrics_endpoint"] = endpoint

    def get_default_config(self):
        exclude = []
        user_exclude = self.instance.get("exclude_metrics", [])
        if isinstance(user_exclude, list):
            exclude.extend(user_exclude)

        return {
            "metrics": [METRIC_MAP],
            "rename_labels": {
                "cluster_id": "ravendb_cluster_id",
                "server_version": "ravendb_server_version",
                "server_full_version": "ravendb_server_full_version",
            },
            "exclude_metrics": exclude,
        }
