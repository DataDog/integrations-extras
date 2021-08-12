from distutils.version import LooseVersion

import pytest
import requests

from datadog_checks.logstash import LogstashCheck

from .common import BAD_INSTANCE, BAD_PORT, GOOD_INSTANCE, HOST, PORT, TAGS, URL

STATS_METRICS = {
    "logstash.process.open_file_descriptors": ("gauge", "process.open_file_descriptors"),
    "logstash.process.peak_open_file_descriptors": ("gauge", "process.peak_open_file_descriptors"),
    "logstash.process.max_file_descriptors": ("gauge", "process.max_file_descriptors"),
    "logstash.process.mem.total_virtual_in_bytes": ("gauge", "process.mem.total_virtual_in_bytes"),
    "logstash.process.cpu.total_in_millis": ("gauge", "process.cpu.total_in_millis"),
    "logstash.process.cpu.percent": ("gauge", "process.cpu.percent"),
    "logstash.process.cpu.load_average.1m": ("gauge", "process.cpu.load_average.1m"),
    "logstash.process.cpu.load_average.5m": ("gauge", "process.cpu.load_average.5m"),
    "logstash.process.cpu.load_average.15m": ("gauge", "process.cpu.load_average.15m"),
    "logstash.jvm.threads.count": ("gauge", "jvm.threads.count"),
    "logstash.jvm.threads.peak_count": ("gauge", "jvm.threads.peak_count"),
    "logstash.jvm.mem.heap_used_percent": ("gauge", "jvm.mem.heap_used_percent"),
    "logstash.jvm.mem.heap_committed_in_bytes": ("gauge", "jvm.mem.heap_committed_in_bytes"),
    "logstash.jvm.mem.heap_max_in_bytes": ("gauge", "jvm.mem.heap_max_in_bytes"),
    "logstash.jvm.mem.heap_used_in_bytes": ("gauge", "jvm.mem.heap_used_in_bytes"),
    "logstash.jvm.mem.non_heap_used_in_bytes": ("gauge", "jvm.mem.non_heap_used_in_bytes"),
    "logstash.jvm.mem.non_heap_committed_in_bytes": ("gauge", "jvm.mem.non_heap_committed_in_bytes"),
    "logstash.jvm.mem.pools.survivor.peak_used_in_bytes": ("gauge", "jvm.mem.pools.survivor.peak_used_in_bytes"),
    "logstash.jvm.mem.pools.survivor.used_in_bytes": ("gauge", "jvm.mem.pools.survivor.used_in_bytes"),
    "logstash.jvm.mem.pools.survivor.peak_max_in_bytes": ("gauge", "jvm.mem.pools.survivor.peak_max_in_bytes"),
    "logstash.jvm.mem.pools.survivor.max_in_bytes": ("gauge", "jvm.mem.pools.survivor.max_in_bytes"),
    "logstash.jvm.mem.pools.survivor.committed_in_bytes": ("gauge", "jvm.mem.pools.survivor.committed_in_bytes"),
    "logstash.jvm.mem.pools.old.peak_used_in_bytes": ("gauge", "jvm.mem.pools.old.peak_used_in_bytes"),
    "logstash.jvm.mem.pools.old.used_in_bytes": ("gauge", "jvm.mem.pools.old.used_in_bytes"),
    "logstash.jvm.mem.pools.old.peak_max_in_bytes": ("gauge", "jvm.mem.pools.old.peak_max_in_bytes"),
    "logstash.jvm.mem.pools.old.max_in_bytes": ("gauge", "jvm.mem.pools.old.max_in_bytes"),
    "logstash.jvm.mem.pools.old.committed_in_bytes": ("gauge", "jvm.mem.pools.old.committed_in_bytes"),
    "logstash.jvm.mem.pools.young.peak_used_in_bytes": ("gauge", "jvm.mem.pools.young.peak_used_in_bytes"),
    "logstash.jvm.mem.pools.young.used_in_bytes": ("gauge", "jvm.mem.pools.young.used_in_bytes"),
    "logstash.jvm.mem.pools.young.peak_max_in_bytes": ("gauge", "jvm.mem.pools.young.peak_max_in_bytes"),
    "logstash.jvm.mem.pools.young.max_in_bytes": ("gauge", "jvm.mem.pools.young.max_in_bytes"),
    "logstash.jvm.mem.pools.young.committed_in_bytes": ("gauge", "jvm.mem.pools.young.committed_in_bytes"),
    "logstash.jvm.gc.collectors.old.collection_time_in_millis": (
        "gauge",
        "jvm.gc.collectors.old.collection_time_in_millis",
    ),
    "logstash.jvm.gc.collectors.old.collection_count": ("gauge", "jvm.gc.collectors.old.collection_count"),
    "logstash.jvm.gc.collectors.young.collection_time_in_millis": (
        "gauge",
        "jvm.gc.collectors.young.collection_time_in_millis",
    ),
    "logstash.jvm.gc.collectors.young.collection_count": ("gauge", "jvm.gc.collectors.young.collection_count"),
    "logstash.reloads.successes": ("gauge", "reloads.successes"),
    "logstash.reloads.failures": ("gauge", "reloads.failures"),
}

PIPELINE_METRICS = {
    "logstash.pipeline.dead_letter_queue.queue_size_in_bytes": ("gauge", "dead_letter_queue.queue_size_in_bytes"),
    "logstash.pipeline.events.duration_in_millis": ("gauge", "pipeline.events.duration_in_millis"),
    "logstash.pipeline.events.in": ("gauge", "pipeline.events.in"),
    "logstash.pipeline.events.out": ("gauge", "pipeline.events.out"),
    "logstash.pipeline.events.filtered": ("gauge", "pipeline.events.filtered"),
    "logstash.pipeline.reloads.successes": ("gauge", "pipeline.reloads.successes"),
    "logstash.pipeline.reloads.failures": ("gauge", "pipeline.reloads.failures"),
}

