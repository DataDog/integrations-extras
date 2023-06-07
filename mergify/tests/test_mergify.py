# (C) Datadog, Inc. 2023-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

from pathlib import Path

from datadog_checks.dev.http import MockResponse
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.mergify import MergifyCheck

MERGIFY_RESPONSE_FIXTURES = Path(__file__).absolute().parent / "fixtures"


def test_emits_critical_service_check_when_service_is_down(aggregator, instance):
    # type: (AggregatorStub, Dict[str, Any]) -> None
    check = MergifyCheck("mergify", {}, [instance])
    check.run()
    aggregator.assert_service_check("mergify.can_connect", MergifyCheck.CRITICAL)


def test_check(dd_run_check, aggregator, instance, mocker):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any], MockResponse) -> None

    headers = {"Content-Type": "application/json"}

    def mock_requests_get(url, *args, **kwargs):
        if url.endswith("time_to_merge?branch=main"):
            return MockResponse(
                file_path=MERGIFY_RESPONSE_FIXTURES / "time_to_merge_main.json",
                headers=headers,
            )

        if url.endswith("queue_checks_outcome?branch=main"):
            return MockResponse(
                file_path=MERGIFY_RESPONSE_FIXTURES / "queue_checks_outcome_main.json",
                headers=headers,
            )

        if url.endswith("queues"):
            return MockResponse(
                file_path=MERGIFY_RESPONSE_FIXTURES / "queues.json",
                headers=headers,
            )

        raise AssertionError(f"URL not mocked: {url}")

    mocker.patch("requests.get", mock_requests_get)
    check = MergifyCheck("mergify", {}, [instance])

    dd_run_check(check)

    aggregator.assert_metric(
        "mergify.merge_queue_length",
        value=2,
        tags=instance["tags"] + ["branch:main", "repository:owner/repository"],
    )

    # ### Time to merge metrics
    default_queue_tags = instance["tags"] + [
        "branch:main",
        "repository:owner/repository",
        "partition:__default__",
        "queue:default",
    ]
    hotfix_queue_tags = instance["tags"] + [
        "branch:main",
        "repository:owner/repository",
        "partition:__default__",
        "queue:hotfix",
    ]

    # Default queue
    aggregator.assert_metric(
        "mergify.time_to_merge.median",
        value=60.1,
        tags=default_queue_tags,
    )
    aggregator.assert_metric(
        "mergify.time_to_merge.mean",
        value=70.2,
        tags=default_queue_tags,
    )

    # Hotfix queue
    aggregator.assert_metric(
        "mergify.time_to_merge.median",
        value=5.0,
        tags=hotfix_queue_tags,
    )
    aggregator.assert_metric(
        "mergify.time_to_merge.mean",
        value=4.5,
        tags=hotfix_queue_tags,
    )

    # ### Queue checks outcome metrics

    # Default queue
    expected_metrics = {
        "PR_DEQUEUED": 16,
        "PR_AHEAD_DEQUEUED": 15,
        "PR_AHEAD_FAILED_TO_MERGE": 14,
        "PR_WITH_HIGHER_PRIORITY_QUEUED": 13,
        "PR_QUEUED_TWICE": 12,
        "SPECULATIVE_CHECK_NUMBER_REDUCED": 11,
        "CHECKS_TIMEOUT": 10,
        "CHECKS_FAILED": 9,
        "QUEUE_RULE_MISSING": 8,
        "UNEXPECTED_QUEUE_CHANGE": 7,
        "PR_FROZEN_NO_CASCADING": 6,
        "TARGET_BRANCH_CHANGED": 4,
        "TARGET_BRANCH_MISSING": 3,
        "PR_UNEXPECTEDLY_FAILED_TO_MERGE": 2,
        "BATCH_MAX_FAILURE_RESOLUTION_ATTEMPTS": 1,
    }
    for metric, value in expected_metrics.items():
        aggregator.assert_metric(
            "mergify.queue_checks_outcome",
            value=value,
            tags=default_queue_tags + [f"outcome_type:{metric}"],
        )

    # Hotfix queue
    expected_metrics = {
        "PR_DEQUEUED": 1,
        "PR_AHEAD_DEQUEUED": 2,
        "PR_AHEAD_FAILED_TO_MERGE": 3,
        "PR_WITH_HIGHER_PRIORITY_QUEUED": 4,
        "PR_QUEUED_TWICE": 5,
        "SPECULATIVE_CHECK_NUMBER_REDUCED": 6,
        "CHECKS_TIMEOUT": 7,
        "CHECKS_FAILED": 8,
        "QUEUE_RULE_MISSING": 9,
        "UNEXPECTED_QUEUE_CHANGE": 10,
        "PR_FROZEN_NO_CASCADING": 11,
        "TARGET_BRANCH_CHANGED": 13,
        "TARGET_BRANCH_MISSING": 14,
        "PR_UNEXPECTEDLY_FAILED_TO_MERGE": 15,
        "BATCH_MAX_FAILURE_RESOLUTION_ATTEMPTS": 16,
    }
    for metric, value in expected_metrics.items():
        aggregator.assert_metric(
            "mergify.queue_checks_outcome",
            value=value,
            tags=hotfix_queue_tags + [f"outcome_type:{metric}"],
        )

    # ######
    aggregator.assert_service_check("mergify.can_connect", MergifyCheck.OK)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_check_empty_values(dd_run_check, aggregator, instance, mocker):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any], MockResponse) -> None

    headers = {"Content-Type": "application/json"}

    def mock_requests_get(url, *args, **kwargs):
        if url.endswith("time_to_merge?branch=main"):
            return MockResponse(
                file_path=MERGIFY_RESPONSE_FIXTURES / "time_to_merge_empty.json",
                headers=headers,
            )

        if url.endswith("queue_checks_outcome?branch=main"):
            return MockResponse(
                file_path=MERGIFY_RESPONSE_FIXTURES / "queue_checks_outcome_empty.json",
                headers=headers,
            )

        if url.endswith("queues"):
            return MockResponse(
                file_path=MERGIFY_RESPONSE_FIXTURES / "queues_empty.json",
                headers=headers,
            )

        raise AssertionError(f"URL not mocked: {url}")

    mocker.patch("requests.get", mock_requests_get)
    check = MergifyCheck("mergify", {}, [instance])

    dd_run_check(check)

    aggregator.assert_metric(
        "mergify.merge_queue_length",
        value=0,
        tags=instance["tags"] + ["branch:main", "repository:owner/repository"],
    )
    default_queue_tags = instance["tags"] + [
        "branch:main",
        "repository:owner/repository",
        "partition:__default__",
        "queue:default",
    ]
    hotfix_queue_tags = instance["tags"] + [
        "branch:main",
        "repository:owner/repository",
        "partition:__default__",
        "queue:hotfix",
    ]

    # ### Time to merge metrics should not be sent since they are set to None
    # (no data yet)

    # ### Queue checks outcome metrics
    # Default queue
    expected_metrics = {
        "PR_DEQUEUED": 0,
        "PR_AHEAD_DEQUEUED": 0,
        "PR_AHEAD_FAILED_TO_MERGE": 0,
        "PR_WITH_HIGHER_PRIORITY_QUEUED": 0,
        "PR_QUEUED_TWICE": 0,
        "SPECULATIVE_CHECK_NUMBER_REDUCED": 0,
        "CHECKS_TIMEOUT": 0,
        "CHECKS_FAILED": 0,
        "QUEUE_RULE_MISSING": 0,
        "UNEXPECTED_QUEUE_CHANGE": 0,
        "PR_FROZEN_NO_CASCADING": 0,
        "TARGET_BRANCH_CHANGED": 0,
        "TARGET_BRANCH_MISSING": 0,
        "PR_UNEXPECTEDLY_FAILED_TO_MERGE": 0,
        "BATCH_MAX_FAILURE_RESOLUTION_ATTEMPTS": 0,
    }
    for metric, value in expected_metrics.items():
        aggregator.assert_metric(
            "mergify.queue_checks_outcome",
            value=value,
            tags=default_queue_tags + [f"outcome_type:{metric}"],
        )

    # Hotfix queue
    for metric, value in expected_metrics.items():
        aggregator.assert_metric(
            "mergify.queue_checks_outcome",
            value=value,
            tags=hotfix_queue_tags + [f"outcome_type:{metric}"],
        )

    # ######
    aggregator.assert_service_check("mergify.can_connect", MergifyCheck.OK)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
