from typing import Any, Callable, Dict

from datadog_checks.base import AgentCheck
from datadog_checks.base.stubs.aggregator import AggregatorStub
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.homer import HomerCheck

INVALID_TEST_INSTANCE = {}
VALID_TEST_INSTANCE = {
    "homer_service_checks": ["postgres", "heplify-server", "homer-app"],
    "homer_config_db": {"user": "homer", "pass": "secret", "host": "localhost", "port": 5432, "name": "homer_config"},
    "homer_data_db": {"user": "homer", "pass": "secret", "host": "localhost", "port": 5432, "name": "homer_data"},
}


def test_check(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = HomerCheck('homer', {}, [instance])
    dd_run_check(check, True)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_instance_misconfigured(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = HomerCheck('homer', {}, [INVALID_TEST_INSTANCE])
    dd_run_check(check, True)

    aggregator.assert_service_check('homer.services_up', AgentCheck.WARNING)


def test_services_down(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = HomerCheck('homer', {}, [VALID_TEST_INSTANCE])
    dd_run_check(check, True)

    aggregator.assert_service_check('homer.services_up', AgentCheck.CRITICAL)


# TODO: validate aggregator.assert_service_check('homer.services_up', AgentCheck.OK)
# TODO: validate aggregator.assert_service_check('homer.metrics_up', AgentCheck.WARNING)
# TODO: validate aggregator.assert_service_check('homer.metrics_up', AgentCheck.OK)
