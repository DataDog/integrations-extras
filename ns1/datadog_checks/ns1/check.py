# from typing import Any
from datadog_checks.base import AgentCheck, ConfigurationError
from requests.exceptions import ConnectionError, HTTPError, InvalidURL, Timeout
import json


class Ns1Check(AgentCheck):
    NS1_SERVICE_CHECK = "ns1.can_connect"

    # def __init__(self, name, init_config, instances):
    # super(Ns1Check, self).__init__(name, init_config, instances)

    # If the check is going to perform SQL queries you should define a query manager here.
    # More info at
    # https://datadoghq.dev/integrations-core/base/databases/#datadog_checks.base.utils.db.core.QueryManager
    # sample_query = {
    #     "name": "sample",
    #     "query": "SELECT * FROM sample_table",
    #     "columns": [
    #         {"name": "metric", "type": "gauge"}
    #     ],
    # }
    # self._query_manager = QueryManager(self, self.execute_query, queries=[sample_query])
    # self.check_initializations.append(self._query_manager.compile_queries)

    # pass

    def check(self, instance):
        # Use self.instance to read the check configuration

        self.api_endpoint = self.instance.get("api_endpoint")
        if not self.api_endpoint:
            raise ConfigurationError('NS1 API endpoint must be sepcified in configuration')
        self.api_key = self.instance.get("api_key")
        self.headers = {"X-NSONE-Key": self.api_key}

        metrics = self.instance.get("metrics")
        if len(metrics) == 0 or len(metrics) < 4:
            raise ConfigurationError('Invalid metrics config!')

        checkUrl = {}
        for key, val in metrics.items():
            if key == "qps":
                checkUrl.update(self.getStatsUrl(key, val))  # append dictionary
            elif key == "usage":
                checkUrl.update(self.getStatsUrl(key, val))  # append dictionary
            elif key == "account":
                checkUrl.update(self.getZonesUrl(key, val))  # append dictionary
                checkUrl.update(self.getPlanUrl(key, val))  # append dictionary
            elif key == "pulsar_by_app":
                checkUrl.update(self.getPulsarAppUrl(key, val))  # append dictionary
            elif key == "pulsar_by_record":
                checkUrl.update(self.getPulsarRecordUrl(key, val))  # append dictionary

        # QPS and Usage stats
        for k, v in checkUrl.items():
            # for u in checkUrl:
            try:
                res = self.getStats(v)
                if res:
                    val = self.extractMetric(k, res)
                else:
                    # should maybe throw exception?
                    val = 0.0
                self.sendMetrics(k, val)
            except Exception:
                raise

        # account limits and zone info
        accUrl = {}
        for key, val in metrics.items():
            if key == "account":
                accUrl.update(self.getZonesUrl(key, val))  # append dictionary
                accUrl.update(self.getPlanUrl(key, val))  # append dictionary
        # pulsar
        # DDI

        # If your check ran successfully, you can send the status.
        # More info at
        # https://datadoghq.dev/integrations-core/base/api/#datadog_checks.base.checks.base.AgentCheck.service_check
        # self.service_check("ns1.can_connect", AgentCheck.OK)

        # pass

    def extractMetric(self, key, result):
        # APis are returning different data structures, extract values depending on which API was called
        try:
            if "qps" in key:
                qps = result["qps"]
                return qps
            elif "usage" in key:
                queries = result[0]["queries"]
                return queries
            elif "plan" in key:
                queries = result["included"]["any"]["queries"]
                return queries
            elif "zones" in key:
                zonesTtl = self.extractRecordsTtl(result)
                return zonesTtl
            elif "pulsar_by_app" in key:
                queries = result[0]["queries"]
                return queries
            elif "ddi" in key:
                queries = result[0]["queries"]
                return queries
        except Exception:
            raise
            # return None

    def extractRecordsTtl(self, jsonResult):
        zoneTtl = {}
        for zone in jsonResult["records"]:
            zoneTtl[zone["domain"]] = zone["ttl"]
        return zoneTtl

    def getStatsUrl(self, key, val):
        urlList = {}  # dictionary in form of <metric name>:<metric url>}
        suffix = ""
        if key == "qps":
            suffix = ""
        elif key == "usage":
            suffix = "?period=1h&expand=false&networks=*"
        elif key == "pulsar":
            suffix = ""
        elif key == "ddi":
            suffix = ""

        # just get account wide stats
        # url = "%s/v1/stats/%s%s" % (self.api_endpoint, key, suffix)
        url = "{apiendpoint}/v1/stats/{key}{suffix}".format(apiendpoint=self.api_endpoint, key=key, suffix=suffix)
        urlList[key] = url

        if val:
            for zoneDict in val:
                # zone is again dictionary, with zone name as key and records as list of objects
                for domain, records in zoneDict.items():
                    # here, domain is zone name, records is list of records and record types
                    # url = "%s/v1/stats/%s/%s%s" % (self.api_endpoint, key, domain, suffix)
                    url = "{apiendpoint}/v1/stats/{key}/{domain}{suffix}".format(
                        apiendpoint=self.api_endpoint, key=key, domain=domain, suffix=suffix
                    )
                    # urlList["%s.%s" % (key, domain)] = url
                    urlList["{key}.{domain}".format(key=key, domain=domain)] = url

                    if records:
                        for rec in records:
                            for r, t in rec.items():
                                url = "{apiendpoint}/v1/stats/{key}/{domain}/{record}/{rectype}{suffix}".format(
                                    apiendpoint=self.api_endpoint,
                                    key=key,
                                    domain=domain,
                                    record=r + "." + domain,
                                    rectype=t,
                                    suffix=suffix,
                                )
                                urlkey = "{key}.{domain}.{record}.{rectype}".format(
                                    key=key, domain=domain, record=r, rectype=t
                                )
                                urlList[urlkey] = url
        return urlList

    def getZonesUrl(self, key, val):
        urlList = {}  # dictionary in form of <metric name>:<metric url>}

        if val:
            for accDict in val:
                # account section is dictionary, with 2 entries: 'plan' and 'zones'. zones object is list of zones
                for _, domainList in accDict.items():
                    # here, zones object contains list of zones
                    # if there is no list of objects, then ignore, that is 'plan' entry
                    if domainList:
                        for domain in domainList:
                            url = "{apiendpoint}/v1/zones/{domain}".format(apiendpoint=self.api_endpoint, domain=domain)
                            urlList["{key}.zones.{domain}".format(key=key, domain=domain)] = url
        return urlList

    def getPlanUrl(self, key, val):
        urlList = {}  # dictionary in form of <metric name>:<metric url>}

        # just get account plan limits
        url = "{apiendpoint}/v1/account/plan".format(apiendpoint=self.api_endpoint)
        urlList["{key}.plan".format(key=key)] = url

        return urlList

    def getPulsarAppUrl(self, key, val):

        urlList = {}  # dictionary in form of <metric name>:<metric url>}

        # just get account plan limits
        url = "{apiendpoint}/v1/account/plan".format(apiendpoint=self.api_endpoint)
        urlList["{key}.plan".format(key=key)] = url

        return urlList

    def getPulsarRecordUrl(self, key, val):

        urlList = {}  # dictionary in form of <metric name>:<metric url>}

        # just get account plan limits
        url = "{apiendpoint}/v1/account/plan".format(apiendpoint=self.api_endpoint)
        urlList["{key}.plan".format(key=key)] = url

        return urlList

    def _build_stats_url(self, querytype, url):

        if querytype == "qps":
            return "%s/v1/stats/%s" % (self.api_endpoint, url)
        elif querytype == "usage":
            # usage account wide
            return "%s/v1/stats/%s?period=1h&expand=true&networks=*" % (self.api_endpoint, url)
            # https://{{api_url}}/v1/stats/usage?period=24h&expand=true&networks=*
        elif querytype == "pulsar":
            # usage account wide
            return "%s/v1/stats/%s?period=1h&expand=true&networks=*" % (self.api_endpoint, url)
            # https://{{api_url}}/v1/pulsar/apps/{{pulsar_app_id}}/jobs/{{pulsar_job_id}}/data?period=1h&agg=p50
        elif querytype == "account":
            # Account plan details
            # https://{{api_url}}/v1/account/plan
            return "%s/v1/account/plan" % (self.api_endpoint)

            # Account zone details
            # https://{{api_url}}/v1/zones/{{zone_name}}

    def getStats(self, url):
        # Perform HTTP Requests with our HTTP wrapper.
        # More info at https://datadoghq.dev/integrations-core/base/http/
        try:
            # response = self.http.get(self._build_url(url), headers=self.headers)
            response = self.http.get(url, headers=self.headers)
            response.raise_for_status()
            response_json = response.json()

            return response_json

        except Timeout as e:
            self.service_check(
                self.NS1_SERVICE_CHECK,
                AgentCheck.CRITICAL,
                message="Request timeout: {}, {}".format(url, e),
            )
            raise

        except (HTTPError, InvalidURL, ConnectionError) as e:
            self.service_check(
                self.NS1_SERVICE_CHECK,
                AgentCheck.CRITICAL,
                message="Request failed: {}, {}".format(url, e),
            )
            raise

        except json.JSONDecodeError as e:
            self.service_check(
                self.NS1_SERVICE_CHECK,
                AgentCheck.CRITICAL,
                message="JSON Parse failed: {}, {}".format(url, e),
            )
            raise

        except ValueError as e:
            self.service_check(self.NS1_SERVICE_CHECK, AgentCheck.CRITICAL, message=str(e))
            raise
        except Exception:
            self.service_check(self.NS1_SERVICE_CHECK, AgentCheck.CRITICAL, message="Error getting stats frmo NS1 DNS")
            raise

    def sendMetrics(self, metricName, metricValue):
        if isinstance(metricValue, dict):
            for k, v in metricValue.items():
                # urlList["{key}.zones.{domain}"] = url
                # zoneTtl[zone["domain"]] = zone["ttl"]
                self.gauge('ns1.{name}.{record}'.format(name=metricName, record=k), v)
        else:
            self.gauge('ns1.{}'.format(metricName), metricValue)
