import os

HERE = os.path.dirname(os.path.abspath(__file__))

EXPECTED_METRICS = [
    'log10x.check.up',
    'log10x.events.read.count',
    'log10x.bytes.read.count',
    'log10x.events.forwarded.count',
    'log10x.bytes.forwarded.count',
    'log10x.bytes.encoded.count',
    'log10x.events.offloaded.count',
    'log10x.bytes.offloaded.count',
    'log10x.events.retrieved.count',
    'log10x.bytes.retrieved.count',
]

MOCKED_INSTANCE = {'openmetrics_endpoint': 'http://localhost:9100/metrics'}

BAD_HOSTNAME_INSTANCE = {'openmetrics_endpoint': 'http://invalid-hostname:9100/metrics'}


def get_fixture_path(filename):
    return os.path.join(HERE, 'fixtures', filename)
