"""
A definition of the metrics publicly exposed in SpiceDB.
"""
# For the metrics, the key is the SpiceDB name and the
# value is the Datadog name. They're manually rewritten
# because Datadog likes dot-separated names and SpiceDB
# likes underscore-separated names.

# For all spicedb_ prefixed metrics, we make the prefix
# `application.` because all of these metrics will come in
# with a `spicedb.` prefix.

METRIC_MAP = {
    # SpiceDB counter metrics
    "spicedb_cache_cost_added_bytes": "application.cache.cost_added",
    "spicedb_cache_cost_evicted_bytes": "application.cache.cost_evicted",
    "spicedb_cache_hits_total": "application.cache.hits",
    "spicedb_cache_misses_total": "application.cache.misses",
    "spicedb_datastore_hedgeable_requests_total": "application.datastore.hedgeable_requests",
    "spicedb_datastore_hedged_requests_total": "application.datastore.hedged_requests",
    "spicedb_dispatch_client_check_from_cache_total": "application.dispatch_client.check_from_cache",
    "spicedb_dispatch_client_check_total": "application.dispatch_client.check",
    "spicedb_dispatch_client_lookup_resources_from_cache_total": "application.dispatch_client.lookup_resources_from_cache",
    "spicedb_dispatch_client_lookup_resources_total": "application.dispatch_client.lookup_resources",
    "spicedb_dispatch_client_lookup_subjects_from_cache_total": "application.dispatch_client.lookup_subjects_from_cache",
    "spicedb_dispatch_client_lookup_subjects_total": "application.dispatch_client.lookup_subjects",
    "spicedb_dispatch_client_reachable_resources_from_cache_total": "application.dispatch_client.reachable_resources_from_cache",
    "spicedb_dispatch_client_reachable_resources_total": "application.dispatch_client.reachable_resources",
    # SpiceDB gauge metrics
    "spicedb_datastore_watching_schema_cache_caveats_fallback_mode": "application.datastore.watching_schema_cache.caveats_fallback_mode",
    "spicedb_datastore_watching_schema_cache_namespaces_fallback_mode": "application.datastore.watching_schema_cache.namespaces_fallback_mode",
    "spicedb_datastore_watching_schema_cache_tracked_revision": "application.datastore.watching_schema_cache.tracked_revision",
    # SpiceDB histogram metrics
    "spicedb_check_direct_dispatch_query_count": "application.check.direct_dispatch_query_count",
    "spicedb_check_dispatch_chunk_count": "application.check.dispatch_chunk_count",
    "spicedb_datastore_crdb_watch_retries": "application.datastore.crdb_watch_retries",
    "application.datastore.loaded_relationships_count": "application.datastore.loaded_relationships_count",
    "spicedb_datastore_query_latency": "application.datastore.query_latency",
    "spicedb_datastore_spanner_watch_retries": "application.datastore.spanner_watch_retries",
    "spicedb_services_dispatches": "application.services.dispatches",
    # gRPC counter metrics
    "grpc_server_handled_total": "grpc.server.handled",
    "grpc_server_msg_received_total": "grpc.server.msg_received",
    "grpc_server_msg_sent_total": "grpc.server.msg_sent",
    "grpc_server_started_total": "grpc.server.started",
    # gRPC histogram metrics
    "grpc_server_handling_seconds": "grpc.server.handling_seconds",
    # process counter metrics
    "process_cpu_seconds_total": "process.cpu.seconds",
    # process gauge metrics
    "process_virtual_memory_bytes": "process.virtual_memory_bytes",
}


def construct_metric_config(raw: str, dotted: str):
    """
    Transforms openmetrics configuration names into names that datadog likes.
    """

    # Datadog doesn't like _total as a suffix on openmetrics
    # counter metrics, so we remove it
    return {raw.removesuffix("_total"): {"name": dotted}}


METRICS_CONFIG: list[dict[str, dict[str, str]]] = [
        construct_metric_config(raw, dotted) for raw, dotted in METRIC_MAP.items()
        ]
