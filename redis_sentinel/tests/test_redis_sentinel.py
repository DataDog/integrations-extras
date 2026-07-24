import mock
import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.redis_sentinel import RedisSentinelCheck

METRICS = [
    'redis.sentinel.odown_slaves',
    'redis.sentinel.sdown_slaves',
    'redis.sentinel.ok_slaves',
    'redis.sentinel.ok_sentinels',
    'redis.sentinel.known_sentinels',
    'redis.sentinel.known_slaves',
    'redis.sentinel.link_pending_commands',
]

SERVICE_CHECKS = [
    'redis.sentinel.master_is_disconnected',
    'redis.sentinel.master_is_down',
    'redis.sentinel.slave_is_disconnected',
    'redis.sentinel.slave_master_link_down',
]

CHECK_NAME = 'redis_sentinel'


@pytest.mark.unit
def test_load_config():
    instance = {}
    c = RedisSentinelCheck('redis_sentinel', {}, instance)

    # Error on empty instance
    with pytest.raises(ConfigurationError):
        c._load_config(instance)

    # When sentinel_port is not set.
    with pytest.raises(ConfigurationError):
        c._load_config({'sentinel_host': 'localhost'})

    # When sentinel_port is a float.
    with pytest.raises(ConfigurationError):
        c._load_config({'sentinel_host': 'localhost', 'sentinel_port': 123.0})

    # When sentinel_port is a string
    with pytest.raises(ConfigurationError):
        c._load_config({'sentinel_host': 'localhost', 'sentinel_port': 'port'})

    # Expect to pass when port is an integer, with no password defined.
    host, port, password, username, socket_timeout, ssl_kwargs = c._load_config(
        {'sentinel_host': 'localhost', 'sentinel_port': 123, 'masters': 'mymaster'}
    )
    assert host == 'localhost'
    assert port == 123
    assert password is None
    assert username is None
    assert socket_timeout == 5
    assert ssl_kwargs == {}

    # Expect to pass when port is an integer, with password defined.
    host, port, password, username, socket_timeout, ssl_kwargs = c._load_config(
        {'sentinel_host': 'localhost', 'sentinel_port': 123, 'masters': 'mymaster', 'sentinel_password': 'password1'}
    )
    assert host == 'localhost'
    assert port == 123
    assert password == 'password1'
    assert username is None
    assert ssl_kwargs == {}


@pytest.mark.unit
def test_load_config_username():
    c = RedisSentinelCheck('redis_sentinel', {}, {})

    host, port, password, username, socket_timeout, ssl_kwargs = c._load_config(
        {
            'sentinel_host': 'localhost',
            'sentinel_port': 123,
            'masters': 'mymaster',
            'sentinel_password': 'password1',
            'sentinel_username': 'myuser',
        }
    )
    assert username == 'myuser'
    assert password == 'password1'


@pytest.mark.unit
def test_load_config_ssl():
    c = RedisSentinelCheck('redis_sentinel', {}, {})

    # SSL disabled by default
    _, _, _, _, _, ssl_kwargs = c._load_config(
        {'sentinel_host': 'localhost', 'sentinel_port': 123, 'masters': 'mymaster'}
    )
    assert ssl_kwargs == {}

    # SSL enabled with all options
    _, _, _, _, _, ssl_kwargs = c._load_config(
        {
            'sentinel_host': 'localhost',
            'sentinel_port': 123,
            'masters': 'mymaster',
            'ssl': True,
            'ssl_certfile': '/path/to/cert.pem',
            'ssl_keyfile': '/path/to/key.pem',
            'ssl_ca_certs': '/path/to/ca.pem',
            'ssl_cert_reqs': 2,
        }
    )
    assert ssl_kwargs == {
        'ssl': True,
        'ssl_certfile': '/path/to/cert.pem',
        'ssl_keyfile': '/path/to/key.pem',
        'ssl_ca_certs': '/path/to/ca.pem',
        'ssl_cert_reqs': 2,
    }

    # SSL enabled with minimal options
    _, _, _, _, _, ssl_kwargs = c._load_config(
        {'sentinel_host': 'localhost', 'sentinel_port': 123, 'masters': 'mymaster', 'ssl': True}
    )
    assert ssl_kwargs == {'ssl': True}


@pytest.mark.unit
def test_load_config_socket_timeout():
    c = RedisSentinelCheck('redis_sentinel', {}, {})

    _, _, _, _, socket_timeout, _ = c._load_config(
        {'sentinel_host': 'localhost', 'sentinel_port': 123, 'masters': 'mymaster', 'socket_timeout': 10}
    )
    assert socket_timeout == 10


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_check(aggregator, instance):
    """
    Testing Redis_sentinel check.
    """
    check = RedisSentinelCheck(CHECK_NAME, {}, {})
    check.check(instance)

    for mname in METRICS:
        aggregator.assert_metric(mname, at_least=1)

    for svc_chk in SERVICE_CHECKS:
        aggregator.assert_service_check(svc_chk, status=RedisSentinelCheck.OK, count=1)

    aggregator.assert_all_metrics_covered()


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_down_slaves(aggregator, instance):
    """
    Testing Redis_sentinel check.
    """
    check = RedisSentinelCheck(CHECK_NAME, {}, {})

    sentinel_slaves = []
    for _ in range(5):
        sentinel_slaves.append({'is_odown': True, 'is_sdown': False})
    for _ in range(7):
        sentinel_slaves.append({'is_odown': False, 'is_sdown': True})

    with mock.patch.object(check, '_get_sentinel_replicas', return_value=sentinel_slaves):
        check.check(instance)

        aggregator.assert_metric('redis.sentinel.odown_slaves', 5)
        aggregator.assert_metric('redis.sentinel.sdown_slaves', 7)
