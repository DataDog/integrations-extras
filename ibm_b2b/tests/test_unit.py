# (C) Datadog, Inc. 2026-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

from unittest.mock import MagicMock, Mock
from datetime import datetime

import pytest
from requests import Response
from requests.cookies import RequestsCookieJar
from requests.exceptions import HTTPError, Timeout

from datadog_checks.base.constants import ServiceCheck
from datadog_checks.ibm_b2b import IbmB2bCheck
from datadog_checks.ibm_b2b import check as check_module
from datadog_checks.ibm_b2b.config_models.instance import InstanceConfig


@pytest.fixture
def configured_check():
    instance = {
        'url': 'https://connect.example.test:9443/',
        'username': 'monitor',
        'password': 'private',
        'cd_node': '192.0.2.10',
        'cd_port': 1363,
        'cd_protocol': 'TCPIP',
        'tls_verify': True,
        'timeout': 10,
        'statistics_lookback_minutes': 2,
        'statistics_timezone': 'America/Chicago',
    }
    check = IbmB2bCheck('ibm_b2b', {}, [instance])
    check._config_model_instance = InstanceConfig.model_validate(
        instance,
        context={'configured_fields': set(instance)},
    )
    check.service_check_calls = Mock()
    check.service_check = check.service_check_calls
    check.gauge_calls = Mock()
    check.gauge = check.gauge_calls
    return check


def mock_session(monkeypatch, signon_response=None, statistics_response=None, signon_error=None):
    session = MagicMock()
    session.cookies = RequestsCookieJar()
    session.__enter__.return_value = session

    if signon_error is not None:
        session.post.side_effect = signon_error
    else:
        def post(*args, **kwargs):
            for name, value in signon_response.cookies.items():
                session.cookies.set(name, value)
            return signon_response

        session.post.side_effect = post
    session.get.return_value = statistics_response
    session_factory = Mock(return_value=session)
    monkeypatch.setattr(check_module, 'Session', session_factory)
    return session, session_factory


def test_config_defaults_and_validation():
    config = InstanceConfig.model_validate(
        {'url': 'https://connect.example.test', 'username': 'monitor', 'password': 'secret', 'cd_node': '192.0.2.10'},
        context={'configured_fields': {'url', 'username', 'password', 'cd_node'}},
    )
    assert config.cd_port == 1363
    assert config.cd_protocol == 'TCPIP'
    assert config.tls_verify is True
    assert config.timeout == 10
    assert config.statistics_lookback_minutes == 2
    assert config.statistics_timezone is None
    assert 'secret' not in repr(config)

    with pytest.raises(ValueError, match='absolute HTTP'):
        InstanceConfig.model_validate(
            {'url': '/relative', 'username': 'monitor', 'password': 'secret', 'cd_node': 'node'},
            context={'configured_fields': {'url', 'username', 'password', 'cd_node'}},
        )

    with pytest.raises(ValueError, match='valid IANA timezone'):
        InstanceConfig.model_validate(
            {
                'url': 'https://connect.example.test',
                'username': 'monitor',
                'password': 'secret',
                'cd_node': 'node',
                'statistics_timezone': 'Not/AZone',
            },
            context={'configured_fields': {'url', 'username', 'password', 'cd_node', 'statistics_timezone'}},
        )


def test_signon_success(configured_check, monkeypatch):
    response = Mock(status_code=200)
    response.json.return_value = [
        {
            'messageCode': 200,
            'message': 'Signon is successful',
            'version': '6.4.0.0',
            'cdVersion': '6.4.0.0',
            'nodeMachineName': 'VM-B2B',
            'osType': 'Windows',
            'userName': 'administrator',
            'nodeName': 'VM-B2B',
        }
    ]
    response.headers = {'Authorization': 'mock-jwt', '_csrf': 'mock-csrf'}
    response.cookies = {'XSRF-TOKEN': 'mock-xsrf', 'JSESSIONID': 'mock-session'}
    stats_response = Mock(status_code=200)
    stats_response.json.return_value = []
    session, session_factory = mock_session(monkeypatch, response, stats_response)

    configured_check.check({})

    session.post.assert_called_once_with(
        'https://connect.example.test:9443/cdwebconsole/svc/signon',
        json={'ipAddress': '192.0.2.10', 'port': 1363, 'protocol': 'TCPIP'},
        auth=('monitor', 'private'),
        headers={'Content-Type': 'application/json; charset=utf-8', 'X-XSRF-TOKEN': 'Y2hlY2tpdA=='},
        verify=True,
        timeout=10,
    )
    session.get.assert_called_once()
    session_factory.assert_called_once_with()
    session.__enter__.assert_called_once_with()
    assert session.get.call_args.args[0] == 'https://connect.example.test:9443/cdwebconsole/svc/selectstatistics'
    assert session.get.call_args.kwargs['params']['sortOrder'] == 'DESC'
    query_times = session.get.call_args.kwargs['params']
    start_time = datetime.strptime(query_times['startTime'], '%m/%d/%Y,%I:%M:%S %p')
    stop_time = datetime.strptime(query_times['stopTime'], '%m/%d/%Y,%I:%M:%S %p')
    assert 118 <= (stop_time - start_time).total_seconds() <= 120
    assert session.get.call_args.kwargs['headers'] == {
        'Authorization': 'mock-jwt',
        'X-XSRF-TOKEN': 'mock-xsrf',
        'Content-Type': 'application/json; charset=utf-8',
    }
    assert 'cookies' not in session.get.call_args.kwargs
    assert 'auth' not in session.get.call_args.kwargs
    assert session.cookies.get('JSESSIONID') == 'mock-session'
    assert session.cookies.get('XSRF-TOKEN') == 'mock-xsrf'
    assert session.post.call_args.args[0].split('/cdwebconsole/')[0] == session.get.call_args.args[0].split(
        '/cdwebconsole/'
    )[0]
    assert configured_check.service_check_calls.call_args_list == [
        (('can_connect', ServiceCheck.OK), {'tags': []}),
        (('statistics.can_collect', ServiceCheck.OK), {'tags': []}),
    ]


