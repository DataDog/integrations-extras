import pytest


@pytest.fixture(scope='session')
def dd_environment():
    yield


@pytest.fixture
def instance_ok():
    return {
        'AmazonEC2': 'YQHNG5NBWUE3D67S.4NA7Y494T4.6YS6EN2CT7',
        'AmazonCloudFront': '84Z32PF576RHPTMX.JRTCKXETXF.SW9U2ZKBYX'
    }


@pytest.fixture
def instance_warning():
    return {
        'AmazonEC2': '1234567891011121.1234567891.1234567891',
        'AmazonCloudFront': '84Z32PF576RHPTMX.JRTCKXETXF.SW9U2ZKBYX'
    }
