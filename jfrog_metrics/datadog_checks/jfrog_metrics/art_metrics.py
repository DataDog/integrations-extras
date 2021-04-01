# (C) Datadog, Inc. 2019
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

ART_METRIC_MAP = {
    'app_disk_free_bytes': 'app_disk_free',
    'app_disk_total_bytes': 'app_disk_total',
    'jfrt_runtime_heap_processors_total': 'runtime_heap_processors',
    'jfrt_db_connections_active_total': 'db_connections_active',
    'jfrt_db_connections_idle_total': 'db_connections_idle',
    'jfrt_db_connections_max_active_total': 'db_connections_max_active',
    'jfrt_db_connections_min_idle_total': 'db_connections_min_idle',
    'jfrt_runtime_heap_maxmemory_bytes': 'runtime_heap_maxmemory',
    'jfrt_runtime_heap_freememory_bytes': 'runtime_heap_freememory',
    'jfrt_runtime_heap_totalmemory_bytes': 'runtime_heap_totalmemory',
    'jfrt_artifacts_gc_size_cleaned_bytes': 'artifacts_gc_size_cleaned',
    'jfrt_artifacts_gc_binaries_total': 'artifacts_gc_binaries',
    'jfrt_artifacts_gc_duration_seconds': 'artifacts_gc_duration',
    'sys_memory_free_bytes': 'xray.sys_memory_free',
    'sys_memory_used_bytes': 'xray.sys_memory_used',
}