PIPELINE_QUEUE_METRICS = {
    "logstash.pipeline.queue.events": ("gauge", "queue.events"),
    "logstash.pipeline.queue.capacity.max_queue_size_in_bytes": ("gauge", "queue.capacity.max_queue_size_in_bytes"),
    "logstash.pipeline.queue.capacity.queue_size_in_bytes": ("gauge", "queue.capacity.queue_size_in_bytes"),
    "logstash.pipeline.queue.capacity.max_unread_events": ("gauge", "queue.capacity.max_unread_events"),
    "logstash.pipeline.queue.capacity.page_capacity_in_bytes": ("gauge", "queue.capacity.page_capacity_in_bytes"),
}

PIPELINE_INPUTS_METRICS = {
    "logstash.pipeline.plugins.inputs.events.out": ("gauge", "events.out"),
    "logstash.pipeline.plugins.inputs.events.queue_push_duration_in_millis": (
        "gauge",
        "events.queue_push_duration_in_millis",
    ),
}

PIPELINE_OUTPUTS_METRICS = {
    "logstash.pipeline.plugins.outputs.events.in": ("gauge", "events.in"),
    "logstash.pipeline.plugins.outputs.events.out": ("gauge", "events.out"),
    "logstash.pipeline.plugins.outputs.events.duration_in_millis": ("gauge", "events.duration_in_millis"),
}

PIPELINE_FILTERS_METRICS = {
    "logstash.pipeline.plugins.filters.events.in": ("gauge", "events.in"),
    "logstash.pipeline.plugins.filters.events.out": ("gauge", "events.out"),
    "logstash.pipeline.plugins.filters.events.duration_in_millis": ("gauge", "events.duration_in_millis"),
}

CHECK_NAME = 'logstash'


@pytest.mark.usefixtures('dd_environment')
def test_failed_connection(aggregator):
    bad_sc_tags = ['host:{}'.format(HOST), 'port:{}'.format(BAD_PORT)]

    check = LogstashCheck(CHECK_NAME, {}, [BAD_INSTANCE])
    with pytest.raises(requests.exceptions.ConnectionError):
        check.check(BAD_INSTANCE)

    aggregator.assert_service_check('logstash.can_connect', tags=bad_sc_tags, status=LogstashCheck.CRITICAL)


@pytest.mark.usefixtures('dd_environment')
def test_check(aggregator):

    check = LogstashCheck(CHECK_NAME, {}, [GOOD_INSTANCE])

    check.check(GOOD_INSTANCE)
    default_tags = ["url:{}".format(URL)]

    instance_config = check.get_instance_config(GOOD_INSTANCE)

    logstash_version = check._get_logstash_version(instance_config)
    is_multi_pipeline = logstash_version and LooseVersion("6.0.0") <= LooseVersion(logstash_version)

    input_tag = [u"plugin_conf_id:dummy_input"]
    output_tag = [u"plugin_conf_id:dummy_output", u"output_name:stdout"]
    filter_tag = [u"plugin_conf_id:dummy_filter", u"filter_name:json"]
    if is_multi_pipeline:
        input_tag.append(u"input_name:beats")
    else:
        input_tag.append(u"input_name:stdin")

    expected_metrics = dict(STATS_METRICS)
    expected_metrics.update(PIPELINE_METRICS)
    expected_metrics.update(PIPELINE_INPUTS_METRICS)
    expected_metrics.update(PIPELINE_OUTPUTS_METRICS)
    expected_metrics.update(PIPELINE_FILTERS_METRICS)
    if is_multi_pipeline:
        expected_metrics.update(PIPELINE_QUEUE_METRICS)

    good_sc_tags = ['host:{}'.format(HOST), 'port:{}'.format(PORT)]

    pipeline_metrics = dict(PIPELINE_METRICS, **PIPELINE_INPUTS_METRICS)
    pipeline_metrics.update(PIPELINE_FILTERS_METRICS)
    pipeline_metrics.update(PIPELINE_OUTPUTS_METRICS)

    for metric_name, desc in expected_metrics.items():
        metric_tags = TAGS + default_tags
        if metric_name in PIPELINE_INPUTS_METRICS:
            metric_tags = metric_tags + input_tag
        if metric_name in PIPELINE_OUTPUTS_METRICS:
            metric_tags = metric_tags + output_tag
        if metric_name in PIPELINE_FILTERS_METRICS:
            metric_tags = metric_tags + filter_tag
        is_pipeline_queue_metric = metric_name in PIPELINE_QUEUE_METRICS

        is_pipeline_metric = metric_name in pipeline_metrics

        if desc[0] == "gauge":
            if is_multi_pipeline and is_pipeline_metric:
                aggregator.assert_metric(metric_name, count=1, tags=metric_tags + [u'pipeline_name:main'])
                aggregator.assert_metric(metric_name, count=1, tags=metric_tags + [u'pipeline_name:second_pipeline'])
            elif is_multi_pipeline and is_pipeline_queue_metric:
                aggregator.assert_metric(metric_name, count=0, tags=metric_tags + [u'pipeline_name:main'])
                aggregator.assert_metric(metric_name, count=1, tags=metric_tags + [u'pipeline_name:second_pipeline'])
            else:
                aggregator.assert_metric(metric_name, count=1, tags=metric_tags)

    aggregator.assert_service_check('logstash.can_connect', tags=good_sc_tags + TAGS, status=LogstashCheck.OK)
