# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

import pytest

from datadog_checks.dev.docker import get_container_ip
from datadog_checks.gnatsd import GnatsdCheck

CHECK_NAME = 'gnatsd'

CONNECTION_FAILURE = {'host': 'http://totally_not_locallhost', 'port': 8222}


def test_connection_failure(aggregator):
    c = GnatsdCheck(CHECK_NAME, {}, [CONNECTION_FAILURE])

    with pytest.raises(Exception):
        c.check(CONNECTION_FAILURE)

    aggregator.assert_service_check('gnatsd.can_connect', status=GnatsdCheck.CRITICAL, count=1)


@pytest.mark.usefixtures('dd_environment')
def test_metrics(aggregator, instance):
    c = GnatsdCheck(CHECK_NAME, {}, [instance])
    c.check(instance)

    aggregator.assert_service_check('gnatsd.can_connect', status=GnatsdCheck.OK, count=1)
    aggregator.assert_metric('gnatsd.varz.connections', metric_type=aggregator.GAUGE)
    aggregator.assert_metric('gnatsd.varz.subscriptions', metric_type=aggregator.GAUGE)
    aggregator.assert_metric('gnatsd.varz.slow_consumers', metric_type=aggregator.COUNT)
    aggregator.assert_metric('gnatsd.varz.remotes', metric_type=aggregator.GAUGE)
    aggregator.assert_metric('gnatsd.varz.routes', metric_type=aggregator.GAUGE)
    aggregator.assert_metric('gnatsd.varz.in_msgs', metric_type=aggregator.COUNT)
    aggregator.assert_metric('gnatsd.varz.out_msgs', metric_type=aggregator.COUNT)
    aggregator.assert_metric('gnatsd.varz.in_bytes', metric_type=aggregator.COUNT)
    aggregator.assert_metric('gnatsd.varz.out_bytes', metric_type=aggregator.COUNT)
    aggregator.assert_metric('gnatsd.varz.mem', metric_type=aggregator.GAUGE)
    aggregator.assert_metric('gnatsd.connz.num_connections', metric_type=aggregator.GAUGE)
    aggregator.assert_metric('gnatsd.connz.total', metric_type=aggregator.COUNT)
    aggregator.assert_metric('gnatsd.connz.connections.foo-sub.pending_bytes', metric_type=aggregator.GAUGE)
    aggregator.assert_metric('gnatsd.connz.connections.foo-sub.in_msgs', metric_type=aggregator.COUNT)
    # We sent 2 messages to this queue in the ci setup
    aggregator.assert_metric('gnatsd.connz.connections.foo-sub.out_msgs', metric_type=aggregator.COUNT)
    aggregator.assert_metric('gnatsd.connz.connections.foo-sub.subscriptions', metric_type=aggregator.GAUGE)
    aggregator.assert_metric('gnatsd.connz.connections.foo-sub.in_bytes', metric_type=aggregator.COUNT)
    aggregator.assert_metric('gnatsd.connz.connections.foo-sub.out_bytes', metric_type=aggregator.COUNT)
    aggregator.assert_metric('gnatsd.connz.connections.unnamed.pending_bytes', metric_type=aggregator.GAUGE)
    aggregator.assert_metric('gnatsd.connz.connections.unnamed.in_msgs', metric_type=aggregator.COUNT)
    # We sent 1 message to this queue in the ci setup
    aggregator.assert_metric('gnatsd.connz.connections.unnamed.out_msgs', metric_type=aggregator.COUNT, value=1)
    aggregator.assert_metric('gnatsd.connz.connections.unnamed.subscriptions', metric_type=aggregator.GAUGE)
    aggregator.assert_metric('gnatsd.connz.connections.unnamed.in_bytes', metric_type=aggregator.COUNT)
    aggregator.assert_metric('gnatsd.connz.connections.unnamed.out_bytes', metric_type=aggregator.COUNT)
    aggregator.assert_metric('gnatsd.routez.num_routes', metric_type=aggregator.GAUGE)

    route_ip = get_container_ip('docker_nats_serverA_1').replace('.', '_')
    aggregator.assert_metric('gnatsd.routez.routes.{}.in_msgs'.format(route_ip), metric_type=aggregator.COUNT)
    aggregator.assert_metric('gnatsd.routez.routes.{}.out_msgs'.format(route_ip), metric_type=aggregator.COUNT)
    aggregator.assert_metric('gnatsd.routez.routes.{}.subscriptions'.format(route_ip), metric_type=aggregator.GAUGE)
    aggregator.assert_metric('gnatsd.routez.routes.{}.in_bytes'.format(route_ip), metric_type=aggregator.COUNT)
    aggregator.assert_metric('gnatsd.routez.routes.{}.out_bytes'.format(route_ip), metric_type=aggregator.COUNT)
    aggregator.assert_metric('gnatsd.routez.routes.{}.pending_size'.format(route_ip), metric_type=aggregator.GAUGE)
    aggregator.assert_all_metrics_covered()


@pytest.mark.usefixtures('dd_environment')
def test_metric_tags(aggregator, instance):
    c = GnatsdCheck(CHECK_NAME, {}, [instance])
    c.check(instance)

    aggregator.assert_metric_has_tag_prefix('gnatsd.varz.connections', 'gnatsd-server_id', at_least=1)
    aggregator.assert_metric_has_tag_prefix('gnatsd.connz.connections.foo-sub.out_msgs', 'gnatsd-cid', at_least=1)
    aggregator.assert_metric_has_tag_prefix('gnatsd.connz.connections.foo-sub.out_msgs', 'gnatsd-ip', at_least=1)
    aggregator.assert_metric_has_tag_prefix('gnatsd.connz.connections.foo-sub.out_msgs', 'gnatsd-name', at_least=1)
    aggregator.assert_metric_has_tag_prefix('gnatsd.connz.connections.foo-sub.out_msgs', 'gnatsd-lang', at_least=1)
    aggregator.assert_metric_has_tag_prefix('gnatsd.connz.connections.foo-sub.out_msgs', 'gnatsd-version', at_least=1)

    route_ip = get_container_ip('docker_nats_serverA_1').replace('.', '_')
    aggregator.assert_metric_has_tag_prefix(
        'gnatsd.routez.routes.{}.in_msgs'.format(route_ip), 'gnatsd-rid', at_least=1
    )
    aggregator.assert_metric_has_tag_prefix(
        'gnatsd.routez.routes.{}.in_msgs'.format(route_ip), 'gnatsd-remote_id', at_least=1
    )
    aggregator.assert_metric_has_tag_prefix('gnatsd.routez.routes.{}.in_msgs'.format(route_ip), 'gnatsd-ip', at_least=1)


@pytest.mark.usefixtures('dd_environment')
def test_deltas(aggregator, instance):
    c = GnatsdCheck(CHECK_NAME, {}, [instance])
    c.check(instance)

    aggregator.assert_metric('gnatsd.connz.connections.foo-sub.out_msgs', metric_type=aggregator.COUNT)
    aggregator.reset()
    c.check(instance)
    aggregator.assert_metric('gnatsd.connz.connections.foo-sub.out_msgs', metric_type=aggregator.COUNT, value=0)
    aggregator.reset()
    c.check(instance)
    aggregator.assert_metric('gnatsd.connz.connections.foo-sub.out_msgs', metric_type=aggregator.COUNT, value=0)
    aggregator.reset()
    c.check(instance)
    aggregator.assert_metric('gnatsd.connz.connections.foo-sub.out_msgs', metric_type=aggregator.COUNT, value=0)
