# from typing import Any
import errno
import json
import os

from requests.exceptions import ConnectionError, HTTPError, InvalidURL, Timeout

from datadog_checks.base import AgentCheck, ConfigurationError


class Ns1Check(AgentCheck):
    NS1_SERVICE_CHECK = "ns1.can_connect"

    # def __init__(self, name, init_config, instances):
    #     super(Ns1Check, self).__init__(name, init_config, instances)
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
    def checkConfig(self):
        self.api_endpoint = self.instance.get("api_endpoint")
        if not self.api_endpoint:
            raise ConfigurationError('NS1 API endpoint must be specified in configuration')
        self.api_key = self.instance.get("api_key")
        if not self.api_key:
            raise ConfigurationError('NS1 API key must be specified in configuration')
        self.headers = {"X-NSONE-Key": self.api_key}

        self.metrics = self.instance.get("metrics")
        if not self.metrics or len(self.metrics) == 0:
            raise ConfigurationError('Invalid metrics config!')

        self.usage_count_path = "/opt/datadog-agent/log"
        self.usage_count_fname = 'ns1_usage_count.txt'

    def check(self, instance):
        # Use self.instance to read the check configuration
        self.checkConfig()
        self.getUsageCount()

        # create URLs to query API for all configured metrics
        checkUrl = self.createUrl(self.metrics)

        for k, v in checkUrl.items():
            try:
                url = v[0]
                name = v[1]
                tags = v[2]
                # Query API to get metrics
                res = self.getStats(url)
                if res:
                    # extract metric from API result
                    val = self.extractMetric(k, res)

                    # send metric to datadog
                    # self.sendMetrics(k, val)
                    self.sendMetrics(name, val, tags)
            except Exception:
                raise
        self.setUsageCount()

    def getUsageCount(self):

        try:
            os.makedirs(self.usage_count_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        fullname = os.path.join(self.usage_count_path, self.usage_count_fname)

        self.usage_count = {"usage": [0, 0]}
        if os.path.isfile(fullname):
            with open(fullname, 'r+') as f:
                self.usage_count = json.load(f)
        else:
            with open(fullname, 'w+') as f:
                json.dump(self.usage_count, f)

    def setUsageCount(self):

        fullname = '/opt/datadog-agent/log/ns1_usage_count.txt'

        if os.path.isfile(fullname):
            with open(fullname, 'w+') as f:
                json.dump(self.usage_count, f)

    def createUrl(self, metrics):
        # create dictionary with metrics name and url to check for all configured metrics in conf.yaml file
        checkUrl = {}
        for key, val in metrics.items():
            if key == "qps":
                checkUrl.update(self.getStatsUrl(key, val))
            elif key == "usage":
                checkUrl.update(self.getStatsUrl(key, val))
            # elif key == "account":
            #     checkUrl.update(self.getZoneInfoUrl(key, val))
            #     checkUrl.update(self.getPlanDetailsUrl(key, val))
            # elif key == "pulsar_by_app":
            #     checkUrl.update(self.getPulsarAppUrl(key, val))
            # elif key == "pulsar_by_record":
            #     checkUrl.update(self.getPulsarRecordUrl(key, val))

        return checkUrl

    def extractMetric(self, key, result):
        # Various NS1 APis are returning different data structures, extract values depending on which API was called
        try:
            if "qps" in key:
                qps = result["qps"]
                return qps
            elif "usage" in key:
                # result[0]["queries"]
                queries = self.extractUsageCount(key, result)
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

    def extractUsageCount(self, key, jsonResult):
        graph = jsonResult[0]["graph"]
        # usage api will return array of dictionaries, we want to get 'graph' object
        # which in turh is list of lists, each element being [timestamp, query_count]
        # so, get last query count from result. Sort by timestamp descending order to make sure we get latest
        res = sorted(graph, key=lambda x: x[0], reverse=True)
        print(res)
        curr_timestamp = res[0][0]
        curr_count = res[0][1]
        # find this metric in usage count
        if key in self.usage_count:
            prev_timestamp = self.usage_count[key][0]
            prev_count = self.usage_count[key][1]
            if curr_timestamp == prev_timestamp:
                self.usage_count[key] = [prev_timestamp, curr_count]
                return curr_count - prev_count
            else:
                self.usage_count[key] = [curr_timestamp, curr_count]
                return curr_count
        else:
            self.usage_count[key] = [curr_timestamp, curr_count]
            return curr_count

    def extractRecordsTtl(self, jsonResult):
        zoneTtl = {}
        for zone in jsonResult["records"]:
            zoneTtl[zone["domain"]] = zone["ttl"]
        return zoneTtl

    # generate url for QPS and usages statistics
    # returns dictionary in form of <metric name>:<metric url>}
    def getStatsUrl(self, key, val):
        urlList = {}

        if key == "usage":
            query_string = "?period=1h&expand=false&networks=*"
            metric_name = "usage"
            metric_zone = "usage.zone"
            metric_record = "usage.record"
        else:
            query_string = ""
            metric_name = "qps"
            metric_zone = "qps.zone"
            metric_record = "qps.record"

        # first get account wide stats
        url = "{apiendpoint}/v1/stats/{key}{suffix}".format(apiendpoint=self.api_endpoint, key=key, suffix=query_string)
        # tags=["env:dev","metric_submission_type:count"]
        tags = ["network:*"]
        urlList[key] = [url, metric_name, tags]

        if val:
            for zoneDict in val:
                # zone is again dictionary, with zone name as key and records as list of objects
                # metric_name=metric_name + ".zone"
                for domain, records in zoneDict.items():
                    # here, domain is zone name, records is list of records and record types
                    url = "{apiendpoint}/v1/stats/{key}/{domain}{suffix}".format(
                        apiendpoint=self.api_endpoint, key=key, domain=domain, suffix=query_string
                    )
                    tags = ["network:*", "zone:{zone}".format(zone=domain)]
                    urlList["{key}.{domain}".format(key=key, domain=domain)] = [url, metric_zone, tags]

                    if records:
                        # metric_name=metric_name + ".record"
                        for rec in records:
                            for r, t in rec.items():
                                url = "{apiendpoint}/v1/stats/{key}/{domain}/{record}/{rectype}{suffix}".format(
                                    apiendpoint=self.api_endpoint,
                                    key=key,
                                    domain=domain,
                                    record=r + "." + domain,
                                    rectype=t,
                                    suffix=query_string,
                                )
                                tags = [
                                    "network:*",
                                    "zone:{zone}".format(zone=domain),
                                    "record:{record}".format(record=r),
                                ]
                                urlkey = "{key}.{domain}.{record}.{rectype}".format(
                                    key=key, domain=domain, record=r, rectype=t
                                )
                                urlList[urlkey] = [url, metric_record, tags]
        return urlList

    def getZoneInfoUrl(self, key, val):
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

    def getPlanDetailsUrl(self, key, val):
        urlList = {}

        # just get account plan limits
        url = "{apiendpoint}/v1/account/plan".format(apiendpoint=self.api_endpoint)
        urlList["{key}.plan".format(key=key)] = url

        return urlList

    def getPulsarAppUrl(self, key, val):

        urlList = {}

        # pulsar aggregate performance data
        # https://{{api_url}}/v1/pulsar/apps/{{pulsar_app_id}}/jobs/{{pulsar_job_id}}/data?period=30s
        url = "{apiendpoint}/v1/pulsar/apps/{pulsar_app_id}/jobs/{pulsar_job_id}/data".format(
            apiendpoint=self.api_endpoint, pulsar_app_id=0, pulsar_job_id=0
        )
        # pulsar availability data
        # https://{{api_url}}/v1/pulsar/apps/{{pulsar_app_id}}/jobs/{{pulsar_job_id}}/availability?period=3s&agg=p50&expand=true
        url = "{apiendpoint}/v1/pulsar/apps/{pulsar_app_id}/jobs/{pulsar_job_id}/availability".format(
            apiendpoint=self.api_endpoint, pulsar_app_id=0, pulsar_job_id=0
        )

        # pulsar decisions account wide
        # https://{{api_url}}/v1/pulsar/query/decision/customer?period=3d
        url = "{apiendpoint}/v1/pulsar/query/decision/customer".format(apiendpoint=self.api_endpoint)

        # pulsar insufficient decision data for account
        # https://{{api_url}}/v1/pulsar/query/decision/customer/undetermined?period=3d
        url = "{apiendpoint}/v1/pulsar/query/decision/customer/undetermined".format(apiendpoint=self.api_endpoint)

        # pulsar decisions for record
        # https://{{api_url}}/v1/pulsar/query/decision/record/{{record_name}}/{{record_type}}?period=30d
        url = "{apiendpoint}/v1/pulsar/query/decision/record/{pulsar_record}/{record_type}".format(
            apiendpoint=self.api_endpoint, pulsar_record=0, record_type=0
        )

        # pulsar all route maps
        # https://{{api_url}}/v1/pulsar/query/routemap/hit/customer?period=30d
        url = "{apiendpoint}/v1/pulsar/query/routemap/hit/customer".format(apiendpoint=self.api_endpoint)

        # View route map misses by record
        # https://{{api_url}}/v1/pulsar/query/routemap/miss/record/{{record_name}}/{{record_type}}?period=30d
        url = "{apiendpoint}/v1/pulsar/query/routemap/miss/record/{record_name}/{record_type}".format(
            apiendpoint=self.api_endpoint, record_name=0, record_type=0
        )

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

    def sendMetrics(self, metricName, metricValue, tags):
        if isinstance(metricValue, dict):
            for k, v in metricValue.items():
                # urlList["{key}.zones.{domain}"] = url
                # zoneTtl[zone["domain"]] = zone["ttl"]
                self.gauge('ns1.{name}.{record}'.format(name=metricName, record=k), v)
        else:
            self.gauge('ns1.{}'.format(metricName), metricValue, tags)
