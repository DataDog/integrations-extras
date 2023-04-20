# (C) Datadog, Inc. 2023-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

from pathlib import Path

from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.mergify import MergifyCheck

MERGIFY_RESPONSE_FIXTURES = Path(__file__).absolute().parent / "fixtures"


def test_emits_critical_service_check_when_service_is_down(aggregator, instance):
    # type: (AggregatorStub, Dict[str, Any]) -> None
    check = MergifyCheck("mergify", {}, [instance])
    check.run()
    aggregator.assert_service_check("mergify.can_connect", MergifyCheck.CRITICAL)


def test_check(dd_run_check, aggregator, instance, mock_http_response):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any], MockResponse) -> None

    mock_http_response(
        file_path=MERGIFY_RESPONSE_FIXTURES / "queues.json",
        headers={"Content-Type": "application/json"},
    )
    check = MergifyCheck("mergify", {}, [instance])

    dd_run_check(check)
    aggregator.assert_metric(
        "mergify.merge_queue_length",
        value=2,
        tags=instance["tags"] + ["branch:main", "repository:owner/repository"],
    )
    aggregator.assert_service_check("mergify.can_connect", MergifyCheck.OK)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
