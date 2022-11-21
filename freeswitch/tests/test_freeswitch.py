from typing import Any, Callable, Dict

from datadog_checks.base import AgentCheck
from datadog_checks.base.stubs.aggregator import AggregatorStub
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.freeswitch import FreeswitchCheck

INVALID_TEST_INSTANCE = {}
VALID_TEST_INSTANCE = {
    "freeswitch_conf_dir": "/etc/freeswitch",
}


def test_check(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = FreeswitchCheck('freeswitch', {}, [instance])
    dd_run_check(check, True)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_instance_misconfigured(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = FreeswitchCheck('freeswitch', {}, [INVALID_TEST_INSTANCE])
    dd_run_check(check, True)

    aggregator.assert_service_check('freeswitch.services_up', AgentCheck.WARNING)


def test_services_down(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = FreeswitchCheck('freeswitch', {}, [VALID_TEST_INSTANCE])
    dd_run_check(check, True)

    aggregator.assert_service_check('freeswitch.services_up', AgentCheck.CRITICAL)


# TODO: validate aggregator.assert_service_check('freeswitch.services_up', AgentCheck.OK)
# TODO: validate aggregator.assert_service_check('freeswitch.metrics_up', AgentCheck.WARNING)
# TODO: validate aggregator.assert_service_check('freeswitch.metrics_up', AgentCheck.OK)
