"""
Integration tests for the Huntress SIEM check against a live Mockoon mock server.

Run with Docker available:
  ddev test huntress -m integration
"""
import pytest

from datadog_checks.base import AgentCheck
from datadog_checks.huntress import HuntressCheck

pytestmark = pytest.mark.integration


def test_integration_check_runs(dd_environment, aggregator):
    """Full check run against the Mockoon server — verifies happy path end-to-end."""
    instance = dd_environment
    check = HuntressCheck("huntress", {}, [instance])
    check.check(instance)

    aggregator.assert_metric("huntress.siem.logs_collected", at_least=0)
    aggregator.assert_metric("huntress.siem.pages_fetched", at_least=1)
    aggregator.assert_metric("huntress.siem.run_duration_seconds", at_least=0)
    aggregator.assert_metric("huntress.siem.api_call_limit", value=60)
    aggregator.assert_metric("huntress.siem.api_call_remaining", value=55)
    aggregator.assert_service_check("huntress.siem.check_status", status=AgentCheck.OK)
    aggregator.assert_all_metrics_covered()


def test_integration_org_enrichment(dd_environment, aggregator):
    """Verify org metadata is fetched from the mock and applied to logs."""
    instance = dict(dd_environment, enrich_with_org_tags=True, org_cache_ttl_seconds=0)
    check = HuntressCheck("huntress", {}, [instance])

    sent_logs = []
    original_send = check._send_logs_batch

    def capture(batch):
        sent_logs.extend(batch)
        original_send(batch)

    check._send_logs_batch = capture
    check.check(instance)

    assert sent_logs, "Expected at least one log to be forwarded"
    for log in sent_logs:
        assert "huntress_account_id" in log.get("ddtags", ""), (
            f"Missing huntress_account_id in ddtags: {log.get('ddtags')}"
        )


def test_integration_rate_limit_metrics(dd_environment, aggregator):
    """Verify rate limit headers are parsed and emitted as metrics."""
    instance = dict(dd_environment, enrich_with_org_tags=False)
    check = HuntressCheck("huntress", {}, [instance])
    check.check(instance)

    aggregator.assert_metric("huntress.siem.api_call_limit", value=60)
    aggregator.assert_metric("huntress.siem.api_call_remaining", value=55)
