# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

import os
import re
from collections import namedtuple

import mock
import pytest

from datadog_checks.filebeat import FilebeatCheck

from .common import BAD_ENDPOINT, registry_file_path

mocked_file_stats = namedtuple("mocked_file_stats", ["st_size", "st_ino", "st_dev"])


# allows mocking `os.stat` only for certain paths; for all others it will call
# the actual function - needed as a number of test helpers do make calls to it
def mocked_os_stat(mocked_paths_and_stats):
    vanilla_os_stat = os.stat

    def internal_mock(path):
        if path in mocked_paths_and_stats:
            return mocked_paths_and_stats[path]
        return vanilla_os_stat(path)

    return mock.patch.object(os, "stat", side_effect=internal_mock)


def _build_instance(
    name, ignore_registry=None, stats_endpoint=None, only_metrics=None, timeout=None, normalize_metrics=None
):
    instance = {"registry_file_path": registry_file_path(name)}

    if ignore_registry is not None:
        instance["ignore_registry"] = ignore_registry

    if stats_endpoint is not None:
        instance["stats_endpoint"] = stats_endpoint

    if only_metrics is not None:
        instance["only_metrics"] = only_metrics

    if timeout is not None:
        instance["timeout"] = timeout

    if normalize_metrics is not None:
        instance["normalize_metrics"] = normalize_metrics

    return instance


def test_registry_happy_path(aggregator):
    config = _build_instance("happy_path")
    check = FilebeatCheck("filebeat", {}, [config])
    with mocked_os_stat(
        {
            "/test_dd_agent/var/log/nginx/access.log": mocked_file_stats(394154, 277025, 51713),
            "/test_dd_agent/var/log/syslog": mocked_file_stats(1024917, 152172, 51713),
        }
    ):
        check.check(config)

    aggregator.assert_metric(
        "filebeat.registry.unprocessed_bytes", value=2407, tags=["source:/test_dd_agent/var/log/nginx/access.log"]
    )
    aggregator.assert_metric(
        "filebeat.registry.unprocessed_bytes", value=0, tags=["source:/test_dd_agent/var/log/syslog"]
    )


# tests that we still support the format from filebeat < 5
def test_registry_happy_path_with_legacy_format(aggregator):
    config = _build_instance("happy_path_legacy_format")
    check = FilebeatCheck("filebeat", {}, [config])
    with mocked_os_stat(
        {
            "/test_dd_agent/var/log/nginx/access.log": mocked_file_stats(394154, 277025, 51713),
            "/test_dd_agent/var/log/syslog": mocked_file_stats(1024917, 152172, 51713),
        }
    ):
        check.check(config)

    aggregator.assert_metric(
        "filebeat.registry.unprocessed_bytes", value=2407, tags=["source:/test_dd_agent/var/log/nginx/access.log"]
    )
    aggregator.assert_metric(
        "filebeat.registry.unprocessed_bytes", value=0, tags=["source:/test_dd_agent/var/log/syslog"]
    )


def test_bad_config():
    check = FilebeatCheck("filebeat", {}, {})
    with pytest.raises(Exception) as excinfo:
        check.check({})
        assert "an absolute path to a filebeat registry path must be specified" in excinfo.value


def test_missing_registry_file(aggregator):
    config = _build_instance("i_dont_exist")
    check = FilebeatCheck("filebeat", {}, [config])
    # tests that it simply silently ignores it
    check.check(config)
    aggregator.assert_metric("filebeat.registry.unprocessed_bytes", count=0)


@pytest.mark.usefixtures('dd_environment')
def test_ignore_registry(aggregator, instance):
    instance['registry_file_path'] = "malformed_json"
    instance["ignore_registry"] = True
    check = FilebeatCheck("filebeat", {}, [instance])
    # test that it silently ignores the registry file
    # and does the http check
    check.check(instance)
    tags = ["stats_endpoint:{}".format(instance['stats_endpoint'])]
    aggregator.assert_service_check("filebeat.can_connect", status=FilebeatCheck.OK, tags=tags)


@pytest.mark.usefixtures('dd_environment')
def test_instance_tags(aggregator, instance):
    instance['registry_file_path'] = "happy_path"
    instance['tags'] = ["foo:bar"]
    check = FilebeatCheck("filebeat", {}, [instance])
    # test that it uses both the instance tags and the
    # `stats_endpoint` tag generated
    check.check(instance)
    tags = instance['tags'] + ["stats_endpoint:{}".format(instance['stats_endpoint'])]
    aggregator.assert_service_check("filebeat.can_connect", status=FilebeatCheck.OK, tags=tags)


