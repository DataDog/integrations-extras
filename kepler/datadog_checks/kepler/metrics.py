# (C) Datadog, Inc. 2024-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

METRIC_MAP = {
    'kepler_container_joules': {'name': 'container.joules', 'type': 'gauge'},
    'kepler_container_core_joules': {'name': 'container.core_joules', 'type': 'gauge'},
    'kepler_container_dram_joules': {'name': 'container.dram_joules', 'type': 'gauge'},
    'kepler_container_uncore_joules': {'name': 'container.uncore_joules', 'type': 'gauge'},
    'kepler_container_package_joules': {'name': 'container.package_joules', 'type': 'gauge'},
    'kepler_container_other_joules': {'name': 'container.other_joules', 'type': 'gauge'},
    'kepler_container_gpu_joules': {'name': 'container.gpu_joules', 'type': 'gauge'},
    'kepler_container_energy_stat': {'name': 'container.energy_stat', 'type': 'gauge'},
    'kepler_container_bpf_cpu_time_us': {'name': 'ontainer.bpf_cpu_time_us', 'type': 'gauge'},
    'kepler_container_cpu_cycles': {'name': 'container.cpu_cycles', 'type': 'gauge'},
    'kepler_container_cpu_instructions': {'name': 'container.cpu_instructions', 'type': 'gauge'},
    'kepler_container_cache_miss': {'name': 'container.cache_miss', 'type': 'gauge'},
    'kepler_container_cgroupfs_cpu_usage_us': {
        'name': 'container.cgroupfs_cpu_usage_us',
        'type': 'gauge',
    },
    'kepler_container_cgroupfs_memory_usage_bytes': {
        'name': 'container.cgroupfs_memory_usage_bytes',
        'type': 'gauge',
    },
    'kepler_container_cgroupfs_system_cpu_usage_us': {
        'name': 'container.cgroupfs_system_cpu_usage_us',
        'type': 'gauge',
    },
    'kepler_container_cgroupfs_user_cpu_usage_us': {
        'name': 'container.cgroupfs_user_cpu_usage_us',
        'type': 'gauge',
    },
    'kepler_container_bpf_net_tx_irq': {'name': 'container.bpf_net_tx_irq', 'type': 'gauge'},
    'kepler_container_bpf_net_rx_irq': {'name': 'container.bpf_net_rx_irq', 'type': 'gauge'},
    'kepler_container_bpf_block_irq': {'name': 'container.bpf_block_irq', 'type': 'gauge'},
    'kepler_node_info': {'name': 'node_info', 'type': 'gauge'},
    'kepler_node_core_joules': {'name': 'node.core_joules', 'type': 'gauge'},
    'kepler_node_uncore_joules': {'name': 'node.uncore_joules', 'type': 'gauge'},
    'kepler_node_dram_joules': {'name': 'node.dram_joules', 'type': 'gauge'},
    'kepler_node_package_joules': {'name': 'node.package_joules', 'type': 'gauge'},
    'kepler_node_other_host_components_joules': {
        'name': 'node.other_host_components_joules',
        'type': 'gauge',
    },
    'kepler_node_gpu_joules': {'name': 'node.gpu_joules', 'type': 'gauge'},
    'kepler_node_platform_joules': {'name': 'node.platform_joules', 'type': 'gauge'},
    'kepler_node_energy_stat': {'name': 'node.energy_stat', 'type': 'gauge'},
    'kepler_node_accelerator_intel_qat': {'name': 'node.accelerator_intel_qat', 'type': 'gauge'},
}
RENAME_LABELS_MAP = {'container_namespace': 'kube_namespace', 'source': 'kepler_source', 'mode': 'kepler_mode'}
