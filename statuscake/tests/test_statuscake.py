import pytest
from typing import Any, Callable, Dict  # noqa: F401

from datadog_checks.base import AgentCheck  # noqa: F401
from datadog_checks.base.stubs.aggregator import AggregatorStub  # noqa: F401
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.statuscake import StatuscakeCheck

#def test_check(dd_run_check, aggregator, instance):
#    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
#    check = StatuscakeCheck('statuscake', {}, [instance])
#    dd_run_check(check)
#
#    aggregator.assert_all_metrics_covered()
#    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
#
#
#def test_emits_critical_service_check_when_service_is_down(dd_run_check, aggregator, instance):
#    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
#    check = StatuscakeCheck('statuscake', {}, [instance])
#    dd_run_check(check)
#    aggregator.assert_service_check('statuscake.can_connect', StatuscakeCheck.CRITICAL)
#
@pytest.mark.unit
def test_config():
    instance = {}
    c = StatuscakeCheck('statuscake', {}, [instance])

    # empty instance. Expects CRITICAL.
    with pytest.raises(ConfigurationError):
        c.check(instance)

    # Test uptime. Expects OK.
    with pytest.raises(ConfigurationError):
        c.check({'statuscake_api_key':'jQWP8KOVstYwLJBTAdRDhMv16pf4E9','check_type':'uptime'})