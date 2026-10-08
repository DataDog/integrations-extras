import json
import os

import pytest

from datadog_checks.dev.http import MockResponse
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.kurrentdb import KurrentdbCheck
from datadog_checks.kurrentdb.check import parse_duration

from .conftest import HERE
from .expected_metrics import EXPECTED_METRICS

BASE_URL = 'http://localhost:2113'
API_FIXTURES = {
    '/stats': 'stats.json',
    '/info': 'info.json',
    '/projections/all-non-transient': 'projections.json',
    '/subscriptions': 'subscriptions.json',
    '/gossip': 'gossip.json',
}


def fixture_path(name):
    return os.path.join(HERE, 'fixtures', name)


def load_fixture(name):
    with open(fixture_path(name)) as f:
        return json.load(f)


@pytest.fixture
def mock_kurrentdb(mock_http_response_per_endpoint):
    def mock(overrides=None, base_url=BASE_URL):
        responses = {base_url + '/metrics': [MockResponse(file_path=fixture_path('metrics.txt'))]}
        for endpoint, name in API_FIXTURES.items():
            responses[base_url + endpoint] = [MockResponse(file_path=fixture_path(name))]
        for endpoint, response in (overrides or {}).items():
            responses[base_url + endpoint] = [response]
        return mock_http_response_per_endpoint(responses, mode='cycle', strict=False)

    return mock


def run(dd_run_check, instance, **extra):
    check = KurrentdbCheck('kurrentdb', {}, [{**instance, **extra}])
    dd_run_check(check)
    return check


def test_check(dd_run_check, aggregator, instance, mock_kurrentdb):
    mock_kurrentdb()
    run(dd_run_check, instance)

    for metric in EXPECTED_METRICS:
        aggregator.assert_metric(metric)

    aggregator.assert_service_check('kurrentdb.openmetrics.health', KurrentdbCheck.OK)
    for endpoint in API_FIXTURES:
        aggregator.assert_service_check(
            'kurrentdb.api.can_connect', KurrentdbCheck.OK, tags=[f'endpoint:{BASE_URL}{endpoint}']
        )
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_prometheus_labels_become_tags(dd_run_check, aggregator, instance, mock_kurrentdb):
    mock_kurrentdb()
    run(dd_run_check, instance)

    aggregator.assert_metric(
        'kurrentdb.persistent_sub_parked_messages',
        tags=['endpoint:http://localhost:2113/metrics', 'event_stream_id:test-stream', 'group_name:group1'],
    )


def test_api_metric_values_and_tags(dd_run_check, aggregator, instance, mock_kurrentdb):
    mock_kurrentdb()
    run(dd_run_check, instance)

    member = load_fixture('gossip.json')['members'][0]
    member_tags = [
        f'endpoint:{BASE_URL}/gossip',
        f'http_end_point_ip:{member["httpEndPointIp"]}',
        f'http_end_point_port:{member["httpEndPointPort"]}',
    ]
    aggregator.assert_metric('kurrentdb.cluster.member_alive', 1, tags=member_tags)
    aggregator.assert_metric('kurrentdb.cluster.last_commit_position', member['lastCommitPosition'], tags=member_tags)

    aggregator.assert_metric('kurrentdb.is_leader', 1, tags=[f'endpoint:{BASE_URL}/info'])
    aggregator.assert_metric('kurrentdb.is_follower', 0, tags=[f'endpoint:{BASE_URL}/info'])
    aggregator.assert_metric('kurrentdb.is_readonlyreplica', 0, tags=[f'endpoint:{BASE_URL}/info'])

    aggregator.assert_metric(
        'kurrentdb.subscription.live',
        1,
        tags=[f'endpoint:{BASE_URL}/subscriptions', 'event_stream_id:newstream', 'group_name:examplegroup'],
    )
    aggregator.assert_metric(
        'kurrentdb.projection.running',
        0,
        tags=[f'endpoint:{BASE_URL}/projections/all-non-transient', 'projection:$by_category'],
    )
    aggregator.assert_metric(
        'kurrentdb.es.queue.length',
        tags=[f'endpoint:{BASE_URL}/stats', 'queue_name:MainQueue'],
    )
    aggregator.assert_metric('kurrentdb.es.queue.current_processing_time', 0.0012345)


def test_custom_tags_are_applied_to_api_metrics(dd_run_check, aggregator, instance, mock_kurrentdb):
    mock_kurrentdb()
    run(dd_run_check, instance, tags=['team:storage'], endpoints=['/info'])

    aggregator.assert_metric('kurrentdb.is_leader', tags=['team:storage', f'endpoint:{BASE_URL}/info'])


def test_unavailable_endpoint_is_skipped(dd_run_check, aggregator, instance, mock_kurrentdb):
    mock_kurrentdb({'/projections/all-non-transient': MockResponse(status_code=404)})
    run(dd_run_check, instance)

    aggregator.assert_metric('kurrentdb.is_leader')
    aggregator.assert_metric('kurrentdb.projection.running', count=0)
    aggregator.assert_service_check(
        'kurrentdb.api.can_connect', count=0, tags=[f'endpoint:{BASE_URL}/projections/all-non-transient']
    )


