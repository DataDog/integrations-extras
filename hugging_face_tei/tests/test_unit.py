import pytest

from datadog_checks.base.constants import ServiceCheck
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.hugging_face_tei import HuggingFaceTeiCheck

from .common import BAD_HOSTNAME_INSTANCE, EMBEDDING_METRICS, RERANK_METRICS
from .conftest import mock_metrics_response

pytestmark = [pytest.mark.unit]


def test_connect_exception(dd_run_check, aggregator):
    with pytest.raises(Exception, match="Failed to resolve 'invalid-hostname'|Max retries exceeded"):
        check = HuggingFaceTeiCheck('hugging_face_tei', {}, [BAD_HOSTNAME_INSTANCE])
        dd_run_check(check)

    aggregator.assert_service_check('hugging_face_tei.openmetrics.health', ServiceCheck.CRITICAL)


@pytest.mark.parametrize(
    'fixture_name, expected_metrics',
    [
        pytest.param('metrics.txt', EMBEDDING_METRICS, id='embedding model'),
        pytest.param('metrics_rerank.txt', RERANK_METRICS, id='re-ranker model'),
    ],
)
def test_check_metrics(dd_run_check, aggregator, instance, fixture_name, expected_metrics):
    check = HuggingFaceTeiCheck('hugging_face_tei', {}, [instance])
    with mock_metrics_response(fixture_name):
        dd_run_check(check)

    for metric_name in expected_metrics:
        aggregator.assert_metric(metric_name, at_least=1)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_service_check('hugging_face_tei.openmetrics.health', ServiceCheck.OK)


def test_metadata_covers_both_model_types(dd_run_check, aggregator, instance):
    for fixture_name in ('metrics.txt', 'metrics_rerank.txt'):
        check = HuggingFaceTeiCheck('hugging_face_tei', {}, [instance])
        with mock_metrics_response(fixture_name):
            dd_run_check(check)

    aggregator.assert_metrics_using_metadata(get_metadata_metrics(), check_symmetric_inclusion=True)


def test_labels(dd_run_check, aggregator, check):
    with mock_metrics_response('metrics.txt'):
        dd_run_check(check)

    aggregator.assert_metric(
        'hugging_face_tei.request.count',
        value=5,
        tags=['endpoint:' + check.instance['openmetrics_endpoint'], 'method:batch'],
    )
    aggregator.assert_metric_has_tag('hugging_face_tei.request.failure.count', 'error_type:tokenization')
    aggregator.assert_metric('hugging_face_tei.queue.size', value=0, metric_type=aggregator.GAUGE)


def test_empty_instance(dd_run_check):
    with pytest.raises(
        Exception,
        match='\nopenmetrics_endpoint\n  Field required',
    ):
        check = HuggingFaceTeiCheck('hugging_face_tei', {}, [{}])
        dd_run_check(check)
