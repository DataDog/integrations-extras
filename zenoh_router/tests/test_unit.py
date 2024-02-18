from typing import Any, Callable, Dict  # noqa: F401

from datadog_checks.base import AgentCheck  # noqa: F401
from datadog_checks.base.stubs.aggregator import AggregatorStub  # noqa: F401
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.zenoh_router import ZenohRouterCheck


def test_check(dd_run_check, aggregator, instance, mock_http_response):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    STATS_RESPONSE = '''
[
  {
    "key": "@/router/9bafaff963b9465d80552419bf397add",
    "value": {
      "locators": [
        "tcp/172.10.0.2:7449",
        "tls/172.10.0.2:7447"
      ],
      "metadata": {
        "name": "mediahome",
        "on_premise": true,
        "organization_id": "234a96da-d088-4107-abb1-6407d64cb3bb",
        "project": "Test router",
        "project_id": "7e62b902-2b31-490f-8e2f-58364d58e7ee",
        "provider": "On Premise",
        "provider_id": "00000000-0000-0000-0000-000000000000",
        "region": "Local",
        "region_id": "00000000-0000-0000-0000-000000000000",
        "version": "v1",
        "zenoh_version": "v0"
      },
      "sessions": [
        {
          "links": [
            "tls/18.157.60.29:7447"
          ],
          "peer": "d9adb96a1ae24e2d84dfdc0044eb6e00",
          "whatami": "router"
        },
        {
          "links": [
            "tcp/192.168.0.152:56004"
          ],
          "peer": "97be4f71efdbe237aa60afcb1668eae5",
          "whatami": "client"
        },
        {
          "links": [
            "tcp/172.18.0.1:52646"
          ],
          "peer": "421dd221176a4f3a0463238e72cb0848",
          "whatami": "peer"
        },
        {
          "links": [
            "tcp/172.18.0.1:38280"
          ],
          "peer": "362bd2d45a4c309f98d3cf3527ce117b",
          "whatami": "peer"
        }
      ],
      "stats": {
        "rx_bytes": 40522730,
        "rx_n_dropped": 0,
        "rx_n_msgs": 0,
        "rx_t_msgs": 6048007,
        "rx_z_del_msgs": {
          "admin": 0,
          "user": 0
        },
        "rx_z_put_msgs": {
          "admin": 0,
          "user": 69304
        },
        "rx_z_put_pl_bytes": {
          "admin": 0,
          "user": 16971548
        },
        "rx_z_query_msgs": {
          "admin": 107026,
          "user": 0
        },
        "rx_z_query_pl_bytes": {
          "admin": 0,
          "user": 0
        },
        "rx_z_reply_msgs": {
          "admin": 0,
          "user": 0
        },
        "rx_z_reply_pl_bytes": {
          "admin": 0,
          "user": 0
        },
        "tx_bytes": 484885104,
        "tx_n_dropped": 0,
        "tx_n_msgs": 277787,
        "tx_t_msgs": 4281639,
        "tx_z_del_msgs": {
          "admin": 0,
          "user": 0
        },
        "tx_z_put_msgs": {
          "admin": 0,
          "user": 61600
        },
        "tx_z_put_pl_bytes": {
          "admin": 0,
          "user": 15896164
        },
        "tx_z_query_msgs": {
          "admin": 0,
          "user": 0
        },
        "tx_z_query_pl_bytes": {
          "admin": 0,
          "user": 0
        },
        "tx_z_reply_msgs": {
          "admin": 108060,
          "user": 0
        },
        "tx_z_reply_pl_bytes": {
          "admin": 442923663,
          "user": 0
        }
      },
      "version": "v0.10.0-rc-modified built with rustc 1.72.0 (5680fa18f 2023-08-23)",
      "zid": "9bafaff963b9465d80552419bf397add"
    },
    "encoding": "application/json",
    "time": "None"
  }
]'''

    mock_http_response(STATS_RESPONSE)

    check = ZenohRouterCheck('zenoh_router', {}, [instance])
    dd_run_check(check)
    # run second time, because first call stats not processed
    dd_run_check(check)

    gtags = ['name:mediahome', 'zenoh_version:v0', 'zid:9bafaff963b9465d80552419bf397add']

    expected = [
        {'name': 'zenoh.router.sessions', 'value': 2, 'tags': gtags + ['whatami:client']},
        {'name': 'zenoh.router.sessions', 'value': 2, 'tags': gtags + ['whatami:router']},
        {'name': 'zenoh.router.sessions', 'value': 4, 'tags': gtags + ['whatami:peer']},
        {'name': 'zenoh.router.rx_bytes', 'tags': gtags + ['space:']},
        {'name': 'zenoh.router.rx_n_dropped', 'tags': gtags + ['space:']},
        {'name': 'zenoh.router.rx_n_msgs', 'tags': gtags + ['space:']},
        {'name': 'zenoh.router.rx_t_msgs', 'tags': gtags + ['space:']},
        {'name': 'zenoh.router.rx_z_del_msgs', 'tags': gtags + ['space:user']},
        {'name': 'zenoh.router.rx_z_del_msgs', 'tags': gtags + ['space:admin']},
        {'name': 'zenoh.router.rx_z_put_msgs', 'tags': gtags + ['space:user']},
        {'name': 'zenoh.router.rx_z_put_msgs', 'tags': gtags + ['space:admin']},
        {'name': 'zenoh.router.rx_z_put_pl_bytes', 'tags': gtags + ['space:user']},
        {'name': 'zenoh.router.rx_z_put_pl_bytes', 'tags': gtags + ['space:admin']},
        {'name': 'zenoh.router.rx_z_query_msgs', 'tags': gtags + ['space:user']},
        {'name': 'zenoh.router.rx_z_query_msgs', 'tags': gtags + ['space:admin']},
        {'name': 'zenoh.router.rx_z_query_pl_bytes', 'tags': gtags + ['space:user']},
        {'name': 'zenoh.router.rx_z_query_pl_bytes', 'tags': gtags + ['space:admin']},
        {'name': 'zenoh.router.rx_z_reply_msgs', 'tags': gtags + ['space:user']},
        {'name': 'zenoh.router.rx_z_reply_msgs', 'tags': gtags + ['space:admin']},
        {'name': 'zenoh.router.rx_z_reply_pl_bytes', 'tags': gtags + ['space:user']},
        {'name': 'zenoh.router.rx_z_reply_pl_bytes', 'tags': gtags + ['space:admin']},
        {'name': 'zenoh.router.tx_bytes', 'tags': gtags + ['space:']},
        {'name': 'zenoh.router.tx_n_dropped', 'tags': gtags + ['space:']},
        {'name': 'zenoh.router.tx_n_msgs', 'tags': gtags + ['space:']},
        {'name': 'zenoh.router.tx_t_msgs', 'tags': gtags + ['space:']},
        {'name': 'zenoh.router.tx_z_del_msgs', 'tags': gtags + ['space:user']},
        {'name': 'zenoh.router.tx_z_del_msgs', 'tags': gtags + ['space:admin']},
        {'name': 'zenoh.router.tx_z_put_msgs', 'tags': gtags + ['space:user']},
        {'name': 'zenoh.router.tx_z_put_msgs', 'tags': gtags + ['space:admin']},
        {'name': 'zenoh.router.tx_z_put_pl_bytes', 'tags': gtags + ['space:user']},
        {'name': 'zenoh.router.tx_z_put_pl_bytes', 'tags': gtags + ['space:admin']},
        {'name': 'zenoh.router.tx_z_query_msgs', 'tags': gtags + ['space:user']},
        {'name': 'zenoh.router.tx_z_query_msgs', 'tags': gtags + ['space:admin']},
        {'name': 'zenoh.router.tx_z_query_pl_bytes', 'tags': gtags + ['space:user']},
        {'name': 'zenoh.router.tx_z_query_pl_bytes', 'tags': gtags + ['space:admin']},
        {'name': 'zenoh.router.tx_z_reply_msgs', 'tags': gtags + ['space:user']},
        {'name': 'zenoh.router.tx_z_reply_msgs', 'tags': gtags + ['space:admin']},
        {'name': 'zenoh.router.tx_z_reply_pl_bytes', 'tags': gtags + ['space:user']},
        {'name': 'zenoh.router.tx_z_reply_pl_bytes', 'tags': gtags + ['space:admin']},
    ]

    for e in expected:
        aggregator.assert_metric(e['name'], value=e.get('value', None), tags=e['tags'])

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_emits_critical_service_check_when_service_is_down(dd_run_check, aggregator, instance, mock_http_response):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None

    mock_http_response('')

    check = ZenohRouterCheck('zenoh_router', {}, [instance])
    dd_run_check(check)
    aggregator.assert_service_check('zenoh.router.can_connect', ZenohRouterCheck.CRITICAL)