def test_failing_endpoint_reports_critical(dd_run_check, aggregator, instance, mock_kurrentdb):
    mock_kurrentdb({'/gossip': MockResponse(status_code=500)})
    run(dd_run_check, instance)

    aggregator.assert_service_check(
        'kurrentdb.api.can_connect', KurrentdbCheck.CRITICAL, tags=[f'endpoint:{BASE_URL}/gossip']
    )
    aggregator.assert_metric('kurrentdb.cluster.member_alive', count=0)
    aggregator.assert_metric('kurrentdb.is_leader')
    aggregator.assert_metric('kurrentdb.proc_thread_count')


def test_invalid_json_reports_critical(dd_run_check, aggregator, instance, mock_kurrentdb):
    mock_kurrentdb({'/info': MockResponse(content='not json')})
    run(dd_run_check, instance)

    aggregator.assert_service_check(
        'kurrentdb.api.can_connect', KurrentdbCheck.CRITICAL, tags=[f'endpoint:{BASE_URL}/info']
    )


def test_endpoints_option_selects_endpoints(dd_run_check, aggregator, instance, mock_kurrentdb):
    mock_kurrentdb()
    run(dd_run_check, instance, endpoints=['/gossip'])

    aggregator.assert_metric('kurrentdb.cluster.member_alive')
    aggregator.assert_metric('kurrentdb.is_leader', count=0)
    aggregator.assert_metric('kurrentdb.proc.mem', count=0)
    aggregator.assert_metric('kurrentdb.proc_thread_count')


def test_empty_endpoints_only_collects_prometheus_metrics(dd_run_check, aggregator, instance, mock_kurrentdb):
    mock_kurrentdb()
    run(dd_run_check, instance, endpoints=[])

    aggregator.assert_metric('kurrentdb.cluster.member_alive', count=0)
    aggregator.assert_metric('kurrentdb.proc_thread_count')
    aggregator.assert_service_check('kurrentdb.api.can_connect', count=0)


def test_unknown_endpoint_is_ignored(dd_run_check, aggregator, instance, mock_kurrentdb):
    mock_kurrentdb()
    run(dd_run_check, instance, endpoints=['/nope', '/info'])

    aggregator.assert_metric('kurrentdb.is_leader')
    aggregator.assert_service_check('kurrentdb.api.can_connect', count=1)


def test_url_option_overrides_api_base_url(dd_run_check, aggregator, instance, mock_http_response_per_endpoint):
    mock_http_response_per_endpoint(
        {
            BASE_URL + '/metrics': [MockResponse(file_path=fixture_path('metrics.txt'))],
            'http://api.example:2113/info': [MockResponse(file_path=fixture_path('info.json'))],
        },
        mode='cycle',
        strict=False,
    )
    run(dd_run_check, instance, url='http://api.example:2113/', endpoints=['/info'])

    aggregator.assert_metric('kurrentdb.is_leader', tags=['endpoint:http://api.example:2113/info'])


@pytest.mark.parametrize(
    'value, expected',
    [
        ('0:00:00:00.9254789', 0.9254789),
        ('0:00:00:00.0012345', 0.0012345),
        ('1:02:03:04.5', 93784.5),
        ('739876.19:46:44.5430170', 739876 * 86400 + 19 * 3600 + 46 * 60 + 44.543017),
        ('00:01:30', 90.0),
        ('not a duration', None),
        (None, None),
        (5, None),
    ],
)
def test_parse_duration(value, expected):
    result = parse_duration(value)
    if expected is None:
        assert result is None
    else:
        assert result == pytest.approx(expected)


def test_api_base_url_is_derived_from_openmetrics_endpoint(dd_run_check, aggregator, mock_http_response_per_endpoint):
    mock_http_response_per_endpoint(
        {
            'https://kurrent.example:2113/metrics': [MockResponse(file_path=fixture_path('metrics.txt'))],
            'https://kurrent.example:2113/info': [MockResponse(file_path=fixture_path('info.json'))],
        },
        mode='cycle',
        strict=False,
    )
    run(dd_run_check, {'openmetrics_endpoint': 'https://kurrent.example:2113/metrics'}, endpoints=['/info'])

    aggregator.assert_metric('kurrentdb.is_leader', tags=['endpoint:https://kurrent.example:2113/info'])


def test_exclude_metrics_drops_matching_metrics(dd_run_check, aggregator, instance, mock_kurrentdb):
    mock_kurrentdb()
    run(dd_run_check, instance, exclude_metrics=['aspnetcore_.*', 'kurrentdb_io_events'])

    aggregator.assert_metric('kurrentdb.aspnetcore_memory_pool_allocated_bytes.count', count=0)
    aggregator.assert_metric('kurrentdb.aspnetcore_memory_pool_pooled_bytes', count=0)
    aggregator.assert_metric('kurrentdb.io_events.count', count=0)
    aggregator.assert_metric('kurrentdb.io_bytes.count')
