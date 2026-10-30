import os
from unittest import mock

import pytest

from datadog_checks.upbound_uxp import UpboundUxpCheck

FIXTURE = os.path.join(os.path.dirname(__file__), 'docker', 'fixtures', 'metrics')
INSTANCE_TAGS = ['team:platform', 'kube_cluster_name:test-cluster']


def _instance():
    return {
        'uxp_hosts': ['localhost'],
        'uxp_port': '8080',
        'uxp_url': '/metrics',
        'metrics_default': 'max',
        'tags': list(INSTANCE_TAGS),
    }


def _run(dd_run_check, payload, instance=None):
    check = UpboundUxpCheck('upbound_uxp', {}, [instance or _instance()])
    with mock.patch('datadog_checks.upbound_uxp.check.requests.get', return_value=mock.MagicMock(text=payload)):
        dd_run_check(check)
    return check


def _fixture():
    with open(FIXTURE) as f:
        return f.read()


def _types(aggregator, name):
    return {m.type for m in aggregator.metrics(name)}


@pytest.mark.unit
def test_instance_tags_on_metrics(dd_run_check, aggregator):
    _run(dd_run_check, _fixture())

    for name in ('uxp.go_goroutines', 'uxp.controller_runtime_reconcile_total'):
        submissions = aggregator.metrics(name)
        assert submissions, name
        for m in submissions:
            for tag in INSTANCE_TAGS:
                assert tag in m.tags, (name, m.tags)


@pytest.mark.unit
def test_instance_tags_on_service_check(dd_run_check, aggregator):
    _run(dd_run_check, _fixture())

    aggregator.assert_service_check('uxp.can_connect', UpboundUxpCheck.OK, tags=INSTANCE_TAGS)


@pytest.mark.unit
def test_no_instance_tags(dd_run_check, aggregator):
    instance = _instance()
    del instance['tags']
    _run(dd_run_check, _fixture(), instance)

    for m in aggregator.metrics('uxp.go_goroutines'):
        assert not any(t.startswith('team:') for t in m.tags)


@pytest.mark.unit
def test_counters_are_monotonic_counts(dd_run_check, aggregator):
    _run(dd_run_check, _fixture())

    # Counters
    assert _types(aggregator, 'uxp.controller_runtime_reconcile_total') == {aggregator.MONOTONIC_COUNT}
    assert _types(aggregator, 'uxp.workqueue_adds_total') == {aggregator.MONOTONIC_COUNT}
    # Histogram _sum and _count are cumulative
    assert _types(aggregator, 'uxp.workqueue_work_duration_seconds_sum') == {aggregator.MONOTONIC_COUNT}
    assert _types(aggregator, 'uxp.workqueue_work_duration_seconds_count') == {aggregator.MONOTONIC_COUNT}
    # Summary _sum and _count are cumulative
    assert _types(aggregator, 'uxp.go_gc_duration_seconds_sum') == {aggregator.MONOTONIC_COUNT}
    assert _types(aggregator, 'uxp.go_gc_duration_seconds_count') == {aggregator.MONOTONIC_COUNT}


@pytest.mark.unit
def test_gauges_buckets_and_quantiles_are_gauges(dd_run_check, aggregator):
    _run(dd_run_check, _fixture())

    assert _types(aggregator, 'uxp.go_goroutines') == {aggregator.GAUGE}
    assert _types(aggregator, 'uxp.workqueue_work_duration_seconds_bucket') == {aggregator.GAUGE}
    # Summary quantiles were previously submitted as counts
    assert _types(aggregator, 'uxp.go_gc_duration_seconds') == {aggregator.GAUGE}


@pytest.mark.unit
def test_gauge_named_count_stays_gauge(dd_run_check, aggregator):
    payload = '# HELP uxp_test_items_count Number of items\n# TYPE uxp_test_items_count gauge\nuxp_test_items_count 5\n'
    _run(dd_run_check, payload)

    aggregator.assert_metric('uxp.uxp_test_items_count', value=5, metric_type=aggregator.GAUGE)


@pytest.mark.unit
@pytest.mark.parametrize(
    'family_type, sample_name, expected',
    [
        ('counter', 'foo_total', 'monotonic_count'),
        ('gauge', 'foo_count', 'gauge'),
        ('histogram', 'foo_bucket', 'gauge'),
        ('histogram', 'foo_sum', 'monotonic_count'),
        ('histogram', 'foo_count', 'monotonic_count'),
        ('summary', 'foo', 'gauge'),
        ('summary', 'foo_sum', 'monotonic_count'),
        ('untyped', 'foo_total', 'monotonic_count'),
        ('', 'foo_bucket', 'gauge'),
        ('untyped', 'foo', None),
    ],
)
def test_submission_type(family_type, sample_name, expected):
    assert UpboundUxpCheck._submission_type(family_type, sample_name) == expected


@pytest.mark.unit
def test_instance_tags_on_heartbeat(dd_run_check, aggregator):
    _run(dd_run_check, _fixture())

    submissions = aggregator.metrics('uxp.datadog_agent_checks')
    assert submissions
    for m in submissions:
        for tag in INSTANCE_TAGS:
            assert tag in m.tags, m.tags
