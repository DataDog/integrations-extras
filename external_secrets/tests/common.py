import os


HERE = os.path.dirname(os.path.abspath(__file__))

EXPECTED_PROMETHEUS_METRICS = [
    'external_secrets.externalsecret.status_condition',
    'external_secrets.externalsecret.reconcile_duration',
    'external_secrets.externalsecret.sync_calls.count',
    'external_secrets.externalsecret.sync_calls_error.count',
    'external_secrets.externalsecret.provider_api_calls.count',
    'external_secrets.clusterexternalsecret.status_condition',
    'external_secrets.clusterexternalsecret.reconcile_duration',
    'external_secrets.pushsecret.status_condition',
    'external_secrets.pushsecret.reconcile_duration',
    'external_secrets.clustersecretstore.status_condition',
    'external_secrets.clustersecretstore.reconcile_duration',
    'external_secrets.secretstore.status_condition',
    'external_secrets.secretstore.reconcile_duration',
    'external_secrets.controller_runtime.reconcile.count',
    'external_secrets.controller_runtime.reconcile_errors.count',
    'external_secrets.controller_runtime.reconcile_time_seconds.count',
    'external_secrets.controller_runtime.reconcile_time_seconds.sum',
    'external_secrets.controller_runtime.reconcile_time_seconds.bucket',
    'external_secrets.controller_runtime.active_workers',
    'external_secrets.controller_runtime.max_concurrent_reconciles',
    'external_secrets.workqueue.depth',
]

MOCKED_INSTANCE = {'openmetrics_endpoint': 'http://localhost:8080/metrics'}

BAD_HOSTNAME_INSTANCE = {'openmetrics_endpoint': 'http://invalid-hostname:8080/metrics'}


def get_fixture_path(filename):
    return os.path.join(HERE, 'fixtures', filename)