def test_missing_source_file(aggregator):
    config = _build_instance("missing_source_file")
    check = FilebeatCheck("filebeat", {}, [config])
    check.check(config)
    aggregator.assert_metric("filebeat.registry.unprocessed_bytes", count=0)


def test_source_file_inode_has_changed(aggregator):
    config = _build_instance("single_source")
    check = FilebeatCheck("filebeat", {}, [config])
    with mocked_os_stat({"/test_dd_agent/var/log/syslog": mocked_file_stats(1024917, 152171, 51713)}):
        check.check(config)
    aggregator.assert_metric("filebeat.registry.unprocessed_bytes", count=0)


def test_source_file_device_has_changed(aggregator):
    config = _build_instance("single_source")
    check = FilebeatCheck("filebeat", {}, [config])
    with mocked_os_stat({"/test_dd_agent/var/log/syslog": mocked_file_stats(1024917, 152171, 51714)}):
        check.check(config)
    aggregator.assert_metric("filebeat.registry.unprocessed_bytes", count=0)


def generate_http_profiler_body(body_update):
    base_body = {
        "cmdline": [
            "/usr/share/filebeat/bin/filebeat",
            "-c",
            "/etc/filebeat/filebeat.yml",
            "-path.home",
            "/usr/share/filebeat",
            "-path.config",
            "/etc/filebeat",
            "-path.data",
            "/var/lib/filebeat",
            "-path.logs",
            "/var/log/filebeat",
            "-httpprof",
            ":2828",
        ],
        "filebeat.harvester.closed": 108,
        "filebeat.harvester.files.truncated": 0,
        "filebeat.harvester.open_files": 10,
        "filebeat.harvester.running": 10,
        "filebeat.harvester.skipped": 0,
        "filebeat.harvester.started": 118,
        "filebeat.prospector.log.files.renamed": 0,
        "filebeat.prospector.log.files.truncated": 104,
        "libbeat.config.module.running": 0,
        "libbeat.config.module.starts": 0,
        "libbeat.config.module.stops": 0,
        "libbeat.config.reloads": 0,
        "libbeat.es.call_count.PublishEvents": 0,
        "libbeat.es.publish.read_bytes": 0,
        "libbeat.es.publish.read_errors": 0,
        "libbeat.es.publish.write_bytes": 0,
        "libbeat.es.publish.write_errors": 0,
        "libbeat.es.published_and_acked_events": 0,
        "libbeat.es.published_but_not_acked_events": 0,
        "libbeat.kafka.call_count.PublishEvents": 0,
        "libbeat.kafka.published_and_acked_events": 0,
        "libbeat.kafka.published_but_not_acked_events": 0,
        "libbeat.logstash.call_count.PublishEvents": 8691,
        "libbeat.logstash.publish.read_bytes": 52146,
        "libbeat.logstash.publish.read_errors": 0,
        "libbeat.logstash.publish.write_bytes": 161035867,
        "libbeat.logstash.publish.write_errors": 0,
        "libbeat.logstash.published_and_acked_events": 1138928,
        "libbeat.logstash.published_but_not_acked_events": 0,
        "libbeat.outputs.messages_dropped": 0,
        "libbeat.publisher.messages_in_worker_queues": 0,
        "libbeat.publisher.published_events": 1138928,
        "libbeat.redis.publish.read_bytes": 0,
        "libbeat.redis.publish.read_errors": 0,
        "libbeat.redis.publish.write_bytes": 0,
        "libbeat.redis.publish.write_errors": 0,
        "memstats": {
            "Alloc": 6561080,
            "TotalAlloc": 24661290312,
            "Sys": 25938232,
            "Lookups": 35143,
            "Mallocs": 86545328,
            "Frees": 86527266,
            "HeapAlloc": 6561080,
            "HeapSys": 17006592,
            "HeapIdle": 7553024,
            "HeapInuse": 9453568,
            "HeapReleased": 0,
            "HeapObjects": 18062,
            "StackInuse": 819200,
            "StackSys": 819200,
            "MSpanInuse": 129920,
            "MSpanSys": 229376,
            "MCacheInuse": 2400,
            "MCacheSys": 16384,
            "BuckHashSys": 1556137,
            "GCSys": 2643968,
            "OtherSys": 3666575,
            "NextGC": 9491669,
            "LastGC": 1520619692758256437,
            "PauseTotalNs": 14387932504,
            "PauseNs": [354477, 126296, 93752, 303703, 156045, 6939651, 107696, 115597, 110226, 87639],
        },
        "publish.events": 1139450,
        "registrar.states.cleanup": 0,
        "registrar.states.current": 151,
        "registrar.states.update": 1139450,
        "registrar.writes": 8690,
    }

    if body_update:
        base_body.update(body_update)

    return base_body


