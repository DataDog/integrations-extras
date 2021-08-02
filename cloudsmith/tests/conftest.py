import pytest


@pytest.fixture(scope='session')
def dd_environment():
    yield


@pytest.fixture
def instance():
    return {}


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
def vulnerability_test_json():
    vul_json = [
        {
            'identifier': 'Mfi4y3P2oFVfKeXT',
            'created_at': '2021-07-26T00:07:50.138520Z',
            'package': {
                'identifier': 'Kx1K9sre9vhy',
                'name': 'cloudsmith-docker-native-multiarch',
                'version': '8ea9bd2cc7b4b557e1efd78f19c487f879c42cb66857be53ef1055f69456085e',
                'url': 'https://api.cloudsmith.io/v1/packages/cloudsmith/testing-private/Kx1K9sre9vhy/',
            },
            'scan_id': 1,
            'has_vulnerabilities': True,
            'num_vulnerabilities': 28,
            'max_severity': 'Critical',
        },
        {
            'identifier': 'LRF19CJKUgUoSNCV',
            'created_at': '2021-07-26T00:07:39.766276Z',
            'package': {
                'identifier': 'rBr3HJ1M393Z',
                'name': 'cloudsmith-docker-native',
                'version': '4b5df1ca6eb1247a31563272dc6dd3c62c42ed9d8212b84a44e3182b7233eb44',
                'url': 'https://api.cloudsmith.io/v1/packages/cloudsmith/testing-private/rBr3HJ1M393Z/',
            },
            'scan_id': 1,
            'has_vulnerabilities': True,
            'num_vulnerabilities': 14,
            'max_severity': 'High',
        },
        {
            'identifier': 'l3iHZwP4W5VYqhZ2',
            'created_at': '2021-07-26T00:07:25.281774Z',
            'package': {
                'identifier': 'oCqRvwhM4vd5',
                'name': 'cloudsmith-docker-cli',
                'version': 'ac05dcd9e2b9fb8f4ab23ea1327c0a5179a2cb078c030e25a7092d8009252f1e',
                'url': 'https://api.cloudsmith.io/v1/packages/cloudsmith/testing-private/oCqRvwhM4vd5/',
            },
            'scan_id': 1,
            'has_vulnerabilities': False,
            'num_vulnerabilities': 0,
            'max_severity': 'Unknown',
        },
    ]
    return vul_json


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
                    'percentage_used': 80,
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