def test_statistics_http_error_does_not_change_connectivity(configured_check, monkeypatch):
    signon = Mock(status_code=200)
    signon.json.return_value = [{'messageCode': 200, 'message': 'Signon is successful'}]
    signon.headers = {'Authorization': 'sensitive-jwt', '_csrf': 'a-different-csrf-header'}
    signon.cookies = {'XSRF-TOKEN': 'sensitive-cookie', 'JSESSIONID': 'sensitive-session'}
    error_response = Response()
    error_response.status_code = 400
    statistics = Mock()
    statistics.raise_for_status.side_effect = HTTPError(response=error_response)
    session, _ = mock_session(monkeypatch, signon, statistics)

    configured_check.check({})

    assert configured_check.service_check_calls.call_args_list == [
        (('can_connect', ServiceCheck.OK), {'tags': []}),
        (
            ('statistics.can_collect', ServiceCheck.CRITICAL),
            {
                'tags': [],
                'message': 'selectstatistics failed with HTTP 400 at /cdwebconsole/svc/selectstatistics',
            },
        ),
    ]
    message = configured_check.service_check_calls.call_args.kwargs['message']
    for secret in ('monitor', 'private', 'sensitive-jwt', 'sensitive-xsrf', 'sensitive-cookie', 'sensitive-session'):
        assert secret not in message


def test_missing_statistics_timezone_is_a_clear_config_error(configured_check, monkeypatch):
    configured_check._config_model_instance = configured_check.config.model_copy(update={'statistics_timezone': None})
    signon = Mock(status_code=200)
    signon.json.return_value = [{'messageCode': 200, 'message': 'Signon is successful'}]
    signon.headers = {'Authorization': 'jwt'}
    signon.cookies = {'XSRF-TOKEN': 'xsrf', 'JSESSIONID': 'session'}
    session, _ = mock_session(monkeypatch, signon, Mock())

    configured_check.check({})

    assert not session.get.called
    assert configured_check.service_check_calls.call_args_list == [
        (('can_connect', ServiceCheck.OK), {'tags': []}),
        (
            ('statistics.can_collect', ServiceCheck.CRITICAL),
            {
                'tags': [],
                'message': 'statistics_timezone is required; configure the Connect:Direct server IANA timezone',
            },
        ),
    ]


