import pytest

from datadog_checks.base.constants import ServiceCheck
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.xinference import XinferenceCheck

from .common import BAD_HOSTNAME_INSTANCE, SUPERVISOR_METRICS, WORKER_METRICS
from .conftest import mock_metrics_response

pytestmark = [pytest.mark.unit]

MODEL_TAGS = [
    'engine:llama.cpp',
    'format:ggufv2',
    'gpu_index:',
    'model_name:stories',
    'model_type:LLM',
    'model_uid:stories',
    'quantization:none',
    'replica_index:0',
    'worker_address:127.0.0.1:14454',
]


def test_connect_exception(dd_run_check, aggregator):
    with pytest.raises(Exception, match="Failed to resolve 'invalid-hostname'|Max retries exceeded"):
        check = XinferenceCheck('xinference', {}, [BAD_HOSTNAME_INSTANCE])
        dd_run_check(check)

    aggregator.assert_service_check('xinference.openmetrics.health', ServiceCheck.CRITICAL)


@pytest.mark.parametrize(
    'fixture_name, expected_metrics',
    [
        pytest.param('supervisor.txt', SUPERVISOR_METRICS, id='supervisor'),
        pytest.param('worker.txt', WORKER_METRICS, id='worker'),
    ],
)
def test_check_metrics(dd_run_check, aggregator, instance, fixture_name, expected_metrics):
    check = XinferenceCheck('xinference', {}, [instance])
    with mock_metrics_response(fixture_name):
        dd_run_check(check)

    for metric_name in expected_metrics:
        aggregator.assert_metric(metric_name, at_least=1)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_service_check('xinference.openmetrics.health', ServiceCheck.OK)


def test_metadata_covers_all_components(dd_run_check, aggregator, instance):
    for fixture_name in ('supervisor.txt', 'worker.txt'):
        check = XinferenceCheck('xinference', {}, [instance])
        with mock_metrics_response(fixture_name):
            dd_run_check(check)

    aggregator.assert_metrics_using_metadata(get_metadata_metrics(), check_symmetric_inclusion=True)


def test_supervisor_labels(dd_run_check, aggregator, check):
    with mock_metrics_response('supervisor.txt'):
        dd_run_check(check)

    endpoint_tag = 'endpoint:' + check.instance['openmetrics_endpoint']
    aggregator.assert_metric('xinference.workers', value=1, metric_type=aggregator.GAUGE, tags=[endpoint_tag])
    aggregator.assert_metric(
        'xinference.model.status',
        value=1,
        metric_type=aggregator.GAUGE,
        tags=[endpoint_tag, 'model_name:stories', 'model_uid:stories', 'status:READY'],
    )
    aggregator.assert_metric(
        'xinference.api_key.requests.count',
        value=1,
        tags=[
            endpoint_tag,
            'api_key_name:limited2',
            'model_id:stories',
            'model_name:stories',
            'model_type:LLM',
            'status:denied',
            'user:admin',
        ],
    )
    aggregator.assert_metric_has_tag('xinference.api.responses.by_status.count', 'status_code:404')


def test_worker_labels(dd_run_check, aggregator, check):
    with mock_metrics_response('worker.txt'):
        dd_run_check(check)

    endpoint_tag = 'endpoint:' + check.instance['openmetrics_endpoint']
    aggregator.assert_metric('xinference.tokens.output.count', value=148, tags=[endpoint_tag] + MODEL_TAGS)
    aggregator.assert_metric('xinference.model.request.errors.count', value=1, tags=[endpoint_tag] + MODEL_TAGS)
    aggregator.assert_metric_has_tag('xinference.time_to_first_token.count', 'stream:true')


def test_empty_instance(dd_run_check):
    with pytest.raises(
        Exception,
        match='\nopenmetrics_endpoint\n  Field required',
    ):
        check = XinferenceCheck('xinference', {}, [{}])
        dd_run_check(check)
