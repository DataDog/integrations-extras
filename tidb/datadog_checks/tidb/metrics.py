TIDB_METRICS = ['tidb*', 'pd_client*', 'process*', 'go*', 'etcd*']
PD_METRICS = ['pd*', 'process*', 'go*', 'grpc*', 'etcd*']
TIKV_METRICS = [
    'tikv*',
    'process*',
]
TIFLASH_METRICS = ['tiflash*']
TICDC_METRICS = ['ticdc*', 'process*', 'go*']
DM_METRICS = ['dm*', 'process*', 'go*']
PUMP_METRICS = ['binlog*', 'process*', 'go*']

# rename datadog reserved tags, referring to `datadog_checks/base/utils/tagging.py`
LABEL_MAPPERS = {
    'cluster_name': 'cluster_name_in_app',
    'clustername': 'clustername_in_app',
    'cluster': 'cluster_in_app',
    'clusterid': 'clusterid_in_app',
    'cluster_id': 'cluster_id_in_app',
    'env': 'env_in_app',
    'host_name': 'host_name_in_app',
    'hostname': 'hostname_in_app',
    'host': 'host_in_app',
    'service': 'service_in_app',
    'version': 'version_in_app',
}
