import json
import logging

import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.ns1 import Ns1Check
from requests.exceptions import HTTPError


def test_empty_instance(aggregator, instance_empty):
    with pytest.raises(ConfigurationError):
        _ = Ns1Check('ns1', {}, [instance_empty])


def test_config(aggregator, instance):
    check = Ns1Check('ns1', {}, [instance])
    assert check.api_endpoint is not None
    aggregator.assert_all_metrics_covered()


def test_no_key(aggregator, instance_nokey):
    with pytest.raises(ConfigurationError):
        _ = Ns1Check('ns1', {}, [instance_nokey])


def test_no_metrics(aggregator, instance_nometrics):

    with pytest.raises(ConfigurationError):
        _ = Ns1Check('ns1', {}, [instance_nometrics])


def test_parse_metrics(aggregator, instance):
    check = Ns1Check('ns1', {}, [instance])
    metric = instance["metrics"]

    assert len(metric) > 0
    assert check.api_endpoint is not None


def test_get_zone_info_url(aggregator, instance_ddi, requests_mock):
    check = Ns1Check('ns1', {}, [instance_ddi])
    aggregator.assert_all_metrics_covered()
    checkUrl = check.ns1.get_zone_info_url("test", None)
    assert len(checkUrl.items()) == 0  # is None


def test_429_http_error(aggregator, instance_ddi, requests_mock):
    check = Ns1Check('ns1', {}, [instance_ddi])
    aggregator.assert_all_metrics_covered()

    url = "{apiendpoint}/v1/zones/dloc1.com".format(apiendpoint=check.api_endpoint)

    requests_mock.register_uri(
        'GET',
        url,
        status_code=429,
        reason="Too many requests",
        headers={
            'X-Ratelimit-By': 'customer',
            'X-Ratelimit-Limit': '1000',
            'X-Ratelimit-Period': '1',
            'X-Ratelimit-Remaining': '0'
        }
    )
    with pytest.raises(HTTPError):
        stats = check.get_stats(url)
        assert stats is None


def test_set_max_retries(aggregator, instance_ddi, requests_mock, caplog):
    max_retries = 3
    instance_ddi["max_retry_attempts"] = max_retries
    check = Ns1Check('ns1', {}, [instance_ddi])

    with caplog.at_level(logging.WARNING):
        url = "{apiendpoint}/v1/zones/dloc1.com".format(apiendpoint=check.api_endpoint)

        requests_mock.register_uri(
            'GET',
            url,
            status_code=429,
            reason="Too many requests",
            headers={
                'X-Ratelimit-By': 'customer',
                'X-Ratelimit-Limit': '1000',
                'X-Ratelimit-Period': '1',
                'X-Ratelimit-Remaining': '0'
            }
        )
        with pytest.raises(HTTPError):
            check.get_stats(url)

        log_list = caplog.text.split('\n')
        assert len(log_list) == max_retries + 1
        for i in range(max_retries):
            assert 'Rate limit reached' in log_list[i]


def test_url_gen_ddi(aggregator, instance_ddi, requests_mock):
    check = Ns1Check('ns1', {}, [instance_ddi])
    aggregator.assert_all_metrics_covered()
    url = "{apiendpoint}/v1/dhcp/scopegroup".format(apiendpoint=check.api_endpoint)
    ddiresponse = '''
    [
        {
            "dhcp_service_id": 3,
            "name": "scope1",
            "client_class_ids": [],
            "dhcpv4": {
                "enabled": true,
                "options": [
                    {
                        "name": "dhcpv4/example-single-type",
                        "value": "markmpeterson.xyz"
                    }
                ],
                "rebind_timer_secs": 43200,
                "renew_timer_secs": 21600,
                "valid_lifetime_secs": 86400,
                "echo_client_id": true,
                "match_client_id": true,
                "synthesize_dns_records": {
                    "enabled": true
                }
            },
            "dhcpv6": {
                "enabled": false,
                "options": [],
                "synthesize_dns_records": {}
            },
            "blocked_tags": [],
            "local_tags": [
                "Site Code",
                "auth:Security Lvl"
            ],
            "tags": {
                "Site Code": "DO",
                "auth:Security Lvl": "2"
            },
            "id": 2,
            "network_id": 1,
            "template_config": []
        }
    ]
    '''
    requests_mock.get(url, text=ddiresponse)
    checkUrl = check.create_url(check.metrics, check.query_params, check.networks)

    assert len(checkUrl) > 0
    assert check.api_endpoint is not None
    # leases
    assert checkUrl["leases"][0] == "https://localhost/v1/stats/leases?period=24h"
    assert checkUrl["leases.2"][0] == "https://localhost/v1/stats/leases/2?period=24h"
    # lps
    assert checkUrl["peak_lps"][0] == "https://localhost/v1/stats/lps?period=24h"
    assert checkUrl["peak_lps.2"][0] == "https://localhost/v1/stats/lps/2?period=24h"


