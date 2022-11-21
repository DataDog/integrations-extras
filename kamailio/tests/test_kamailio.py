from typing import Any, Callable, Dict

from datadog_checks.base import AgentCheck
from datadog_checks.base.stubs.aggregator import AggregatorStub
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.kamailio import KamailioCheck

INVALID_TEST_INSTANCE = {}
VALID_TEST_INSTANCE = {
    "jsonrpc_api_url": "http://127.0.0.1:5060/api/kamailio",
}


def test_check(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = KamailioCheck('kamailio', {}, [instance])
    dd_run_check(check, True)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_instance_misconfigured(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = KamailioCheck('kamailio', {}, [INVALID_TEST_INSTANCE])
    dd_run_check(check, True)

    aggregator.assert_service_check('kamailio.services_up', AgentCheck.WARNING)


def test_services_down(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = KamailioCheck('kamailio', {}, [VALID_TEST_INSTANCE])
    dd_run_check(check, True)

    aggregator.assert_service_check('kamailio.services_up', AgentCheck.CRITICAL)


# TODO: validate aggregator.assert_service_check('kamailio.services_up', AgentCheck.OK)
# TODO: validate aggregator.assert_service_check('kamailio.metrics_up', AgentCheck.WARNING)
# TODO: validate aggregator.assert_service_check('kamailio.metrics_up', AgentCheck.OK)
