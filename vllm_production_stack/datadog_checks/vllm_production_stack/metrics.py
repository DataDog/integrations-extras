METRIC_MAP = {
    ## Requests observed by the router
    'vllm:num_incoming_requests': 'requests.incoming',
    'vllm:request_latency_seconds': 'request.latency',
    'vllm:request_errors': 'request.errors',
    'vllm:input_tokens': 'tokens.input',
    'vllm:output_tokens': 'tokens.output',
    ## Per-backend request statistics (sliding window)
    'vllm:current_qps': 'backend.qps',
    'vllm:avg_latency': 'backend.latency.avg',
    'vllm:avg_itl': 'backend.inter_token_latency.avg',
    'vllm:avg_decoding_length': 'backend.decoding_length.avg',
    'vllm:num_requests_running': 'backend.requests.running',
    'vllm:num_prefill_requests': 'backend.requests.prefill',
    'vllm:num_decoding_requests': 'backend.requests.decoding',
    'vllm:num_requests_swapped': 'backend.requests.swapped',
    ## Per-backend engine statistics scraped by the router
    'vllm:gpu_prefix_cache_hit_rate': 'backend.prefix_cache.hit_rate',
    # Exposed as gauges holding the engine counters.
    'vllm:gpu_prefix_cache_hits_total': 'backend.prefix_cache.hits',
    'vllm:gpu_prefix_cache_queries_total': 'backend.prefix_cache.queries',
    'vllm:healthy_pods_total': 'backend.healthy',
    ## Router process host
    'router_cpu_usage_percent': 'router.cpu.usage',
    'router_memory_usage_percent': 'router.memory.usage',
    'router_disk_usage_percent': 'router.disk.usage',
}

RENAME_LABELS_MAP = {
    'server': 'backend',
}