def test_selectstatistics_parses_observed_payload(configured_check, monkeypatch):
    signon = Mock(status_code=200)
    signon.json.return_value = [{'messageCode': 200, 'message': 'Signon is successful'}]
    signon.headers = {'Authorization': 'jwt', '_csrf': 'different-csrf-header'}
    signon.cookies = {'XSRF-TOKEN': 'xsrf', 'JSESSIONID': 'session'}
    # CTRC records mirror the observed Connect:Direct payload; totalRecords is metadata.
    statistics = Mock(status_code=200)
    statistics.json.return_value = [
        {
            'recordId': 'CTRC', 'recordCategory': 'CAPR', 'processName': 'TESTE', 'processNumber': 2,
            'secondaryNode': 'VM-B2B', 'conditionCode': 8, 'bytesSent': 0, 'bytesReceived': '0',
            'sourceFile': r'C:\\Users\\Administrator\\Desktop\\cabrito.txt',
        },
        {
            'recordId': 'PSTR', 'recordCategory': 'CAPR', 'processName': 'TESTE', 'processNumber': 2,
            'secondaryNode': 'VM-B2B', 'conditionCode': 0,
        },
        {
            'recordId': 'CTRC', 'recordCategory': 'CAPR', 'processName': 'TESTE', 'processNumber': 2,
            'secondaryNode': 'VM-B2B', 'conditionCode': 8, 'bytesSent': 0, 'bytesReceived': '0',
        },
        {'recordId': 'SMED', 'processName': '', 'processNumber': 0, 'conditionCode': 0},
        {'processName': 'IGNORED', 'processNumber': 99, 'conditionCode': 0},
        {'totalRecords': 77},
    ]
    session, _ = mock_session(monkeypatch, signon, statistics)

    configured_check.check({})

    session.get.assert_called_once()
    query = session.get.call_args.kwargs['params']
    assert set(query) == {'startTime', 'stopTime', 'sortOrder'}
    assert query['sortOrder'] == 'DESC'
    metric_values = {
        call.args[0]: (call.args[1], call.kwargs['tags'])
        for call in configured_check.gauge_calls.call_args_list
    }
    tags = ['process_name:TESTE', 'secondary_node:VM-B2B']
    assert metric_values == {
        'processes.total': (1, tags),
        'processes.success': (0, tags),
        'processes.failed': (1, tags),
        'transfer.bytes_sent': (0, tags),
        'transfer.bytes_received': (0, tags),
    }


def test_invalid_numeric_fields_skip_only_affected_metrics(configured_check):
    configured_check._submit_statistics(
        [
            {
                'recordId': 'PSTR',
                'processName': 'TESTE',
                'processNumber': '7',
                'conditionCode': 'invalid',
                'secondaryNode': 'VM-B2B',
                'sourceFile': 'must-not-be-a-tag',
            },
            {
                'recordId': 'CTRC',
                'processName': 'TESTE',
                'processNumber': 0,
                'secondaryNode': 'VM-B2B',
                'bytesSent': 'invalid',
                'bytesReceived': '256',
                'destinationFile': 'must-not-be-a-tag',
            },
        ],
        [],
    )

    metric_values = {
        call.args[0]: (call.args[1], call.kwargs['tags'])
        for call in configured_check.gauge_calls.call_args_list
    }
    tags = ['process_name:TESTE', 'secondary_node:VM-B2B']
    assert metric_values == {
        'processes.total': (1, tags),
        'processes.success': (0, tags),
        'processes.failed': (0, tags),
        'transfer.bytes_received': (256, tags),
    }


def test_duplicate_process_is_counted_once_within_lookback(configured_check):
    payload = [
        {
            'recordId': 'PSTR',
            'processName': 'TESTE',
            'processNumber': 42,
            'conditionCode': 0,
            'secondaryNode': 'VM-B2B',
        }
    ]

    configured_check._submit_statistics(payload, [])
    configured_check.gauge_calls.reset_mock()
    configured_check._submit_statistics(payload, [])

    configured_check.gauge_calls.assert_not_called()


def test_process_is_counted_again_only_after_dedup_retention_expires(configured_check, monkeypatch):
    payload = [
        {
            'recordId': 'PSTR',
            'processName': 'TESTE',
            'processNumber': 42,
            'conditionCode': 0,
            'secondaryNode': 'VM-B2B',
        }
    ]
    monkeypatch.setattr(check_module, 'monotonic', Mock(side_effect=[0, 241]))

    configured_check._submit_statistics(payload, [])
    configured_check.gauge_calls.reset_mock()
    configured_check._submit_statistics(payload, [])

    emitted = [call.args[0] for call in configured_check.gauge_calls.call_args_list]
    assert emitted == ['processes.total', 'processes.success', 'processes.failed']


@pytest.mark.parametrize(
    'error',
    [HTTPError('unauthorized'), Timeout('slow request'), ValueError('invalid JSON')],
)
def test_signon_request_failure_is_redacted(configured_check, error, monkeypatch):
    session = mock_session(monkeypatch, signon_error=error)

    configured_check.check({})

    args, kwargs = configured_check.service_check_calls.call_args
    assert args[:2] == ('can_connect', ServiceCheck.CRITICAL)
    assert 'private' not in kwargs['message']
    assert 'monitor' not in kwargs['message']


@pytest.mark.parametrize(
    'payload',
    [
        {},
        [],
        [{'messageCode': 401, 'message': 'Unauthorized'}],
        [{'messageCode': 200, 'message': 'Signon failed'}],
        {'unexpected': True},
    ],
)
def test_signon_rejection_is_critical(configured_check, payload, monkeypatch):
    response = Mock(status_code=200)
    response.json.return_value = payload
    mock_session(monkeypatch, response, Mock())

    configured_check.check({})

    args, kwargs = configured_check.service_check_calls.call_args
    assert args[:2] == ('can_connect', ServiceCheck.CRITICAL)
    assert 'private' not in kwargs['message']
    assert 'monitor' not in kwargs['message']
