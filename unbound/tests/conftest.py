import logging
import os

import mock
import pytest

from datadog_checks.dev import get_here

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture()
def mock_which():
    with mock.patch('datadog_checks.unbound.unbound.which', return_value='arbitrary'):
        yield


@pytest.fixture
def mock_basic_stats_1_4_22():
    with open(os.path.join(get_here(), 'fixtures', 'stats.basic.1.4.22'), 'r') as f:
        stats = f.read()

    with mock.patch('datadog_checks.unbound.unbound.get_subprocess_output', return_value=(stats, '', 0)):
        yield


@pytest.fixture
def mock_basic_stats_1_9_2():
    with open(os.path.join(get_here(), 'fixtures', 'stats.basic.1.9.2'), 'r') as f:
        stats = f.read()

    with mock.patch('datadog_checks.unbound.unbound.get_subprocess_output', return_value=(stats, '', 0)):
        yield


@pytest.fixture
def mock_multithread_stats():
    with open(os.path.join(get_here(), 'fixtures', 'stats.multithread'), 'r') as f:
        stats = f.read()

    with mock.patch('datadog_checks.unbound.unbound.get_subprocess_output', return_value=(stats, '', 0)):
        yield


@pytest.fixture
def mock_extended_stats_1_4_22():
    with open(os.path.join(get_here(), 'fixtures', 'stats.extended.1.4.22'), 'r') as f:
        stats = f.read()

    with mock.patch('datadog_checks.unbound.unbound.get_subprocess_output', return_value=(stats, '', 0)):
        yield


@pytest.fixture
def mock_extended_stats_1_9_2():
    with open(os.path.join(get_here(), 'fixtures', 'stats.extended.1.9.2'), 'r') as f:
        stats = f.read()

    with mock.patch('datadog_checks.unbound.unbound.get_subprocess_output', return_value=(stats, '', 0)):
        yield


@pytest.fixture
def env_setup(monkeypatch):
    log = logging.getLogger('env_setup')
    log.debug('env_setup: before: PATH: {}'.format(os.environ['PATH']))
    no_sbin_path_list = [item for item in os.environ['PATH'].split(os.pathsep) if 'sbin' not in item]
    log.debug('env_setup: selected items: {}'.format(no_sbin_path_list))
    no_sbin_path = os.pathsep.join(no_sbin_path_list)
    log.debug('env_setup: no_sbin_path: {}'.format(no_sbin_path))
    monkeypatch.setenv('PATH', no_sbin_path)
    log.debug('env_setup: after: PATH: {}'.format(os.environ['PATH']))
