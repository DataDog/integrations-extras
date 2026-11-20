# (C) Datadog, Inc. 2026-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import pytest

from datadog_checks.base.constants import ServiceCheck
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.log10x import Log10xCheck

from .common import BAD_HOSTNAME_INSTANCE, EXPECTED_METRICS

pytestmark = [pytest.mark.unit]


def test_connect_exception(dd_run_check, aggregator):
    with pytest.raises(Exception, match="Failed to resolve 'invalid-hostname'|Max retries exceeded"):
        check = Log10xCheck('log10x', {}, [BAD_HOSTNAME_INSTANCE])
        dd_run_check(check)

    aggregator.assert_service_check('log10x.openmetrics.health', ServiceCheck.CRITICAL)
    # The heartbeat is emitted before the scrape, so it survives an unreachable engine.
    aggregator.assert_metric('log10x.check.up', value=1, count=1)


def test_check_scrape(dd_run_check, aggregator, check, mock_prometheus_metrics):
    dd_run_check(check)
    for metric_name in EXPECTED_METRICS:
        aggregator.assert_metric(metric_name, at_least=1)
    aggregator.assert_metric_has_tag_prefix('log10x.bytes.read.count', 'message_pattern:')
    aggregator.assert_metric_has_tag_prefix('log10x.bytes.read.count', 'severity_level:')
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
    aggregator.assert_all_metrics_covered()
    aggregator.assert_service_check('log10x.openmetrics.health', ServiceCheck.OK)


def test_identity_labels_dropped(dd_run_check, aggregator, check, mock_prometheus_metrics):
    dd_run_check(check)
    for m in aggregator.metrics('log10x.bytes.read.count'):
        assert not any(t.startswith('tenx_pipeline_uuid:') or t.startswith('tenx_hash:') for t in m.tags)


def test_empty_instance(dd_run_check):
    with pytest.raises(Exception, match='\nopenmetrics_endpoint\n  Field required'):
        check = Log10xCheck('log10x', {}, [{}])
        dd_run_check(check)
