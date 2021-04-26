from .metrics import DM_METRICS, PD_METRICS, PUMP_METRICS, TICDC_METRICS, TIDB_METRICS, TIFLASH_METRICS, TIKV_METRICS

DEFAULT_INSTANCES = {
    'pd': {
        'prometheus_url': 'http://localhost:2379/metrics',
        'namespace': "pd",
        'metrics': [PD_METRICS],
    },
    'tidb': {
        'prometheus_url': 'http://localhost:10080/metrics',
        'namespace': "tidb",
        'metrics': [TIDB_METRICS],
    },
    'tikv': {
        'prometheus_url': 'http://localhost:20180/metrics',
        'namespace': "tikv",
        'metrics': [TIKV_METRICS],
    },
    'tiflash_proxy': {
        'prometheus_url': 'http://localhost:20292/metrics',
        'namespace': "tiflash_proxy",
        'metrics': [TIFLASH_METRICS],
    },
    'tiflash': {
        'prometheus_url': 'http://localhost:8234/metrics',
        'namespace': "tiflash",
        'metrics': [TIFLASH_METRICS],
    },
    'ticdc': {
        'prometheus_url': 'http://localhost:8301/metrics',
        'namespace': "ticdc",
        'metrics': [TICDC_METRICS],
    },
    'dm_master': {
        'prometheus_url': 'http://localhost:8261/metrics',
        'namespace': "dm_master",
        'metrics': [DM_METRICS],
    },
    'dm_worker': {
        'prometheus_url': 'http://localhost:8262/metrics',
        'namespace': "dm_worker",
        'metrics': [DM_METRICS],
    },
    'pump': {
        'prometheus_url': 'http://localhost:8250/metrics',
        'namespace': "pump",
        'metrics': [PUMP_METRICS],
    },
}
