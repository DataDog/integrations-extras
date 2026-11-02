import pytest


def metric_emitted_if_any_series_is_finite(aggregator, instance):
    # special case where same metric can be emitted and not based on value (dd filter NaN/+-inf vals).
    # for example:
    ## HELP ravendb_database_time_since_last_backup_seconds Last backup
    ## TYPE ravendb_database_time_since_last_backup_seconds gauge
    # ravendb_database_time_since_last_backup_seconds{database_name="DemoUser-a7908b7b-efc0-4f39-9e83-144d65b236b3"} 13
    # ravendb_database_time_since_last_backup_seconds{database_name="a"} NaN
    # ravendb_database_time_since_last_backup_seconds{database_name="DemoUser-6ec17361-4ca6-49bc-993b-1f28af504421"} NaN
    with pytest.raises(AssertionError):
        aggregator.assert_metric(
            "ravendb.database.time.since.last.backup.seconds",
            tags=[
                "database_name:a",
                f"endpoint:{instance['openmetrics_endpoint']}",
            ],
        )

    aggregator.assert_metric(
        "ravendb.database.time.since.last.backup.seconds",
        tags=[
            "database_name:DemoUser-a7908b7b-efc0-4f39-9e83-144d65b236b3",
            f"endpoint:{instance['openmetrics_endpoint']}",
        ],
    )


def metric_stubs(aggregator, metric_name):
    stubs = aggregator.metrics(metric_name)
    assert stubs, f"Expected metric '{metric_name}' to be emitted at least once"
    return stubs


def tags_contain_prefix(stubs, prefix):
    for stub in stubs:
        for tag in stub.tags or []:
            if isinstance(tag, str) and tag.startswith(prefix):
                return True
    return False


def has_tag_starting_with(stub, prefix):
    for t in stub.tags or []:
        if t.startswith(prefix):
            return True
    return False


def is_excluded_metric(metric_name, instance):
    excluded = []

    if not instance.get("enable_database_metrics", False):
        excluded.append("ravendb.database.")

    if not instance.get("enable_index_metrics", False):
        excluded.append("ravendb.index.")

    if not instance.get("enable_collection_metrics", False):
        excluded.append("ravendb.collection.")

    return metric_name.startswith(tuple(excluded))


def emitted_metric_names(aggregator):
    return sorted(aggregator._metrics.keys())


def assert_any_metric_with_prefix_emitted(aggregator, prefix):
    names = emitted_metric_names(aggregator)
    assert any(name.startswith(prefix) for name in names), (
        f"Expected at least one metric starting with '{prefix}', but none were emitted.\n"
        f"Emitted metrics (first 50): {names}"
    )