def test_url_gen(aggregator, instance_1, requests_mock):
    check = Ns1Check('ns1', {}, [instance_1])
    aggregator.assert_all_metrics_covered()

    url = "{apiendpoint}/v1/pulsar/apps".format(apiendpoint=check.api_endpoint)
    appres = '''
    [
        {
            "customer": 16774,
            "name": "Leandro's app",
            "community": false,
            "appid": "ejgrgw",
            "active": true,
            "jobs_per_transaction": 2
        },
        {
            "customer": 1000,
            "name": "Pulsar community",
            "community": true,
            "appid": "1xy4sn3",
            "active": true,
            "jobs_per_transaction": 2
        }
    ]
    '''
    jobres = '''
    [
        {
            "customer": 1000,
            "typeid": "latency",
            "name": "CDN Latency - Cloudflare",
            "community": true,
            "jobid": "1xtvhvx",
            "appid": "1xy4sn3",
            "active": true
        }
    ]
    '''
    jobres1 = '''
    [
        {
            "customer": 1000,
            "typeid": "latency",
            "name": "CDN Latency - Cloudflare",
            "community": true,
            "jobid": "1xtvhvx",
            "appid": "ejgrgw",
            "active": true
        }
    ]
    '''
    netres = '''
    [
        {
            "network_id": 0,
            "name": "NS1 Managed DNS Network",
            "label": "NSONE"
        },
        {
            "network_id": 80,
            "name": "Custom Network",
            "label": "NSONE"
        }
    ]
    '''
    zoneres = '''
    {
        "nx_ttl": 3600,
        "retry": 7200,
        "zone": "dloc1.com",
        "dnssec": false,
        "network_pools": [
            "p07"
        ],
        "serial": 1619455705,
        "primary": {
            "enabled": false,
            "secondaries": []
        },
        "refresh": 43200,
        "expiry": 1209600,
        "disabled": false,
        "records": [
            {
                "domain": "dloc1.com",
                "ttl": 3600,
                "tier": 1,
                "type": "NS",
                "id": "606f3d48cfd3cd00acfde92c",
                "short_answers": [
                    "dns1.p07.nsone.net",
                    "dns2.p07.nsone.net",
                    "dns3.p07.nsone.net",
                    "dns4.p07.nsone.net"
                ]
            },
            {
                "domain": "email.dloc1.com",
                "ttl": 3600,
                "tier": 1,
                "type": "A",
                "id": "6086eed94590ff00b68598c5",
                "short_answers": [
                    "2.2.2.2"
                ]
            },
            {
                "domain": "www.dloc1.com",
                "ttl": 3600,
                "tier": 1,
                "type": "A",
                "id": "606f3d733991b100b60db03f",
                "short_answers": [
                    "4.5.6.7"
                ]
            }
        ],
        "meta": {},
        "link": null,
        "primary_master": "dns1.p07.nsone.net",
        "ttl": 3600,
        "id": "606f3d48cfd3cd00acfde927",
        "dns_servers": [
            "dns1.p07.nsone.net",
            "dns2.p07.nsone.net",
            "dns3.p07.nsone.net",
            "dns4.p07.nsone.net"
        ],
        "hostmaster": "hostmaster@nsone.net",
        "networks": [
            0
        ],
        "pool": "p07"
    }
    '''
    requests_mock.get(url, text=appres)
    url1 = "{apiendpoint}/v1/pulsar/apps/1xy4sn3/jobs".format(apiendpoint=check.api_endpoint)
    url2 = "{apiendpoint}/v1/pulsar/apps/ejgrgw/jobs".format(apiendpoint=check.api_endpoint)
    url3 = "{apiendpoint}/v1/networks".format(apiendpoint=check.api_endpoint)
    url4 = "{apiendpoint}/v1/zones/dloc1.com".format(apiendpoint=check.api_endpoint)
    requests_mock.get(url1, text=jobres)
    requests_mock.get(url2, text=jobres1)
    requests_mock.get(url3, text=netres)
    requests_mock.get(url4, text=zoneres)
    check.get_pulsar_applications()

    checkUrl = check.create_url(check.metrics, check.query_params, check.networks)

    assert check.get_pulsar_job_name_from_id("1xtvhvx") == "CDN Latency - Cloudflare"
    # if check.query_params:
    query_params = check.query_params
    query_string = "?"
    query_string = query_string + "period=" + query_params["pulsar_period"] + "&"
    query_string = query_string + "geo=" + query_params["pulsar_geo"] + "&"
    query_string = query_string + "asn=" + query_params["pulsar_asn"] + "&"
    query_string = query_string[:-1]
    assert query_string == "?period=1m&geo=*&asn=*"
    assert check.query_params["pulsar_period"] == "1m"

    assert len(checkUrl) > 0
    assert check.api_endpoint is not None
    # qps
    assert checkUrl["qps"][0] == "https://my.nsone.net/v1/stats/qps"
    assert checkUrl["qps.dloc.com"][0] == "https://my.nsone.net/v1/stats/qps/dloc.com"
    # usage
    assert checkUrl["usage"][0] == "https://my.nsone.net/v1/stats/usage?period=1h&expand=false"
    assert checkUrl["usage.0"][0] == "https://my.nsone.net/v1/stats/usage?period=1h&expand=false&networks=0"
    url = "https://my.nsone.net/v1/stats/usage/dloc.com?period=1h&expand=false&networks=0"
    assert checkUrl["usage.dloc.com.0"][0] == url
    url = "https://my.nsone.net/v1/stats/usage/dloc.com?period=1h&expand=false&networks=0"
    assert checkUrl["usage.dloc.com.0"][0] == url
    for k, v in checkUrl.items():
        url, name, tags, metric_type = v
        print("{key} = {val}".format(key=k, val=url))
    url = "https://my.nsone.net/v1/stats/usage/dloc.com/www.dloc.com/A?period=1h&expand=false&networks=0"
    assert checkUrl["usage.www.dloc.com.A.0"][0] == url

    # ttl
    assert checkUrl["account.ttl.dloc.com"][0] == "https://my.nsone.net/v1/zones/dloc.com"
    assert checkUrl["account.ttl.dloc.com"][2] == ["record:dloc.com"]

    # pulsar
    expect = "https://my.nsone.net/v1/pulsar/query/decisions?period=1h&agg=jobid"
    assert checkUrl["pulsar.decisions"][0] == expect
    # pulsar by app
    expect = "https://my.nsone.net/v1/pulsar/apps/1xy4sn3/jobs/1xtvhvx/data?period=1m"
    assert checkUrl["pulsar.performance.1xy4sn3.1xtvhvx"][0] == expect
    expect = "https://my.nsone.net/v1/pulsar/apps/1xy4sn3/jobs/1xtvhvx/availability?period=1m"
    assert checkUrl["pulsar.availability.1xy4sn3.1xtvhvx"][0] == expect
    assert "pulsar.availability.ejgrgw.1xtvhvx" not in checkUrl

    # pulsar by record
    expect = "https://my.nsone.net/v1/pulsar/query/decisions?period=1h&agg=jobid&record=www.dloc1.com_A"
    assert checkUrl["pulsar.decisions.www.dloc1.com.A"][0] == expect
    expect = "https://my.nsone.net/v1/pulsar/query/routemap/hit/record/www.dloc1.com/A?period=1h"
    assert checkUrl["pulsar.routemap.hit.www.dloc1.com.A"][0] == expect

    checkUrl = check.create_url(check.metrics, check.query_params, None)
    # usage
    assert checkUrl["usage"][0] == "https://my.nsone.net/v1/stats/usage?period=1h&expand=false"
    url = "https://my.nsone.net/v1/stats/usage/dloc.com?period=1h&expand=false"
    assert checkUrl["usage.dloc.com"][0] == url
    url = "https://my.nsone.net/v1/stats/usage/dloc.com?period=1h&expand=false"
    assert checkUrl["usage.dloc.com"][0] == url
    url = "https://my.nsone.net/v1/stats/usage/dloc.com/www.dloc.com/A?period=1h&expand=false"
    assert checkUrl["usage.www.dloc.com.A"][0] == url