def mock_request(body_update=None):
    return mock.patch(
        "requests.get",
        return_value=mock.MagicMock(status_code=200, json=lambda: generate_http_profiler_body(body_update)),
    )


def test_happy_path(aggregator):
    config = _build_instance("empty", stats_endpoint="http://localhost:9999")
    check = FilebeatCheck("filebeat", {}, [config])
    tags = ["stats_endpoint:http://localhost:9999"]

    # the first run shouldn't yield any increment metric, but it should
    # still report the gauge metrics
    with mock_request():
        check.check(config)

    aggregator.assert_metric("libbeat.logstash.published_and_acked_events", count=0)
    aggregator.assert_metric("filebeat.harvester.running", metric_type=aggregator.GAUGE, value=10, tags=tags)

    # now the second run should have all the increment metrics as well
    with mock_request({"libbeat.logstash.published_and_acked_events": 1138956, "filebeat.harvester.running": 9}):
        check.check(config)

    aggregator.assert_metric(
        "libbeat.logstash.published_and_acked_events", metric_type=aggregator.COUNTER, value=28, tags=tags
    )
    aggregator.assert_metric(
        "libbeat.kafka.published_and_acked_events", metric_type=aggregator.COUNTER, value=0, tags=tags
    )
    aggregator.assert_metric("filebeat.harvester.running", metric_type=aggregator.GAUGE, value=9, tags=tags)


def test_happy_path_with_an_only_metrics_list(aggregator):
    config = _build_instance(
        "empty", stats_endpoint="http://localhost:9999", only_metrics=[r"^libbeat.kafka", r"truncated$"]
    )
    check = FilebeatCheck("filebeat", {}, [config])
    tags = ["stats_endpoint:http://localhost:9999"]

    with mock_request():
        check.check(config)

    with mock_request(
        {"libbeat.logstash.published_and_acked_events": 1138956, "libbeat.kafka.published_and_acked_events": 12}
    ):
        check.check(config)

    # these metrics shouldn't have been reported, because they don't match
    # any regex in the "only_metrics" list
    aggregator.assert_metric("libbeat.logstash.published_and_acked_events", count=0)
    aggregator.assert_metric("filebeat.harvester.running", count=0)

    # but these 4 should have
    aggregator.assert_metric(
        "libbeat.kafka.published_and_acked_events", metric_type=aggregator.COUNTER, value=12, tags=tags
    )
    aggregator.assert_metric(
        "libbeat.kafka.published_but_not_acked_events", metric_type=aggregator.COUNTER, value=0, tags=tags
    )
    aggregator.assert_metric(
        "libbeat.kafka.call_count.PublishEvents", metric_type=aggregator.COUNTER, value=0, tags=tags
    )
    aggregator.assert_metric("filebeat.harvester.files.truncated", metric_type=aggregator.COUNTER, value=0, tags=tags)


def test_with_an_invalid_regex_in_the_only_metrics_list():
    config = _build_instance("empty", stats_endpoint="http://localhost:9999", only_metrics=["invalid regex ["])
    check = FilebeatCheck("filebeat", {}, [config])

    expected_message = (
        'Invalid only_metric regex for filebeat: "invalid regex [", ' "error: unexpected end of regular expression"
    )

    with pytest.raises(Exception) as excinfo:
        check.check(config)
        assert expected_message in excinfo.value


def test_regexes_only_get_compiled_and_run_once():
    regex = r"^libbeat.kafka"
    config = _build_instance("empty", stats_endpoint="http://localhost:9999", only_metrics=[regex])
    check = FilebeatCheck("filebeat", {}, [config])

    with mock_request():
        # the 1st run should compile regexes & run regexes
        with mock.patch.object(re, "compile") as re_compile:
            with mock.patch.object(re, "search") as re_search:
                check.check(config)

                re_compile.assert_called_once_with(regex)
                # once per metric name
                assert re_search.call_count == 50

    with mock_request(
        {"libbeat.logstash.published_and_acked_events": 1138956, "libbeat.kafka.published_and_acked_events": 12}
    ):
        with mock.patch.object(re, "compile") as re_compile:
            with mock.patch.object(re, "search") as re_search:
                check.check(config)

                # no further regex compiling nor searching should have happened
                assert re_compile.call_count == 0
                assert re_search.call_count == 0


