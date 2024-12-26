import pytest
from datadog_checks.patroni import PatroniCheck


@pytest.mark.integration
@pytest.mark.usefixtures("dd_environment")
def test_check(dd_run_check, aggregator, instance):
    check = PatroniCheck("patroni", {}, [instance])

    dd_run_check(check)

    aggregator.assert_metric("patroni.cluster.unlocked", value=0)
    aggregator.assert_metric("patroni.dcs.last_seen")
    aggregator.assert_metric("patroni.dcs_last_seen_diff")
    aggregator.assert_metric("patroni.failsafe_mode.active", value=0)
    aggregator.assert_metric("patroni.is_paused", value=0)
    aggregator.assert_metric("patroni.pending_restart", value=0)
    aggregator.assert_metric("patroni.postgres.archive_recovery", value=0)
    aggregator.assert_metric("patroni.postgres.running", value=1)
    aggregator.assert_metric("patroni.postgres.server_version")
    aggregator.assert_metric("patroni.postgres.start_time")
    aggregator.assert_metric("patroni.postgres.streaming", value=1)
    aggregator.assert_metric("patroni.postgres.timeline.count")
    aggregator.assert_metric("patroni.primary", value=1)
    aggregator.assert_metric("patroni.quorum_standby", value=0)
    aggregator.assert_metric("patroni.replica", value=1)
    aggregator.assert_metric("patroni.standby_leader", value=0)
    aggregator.assert_metric("patroni.sync_standby", value=0)
    aggregator.assert_metric("patroni.version")
    aggregator.assert_metric("patroni.xlog.location.count")
    aggregator.assert_metric("patroni.xlog.paused", value=0)
    aggregator.assert_metric("patroni.xlog.received_location.count")
    aggregator.assert_metric("patroni.xlog.replayed_location.count")
    aggregator.assert_metric("patroni.xlog.replayed_timestamp")

    expected_metrics = [
        "patroni.cluster.unlocked",
        "patroni.dcs.last_seen",
        "patroni.dcs_last_seen_diff",
        "patroni.failsafe_mode.active",
        "patroni.is_paused",
        "patroni.pending_restart",
        "patroni.postgres.archive_recovery",
        "patroni.postgres.running",
        "patroni.postgres.server_version",
        "patroni.postgres.start_time",
        "patroni.postgres.streaming",
        "patroni.postgres.timeline.count",
        "patroni.primary",
        "patroni.quorum_standby",
        "patroni.replica",
        "patroni.standby_leader",
        "patroni.sync_standby",
        "patroni.version",
        "patroni.xlog.location.count",
        "patroni.xlog.paused",
        "patroni.xlog.received_location.count",
        "patroni.xlog.replayed_location.count",
        "patroni.xlog.replayed_timestamp",
    ]
    for metric in expected_metrics:
        aggregator.assert_metric(metric)

    aggregator.assert_all_metrics_covered()
