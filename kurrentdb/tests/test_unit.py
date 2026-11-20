import json
import os

import pytest
import requests

from datadog_checks.dev.http import MockResponse
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.kurrentdb import KurrentdbCheck
from datadog_checks.kurrentdb.check import parse_duration

from .conftest import HERE

pytestmark = pytest.mark.unit

BASE_URL = 'http://localhost:2113'
# Exposed by KurrentDB before 26.1, so not in the 26.1 `metrics.txt` fixture
PRE_26_1_METRICS = {
    'kurrentdb.queue_busy_seconds.count',
    'kurrentdb.messaging_kurrent_producer_produce_duration_milliseconds.bucket',
    'kurrentdb.messaging_kurrent_producer_produce_duration_milliseconds.count',
    'kurrentdb.messaging_kurrent_producer_produce_duration_milliseconds.sum',
}
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
        mocked = mock_http_response_per_endpoint(responses, mode='cycle', strict=False)
        respond = mocked.side_effect

        # The fixture returns responses as-is, so raise exceptions to simulate transport failures
        def side_effect(*args, **kwargs):
            response = respond(*args, **kwargs)
            if isinstance(response, Exception):
                raise response
            return response

        mocked.side_effect = side_effect
        return mocked

    return mock


def run(dd_run_check, instance, **extra):
    check = KurrentdbCheck('kurrentdb', {}, [{**instance, **extra}])
    dd_run_check(check)
    return check


def test_check(dd_run_check, aggregator, instance, mock_kurrentdb):
    mock_kurrentdb()
    check = run(dd_run_check, instance)

    assert check.warnings == []
    aggregator.assert_service_check('kurrentdb.openmetrics.health', KurrentdbCheck.OK)
    metadata = {name: row for name, row in get_metadata_metrics().items() if name not in PRE_26_1_METRICS}
    aggregator.assert_metrics_using_metadata(metadata, check_submission_type=True, check_symmetric_inclusion=True)


def test_metrics_before_26_1(dd_run_check, aggregator, instance, mock_kurrentdb):
    mock_kurrentdb({'/metrics': MockResponse(file_path=fixture_path('metrics_25.0.txt'))})
    run(dd_run_check, instance)

    for metric in PRE_26_1_METRICS:
        aggregator.assert_metric(metric)
    aggregator.assert_metric(
        'kurrentdb.queue_busy_seconds.count', tags=[f'endpoint:{BASE_URL}/metrics', 'queue:Readers']
    )
    aggregator.assert_metrics_using_metadata(get_metadata_metrics(), check_submission_type=True)


def test_up_time_is_a_gauge(dd_run_check, aggregator, instance, mock_kurrentdb):
    mock_kurrentdb()
    run(dd_run_check, instance)

    aggregator.assert_metric('kurrentdb.proc_up_time_seconds', 5, metric_type=aggregator.GAUGE)
    aggregator.assert_metric('kurrentdb.proc_up_time_seconds.count', count=0)


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
    check = run(dd_run_check, instance)

    assert check.warnings == []
    aggregator.assert_metric('kurrentdb.is_leader')
    aggregator.assert_metric('kurrentdb.projection.running', count=0)


def test_every_endpoint_not_found_warns(dd_run_check, aggregator, instance, mock_kurrentdb):
    mock_kurrentdb()
    check = run(dd_run_check, instance, url='http://localhost:2113/wrong')

    assert len(check.warnings) == 1
    assert 'Every KurrentDB API endpoint returned 404' in check.warnings[0]
    aggregator.assert_metric('kurrentdb.is_leader', count=0)
    aggregator.assert_metric('kurrentdb.proc_thread_count')


@pytest.mark.parametrize(
    'endpoint, response, missing_metric',
    [
        pytest.param('/gossip', MockResponse(status_code=500), 'kurrentdb.cluster.member_alive', id='http_500'),
        pytest.param('/info', MockResponse(content='not json'), 'kurrentdb.is_leader', id='invalid_json'),
        pytest.param(
            '/stats', requests.exceptions.ConnectionError('refused'), 'kurrentdb.proc.mem', id='connection_error'
        ),
    ],
)
def test_api_failure_is_reported(
    dd_run_check, aggregator, instance, mock_kurrentdb, endpoint, response, missing_metric
):
    mock_kurrentdb({endpoint: response})
    check = run(dd_run_check, instance)

    assert len(check.warnings) == 1
    assert check.warnings[0].startswith(f'Unable to collect from KurrentDB API endpoint {BASE_URL}{endpoint}: ')
    aggregator.assert_metric(missing_metric, count=0)
    aggregator.assert_metric('kurrentdb.subscription.live')
    aggregator.assert_metric('kurrentdb.proc_thread_count')


def test_scrape_failure_still_collects_api_metrics(dd_run_check, aggregator, instance, mock_kurrentdb):
    mock_kurrentdb({'/metrics': MockResponse(status_code=500)})
    with pytest.raises(Exception, match='500'):
        run(dd_run_check, instance)

    aggregator.assert_service_check('kurrentdb.openmetrics.health', KurrentdbCheck.CRITICAL)
    aggregator.assert_metric('kurrentdb.cluster.member_alive')
    aggregator.assert_metric('kurrentdb.is_leader')


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


def test_unknown_endpoint_is_a_configuration_error(dd_run_check, aggregator, instance, mock_kurrentdb):
    mock_kurrentdb()
    with pytest.raises(Exception, match=r"Unknown KurrentDB API endpoints \['/stat'\]"):
        run(dd_run_check, instance, endpoints=['/stat', '/info'])

    aggregator.assert_metric('kurrentdb.is_leader', count=0)


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
