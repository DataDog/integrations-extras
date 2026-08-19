METRIC_MAP = {
    ## ExternalSecret Metrics
    'externalsecret_status_condition': 'externalsecret.status_condition',
    'externalsecret_reconcile_duration': 'externalsecret.reconcile_duration',
    'externalsecret_sync_calls_total': 'externalsecret.sync_calls',
    'externalsecret_sync_calls_error': 'externalsecret.sync_calls_error',
    'externalsecret_provider_api_calls_count': 'externalsecret.provider_api_calls',
    ## ClusterExternalSecret Metrics
    'clusterexternalsecret_status_condition': 'clusterexternalsecret.status_condition',
    'clusterexternalsecret_reconcile_duration': 'clusterexternalsecret.reconcile_duration',
    ## PushSecret Metrics
    'pushsecret_status_condition': 'pushsecret.status_condition',
    'pushsecret_reconcile_duration': 'pushsecret.reconcile_duration',
    ## ClusterSecretStore Metrics
    'clustersecretstore_status_condition': 'clustersecretstore.status_condition',
    'clustersecretstore_reconcile_duration': 'clustersecretstore.reconcile_duration',
    ## SecretStore Metrics
    'secretstore_status_condition': 'secretstore.status_condition',
    'secretstore_reconcile_duration': 'secretstore.reconcile_duration',
    ## Controller-runtime Metrics
    'controller_runtime_reconcile_total': 'controller_runtime.reconcile',
    'controller_runtime_reconcile_errors_total': 'controller_runtime.reconcile_errors',
    'controller_runtime_reconcile_time_seconds': 'controller_runtime.reconcile_time_seconds',
    'controller_runtime_active_workers': 'controller_runtime.active_workers',
    'controller_runtime_max_concurrent_reconciles': 'controller_runtime.max_concurrent_reconciles',
    ## Workqueue Metrics
    'workqueue_depth': 'workqueue.depth',
}
