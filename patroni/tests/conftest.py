import pytest
from unittest.mock import patch, MagicMock
from datadog_checks.patroni import PatroniCheck


#@pytest.fixture(scope="session")
#def dd_environment():
#    yield
#
#
#@pytest.fixture
#def instance():
#    return {}




@pytest.fixture
def instance():
    """Sample instance configuration."""
    return {
        "openmetrics_endpoint": "http://127.0.0.1:8008/metrics",
        "namespace": "patroni",
    }


@pytest.fixture
def init_config():
    """Sample init configuration."""
    return {}


@pytest.fixture
def check_instance(init_config, instance):
    """Create a configured instance of PatroniCheck."""
    return PatroniCheck("patroni", init_config, [instance])


def test_check_integration(mocker, check_instance, instance):
    """
    Integration test for the `check` method, ensuring all metrics and events are processed.
    """
    # Mock scraper and its consume_metrics method
    mock_scraper = MagicMock()
    mock_metric_primary = MagicMock()
    mock_metric_primary.name = "patroni_primary"
    mock_metric_primary.samples = [
        MagicMock(value=1.0, labels={"name": "leader"})
    ]
    mock_metric_dcs = MagicMock()
    mock_metric_dcs.name = "patroni_dcs_last_seen"
    mock_metric_dcs.samples = [
        MagicMock(value=int(time.time()) - 5, labels={"scope": "demo", "name": "patroni1"})
    ]

    mock_scraper.consume_metrics.return_value = [mock_metric_primary, mock_metric_dcs]
    check_instance.scrapers = {"http://127.0.0.1:8008/metrics": mock_scraper}

    # Mock Datadog API calls
    mock_gauge = mocker.patch.object(check_instance, "gauge")
    mock_event = mocker.patch.object(check_instance, "event")

    # Call the `check` method
    check_instance.check(instance)

    # Assert `gauge` called for dcs.last_seen_diff
    mock_gauge.assert_any_call(
        "patroni.dcs_last_seen_diff",
        5,
        tags=["scope:demo", "name:patroni1"],
    )

    # Assert `event` called for failover event
    mock_event.assert_called_once_with(
        {
            "msg_title": "Patroni Failover Detected",
            "msg_text": "Failover occurred: Leader changed from None to leader",
            "alert_type": "info",
            "source_type_name": "patroni",
            "tags": ["previous_leader:None", "new_leader:leader"],
        }
    )


def test_process_custom_metrics(mocker, check_instance):
    """
    Integration test for `process_custom_metrics`.
    """
    # Mock scraper and its consume_metrics method
    mock_scraper = MagicMock()
    mock_metric = MagicMock()
    mock_metric.name = "patroni_dcs_last_seen"
    mock_metric.samples = [
        MagicMock(value=int(time.time()) - 10, labels={"scope": "test", "name": "test-node"})
    ]
    mock_scraper.consume_metrics.return_value = [mock_metric]
    check_instance.scrapers = {"http://127.0.0.1:8008/metrics": mock_scraper}

    # Mock Datadog API call
    mock_gauge = mocker.patch.object(check_instance, "gauge")

    # Call process_custom_metrics
    check_instance.process_custom_metrics(instance={})

    # Assert `gauge` was called
    mock_gauge.assert_called_once_with(
        "patroni.dcs_last_seen_diff",
        10,
        tags=["scope:test", "name:test-node"],
    )


def test_handle_failover_event(mocker, check_instance):
    """
    Integration test for `handle_failover_event`.
    """
    # Mock save_state to avoid file operations
    mock_save_state = mocker.patch.object(check_instance, "save_state")

    # Call `handle_failover_event` with a new leader
    check_instance.previous_leader = "leader1"
    check_instance.handle_failover_event("leader2")

    # Assert state is updated
    assert check_instance.previous_leader == "leader2"

    # Assert save_state is called
    mock_save_state.assert_called_once()

    # Mock Datadog event call
    mock_event = mocker.patch.object(check_instance, "event")

    # Call `handle_failover_event`
    check_instance.handle_failover_event("leader3")

    # Assert `event` was called
    mock_event.assert_called_once_with(
        {
            "msg_title": "Patroni Failover Detected",
            "msg_text": "Failover occurred: Leader changed from leader2 to leader3",
            "alert_type": "info",
            "source_type_name": "patroni",
            "tags": ["previous_leader:leader2", "new_leader:leader3"],
        }
    )

