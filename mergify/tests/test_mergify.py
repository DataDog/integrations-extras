# (C) Datadog, Inc. 2023-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

from pathlib import Path

from datadog_checks.dev.http import MockResponse
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.mergify import MergifyCheck

MERGIFY_RESPONSE_FIXTURES = Path(__file__).absolute().parent / "fixtures"

HEADERS = {"Content-Type": "application/json"}


def test_emits_critical_service_check_when_service_is_down(aggregator, instance):
    # type: (AggregatorStub, Dict[str, Any]) -> None
    check = MergifyCheck("mergify", {}, [instance])
    check.run()
    aggregator.assert_service_check("mergify.can_connect", MergifyCheck.CRITICAL)


def test_emits_warning_when_ratelimited(aggregator, instance, mocker):
    # type: (AggregatorStub, Dict[str, Any]) -> None
    check = MergifyCheck("mergify", {}, [instance])

    def mock_requests_get(url, *args, **kwargs):
        return MockResponse(
            status_code=403,
            file_path=MERGIFY_RESPONSE_FIXTURES / "ratelimited_github.json",
            headers=HEADERS,
        )

    mocker.patch("requests.get", mock_requests_get)
    check.run()
    aggregator.assert_service_check("mergify.can_connect", MergifyCheck.WARNING)


def test_check(dd_run_check, aggregator, instance, mocker):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any], MockResponse) -> None

    def mock_requests_get(url, *args, **kwargs):
        if url.endswith("time_to_merge?branch=main"):
            return MockResponse(
                file_path=MERGIFY_RESPONSE_FIXTURES / "time_to_merge_main.json",
                headers=HEADERS,
            )

        if url.endswith("merge_queue_checks_outcome"):
            return MockResponse(
                file_path=MERGIFY_RESPONSE_FIXTURES / "queue_checks_outcome_main.json",
                headers=HEADERS,
            )

        if url.endswith("queues"):
            return MockResponse(
                file_path=MERGIFY_RESPONSE_FIXTURES / "queues.json",
                headers=HEADERS,
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
        "BASE_BRANCH_CHANGED": 12,
        "BASE_BRANCH_MISSING": 9,
        "BATCH_MAX_FAILURE_RESOLUTION_ATTEMPTS": 5,
        "BRANCH_UPDATE_FAILED": 4,
        "CHECKS_FAILED": 1,
        "CHECKS_TIMEOUT": 7,
        "CONFLICT_WITH_BASE_BRANCH": 8,
        "CONFLICT_WITH_PULL_AHEAD": 2,
        "DRAFT_PULL_REQUEST_CHANGED": 9,
        "INCOMPATIBILITY_WITH_BRANCH_PROTECTIONS": 11,
        "MERGE_QUEUE_RESET": 5,
        "PR_AHEAD_DEQUEUED": 0,
        "PR_AHEAD_FAILED_TO_MERGE": 2,
        "PR_CHECKS_STOPPED_BECAUSE_MERGE_QUEUE_PAUSE": 7,
        "PR_DEQUEUED": 12,
        "PR_FROZEN_NO_CASCADING": 6,
        "PR_QUEUED_TWICE": 1,
        "PR_UNEXPECTEDLY_FAILED_TO_MERGE": 3,
        "PR_WITH_HIGHER_PRIORITY_QUEUED": 7,
        "PULL_REQUEST_UPDATED": 10,
        "QUEUE_RULE_MISSING": 0,
        "SPECULATIVE_CHECK_NUMBER_REDUCED": 4,
        "SUCCESS": 4,
        "UNEXPECTED_QUEUE_CHANGE": 30,
    }
    for metric, value in expected_metrics.items():
        aggregator.assert_metric(
            "mergify.queue_checks_outcome",
            value=value,
            tags=default_queue_tags + [f"outcome_type:{metric}"],
        )

    # Hotfix queue
    expected_metrics = {
        "BASE_BRANCH_CHANGED": 1,
        "BASE_BRANCH_MISSING": 2,
        "BATCH_MAX_FAILURE_RESOLUTION_ATTEMPTS": 3,
        "BRANCH_UPDATE_FAILED": 4,
        "CHECKS_FAILED": 5,
        "CHECKS_TIMEOUT": 6,
        "CONFLICT_WITH_BASE_BRANCH": 7,
        "CONFLICT_WITH_PULL_AHEAD": 8,
        "DRAFT_PULL_REQUEST_CHANGED": 9,
        "INCOMPATIBILITY_WITH_BRANCH_PROTECTIONS": 10,
        "MERGE_QUEUE_RESET": 11,
        "PR_AHEAD_DEQUEUED": 12,
        "PR_AHEAD_FAILED_TO_MERGE": 13,
        "PR_CHECKS_STOPPED_BECAUSE_MERGE_QUEUE_PAUSE": 14,
        "PR_DEQUEUED": 15,
        "PR_FROZEN_NO_CASCADING": 16,
        "PR_QUEUED_TWICE": 17,
        "PR_UNEXPECTEDLY_FAILED_TO_MERGE": 18,
        "PR_WITH_HIGHER_PRIORITY_QUEUED": 19,
        "PULL_REQUEST_UPDATED": 20,
        "QUEUE_RULE_MISSING": 21,
        "SPECULATIVE_CHECK_NUMBER_REDUCED": 22,
        "SUCCESS": 23,
        "UNEXPECTED_QUEUE_CHANGE": 24,
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

    def mock_requests_get(url, *args, **kwargs):
        if url.endswith("time_to_merge?branch=main"):
            return MockResponse(
                file_path=MERGIFY_RESPONSE_FIXTURES / "time_to_merge_empty.json",
                headers=HEADERS,
            )

        if url.endswith("merge_queue_checks_outcome"):
            return MockResponse(
                file_path=MERGIFY_RESPONSE_FIXTURES / "queue_checks_outcome_empty.json",
                headers=HEADERS,
            )

        if url.endswith("queues"):
            return MockResponse(
                file_path=MERGIFY_RESPONSE_FIXTURES / "queues_empty.json",
                headers=HEADERS,
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
        "BASE_BRANCH_CHANGED": 0,
        "BASE_BRANCH_MISSING": 0,
        "BATCH_MAX_FAILURE_RESOLUTION_ATTEMPTS": 0,
        "BRANCH_UPDATE_FAILED": 0,
        "CHECKS_FAILED": 0,
        "CHECKS_TIMEOUT": 0,
        "CONFLICT_WITH_BASE_BRANCH": 0,
        "CONFLICT_WITH_PULL_AHEAD": 0,
        "DRAFT_PULL_REQUEST_CHANGED": 0,
        "INCOMPATIBILITY_WITH_BRANCH_PROTECTIONS": 0,
        "MERGE_QUEUE_RESET": 0,
        "PR_AHEAD_DEQUEUED": 0,
        "PR_AHEAD_FAILED_TO_MERGE": 0,
        "PR_CHECKS_STOPPED_BECAUSE_MERGE_QUEUE_PAUSE": 0,
        "PR_DEQUEUED": 0,
        "PR_FROZEN_NO_CASCADING": 0,
        "PR_QUEUED_TWICE": 0,
        "PR_UNEXPECTEDLY_FAILED_TO_MERGE": 0,
        "PR_WITH_HIGHER_PRIORITY_QUEUED": 0,
        "PULL_REQUEST_UPDATED": 0,
        "QUEUE_RULE_MISSING": 0,
        "SPECULATIVE_CHECK_NUMBER_REDUCED": 0,
        "SUCCESS": 0,
        "UNEXPECTED_QUEUE_CHANGE": 0,
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
