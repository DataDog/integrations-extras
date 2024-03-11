import pytest

from typing import Any, Callable, Dict  # noqa: F401

# from datadog_checks.base import AgentCheck  # noqa: F401
# from datadog_checks.base.stubs.aggregator import AggregatorStub  # noqa: F401
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.redis_enterprise import RedisEnterpriseCheck


@pytest.mark.unit
def test_check(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = RedisEnterpriseCheck(
        'redis_enterprise', {}, [{'openmetrics_endpoint': 'https://localhost:8070', 'tls_verify': 'false'}])
    dd_run_check(check)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


@pytest.mark.unit
def test_emits_critical_service_check_when_service_is_down(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = RedisEnterpriseCheck(
        'redis_enterprise', {}, [{'openmetrics_endpoint': 'https://localhost:8071', 'tls_verify': 'false'}])

    dd_run_check(check)
    aggregator.assert_service_check('redis_enterprise.can_connect', RedisEnterpriseCheck.CRITICAL)
