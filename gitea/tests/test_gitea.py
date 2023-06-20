import pytest

from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.gitea import GiteaCheck


@pytest.mark.unit
def test_mock_assert_metrics_using_metadata(dd_run_check, aggregator, check, mock_metrics):
    dd_run_check(check)
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


@pytest.mark.unit
def test_mock_assert_service_check(dd_run_check, aggregator, check, mock_metrics):
    dd_run_check(check)
    aggregator.assert_service_check("gitea.openmetrics.health", status=GiteaCheck.OK)


@pytest.mark.unit
def test_mock_assert_metrics(dd_run_check, aggregator, check, mock_metrics):
    dd_run_check(check)

    expected_metrics = [
        {"name": "gitea.accesses", "value": 1},
        {"name": "gitea.actions", "value": 2},
        {"name": "gitea.attachments", "value": 3},
        {"name": "gitea.comments", "value": 4},
        {"name": "gitea.follows", "value": 5},
        {"name": "gitea.hooktasks", "value": 6},
        {"name": "gitea.issues", "value": 7},
        {"name": "gitea.issues.closed", "value": 8},
        {"name": "gitea.issues.open", "value": 9},
        {"name": "gitea.labels", "value": 10},
        {"name": "gitea.loginsources", "value": 11},
        {"name": "gitea.milestones", "value": 12},
        {"name": "gitea.mirrors", "value": 13},
        {"name": "gitea.oauths", "value": 14},
        {"name": "gitea.organizations", "value": 15},
        {"name": "gitea.projects", "value": 16},
        {"name": "gitea.projects_boards", "value": 17},
        {"name": "gitea.publickeys", "value": 18},
        {"name": "gitea.releases", "value": 19},
        {"name": "gitea.repositories", "value": 20},
        {"name": "gitea.stars", "value": 21},
        {"name": "gitea.teams", "value": 22},
        {"name": "gitea.updatetasks", "value": 23},
        {"name": "gitea.users", "value": 24},
        {"name": "gitea.watches", "value": 25},
        {"name": "gitea.webhooks", "value": 26},
        {"name": "gitea.metric_handler.requests_in_flight", "value": 1},
        {
            "name": "gitea.metric_handler.requests.count",
            "value": 3,
            "type": aggregator.MONOTONIC_COUNT,
            "tags": ["endpoint:http://localhost:3000/metrics", "code:200"],
        },
        {
            "name": "gitea.metric_handler.requests.count",
            "value": 4,
            "type": aggregator.MONOTONIC_COUNT,
            "tags": ["endpoint:http://localhost:3000/metrics", "code:500"],
        },
        {
            "name": "gitea.metric_handler.requests.count",
            "value": 5,
            "type": aggregator.MONOTONIC_COUNT,
            "tags": ["endpoint:http://localhost:3000/metrics", "code:503"],
        },
        {"name": "gitea.go.goroutines", "value": 32},
        {"name": "gitea.go.threads", "value": 18},
        {
            "name": "gitea.go.info",
            "value": 1,
            "tags": ["go-version:go1.18.2", "endpoint:http://localhost:3000/metrics"],
        },
        {
            "name": "gitea.process.cpu_seconds.count",
            "value": 2.44,
            "type": aggregator.MONOTONIC_COUNT,
        },
        {"name": "gitea.process.max_fds", "value": 100},
        {"name": "gitea.process.open_fds", "value": 10},
        {"name": "gitea.process.resident_memory.bytes", "value": 1000},
        {"name": "gitea.process.start_time", "value": 1001},
        {"name": "gitea.process.virtual_memory.bytes", "value": 1002},
        {"name": "gitea.process.virtual_memory.max_bytes", "value": 1003},
    ]

    for expected_metric in expected_metrics:
        aggregator.assert_metric(
            name=expected_metric["name"],
            value=expected_metric["value"],
            metric_type=expected_metric.get("type", aggregator.GAUGE),
            tags=expected_metric.get("tags", ["endpoint:http://localhost:3000/metrics"]),
        )

    aggregator.assert_all_metrics_covered()
    aggregator.assert_no_duplicate_all()


@pytest.mark.integration
@pytest.mark.usefixtures("dd_environment")
def test_check_integration_assert_metrics(dd_run_check, aggregator, check):
    dd_run_check(check)

    metrics = [
        "gitea.accesses",
        "gitea.actions",
        "gitea.attachments",
        "gitea.comments",
        "gitea.follows",
        "gitea.hooktasks",
        "gitea.issues",
        "gitea.issues.closed",
        "gitea.issues.open",
        "gitea.labels",
        "gitea.loginsources",
        "gitea.milestones",
        "gitea.mirrors",
        "gitea.oauths",
        "gitea.organizations",
        "gitea.projects",
        "gitea.projects_boards",
        "gitea.publickeys",
        "gitea.releases",
        "gitea.repositories",
        "gitea.stars",
        "gitea.teams",
        "gitea.updatetasks",
        "gitea.users",
        "gitea.watches",
        "gitea.webhooks",
        "gitea.go.goroutines",
        "gitea.go.info",
        "gitea.go.threads",
        "gitea.metric_handler.requests_in_flight",
        "gitea.metric_handler.requests.count",
        "gitea.process.cpu_seconds.count",
        "gitea.process.max_fds",
        "gitea.process.open_fds",
        "gitea.process.resident_memory.bytes",
        "gitea.process.start_time",
        "gitea.process.virtual_memory.bytes",
        "gitea.process.virtual_memory.max_bytes",
    ]

    for metric in metrics:
        aggregator.assert_metric(metric)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_no_duplicate_all()


@pytest.mark.integration
@pytest.mark.usefixtures("dd_environment")
def test_check_integration_assert_service_check(dd_run_check, aggregator, check):
    dd_run_check(check)
    aggregator.assert_service_check("gitea.openmetrics.health", status=GiteaCheck.OK)


@pytest.mark.integration
@pytest.mark.usefixtures("dd_environment")
def test_check_integration_assert_metrics_using_metadata(dd_run_check, aggregator, check):
    dd_run_check(check)
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
