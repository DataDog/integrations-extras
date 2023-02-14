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

    # assert metrics we expect, and set at_least to 0 for the metrics that may not be present depending on the models
    aggregator.assert_metric('fiddler.accuracy', at_least=0)
    aggregator.assert_metric('fiddler.histogram_drift')
    aggregator.assert_metric('fiddler.feature_average')
    aggregator.assert_metric('fiddler.output_average')
    aggregator.assert_metric('fiddler.traffic_count')
    aggregator.assert_metric('fiddler.binary_cross_entropy', at_least=0)
    aggregator.assert_metric('fiddler.data_count', at_least=0)
    aggregator.assert_metric('fiddler.expected_callibration_error', at_least=0)
    aggregator.assert_metric('fiddler.fpr', at_least=0)
    aggregator.assert_metric('fiddler.precision', at_least=0)
    aggregator.assert_metric('fiddler.auc', at_least=0)
    aggregator.assert_metric('fiddler.auroc', at_least=0)
    aggregator.assert_metric('fiddler.recall', at_least=0)
    aggregator.assert_metric('fiddler.mape', at_least=0)
    aggregator.assert_metric('fiddler.wmape', at_least=0)
    aggregator.assert_metric('fiddler.mae', at_least=0)
    aggregator.assert_metric('fiddler.mse', at_least=0)
    aggregator.assert_metric('fiddler.r2', at_least=0)
    aggregator.assert_metric('fiddler.callibrated_threshold', at_least=0)
    aggregator.assert_metric('fiddler.g_mean', at_least=0)
    aggregator.assert_metric('fiddler.f1_score', at_least=0)

    # ensure all metrics are covered at least 0 or 1 times
    aggregator.assert_all_metrics_covered()


@pytest.mark.e2e
@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_service_check(aggregator, instance):
    c = FiddlerCheck('fiddler', {}, [instance])

    # the check should send OK
    c.check(instance)
    aggregator.assert_service_check('fiddler.can_connect', FiddlerCheck.OK)