def test_when_filebeat_restarts(aggregator):
    config = _build_instance("empty", stats_endpoint="http://localhost:9999")
    check = FilebeatCheck("filebeat", {}, [config])

    with mock_request():
        check.check(config)

    with mock_request(
        {"libbeat.logstash.published_and_acked_events": 0, "libbeat.kafka.published_and_acked_events": 12}
    ):
        check.check(config)

    # none of these metrics should have been reported, because of the restart
    aggregator.assert_metric("libbeat.logstash.published_and_acked_events", count=0)
    aggregator.assert_metric("libbeat.kafka.published_and_acked_events", count=0)

    # at the next run though, we should get normal increment from in between
    # the 2nd & 3rd runs
    with mock_request(
        {"libbeat.logstash.published_and_acked_events": 28, "libbeat.kafka.published_and_acked_events": 23}
    ):
        check.check(config)

    aggregator.assert_metric("libbeat.logstash.published_and_acked_events", metric_type=aggregator.COUNTER, value=28)
    aggregator.assert_metric("libbeat.kafka.published_and_acked_events", metric_type=aggregator.COUNTER, value=11)


def test_when_the_http_call_times_out(aggregator):
    config = _build_instance("empty", stats_endpoint="http://localhost:9999")
    check = FilebeatCheck("filebeat", {}, [config])

    request_failure = mock.Mock()
    request_failure.raise_for_status.side_effect = Exception("Error")
    with mock.patch("requests.get", return_value=request_failure):
        check.check(config)

    aggregator.assert_metric("filebeat.harvester.running", count=0)


def test_when_the_http_connection_is_refused(aggregator):
    config = _build_instance("empty", stats_endpoint="http://0.28.28.0:9999")
    check = FilebeatCheck("filebeat", {}, [config])
    check.check(config)
    aggregator.assert_metric("filebeat.harvester.running", count=0)


def test_with_two_different_instances(aggregator):
    config = _build_instance("empty", stats_endpoint="http://localhost:9999")
    check = FilebeatCheck("filebeat", {}, [config])
    tags = ["stats_endpoint:http://localhost:9999"]

    with mock_request():
        check.check(config)

    with mock_request({"libbeat.logstash.published_and_acked_events": 1138956, "filebeat.harvester.running": 9}):
        check.check(config)

    # metrics for the first instance
    aggregator.assert_metric(
        "libbeat.logstash.published_and_acked_events", metric_type=aggregator.COUNTER, value=28, tags=tags
    )
    aggregator.assert_metric(
        "libbeat.kafka.published_and_acked_events", metric_type=aggregator.COUNTER, value=0, tags=tags
    )
    aggregator.assert_metric("filebeat.harvester.running", metric_type=aggregator.GAUGE, value=9, tags=tags)

    config = _build_instance("empty", stats_endpoint="http://localhost:19999", only_metrics=[r"events$"])

    # and for the second
    tags = ["stats_endpoint:http://localhost:19999"]
    with mock_request():
        check.check(config)
    with mock_request({"libbeat.logstash.published_and_acked_events": 1238956, "filebeat.harvester.running": 29}):
        check.check(config)
    aggregator.assert_metric(
        "libbeat.logstash.published_and_acked_events", metric_type=aggregator.COUNTER, value=100028, tags=tags
    )
    aggregator.assert_metric(
        "libbeat.kafka.published_and_acked_events", metric_type=aggregator.COUNTER, value=0, tags=tags
    )
    aggregator.assert_metric("filebeat.harvester.running", count=0, tags=tags)


def _assert_config_raises(profiler_config, expected_substring):
    bad_config = _build_instance(profiler_config)
    check = FilebeatCheck("filebeat", {}, [bad_config])
    with pytest.raises(Exception) as excinfo:
        check.check(bad_config)
        assert expected_substring in excinfo.value


def test_http_profiler_not_a_dict():
    _assert_config_raises(["port", 82], "must be a dict")


def test_port_absent():
    _assert_config_raises({}, "must be an integer")


def test_port_not_an_int():
    _assert_config_raises({"port": "foo"}, "must be an integer")


