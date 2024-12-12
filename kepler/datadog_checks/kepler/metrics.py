# (C) Datadog, Inc. 2024-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

METRIC_MAP = {
    'kepler_container_joules': {'name': 'container.usage.joules', 'type': 'counter'},
    'kepler_container_core_joules': {'name': 'container.usage.core_joules', 'type': 'counter'},
    'kepler_container_dram_joules': {'name': 'container.usage.dram_joules', 'type': 'counter'},
    'kepler_container_uncore_joules': {'name': 'container.usage.uncore_joules', 'type': 'counter'},
    'kepler_container_package_joules': {'name': 'container.usage.package_joules', 'type': 'counter'},
    'kepler_container_platform_joules': {'name': 'container.usage.platform_joules', 'type': 'counter'},
    'kepler_container_other_joules': {'name': 'container.usage.other_joules', 'type': 'counter'},
    'kepler_container_gpu_joules': {'name': 'container.usage.gpu_joules', 'type': 'counter'},
    'kepler_container_energy_stat': {'name': 'container.usage.energy_stat', 'type': 'counter'},
    'kepler_container_bpf_cpu_time_us': {'name': 'ontainer.bpf_cpu_time_us', 'type': 'counter'},
    'kepler_container_cpu_cycles': {'name': 'container.usage.cpu_cycles', 'type': 'counter'},
    'kepler_container_cpu_instructions': {'name': 'container.usage.cpu_instructions', 'type': 'counter'},
    'kepler_container_cache_miss': {'name': 'container.usage.cache_miss', 'type': 'counter'},
    'kepler_container_cgroupfs_cpu_usage_us': {
        'name': 'container.usage.cgroupfs_cpu_usage_us',
        'type': 'counter',
    },
    'kepler_container_cgroupfs_memory_usage_bytes': {
        'name': 'container.usage.cgroupfs_memory_usage_bytes',
        'type': 'counter',
    },
    'kepler_container_cgroupfs_system_cpu_usage_us': {
        'name': 'container.usage.cgroupfs_system_cpu_usage_us',
        'type': 'counter',
    },
    'kepler_container_cgroupfs_user_cpu_usage_us': {
        'name': 'container.usage.cgroupfs_user_cpu_usage_us',
        'type': 'counter',
    },
    'kepler_container_bpf_net_tx_irq': {'name': 'container.usage.bpf_net_tx_irq', 'type': 'counter'},
    'kepler_container_bpf_net_rx_irq': {'name': 'container.usage.bpf_net_rx_irq', 'type': 'counter'},
    'kepler_container_bpf_block_irq': {'name': 'container.usage.bpf_block_irq', 'type': 'counter'},
    'kepler_container_bpf_cpu_time_ms': {'name': 'container.usage.bpf_cpu_time', 'type': 'counter'},
    'kepler_container_bpf_page_cache_hit': {'name': 'container.usage.bpf_page_cache_hit', 'type': 'counter'},
    'kepler_container_task_clock_ms': {'name': 'container.usage.task_clock', 'type': 'counter'},
    'kepler_node_info': {'name': 'node_info', 'type': 'counter'},
    'kepler_node_core_joules': {'name': 'node.usage.core_joules', 'type': 'counter'},
    'kepler_node_uncore_joules': {'name': 'node.usage.uncore_joules', 'type': 'counter'},
    'kepler_node_dram_joules': {'name': 'node.usage.dram_joules', 'type': 'counter'},
    'kepler_node_package_joules': {'name': 'node.usage.package_joules', 'type': 'counter'},
    'kepler_node_other_host_components_joules': {
        'name': 'node.usage.other_host_components_joules',
        'type': 'counter',
    },
    'kepler_node_gpu_joules': {'name': 'node.usage.gpu_joules', 'type': 'counter'},
    'kepler_node_platform_joules': {'name': 'node.usage.platform_joules', 'type': 'counter'},
    'kepler_node_energy_stat': {'name': 'node.usage.energy_stat', 'type': 'counter'},
    'kepler_node_accelerator_intel_qat': {'name': 'node.usage.accelerator_intel_qat', 'type': 'counter'},
}
RENAME_LABELS_MAP = {'container_namespace': 'kube_namespace', 'source': 'kepler_source', 'mode': 'kepler_mode'}
