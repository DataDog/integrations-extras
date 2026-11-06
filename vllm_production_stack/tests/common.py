import os

HERE = os.path.dirname(os.path.abspath(__file__))

EXPECTED_PROMETHEUS_METRICS = [
    'vllm_production_stack.backend.decoding_length.avg',
    'vllm_production_stack.backend.healthy',
    'vllm_production_stack.backend.inter_token_latency.avg',
    'vllm_production_stack.backend.latency.avg',
    'vllm_production_stack.backend.prefix_cache.hit_rate',
    'vllm_production_stack.backend.prefix_cache.hits',
    'vllm_production_stack.backend.prefix_cache.queries',
    'vllm_production_stack.backend.qps',
    'vllm_production_stack.backend.requests.decoding',
    'vllm_production_stack.backend.requests.prefill',
    'vllm_production_stack.backend.requests.running',
    'vllm_production_stack.backend.requests.swapped',
    'vllm_production_stack.request.errors.count',
    'vllm_production_stack.request.latency.bucket',
    'vllm_production_stack.request.latency.count',
    'vllm_production_stack.request.latency.sum',
    'vllm_production_stack.requests.incoming.count',
    'vllm_production_stack.router.cpu.usage',
    'vllm_production_stack.router.disk.usage',
    'vllm_production_stack.router.memory.usage',
    'vllm_production_stack.tokens.input.count',
    'vllm_production_stack.tokens.output.count',
]

BAD_HOSTNAME_INSTANCE = {'openmetrics_endpoint': 'http://invalid-hostname:8000/metrics'}


def get_fixture_path(filename):
    return os.path.join(HERE, 'fixtures', filename)