def test_get_pulsar_app(aggregator, instance, requests_mock):
    check = Ns1Check('ns1', {}, [instance])
    url = "{apiendpoint}/v1/pulsar/apps".format(apiendpoint=check.api_endpoint)
    appres = '''
    [
        {
            "customer": 1000,
            "name": "Pulsar community",
            "community": true,
            "appid": "1xy4sn3",
            "active": true,
            "jobs_per_transaction": 2
        }
    ]
    '''
    jobres = '''
    [
        {
            "customer": 1000,
            "typeid": "latency",
            "name": "CDN Latency - Cloudflare",
            "community": true,
            "jobid": "1xtvhvx",
            "appid": "1xy4sn3",
            "active": true
        }
    ]
    '''

    requests_mock.get(url, text=appres)
    url1 = "{apiendpoint}/v1/pulsar/apps/1xy4sn3/jobs".format(apiendpoint=check.api_endpoint)
    requests_mock.get(url1, text=jobres)
    pulsar_apps = check.get_pulsar_applications()

    assert len(pulsar_apps) > 0
    key = next(iter(pulsar_apps))
    assert pulsar_apps[key][0] == "Pulsar community"
    assert pulsar_apps["1xy4sn3"][0] == "Pulsar community"
    jobs = pulsar_apps[key][1]
    assert jobs[0]["jobid"] == "1xtvhvx"
    check.pulsar_apps = pulsar_apps
    jobname = check.get_pulsar_job_name_from_id("1xtvhvx")
    assert jobname == "CDN Latency - Cloudflare"
    jobname = check.get_pulsar_job_name_from_id("xxx")
    assert jobname == ""


