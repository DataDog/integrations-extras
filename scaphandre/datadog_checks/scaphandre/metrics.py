# (C) Datadog, Inc. 2024-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
METRIC_MAP = {
    'scaph_host_power_microwatts': 'host.power',
    'scaph_process_power_consumption_microwatts': {'name': 'process.power_consumption', 'type': 'gauge'},
    'scaph_host_energy_microjoules': 'host.energy',
    'scaph_socket_power_microwatts': 'socket.power',
    'scaph_host_rapl_psys_microjoules': 'host.rapl.psys',
    'scaph_host_swap_total_bytes': 'host.swap.total',
    'scaph_host_swap_free_bytes': 'host.swap.free',
    'scaph_host_memory_free_bytes': 'host.memory.free',
    'scaph_host_memory_available_bytes': 'host.memory.available',
    'scaph_host_memory_total_bytes': 'host.memory.total',
    'scaph_host_disk_total_bytes': 'host.disk.total',
    'scaph_host_disk_available_bytes': 'host.disk.available',
    'scaph_host_cpu_frequency': 'host.cpu.frequency',
    'scaph_host_load_avg_fifteen': 'host.load.avg.15',
    'scaph_host_load_avg_five': 'host.load.avg.5',
    'scaph_host_load_avg_one': 'host.load.avg.1',
    'scaph_self_memory_bytes': 'self.memory',
    'scaph_self_memory_virtual_bytes': 'self.memory.virtual',
    'scaph_self_topo_stats_nb': 'self.topo_stats',
    'scaph_self_topo_records_nb': 'self.topo_records',
    'scaph_self_topo_procs_nb': 'self.topo_procs',
    'scaph_self_socket_stats_nb': 'self.socket_stats',
    'scaph_self_socket_records_nb': 'self.socket_records',
    'scaph_self_domain_records_nb': 'self.domain_records',
    'scaph_process_cpu_usage_percentage': {'name': 'process.cpu_usage.pct', 'type': 'gauge'},
    'scaph_process_memory_bytes': {'name': 'process.memory', 'type': 'gauge'},
    'scaph_process_memory_virtual_bytes': {'name': 'process.memory.virtual', 'type': 'gauge'},
    'scaph_process_disk_total_write_bytes': {'name': 'process.disk.total_write', 'type': 'gauge'},
    'scaph_process_disk_write_bytes': {'name': 'process.disk.write', 'type': 'gauge'},
    'scaph_process_disk_read_bytes': {'name': 'process.disk.read', 'type': 'gauge'},
    'scaph_process_disk_total_read_bytes': {'name': 'process.disk.total_read', 'type': 'gauge'},
}

RENAME_LABELS_MAP = {'exe': 'scaphandre_exe', 'cmdline': 'scaphandre_command', 'pid': 'scaphandre_pid'}

# SCAPHANDRE_VERSION = {'scaph_self_version': {'type': 'metadata', 'label': 'version', 'name': 'version'}}
