import pytest


@pytest.fixture(scope='session')
def dd_environment():
    yield


@pytest.fixture()
def instance_good():
    instance = {'url': 'https://api.cloudsmith.io/v1',
                'cloudsmith_api_key': 'aaa', 'organization': 'cloudsmith'}
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


@pytest.fixture()
def audit_log_resp_good():
    audit_log_resp_good = {
        "actor": "test user",
        "actor_ip_address": "XXX.XXX.XXX.XXX",
        "actor_kind": "user",
        "actor_location": {
            "city": "XXX",
            "continent": "Europe",
            "country": "United Kingdom",
            "country_code": "GB",
            "latitude": "1",
            "longitude": "1",
            "postal_code": "BT11"
        },
        "actor_slug_perm": "msle0eeRYz0",
        "actor_url": "https://api.cloudsmith.io/v1/users/profile/test/",
        "context": "",
        "event": "action.login",
        "event_at": "2023-01-10T12:59:03.926729Z",
        "object": "test",
        "object_kind": "user",
        "object_slug_perm": "msle0eeRYz0",
        "uuid": "efb5b5b0-5b5b-5b5b-5b5b-5b5b5b5b5b5b",
        "target": "cloudsmith-test",
        "target_kind": "namespace",
        "target_slug_perm": "eqr0eeRYz0",
    }
    return audit_log_resp_good


@pytest.fixture()
def audit_log_resp_bad_json():
    # create a bad response
    audit_log_resp_bad_json = [
        {
            "actor_ip_address": "XXX.XXX.XXX.XXX",
            "actor_kind": "user",
            "actor_location": {
                "continent": "Europe",
                "country": "United Kingdom",
                "country_code": "GB",
                "latitude": "1",
                "longitude": "1",
                "postal_code": "BT11"
            },
            "actor_slug_perm": "msle0eeRYz0",
            "actor_url": "https://api.cloudsmith.io/v1/users/profile/test/",
            "context": "",
            "object": "test",
            "object_kind": "user",
            "object_slug_perm": "msle0eeRYz0",
            "uuid": "efb5b5b0-5b5b-5b5b-5b5b-5b5b5b5b5b5b",
            "target": "cloudsmith-test",
            "target_kind": "namespace",
            "target_slug_perm": "eqr0eeRYz0",
        }]
    return audit_log_resp_bad_json


@pytest.fixture()
def vulnerabilitiy_resp_json():
    vulnerabilitiy_resp_json = [
        {
            "identifier": "weqwqeqw",
            "created_at": "2023-01-06T18:18:39.546636Z",
            "package": {
                "identifier": "reqwqeqw",
                "name": "library/python",
                "version": "1eff2926e10eed27freqreq3be53538b76eff4f61dfd1f81be4e0c5e854ad1ae5",
                "url": "https://api.cloudsmith.io/v1/packages/cloudsmith-test/test/tqetq/"
            },
            "scan_id": 1,
            "has_vulnerabilities": True,
            "num_vulnerabilities": 88,
            "max_severity": "Critical"
        },
        {
            "identifier": "rqerqerqe",
            "created_at": "2023-01-06T18:18:23.263269Z",
            "package": {
                "identifier": "ereqreq",
                "name": "library/node",
                "version": "a5b5ad15479f19b8r312be69cd52032becacf2f9c600ed16ecb628c9937c80",
                "url": "https://api.cloudsmith.io/v1/packages/cloudsmith-test/test/tqetq/"
            },
            "scan_id": 1,
            "has_vulnerabilities": True,
            "num_vulnerabilities": 104,
            "max_severity": "Critical"
        }]
    return vulnerabilitiy_resp_json


@pytest.fixture()
def vulnerabilitiy_resp_json_bad():
    vulnerabilitiy_resp_json_bad = [
        {
            "identifier": "weqwqeqw",
            "created_at": "2023-01-06T18:18:39.546636Z",
            "package": {
                "identifier": "reqwqeqw",
                "name": "library/python",
                "version": "1eff2926e10eed27freqreq3be53538b76eff4f61dfd1f81be4e0c5e854ad1ae5",
                "url": "https://api.cloudsmith.io/v1/packages/cloudsmith-test/test/tqetq/"
            },
            "scan_id": 1,
            "has_vulnerabilities": True,
            "num_vulnerabilities": 88,
            "max_severity": "Medium"
        }]
    return vulnerabilitiy_resp_json_bad