USAGE_RESULT = """
[
    {
        "jobs": 1,
        "graph": [
            [
                1619217000,
                1408
            ],
            [
                1619218800,
                1410
            ],
            [
                1619220600,
                758
            ]
        ],
        "period": "1h",
        "zones": 8,
        "records": 23,
        "queries": 3576,
        "feeds": 3
    }
]
"""

PULSAR_RESULT_DECISIONS = """
{
    "graphs": [
        {
            "graph": [
                [
                    1619740800,
                    1890.0
                ],
                [
                    1619784000,
                    4090.0
                ],
                [
                    1619827200,
                    1644.0
                ]
            ],
            "tags": {
                "asn": "16509",
                "result": "OK",
                "jobid": "1b1o94j"
            }
        },
        {
            "graph": [
                [
                    1619740800,
                    2955.0
                ],
                [
                    1619784000,
                    2064.0
                ],
                [
                    1619827200,
                    7167.0
                ],
                [
                    1619870400,
                    1901.0
                ]
            ],
            "tags": {
                "asn": "16509",
                "result": "OK",
                "jobid": "1xtvhvx"
            }
        },
        {
            "graph": [
                [
                    1619740800,
                    5293.0
                ],
                [
                    1619784000,
                    3022.0
                ],
                [
                    1619827200,
                    969.0
                ],
                [
                    1619870400,
                    2976.0
                ]
            ],
            "tags": {
                "asn": "16509",
                "result": "OK",
                "jobid": "1xtsor1"
            }
        }
    ],
    "end_ts": 1619908667,
    "start_ts": 1619735867
}
"""

PULSAR_RESULT_PERFORMANCE = """
{
    "agg": "p50",
    "graph": {
        "*": {
            "*": [
                [
                    1619827200,
                    48.32
                ],
                [
                    1619870400,
                    48.094
                ],
                [
                    1619913600,
                    48.255
                ],
                [
                    1619956800,
                    46.605
                ]
            ]
        }
    },
    "end_ts": 1619986378,
    "start_ts": 1619813578,
    "jobid": "1xtvhvx",
    "appid": "1xy4sn3"
}
"""

PULSAR_RESULT_AVAILABILITY = """
{
    "graphs": [
        {
            "graph": [
                [
                    1619827200,
                    1.0
                ],
                [
                    1619870400,
                    1.0
                ],
                [
                    1619913600,
                    1.0
                ],
                [
                    1619956800,
                    0.975
                ]
            ],
            "tags": {
                "instid": "1"
            }
        }
    ],
    "end_ts": 1619987103,
    "start_ts": 1619814303
}
"""