def test_only_metrics_not_a_list():
    _assert_config_raises({"port": 82, "only_metrics": r"truncated$"}, "must be a list of regexes")


def test_timeout_not_a_number():
    _assert_config_raises({"port": 82, "timeout": "0.02"}, "must be a positive number")


def test_negative_timeout():
    _assert_config_raises({"port": 82, "timeout": 0}, "must be a positive number")
    _assert_config_raises({"port": 82, "timeout": -0.5}, "must be a positive number")


@pytest.mark.parametrize(
    'init_config, instance, expected_timeout',
    [
        pytest.param({}, _build_instance("empty", stats_endpoint="http://localhost:9999", timeout=8), (8.0, 8.0)),
        pytest.param({'timeout': 8}, _build_instance("empty", stats_endpoint="http://localhost:9999"), (8.0, 8.0)),
        pytest.param({}, _build_instance("empty", stats_endpoint="http://localhost:9999"), (2.0, 2.0)),
    ],
)
def test_default_timeout(init_config, instance, expected_timeout):
    check = FilebeatCheck("filebeat", init_config, [instance])
    assert check.http.options['timeout'] == expected_timeout


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_check(aggregator, instance):
    check = FilebeatCheck("filebeat", {}, [instance])
    check.check(instance)
    check.check(instance)
    tags = ["stats_endpoint:{}".format(instance['stats_endpoint'])]
    aggregator.assert_metric("filebeat.harvester.running", metric_type=aggregator.GAUGE, count=2, tags=tags)
    aggregator.assert_metric("libbeat.config.module.starts", metric_type=aggregator.COUNTER, count=1, tags=tags)
    aggregator.assert_service_check("filebeat.can_connect", status=FilebeatCheck.OK, tags=tags)


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_check_fail(aggregator, instance):
    instance['stats_endpoint'] = BAD_ENDPOINT
    check = FilebeatCheck("filebeat", {}, [instance])
    check.check(instance)
    aggregator.assert_service_check("filebeat.can_connect", status=FilebeatCheck.CRITICAL, tags=[])
    assert len(aggregator._metrics) == 0


def test_normalize_metrics(aggregator):
    config = _build_instance("empty", stats_endpoint="http://localhost:9999", normalize_metrics=True)
    check = FilebeatCheck("filebeat", {}, [config])
    tags = ["stats_endpoint:http://localhost:9999"]

    with mock_request():
        check.check(config)

    aggregator.assert_metric("filebeat.harvester.running", metric_type=aggregator.GAUGE, tags=tags)

    with mock_request(
        {"filebeat.libbeat.logstash.published_and_acked_events": 1138956, "filebeat.harvester.running": 9}
    ):
        check.check(config)

    aggregator.assert_metric(
        "filebeat.libbeat.logstash.published_and_acked_events", metric_type=aggregator.COUNTER, tags=tags
    )
    aggregator.assert_metric(
        "filebeat.libbeat.kafka.published_and_acked_events", metric_type=aggregator.COUNTER, tags=tags
    )
    aggregator.assert_metric("filebeat.harvester.running", metric_type=aggregator.GAUGE, tags=tags)


def test_normalize_metrics_with_an_only_metrics_list(aggregator):
    config = _build_instance(
        "empty",
        stats_endpoint="http://localhost:9999",
        only_metrics=[r"^libbeat.kafka", r"truncated$"],
        normalize_metrics=True,
    )
    check = FilebeatCheck("filebeat", {}, [config])
    tags = ["stats_endpoint:http://localhost:9999"]

    with mock_request():
        check.check(config)

    with mock_request(
        {
            "filebeat.libbeat.logstash.published_and_acked_events": 1138956,
            "libbeat.kafka.published_and_acked_events": 12,
        }
    ):
        check.check(config)

    aggregator.assert_metric(
        "filebeat.libbeat.kafka.published_and_acked_events", metric_type=aggregator.COUNTER, value=12, tags=tags
    )
    aggregator.assert_metric(
        "filebeat.libbeat.kafka.published_but_not_acked_events", metric_type=aggregator.COUNTER, value=0, tags=tags
    )
    aggregator.assert_metric(
        "filebeat.libbeat.kafka.call_count.PublishEvents", metric_type=aggregator.COUNTER, value=0, tags=tags
    )
    aggregator.assert_metric("filebeat.harvester.files.truncated", metric_type=aggregator.COUNTER, value=0, tags=tags)
