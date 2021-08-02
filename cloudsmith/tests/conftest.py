import pytest


@pytest.fixture(scope='session')
def dd_environment():
    yield


@pytest.fixture()
def instance_good():
    instance = {'url': 'https://api.cloudsmith.io/v1', 'cloudsmith_api_key': 'aaa', 'organization': 'cloudsmith'}
    return instance


@pytest.fixture()
def instance_empty():
    instance = {}
    return instance


@pytest.fixture()
def instance_url_none():
    instance = {'url': None, 'cloudsmith_api_key': 'aaa', 'organization': 'cloudsmith'}
    return instance


@pytest.fixture()
def instance_api_key_none():
    instance = {'url': 'https://api.cloudsmith.io/v1', 'cloudsmith_api_key': None, 'organization': 'cloudsmith'}
    return instance


@pytest.fixture()
def instance_org_none():
    instance = {'url': 'https://api.cloudsmith.io/v1', 'cloudsmith_api_key': 'aaa', 'organization': None}
    return instance


@pytest.fixture()
def entitlements_test_json():
    entitlements_json = {
        'tokens': {
            'active': 19,
            'inactive': 100,
            'total': 119,
            'bandwidth': {
                'lowest': {'value': 1460, 'units': 'bytes', 'display': '1.4 KB'},
                'average': {'value': 1453939, 'units': 'bytes', 'display': '1.4 MB'},
                'highest': {'value': 28062489, 'units': 'bytes', 'display': '26.8 MB'},
                'total': {'value': 37802418, 'units': 'bytes', 'display': '36.1 MB'},
            },
            'downloads': {
                'lowest': {'value': 1},
                'average': {'value': 9},
                'highest': {'value': 64},
                'total': {'value': 240},
            },
        }
    }
    return entitlements_json


@pytest.fixture()
def entitlements_test_bad_json():
    entitlements_test_bad_json = {
        'tokens': {
            'active': 19,
            'inactive': 100,
            'bandwidth': {
                'lowest': {'value': 1460, 'units': 'bytes', 'display': '1.4 KB'},
                'average': {'value': 1453939, 'units': 'bytes', 'display': '1.4 MB'},
                'highest': {'value': 28062489, 'units': 'bytes', 'display': '26.8 MB'},
            },
            'downloads': {'lowest': {'value': 1}, 'average': {'value': 9}, 'highest': {'value': 64}},
        }
    }
    return entitlements_test_bad_json


@pytest.fixture()
def not_found_json():
    not_found_json = {"detail": "Not found."}
    return not_found_json


@pytest.fixture()
def usage_resp_bad_json():
    usage_resp_bad_json = {
        'usage': {
            'raw': {
                'bandwidth': {'used': 57045, 'configured': 2199023255552, 'plan_limit': 64424509440},
                'storage': {'used': 10054602731, 'configured': 1099511627776, 'plan_limit': 32212254720},
            },
            'display': {
                'bandwidth': {
                    'used': '55.7 KB',
                    'configured': '2 TB',
                    'plan_limit': '60 GB',
                    'percentage_used': '0.0%',
                },
                'storage': {'used': '9.4 GB', 'configured': '1 TB', 'plan_limit': '30 GB', 'percentage_used': '0.914%'},
            },
        }
    }
    return usage_resp_bad_json


@pytest.fixture()
def usage_resp_good():
    usage_resp_good = {
        'usage': {
            'raw': {
                'bandwidth': {
                    'used': 57045,
                    'configured': 2199023255552,
                    'plan_limit': 64424509440,
                    'percentage_used': 0.0,
                },
                'storage': {
                    'used': 10054602731,
                    'configured': 1099511627776,
                    'plan_limit': 32212254720,
                    'percentage_used': 0.914,
                },
            },
            'display': {
                'bandwidth': {
                    'used': '55.7 KB',
                    'configured': '2 TB',
                    'plan_limit': '60 GB',
                    'percentage_used': '0.0%',
                },
                'storage': {'used': '9.4 GB', 'configured': '1 TB', 'plan_limit': '30 GB', 'percentage_used': '0.914%'},
            },
        }
    }
    return usage_resp_good


@pytest.fixture()
def usage_resp_warning():
    usage_resp_warning = {
        'usage': {
            'raw': {
                'bandwidth': {
                    'used': 25769803776,
                    'configured': 32212254720,
                    'plan_limit': 32212254720,
                    'percentage_used': 80.0,
                },
                'storage': {
                    'used': 25769803776,
                    'configured': 32212254720,
                    'plan_limit': 32212254720,
                    'percentage_used': 80.0,
                },
            },
            'display': {
                'bandwidth': {
                    'used': '8 GB',
                    'configured': '30 GB',
                    'plan_limit': '30 GB',
                    'percentage_used': '80.0%',
                },
                'storage': {'used': '24 GB', 'configured': '30 GB', 'plan_limit': '30 GB', 'percentage_used': '80%'},
            },
        }
    }
    return usage_resp_warning


@pytest.fixture()
def usage_resp_critical():
    usage_resp_critical = {
        'usage': {
            'raw': {
                'bandwidth': {
                    'used': 64424509440,
                    'configured': 64424509440,
                    'plan_limit': 64424509440,
                    'percentage_used': 100.0,
                },
                'storage': {
                    'used': 32212254720,
                    'configured': 32212254720,
                    'plan_limit': 32212254720,
                    'percentage_used': 100,
                },
            },
            'display': {
                'bandwidth': {
                    'used': '60 GB',
                    'configured': '60 GB',
                    'plan_limit': '60 GB',
                    'percentage_used': '100.0%',
                },
                'storage': {'used': '30 GB', 'configured': '30 GB', 'plan_limit': '30 GB', 'percentage_used': '100%'},
            },
        }
    }
    return usage_resp_critical
