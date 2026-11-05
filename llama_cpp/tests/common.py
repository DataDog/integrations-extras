import os

HERE = os.path.dirname(os.path.abspath(__file__))

EXPECTED_PROMETHEUS_METRICS = [
    'llama_cpp.busy_slots_per_decode',
    'llama_cpp.decode_calls.count',
    'llama_cpp.predicted_tokens_per_second',
    'llama_cpp.prompt_seconds.count',
    'llama_cpp.prompt_tokens.count',
    'llama_cpp.prompt_tokens_cached.count',
    'llama_cpp.prompt_tokens_per_second',
    'llama_cpp.requests.deferred',
    'llama_cpp.requests.processing',
    'llama_cpp.spec_decode.accepted_tokens.count',
    'llama_cpp.spec_decode.draft_tokens.count',
    'llama_cpp.spec_decode.drafts.count',
    'llama_cpp.tokens_max',
    'llama_cpp.tokens_predicted.count',
    'llama_cpp.tokens_predicted_seconds.count',
]

BAD_HOSTNAME_INSTANCE = {'openmetrics_endpoint': 'http://invalid-hostname:8080/metrics'}


def get_fixture_path(filename):
    return os.path.join(HERE, 'fixtures', filename)
