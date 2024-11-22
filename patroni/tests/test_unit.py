# from typing import Any, Callable, Dict  # noqa: F401
#
# from datadog_checks.base import AgentCheck  # noqa: F401
# from datadog_checks.base.stubs.aggregator import AggregatorStub  # noqa: F401
# from datadog_checks.dev.utils import get_metadata_metrics
# from datadog_checks.patroni import PatroniCheck
#
#
# def test_check(dd_run_check, aggregator, instance):
#    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
#    check = PatroniCheck('patroni', {}, [instance])
#    dd_run_check(check)
#
#    aggregator.assert_all_metrics_covered()
#    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
#
#
# def test_emits_critical_service_check_when_service_is_down(dd_run_check, aggregator, instance):
#    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
#    check = PatroniCheck('patroni', {}, [instance])
#    dd_run_check(check)
#    aggregator.assert_service_check('patroni.can_connect', PatroniCheck.CRITICAL)

import json
import os
import pytest
from unittest.mock import patch, mock_open, MagicMock
from datadog_checks.patroni import PatroniCheck
from datadog_checks.patroni.metrics import METRIC_MAP, construct_metrics_config


@pytest.fixture
def check_instance():
    """Fixture to create a PatroniCheck instance."""
    return PatroniCheck(
        "patroni", {}, [{"openmetrics_endpoint": "http://127.0.0.1:8008/metrics"}]
    )


def test_load_state_file_exists(check_instance):
    """Test that state is loaded correctly when the state file exists."""
    state_data = {"previous_leader": "leader1"}
    with patch("os.path.exists", return_value=True), patch(
        "builtins.open", mock_open(read_data=json.dumps(state_data))
    ):
        check_instance.load_state()
        assert check_instance.previous_leader == "leader1"


def test_load_state_file_not_exists(check_instance):
    """Test that previous_leader is None when the state file does not exist."""
    with patch("os.path.exists", return_value=False):
        check_instance.load_state()
        assert check_instance.previous_leader is None


def test_load_state_invalid_file(check_instance):
    """Test that previous_leader is set to None when the state file is invalid."""
    with patch("os.path.exists", return_value=True), patch(
        "builtins.open", mock_open(read_data="invalid-json")
    ):
        with patch.object(check_instance.log, "error") as mock_log_error:
            check_instance.load_state()
            assert check_instance.previous_leader is None
            mock_log_error.assert_called_once()


def test_save_state_success(check_instance):
    """Test that state is saved correctly to the state file."""
    with patch("builtins.open", mock_open()) as mock_file, patch(
        "json.dump"
    ) as mock_json_dump:
        check_instance.previous_leader = "leader1"
        check_instance.save_state()

        # Check that the file was opened in write mode
        mock_file.assert_called_once_with(check_instance.STATE_FILE, "w")

        # Check that json.dump was called with the correct data
        mock_json_dump.assert_called_once_with(
            {"previous_leader": "leader1"}, mock_file()
        )


def test_save_state_failure(check_instance):
    """Test that an error is logged when saving the state fails."""
    with patch("builtins.open", side_effect=IOError), patch.object(
        check_instance.log, "error"
    ) as mock_log_error:
        check_instance.save_state()
        mock_log_error.assert_called_once()


def test_handle_failover_event_same_leader(check_instance):
    """Test that no event is submitted if the leader hasn't changed."""
    check_instance.previous_leader = "leader1"
    with patch.object(check_instance, "event") as mock_event:
        check_instance.handle_failover_event("leader1")
        mock_event.assert_not_called()


def test_handle_failover_event_new_leader(check_instance):
    """Test that an event is submitted when the leader changes."""
    check_instance.previous_leader = "leader1"
    with patch.object(check_instance, "event") as mock_event, patch.object(
        check_instance, "save_state"
    ) as mock_save_state:
        check_instance.handle_failover_event("leader2")
        mock_event.assert_called_once_with(
            {
                "msg_title": "Patroni Failover Detected",
                "msg_text": "Failover occurred: Leader changed from leader1 to leader2",
                "alert_type": "info",
                "source_type_name": "patroni",
                "tags": ["previous_leader:leader1", "new_leader:leader2"],
            }
        )
        mock_save_state.assert_called_once()


def test_process_custom_metrics(check_instance):
    """Test the processing of custom metrics."""
    metric = MagicMock()
    metric.name = "patroni_dcs_last_seen"
    metric.samples = [MagicMock(value=1234567890, labels={"key": "value"})]
    mock_scraper = MagicMock()
    mock_scraper.consume_metrics.return_value = [metric]
    check_instance.scrapers = {"http://127.0.0.1:8008/metrics": mock_scraper}

    with patch("time.time", return_value=1234567900), patch.object(
        check_instance, "gauge"
    ) as mock_gauge:
        check_instance.process_custom_metrics(instance={})
        mock_gauge.assert_called_once_with(
            "patroni.dcs_last_seen_diff", 10, tags=["key:value"]
        )


def test_generate_config(check_instance):
    """Test that configuration is generated correctly."""
    # Input for the test
    input_metrics = {"metric1": "mapped_metric_name"}

    # Call _generate_config
    config = check_instance._generate_config(
        "http://127.0.0.1:8008/metrics", input_metrics, "patroni"
    )

    # Assertions
    assert config["openmetrics_endpoint"] == "http://127.0.0.1:8008/metrics"
    assert config["namespace"] == "patroni"
    assert {"metric1": {"name": "mapped_metric_name"}} in config["metrics"]


def test_parse_config(check_instance):
    """Test that _parse_config generates the correct scraper configurations."""
    with patch.object(check_instance, "_generate_config", return_value="mock_config"):
        check_instance._parse_config()
        assert check_instance.scraper_configs == ["mock_config"]
