# metrics.py
METRIC_MAP = {
    "patroni_version": "version",
    "patroni_postgres_running": "postgres.running",
    "patroni_postmaster_start_time": "postgres.start_time",
    "patroni_primary": "primary",
    "patroni_xlog_location": "xlog.location",
    "patroni_standby_leader": "standby_leader",
    "patroni_replica": "replica",
    "patroni_sync_standby": "sync_standby",
    "patroni_quorum_standby": "quorum_standby",
    "patroni_xlog_received_location": "xlog.received_location",
    "patroni_xlog_replayed_location": "xlog.replayed_location",
    "patroni_xlog_replayed_timestamp": "xlog.replayed_timestamp",
    "patroni_xlog_paused": "xlog.paused",
    "patroni_postgres_streaming": "postgres.streaming",
    "patroni_postgres_in_archive_recovery": "postgres.archive_recovery",
    "patroni_postgres_server_version": "postgres.server_version",
    "patroni_cluster_unlocked": "cluster.unlocked",
    "patroni_failsafe_mode_is_active": "failsafe_mode.active",
    "patroni_postgres_timeline": "postgres.timeline",
    "patroni_dcs_last_seen": "dcs.last_seen",
    "patroni_pending_restart": "pending_restart",
    "patroni_is_paused": "is_paused",
}

# Alert types
ALERT_TYPE_INFO = "info"

# Helper function that will strip _total from both the raw metric name and the metric name
def construct_metrics_config(metric_map):
    metrics = []
    for raw_metric_name, metric_name in metric_map.items():
        if raw_metric_name.endswith("_total"):
            raw_metric_name = raw_metric_name[:-6]
            metric_name = metric_name[:-6]

        config = {raw_metric_name: {"name": metric_name}}
        metrics.append(config)

    return metrics