def test_usage_count(aggregator, instance_1):
    check = Ns1Check('ns1', {}, [instance_1])
    check.usage_count = {"test": [0, 0]}
    usage, status = check.extract_usage_count("test", json.loads(USAGE_RESULT))

    assert usage == 758
    assert status
    assert check.usage_count["test"] == [1619220600, 758]

    check.usage_count = {"usage": [0, 0]}
    usage, status = check.extract_metric("usage", json.loads(USAGE_RESULT))

    assert usage == 758
    assert status
    assert check.usage_count["usage"] == [1619220600, 758]


def test_pulsar_count(aggregator, instance_1):
    check = Ns1Check('ns1', {}, [instance_1])
    check.usage_count = {"test": [0, 0]}
    usage, status = check.extract_pulsar_count("test", json.loads(PULSAR_RESULT_DECISIONS))

    assert usage == 4877
    assert status
    assert check.usage_count["test"] == [1619870400, 4877]

    check.usage_count = {"pulsar": [1619870400, 5000]}
    usage, status = check.extract_pulsar_count("pulsar", json.loads(PULSAR_RESULT_DECISIONS))
    assert usage == 0
    assert check.usage_count["pulsar"] == [1619870400, 5000]
    usage, status = check.extract_metric("pulsar", json.loads(PULSAR_RESULT_DECISIONS))
    assert usage == 0
    assert check.usage_count["pulsar"] == [1619870400, 5000]

    check.usage_count = {"test.1b1o94j": [0, 0]}
    jobs, status = check.extract_pulsar_count_by_job("test", json.loads(PULSAR_RESULT_DECISIONS))
    assert jobs["test.1b1o94j"] == 1644

    check.usage_count = {"pulsar.decisions.1b1o94j": [0, 0]}
    jobs, status = check.extract_metric("pulsar.decisions", json.loads(PULSAR_RESULT_DECISIONS))
    assert jobs["pulsar.decisions.1b1o94j"] == 1644

    check.usage_count = {"test.1b1o94j": [1619827200, 1000]}
    jobs, status = check.extract_pulsar_count_by_job("test", json.loads(PULSAR_RESULT_DECISIONS))
    assert jobs["test.1b1o94j"] == 644

    check.usage_count = {"test.1b1o94j": [1619870400, 1000]}
    # should throw exception due to wrong data
    jobs, status = check.extract_pulsar_count_by_job("test", json.loads(USAGE_RESULT))
    assert status is False


def test_extractPulsarResponseTime(aggregator, instance_1):
    check = Ns1Check('ns1', {}, [instance_1])

    rtime, status = check.extract_pulsar_response_time(json.loads(PULSAR_RESULT_PERFORMANCE))
    assert rtime == 46.605
    assert status

    rtime, status = check.extract_metric("pulsar.performance", json.loads(PULSAR_RESULT_PERFORMANCE))
    assert rtime == 46.605
    assert status


def test_extract_qps(aggregator, instance_1):
    check = Ns1Check('ns1', {}, [instance_1])
    qps_result = """
    {
        "qps": 0.025
    }
    """
    qps, status = check.extract_metric("qps", json.loads(qps_result))
    assert qps == 0.025
    assert status


def test_extract_peak_lps(aggregator, instance_1):
    check = Ns1Check('ns1', {}, [instance_1])
    lsp_result = """
    [
        {
            "graph": [
            [
                1600171200,
                4
            ],
            [
                1600173000,
                1
            ]
            ],
            "period": "24h",
            "aggregation": "peak"
        }
    ]
    """
    lps, status = check.extract_peak_lps(json.loads(lsp_result))
    assert lps == 1
    assert status
    lps, status = check.extract_metric("peak_lps", json.loads(lsp_result))
    assert lps == 1
    assert status


