import pytest

from datadog_checks.base.constants import ServiceCheck
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.volcano import VolcanoCheck

from .common import (
    BAD_HOSTNAME_INSTANCE,
    CAPACITY_METRICS,
    CONTROLLER_METRICS,
    PROPORTION_METRICS,
    SCHEDULER_METRICS,
)
from .conftest import mock_metrics_response

pytestmark = [pytest.mark.unit]

FIXTURES = ('scheduler.txt', 'scheduler_capacity.txt', 'controllers.txt')


def test_connect_exception(dd_run_check, aggregator):
    with pytest.raises(Exception, match="Failed to resolve 'invalid-hostname'|Max retries exceeded"):
        check = VolcanoCheck('volcano', {}, [BAD_HOSTNAME_INSTANCE])
        dd_run_check(check)

    aggregator.assert_service_check('volcano.openmetrics.health', ServiceCheck.CRITICAL)


@pytest.mark.parametrize(
    'fixture_name, expected_metrics',
    [
        pytest.param('scheduler.txt', SCHEDULER_METRICS + PROPORTION_METRICS, id='scheduler (proportion plugin)'),
        pytest.param('scheduler_capacity.txt', SCHEDULER_METRICS + CAPACITY_METRICS, id='scheduler (capacity plugin)'),
        pytest.param('controllers.txt', CONTROLLER_METRICS, id='controller manager'),
    ],
)
def test_check_metrics(dd_run_check, aggregator, instance, fixture_name, expected_metrics):
    check = VolcanoCheck('volcano', {}, [instance])
    with mock_metrics_response(fixture_name):
        dd_run_check(check)

    for metric_name in expected_metrics:
        aggregator.assert_metric(metric_name, at_least=1)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_service_check('volcano.openmetrics.health', ServiceCheck.OK)


def test_metadata_covers_all_components(dd_run_check, aggregator, instance):
    for fixture_name in FIXTURES:
        check = VolcanoCheck('volcano', {}, [instance])
        with mock_metrics_response(fixture_name):
            dd_run_check(check)

    aggregator.assert_metrics_using_metadata(get_metadata_metrics(), check_symmetric_inclusion=True)


def test_labels(dd_run_check, aggregator, check):
    with mock_metrics_response('scheduler.txt'):
        dd_run_check(check)

    endpoint_tag = 'endpoint:' + check.instance['openmetrics_endpoint']
    aggregator.assert_metric(
        'volcano.queue.weight', value=2, metric_type=aggregator.GAUGE, tags=[endpoint_tag, 'queue_name:research']
    )
    aggregator.assert_metric_has_tag('volcano.action_scheduling_latency.count', 'action:allocate')
    aggregator.assert_metric_has_tag('volcano.queue.allocated.scalar_resources', 'resource:pods')


def test_controller_job_phases(dd_run_check, aggregator, check):
    with mock_metrics_response('controllers.txt'):
        dd_run_check(check)

    aggregator.assert_metric_has_tag('volcano.job.completed.count', 'queue_name:research')
    aggregator.assert_metric_has_tag('volcano.job.failed.count', 'queue_name:default')
    aggregator.assert_metric(
        'volcano.queue.pod_group.pending',
        value=1,
        metric_type=aggregator.GAUGE,
        tags=['endpoint:' + check.instance['openmetrics_endpoint'], 'queue_name:research'],
    )


def test_empty_instance(dd_run_check):
    with pytest.raises(
        Exception,
        match='\nopenmetrics_endpoint\n  Field required',
    ):
        check = VolcanoCheck('volcano', {}, [{}])
        dd_run_check(check)
