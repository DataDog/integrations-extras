import os

HERE = os.path.dirname(os.path.abspath(__file__))

# Reported by the supervisor (or xinference-local) on the API port.
SUPERVISOR_METRICS = [
    'xinference.api.requests.count',
    'xinference.api.responses.by_status.count',
    'xinference.api.responses.count',
    'xinference.api_key.request.duration.bucket',
    'xinference.api_key.request.duration.count',
    'xinference.api_key.request.duration.sum',
    'xinference.api_key.requests.count',
    'xinference.api_keys.active',
    'xinference.api_keys.expired',
    'xinference.banned.ips',
    'xinference.banned.keys',
    'xinference.model.status',
    'xinference.models.loaded',
    'xinference.supervisor.uptime',
    'xinference.worker.cpu.utilization',
    'xinference.worker.memory.total',
    'xinference.worker.memory.used',
    'xinference.workers',
]

# Reported by each worker on its metrics exporter port.
WORKER_METRICS = [
    'xinference.model.load.duration',
    'xinference.model.request.duration.bucket',
    'xinference.model.request.duration.count',
    'xinference.model.request.duration.sum',
    'xinference.model.request.errors.count',
    'xinference.model.request.limit',
    'xinference.model.requests.count',
    'xinference.model.requests.serving',
    'xinference.time_to_first_token.bucket',
    'xinference.time_to_first_token.count',
    'xinference.time_to_first_token.sum',
    'xinference.tokens.generated.count',
    'xinference.tokens.input.count',
    'xinference.tokens.output.count',
]

BAD_HOSTNAME_INSTANCE = {'openmetrics_endpoint': 'http://invalid-hostname:9997/metrics'}


def get_fixture_path(filename):
    return os.path.join(HERE, 'fixtures', filename)
