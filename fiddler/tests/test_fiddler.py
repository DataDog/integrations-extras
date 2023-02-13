from typing import Any, Callable, Dict

import pytest

from datadog_checks.base import AgentCheck
from datadog_checks.base.stubs.aggregator import AggregatorStub
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.fiddler import FiddlerCheck

from .conftest import FIDDLER_API_KEY


# Minimal test
def test_check(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = FiddlerCheck('fiddler', {}, [instance])
    # Prevent the integration from failing
    with pytest.raises(Exception) as e:
        dd_run_check(check)
        assert 'Authorization Required' in str(e.value)


@pytest.mark.skipif(not FIDDLER_API_KEY, reason="Local testing only")
def test_metric_collection(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = FiddlerCheck('fiddler', {}, [instance])
    dd_run_check(check)

    aggregator.assert_service_check('fiddler.can_connect', FiddlerCheck.OK)
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())

    aggregator.assert_metric('fiddler.accuracy')
    aggregator.assert_metric('fiddler.histogram_drift')
    aggregator.assert_metric('fiddler.feature_average')
    aggregator.assert_metric('fiddler.output_average')
    aggregator.assert_metric('fiddler.traffic_count')
    aggregator.assert_metric('fiddler.binary_cross_entropy')
    aggregator.assert_metric('fiddler.data_count')
    aggregator.assert_metric('fiddler.expected_callibration_error')
    aggregator.assert_metric('fiddler.fpr')
    aggregator.assert_metric('fiddler.precision')

    # aggregator.assert_all_metrics_covered()


@pytest.mark.e2e
@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_service_check(aggregator, instance):
    c = FiddlerCheck('fiddler', {}, [instance])

    # the check should send OK
    c.check(instance)
    aggregator.assert_service_check('fiddler.can_connect', FiddlerCheck.OK)
