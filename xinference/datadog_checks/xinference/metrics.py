METRIC_MAP = {
    ## Worker: LLM inference
    'xinference:generate_tokens': 'tokens.generated',
    'xinference:input_tokens_total_counter': 'tokens.input',
    'xinference:output_tokens_total_counter': 'tokens.output',
    'xinference:time_to_first_token_seconds': 'time_to_first_token',
    ## Worker: model requests
    'xinference:model_request': 'model.requests',
    'xinference:model_request_errors': 'model.request.errors',
    'xinference:model_request_duration_seconds': 'model.request.duration',
    'xinference:model_serve_count': 'model.requests.serving',
    'xinference:model_request_limit': 'model.request.limit',
    'xinference:model_last_load_duration_seconds': 'model.load.duration',
    ## Supervisor: cluster
    'xinference:supervisor_uptime_seconds': 'supervisor.uptime',
    'xinference:workers_total': 'workers',
    'xinference:models_loaded_total': 'models.loaded',
    'xinference:model_status': 'model.status',
    'xinference:worker_cpu_utilization': 'worker.cpu.utilization',
    'xinference:worker_memory_used_bytes': 'worker.memory.used',
    'xinference:worker_memory_total_bytes': 'worker.memory.total',
    ## Supervisor: API keys
    'xinference:api_key_requests': 'api_key.requests',
    'xinference:api_key_request_duration_seconds': 'api_key.request.duration',
    'xinference:api_keys_active_total': 'api_keys.active',
    'xinference:api_keys_expired_total': 'api_keys.expired',
    'xinference:banned_ips_total': 'banned.ips',
    'xinference:banned_keys_total': 'banned.keys',
    ## Supervisor: HTTP API
    'requests_total_counter': 'api.requests',
    'responses_total_counter': 'api.responses',
    'status_codes_counter': 'api.responses.by_status',
}
