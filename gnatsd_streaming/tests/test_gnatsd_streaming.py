# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

import pytest

from datadog_checks.gnatsd_streaming import GnatsdStreamingCheck

CHECK_NAME = 'gnatsd_streaming'

CONNECTION_FAILURE = {'host': 'http://totally_not_locallhost', 'port': 8222}


def test_connection_failure(aggregator):
    c = GnatsdStreamingCheck(CHECK_NAME, {}, [CONNECTION_FAILURE])

    with pytest.raises(Exception):
        c.check(CONNECTION_FAILURE)

    aggregator.assert_service_check('gnatsd_streaming.can_connect', status=GnatsdStreamingCheck.CRITICAL, count=1)


@pytest.mark.usefixtures('dd_environment')
def test_metrics(aggregator, instance):
    c = GnatsdStreamingCheck(CHECK_NAME, {}, [instance])
    c.check(instance)

    aggregator.assert_service_check('gnatsd_streaming.can_connect', status=GnatsdStreamingCheck.OK, count=1)
    aggregator.assert_metric('gnatsd.streaming.serverz.clients', metric_type=aggregator.GAUGE)
    aggregator.assert_metric('gnatsd.streaming.serverz.subscriptions', metric_type=aggregator.COUNT)
    aggregator.assert_metric('gnatsd.streaming.serverz.channels', metric_type=aggregator.GAUGE)
    aggregator.assert_metric('gnatsd.streaming.serverz.total_msgs', metric_type=aggregator.COUNT)
    aggregator.assert_metric('gnatsd.streaming.serverz.total_bytes', metric_type=aggregator.COUNT)
    aggregator.assert_metric('gnatsd.streaming.storez.total_msgs', metric_type=aggregator.COUNT)
    aggregator.assert_metric('gnatsd.streaming.storez.total_bytes', metric_type=aggregator.COUNT)
    aggregator.assert_metric('gnatsd.streaming.clientsz.total', metric_type=aggregator.GAUGE)
    aggregator.assert_metric('gnatsd.streaming.channelsz.total', metric_type=aggregator.GAUGE)
    aggregator.assert_metric('gnatsd.streaming.channelsz.channels.test_channel1.msgs', metric_type=aggregator.COUNT)
    aggregator.assert_metric('gnatsd.streaming.channelsz.channels.test_channel1.bytes', metric_type=aggregator.COUNT)
    aggregator.assert_metric('gnatsd.streaming.channelsz.channels.test_channel2.msgs', metric_type=aggregator.COUNT)
    aggregator.assert_metric('gnatsd.streaming.channelsz.channels.test_channel2.bytes', metric_type=aggregator.COUNT)
    aggregator.assert_metric('gnatsd.streaming.channelsz.channels.test_channel3.msgs', metric_type=aggregator.COUNT)
    aggregator.assert_metric('gnatsd.streaming.channelsz.channels.test_channel3.bytes', metric_type=aggregator.COUNT)

    aggregator.assert_all_metrics_covered()


@pytest.mark.usefixtures('dd_environment')
def test_metric_tags(aggregator, instance):
    c = GnatsdStreamingCheck(CHECK_NAME, {}, [instance])
    c.check(instance)

    aggregator.assert_metric_has_tag_prefix('gnatsd.streaming.serverz.clients', 'nss-cluster_id', at_least=1)
    aggregator.assert_metric_has_tag_prefix('gnatsd.streaming.serverz.clients', 'nss-server_id', at_least=1)
    aggregator.assert_metric_has_tag_prefix('gnatsd.streaming.serverz.clients', 'nss-version', at_least=1)
    aggregator.assert_metric_has_tag_prefix('gnatsd.streaming.serverz.clients', 'nss-go', at_least=1)
    aggregator.assert_metric_has_tag_prefix('gnatsd.streaming.storez.total_msgs', 'nss-cluster_id', at_least=1)
    aggregator.assert_metric_has_tag_prefix('gnatsd.streaming.storez.total_msgs', 'nss-server_id', at_least=1)
    aggregator.assert_metric_has_tag_prefix('gnatsd.streaming.clientsz.total', 'nss-cluster_id', at_least=1)
    aggregator.assert_metric_has_tag_prefix('gnatsd.streaming.clientsz.total', 'nss-server_id', at_least=1)
    aggregator.assert_metric_has_tag_prefix('gnatsd.streaming.channelsz.total', 'nss-cluster_id', at_least=1)
    aggregator.assert_metric_has_tag_prefix('gnatsd.streaming.channelsz.total', 'nss-server_id', at_least=1)


@pytest.mark.usefixtures('dd_environment')
def test_failover_event(aggregator, instance):
    c = GnatsdStreamingCheck(CHECK_NAME, {}, [instance])
    c.check(instance)
    c.ft_status = 'FT_STANDBY'
    c.check(instance)
    aggregator.assert_event('NATS Streaming Server Changed Status from FT_STANDBY to FT_ACTIVE', count=1)


@pytest.mark.usefixtures('dd_environment')
def test_deltas(aggregator, instance):
    c = GnatsdStreamingCheck(CHECK_NAME, {}, [instance])
    c.check(instance)
    aggregator.assert_metric(
        'gnatsd.streaming.channelsz.channels.test_channel1.msgs', metric_type=aggregator.COUNT, value=10
    )
    aggregator.reset()
    c.check(instance)
    aggregator.assert_metric(
        'gnatsd.streaming.channelsz.channels.test_channel1.msgs', metric_type=aggregator.COUNT, value=0
    )
    aggregator.reset()
    c.check(instance)
    aggregator.assert_metric(
        'gnatsd.streaming.channelsz.channels.test_channel1.msgs', metric_type=aggregator.COUNT, value=0
    )
    aggregator.reset()
    c.check(instance)
    aggregator.assert_metric(
        'gnatsd.streaming.channelsz.channels.test_channel1.msgs', metric_type=aggregator.COUNT, value=0
    )
