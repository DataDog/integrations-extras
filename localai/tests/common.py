import os

HERE = os.path.dirname(os.path.abspath(__file__))

EXPECTED_PROMETHEUS_METRICS = [
    'localai.billed_requests.count',
    'localai.compression.duration.bucket',
    'localai.compression.duration.count',
    'localai.compression.duration.sum',
    'localai.compression.events.count',
    'localai.compression.ratio.bucket',
    'localai.compression.ratio.count',
    'localai.compression.ratio.sum',
    'localai.failover.switches.count',
    'localai.failover.target_up',
    'localai.request.duration.bucket',
    'localai.request.duration.count',
    'localai.request.duration.sum',
    'localai.tokens.count',
    'localai.usage_unrecorded.count',
]

BAD_HOSTNAME_INSTANCE = {'openmetrics_endpoint': 'http://invalid-hostname:8080/metrics'}


def get_fixture_path(filename):
    return os.path.join(HERE, 'fixtures', filename)
