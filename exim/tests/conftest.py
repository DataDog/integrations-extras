import mock
import pytest


@pytest.fixture(scope='session')
def dd_environment():
    yield


@pytest.fixture
def instance():
    return {}


@pytest.fixture(autouse=True)
def no_systemctl():
    # Keep the tests independent of the host: without systemctl the exim.service.running check
    # does not call get_subprocess_output. test_service_check.py patches this per test.
    with mock.patch('datadog_checks.exim.check.shutil.which', return_value=None):
        yield


@pytest.fixture(autouse=True)
def no_version():
    # `exim -bV` is a separate subprocess; keep it out of the queue tests. test_version.py covers it.
    with mock.patch('datadog_checks.exim.check.EximCheck._collect_version'):
        yield