def test_extract_records_ttl(aggregator, instance_1):
    check = Ns1Check('ns1', {}, [instance_1])
    zone_result = """
    {
        "nx_ttl": 3600,
        "retry": 7200,
        "zone": "dloc.com",
        "dnssec": false,
        "network_pools": [
            "p07"
        ],
        "serial": 1620336094,
        "primary": {
            "enabled": false,
            "secondaries": []
        },
        "refresh": 43200,
        "expiry": 1209600,
        "disabled": false,
        "records": [
            {
                "domain": "dloc.com",
                "ttl": 3600,
                "tier": 1,
                "type": "NS",
                "id": "60663db6c44e5500b9d9ec02",
                "short_answers": [
                    "dns1.p07.nsone.net",
                    "dns2.p07.nsone.net",
                    "dns3.p07.nsone.net",
                    "dns4.p07.nsone.net",
                    "dnstest01.p07.nsone.net"
                ]
            },
            {
                "domain": "email.dloc.com",
                "ttl": 3600,
                "tier": 1,
                "type": "A",
                "id": "6086eee91e2d0a00b464c2ec",
                "short_answers": [
                    "3.3.3.3"
                ]
            },
            {
                "domain": "www.dloc.com",
                "ttl": 3600,
                "tier": 3,
                "type": "A",
                "id": "60663de2a4ab1700b1cb826e",
                "short_answers": [
                    "104.26.3.224",
                    "172.67.70.52",
                    "104.26.2.224"
                ]
            }
        ],
        "link": null,
        "primary_master": "dns1.p07.nsone.net",
        "ttl": 3600,
        "id": "60663db6c44e5500b9d9ebfd",
        "dns_servers": [
            "dns1.p07.nsone.net",
            "dns2.p07.nsone.net",
            "dns3.p07.nsone.net",
            "dns4.p07.nsone.net"
        ],
        "hostmaster": "hostmaster@nsone.net",
        "networks": [
            0
        ],
        "pool": "p07"
    }
    """
    zonettl, status = check.extract_records_ttl(json.loads(zone_result))
    assert zonettl["dloc.com"] == 3600
    assert status
    zonettl, status = check.extract_metric("ttl", json.loads(zone_result))
    assert zonettl["dloc.com"] == 3600
    assert status


def test_extract_billing(aggregator, instance_1):
    check = Ns1Check('ns1', {}, [instance_1])
    billing_result = """
    {
        "last_invoice": 1620086400,
        "dynamic": {
            "access_charge": "0.0",
            "records": 0,
            "query_credit": 0,
            "query_cost": "0.00",
            "query_rate_per_million": "0",
            "queries": 0,
            "record_credit": 0,
            "record_cost": "0.00",
            "record_rate": "0"
        },
        "period": "monthly",
        "next_invoice": 1622764800,
        "static": {
            "access_charge": "0.0",
            "records": 30,
            "query_credit": 8,
            "query_cost": "8.07",
            "query_rate_per_million": "8",
            "queries": 1509129,
            "record_credit": 0,
            "record_cost": "0.00",
            "record_rate": "0"
        },
        "plan": "starter",
        "next_base_invoice": 1622764800,
        "recurring_cost": "0.00",
        "any": {
            "record_credit": 50,
            "query_credit": 500000,
            "overage_order": "ascending"
        },
        "bill": "20.87",
        "recurring_cost_next_invoice": "0.00",
        "totals": {
            "query_cost": "8.07",
            "access_charge": "0.00",
            "records": 31,
            "query_credit": 500000,
            "queries": 1509129,
            "record_credit": 31,
            "record_cost": "0.00"
        },
        "balance": 12.8,
        "intelligent": {
            "access_charge": "0.0",
            "records": 1,
            "query_credit": 0,
            "query_cost": "0.00",
            "query_rate_per_million": "0",
            "queries": 0,
            "record_credit": 0,
            "record_cost": "0.00",
            "record_rate": "0"
        }
    }
    """
    billing, status = check.extract_billing(json.loads(billing_result))
    assert billing["usage"] == 1509129
    assert billing["limit"] == 500000
    assert status
    billing, status = check.extract_metric("billing", json.loads(billing_result))
    assert billing["usage"] == 1509129
    assert billing["limit"] == 500000
    assert status


def test_extractPulsarAvailabilityPercent(aggregator, instance_1):
    check = Ns1Check('ns1', {}, [instance_1])
    up_percent, status = check.extract_pulsar_availability(json.loads(PULSAR_RESULT_AVAILABILITY))
    assert up_percent == 0.975
    assert status
    up_percent, status = check.extract_metric("pulsar.availability", json.loads(PULSAR_RESULT_AVAILABILITY))
    assert up_percent == 0.975
    assert status


def test_read_prev_usage_count(aggregator, instance_1):
    check = Ns1Check('ns1', {}, [instance_1])
    check.usage_count_path = "./log"
    check.usage_count_fname = 'ns1_usage_count.txt'
    check.get_usage_count()
    assert check.usage_count["usage"] == [0, 0]


def test_remove_prefix(aggregator, instance_1):
    check = Ns1Check('ns1', {}, [instance_1])
    assert check.remove_prefix("prefix_text", "prefix_") == "text"
    assert check.remove_prefix("text", "noprefix_") == "text"
