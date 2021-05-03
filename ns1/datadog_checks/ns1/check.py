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
        # Use self.instance to read the check configuration
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

        self.query_params = self.instance.get("query_params")
        self.usage_count_path = "/opt/datadog-agent/log"
        self.usage_count_fname = 'ns1_usage_count.txt'

    def getPulsarApplications(self):
        url = "{apiendpoint}/v1/pulsar/apps".format(apiendpoint=self.api_endpoint)
        res = self.getStats(url)
        apps = {}
        for app in res:
            url = url + "/{app_id}/jobs".format(app_id=app["appid"])
            jobs = self.getStats(url)
            apps[app["appid"]] = [app["name"], jobs]
        return apps

    def check(self, instance):

        self.checkConfig()

        # get counters from previous run
        self.getUsageCount()

        # create URLs to query API for all configured metrics
        checkUrl = self.createUrl(self.metrics, self.query_params)

        for k, v in checkUrl.items():
            try:
                url, name, tags, metric_type = v
                # Query API to get metrics
                res = self.getStats(url)
                if res:
                    # extract metric from API result.
                    val, status = self.extractMetric(k, res)

                    # send metric to datadog if extraction was sucessful
                    if status:
                        self.sendMetrics(name, val, tags, metric_type)

            except Exception:
                raise
        # save counters for next run
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

    def createUrl(self, metrics, query_params):
        # create dictionary with metrics name and url to check for all configured metrics in conf.yaml file
        checkUrl = {}

        for key, val in metrics.items():
            if key == "qps":
                checkUrl.update(self.getStatsUrl(key, val, query_params))
            elif key == "usage":
                checkUrl.update(self.getStatsUrl(key, val, query_params))
            elif key == "account":
                checkUrl.update(self.getZoneInfoUrl(key, val))
                checkUrl.update(self.getPlanDetailsUrl(key, val))
            # elif key == "ddi":
            #     checkUrl.update(self.getDdiUrl(key, val))
            elif key == "pulsar":
                checkUrl.update(self.getPulsarAppUrl(key, val, query_params, None))
            elif key == "pulsar_by_app":
                self.pulsar_apps = self.getPulsarApplications()
                checkUrl.update(self.getPulsarAppUrl(key, val, query_params, self.pulsar_apps))
            elif key == "pulsar_by_record":
                checkUrl.update(self.getPulsarAppUrl(key, val, query_params, None))

        return checkUrl

    def extractMetric(self, key, result):
        # Various NS1 APis are returning different data structures, extract values depending on which API was called
        try:
            if "qps" in key:
                res = result["qps"]
                status = True
            elif "usage" in key:
                # result[0]["queries"]
                res, status = self.extractUsageCount(key, result)
            elif "billing" in key:
                res, status = self.extractBilling(result)
            elif "ttl" in key:
                res, status = self.extractRecordsTtl(result)
            elif "pulsar.performance" in key:
                res, status = self.extractPulsarResponseTime(result)
            elif "pulsar.availability" in key:
                res, status = self.extractPulsarAvailability(result)
            elif "pulsar" in key:
                res, status = self.extractPulsarCount(key, result)
            elif "ddi" in key:
                res, status = result[0]["queries"]
                status = True

            return res, status
        except Exception:
            return None, False
            # raise

    def extractPulsarCount(self, key, jsonResult):
        try:
            graphs = jsonResult["graphs"]
            # this is called for each url in checkUrl dictionary
            # get last timestamp and count from self.usage_count
            # make sure decisions are queried with period of 2d in order to get sumarry per 12 hours,
            # so then we can just take last bucket and check count
            curr_timestamp = 0
            curr_count = 0

            # sum count for all elements in array, make sure last time stamp is the same
            # if timestamp is not the same, skip this submission, it's right at the time 
            # buckets are being closed so reporting might be off for a few seconds, 
            # will pick it up on next run
            index = 0
            for element in graphs:
                graph = element["graph"]
                # sort graph array
                # find last timestamp that is >= last time stamp saved in file
                res = sorted(graph, key=lambda x: x[0], reverse=True)
                if res and len(res) > 0:
                    if index == 0:
                        # get timestamp fropm first element to compare with others
                        curr_timestamp = res[0][0]
                        index = -1

                    if curr_timestamp != res[0][0]:
                        # last timestamps in elements are different, we'll just skip submitting this value
                        # and wait for all buckets to come to the same timestamp as otherwise numbers get messed up
                        # just bail out
                        return None, False

                    # result is split accross pulsar jobs, we need sum for all jobs, so sum last count from all arrays
                    curr_count = curr_count + res[0][1]

            # find this metric in usage count
            if key in self.usage_count:
                prev_timestamp = self.usage_count[key][0]
                prev_count = self.usage_count[key][1]
                if curr_timestamp == prev_timestamp:
                    self.usage_count[key] = [prev_timestamp, curr_count]
                    result = curr_count - prev_count
                else:
                    self.usage_count[key] = [curr_timestamp, curr_count]
                    result = curr_count
            else:
                self.usage_count[key] = [curr_timestamp, curr_count]
                result = curr_count

            return result, True
        except Exception:
            return None, False

    def extractPulsarResponseTime(self, jsonResult):
        try:
            geo = "*"
            asn = "*"
            if self.query_params:
                if "pulsar_geo" in self.query_params:
                    geo = self.query_params["pulsar_geo"]
                if "pulsar_asn" in self.query_params:
                    asn = self.query_params["pulsar_asn"]

            graph = jsonResult["graph"]
            data = graph[geo][asn]
            res = sorted(data, key=lambda x: x[0], reverse=True)
            response_time = res[0][1]
            return response_time, True
        except Exception:
            return None, False

    def extractPulsarAvailability(self, jsonResult):
        try:
            graphs = jsonResult["graphs"]
            index = 0
            for element in graphs:
                graph = element["graph"]
                # sort graph array
                # find last timestamp that is >= last time stamp saved in file
                res = sorted(graph, key=lambda x: x[0], reverse=True)
                if res and len(res) > 0:
                    percent_available = res[0][1]
                    return percent_available, True
                else:
                    return None, False
        except Exception:
            return None, False

    def extractUsageCount(self, key, jsonResult):

        try:
            graph = jsonResult[0]["graph"]
            # usage api will return array of dictionaries, we want to get 'graph' object
            # which in turn is list of lists, each element being [timestamp, query_count]
            # so, get last query count from result. Sort by timestamp descending order to make sure we get latest
            res = sorted(graph, key=lambda x: x[0], reverse=True)

            curr_timestamp = res[0][0]
            curr_count = res[0][1]
            # find this metric in usage count
            if key in self.usage_count:
                prev_timestamp = self.usage_count[key][0]
                prev_count = self.usage_count[key][1]
                if curr_timestamp == prev_timestamp:
                    self.usage_count[key] = [prev_timestamp, curr_count]
                    result = curr_count - prev_count
                else:
                    self.usage_count[key] = [curr_timestamp, curr_count]
                    result = curr_count
            else:
                self.usage_count[key] = [curr_timestamp, curr_count]
                result = curr_count

            return result, True
        except Exception:
            return None, False

    def extractRecordsTtl(self, jsonResult):
        try:
            zoneTtl = {}
            for zone in jsonResult["records"]:
                zoneTtl[zone["domain"]] = zone["ttl"]
            return zoneTtl, True
        except Exception:
            return None, False

    def extractBilling(self, jsonResult):
        try:

            billing = {}
            billing["usage"] = jsonResult["totals"]["queries"]
            billing["limit"] = jsonResult["totals"]["query_credit"]
            return billing, True
        except Exception:
            return None, False

    # generate url for QPS and usages statistics
    # returns dictionary in form of <metric name>:<metric url>}
    def getStatsUrl(self, key, val, query_params):
        urlList = {}

        if key == "usage":
            network_id = "*"
            if query_params and "usage_networks" in query_params:
                network_id = query_params["usage_networks"]
            query_string = "?period=1h&expand=false&networks={networks}".format(networks=network_id)
            metric_name = "usage"
            metric_zone = "usage.zone"
            metric_record = "usage.record"
            metric_type = "count"
        else:
            query_string = ""
            metric_name = "qps"
            metric_zone = "qps.zone"
            metric_record = "qps.record"
            metric_type = "gauge"

        # first get account wide stats
        url = "{apiendpoint}/v1/stats/{key}{query}".format(apiendpoint=self.api_endpoint, key=key, query=query_string)
        # tags=["env:dev","metric_submission_type:count"]
        tags = [""]
        urlList[key] = [url, metric_name, tags, metric_type]

        if val:
            for zoneDict in val:
                # zone is again dictionary, with zone name as key and records as list of objects
                # metric_name=metric_name + ".zone"
                for domain, records in zoneDict.items():
                    # here, domain is zone name, records is list of records and record types
                    url = "{apiendpoint}/v1/stats/{key}/{domain}{query}".format(
                        apiendpoint=self.api_endpoint, key=key, domain=domain, query=query_string
                    )
                    if key == "usage":
                        tags = ["network:{network}".format(network=network_id), "zone:{zone}".format(zone=domain)]
                    else:
                        tags = ["zone:{zone}".format(zone=domain)]
                    urlList["{key}.{domain}".format(key=key, domain=domain)] = [url, metric_zone, tags, metric_type]

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
                                    "record:{record}.{zone}".format(record=r, zone=domain),
                                ]
                                urlkey = "{key}.{domain}.{record}.{rectype}".format(
                                    key=key, domain=domain, record=r, rectype=t
                                )
                                urlList[urlkey] = [url, metric_record, tags, metric_type]
        return urlList

    # generate url for DDI
    # returns dictionary in form of <metric name>:<metric url>}
    def getDdiUrl(self, key, val):
        urlList = {}
        metric_lease = "leases"
        metric_lps = "lps"
        metric_type_count = "gauge"
        metric_type_gauge = "gauge"
        # first get account lease stats
        # https://{{api_url}}/v1/stats/leases?period=24h
        # Returns the sum of all leases - new and renewals - for the entire account
        # Period parameter supported values: 24h (default) or 30d

        # View lease statistics by scope group
        # https://{{api_url}}/v1/stats/leases/{{scope_group_ID}}?period=24h
        # Period parameter supported values: 24h (default) or 30d

        # View account-wide peak LPS
        # https://localhost/v1/stats/lps?period=24h
        # Returns current leases per second (LPS) for all scope groups. Optionally,
        # you can specify a period of time by which to filter results.
        # Peak LPS is the maximum number of average leases calculated at 30-minute intervals
        # in a 24-hour period and at 12-hour intervals in a 30-day period.
        # 90th percentile markers: shows 90% of the time, the usage is below this amount
        # 95th percentile markers: shows 95% of the time, the usage is below this amount
        # Period parameter supported values: 24h (default) or 30d

        # View peak LPS by scope group
        # within the specified time range.
        # https://{{api_url}}/v1/stats/lps/{{scope_group_ID}}?period=24h
        # Period parameter supported values: 24h (default) or 30d

        tags = [""]
        url = "{apiendpoint}/v1/stats/leases?period=24h".format(apiendpoint=self.api_endpoint)
        urlList["leases"] = [url, metric_lease, tags, metric_type_count]

        url = "{apiendpoint}/v1/stats/lps?period=24h".format(apiendpoint=self.api_endpoint)
        urlList["lps"] = [url, metric_lps, tags, metric_type_gauge]

        if val:
            for scope in val:
                # here, domain is zone name, records is list of records and record types
                url = "{apiendpoint}/v1/stats/leases/{scope_group_id}?period=24h".format(
                    apiendpoint=self.api_endpoint, scope_group_id=scope
                )
                tags = ["scope_group:{scope_group_id}".format(scope_group_id=scope)]
                urlList["leases.{scope_group_id}".format(scope_group_id=scope)] = [
                    url,
                    metric_lease,
                    tags,
                    metric_type_count,
                ]
                url = "{apiendpoint}/v1/stats/lps/{scope_group_id}?period=24h".format(
                    apiendpoint=self.api_endpoint, scope_group_id=scope
                )
                urlList["lps.{scope_group_id}".format(scope_group_id=scope)] = [
                    url,
                    metric_lps,
                    tags,
                    metric_type_gauge,
                ]

        return urlList

    def getZoneInfoUrl(self, key, val):
        urlList = {}  # dictionary in form of <metric name>:<metric url>}

        if val:
            for accDict in val:
                # account section is dictionary, with 2 entries: 'plan' and 'zones'. zones object is list of zones
                for _, domainList in accDict.items():
                    # here, zones object contains list of zones
                    # if there is no list of objects, then ignore, that is 'plan' entry
                    metric_record = "ttl"
                    metric_type = "gauge"
                    if domainList:
                        for domain in domainList:
                            tags = ["record:{zone}".format(zone=domain)]
                            url = "{apiendpoint}/v1/zones/{domain}".format(apiendpoint=self.api_endpoint, domain=domain)
                            urlList["{key}.ttl.{domain}".format(key=key, domain=domain)] = [
                                url,
                                metric_record,
                                tags,
                                metric_type,
                            ]
        return urlList

    def getPlanDetailsUrl(self, key, val):
        urlList = {}

        # just get account plan limits
        url = "{apiendpoint}/v1/account/billataglance".format(apiendpoint=self.api_endpoint)
        tags = [""]
        metric_record = "billing"
        metric_type = "gauge"
        urlList["{key}.billing".format(key=key)] = [url, metric_record, tags, metric_type]

        return urlList

    def getPulsarAppUrl(self, key, val, query_params, pulsar_apps):

        urlList = {}
        query_string = "?"
        if query_params:
            if "pulsar_period" in query_params:
                query_string = query_string + "period=" + query_params["pulsar_period"] + "&"
            if "pulsar_geo" in query_params:
                if query_params["pulsar_geo"] != "*":
                    query_string = query_string + "geo=" + query_params["pulsar_geo"] + "&"
            if "pulsar_asn" in query_params:
                if query_params["pulsar_asn"] != "*":
                    query_string = query_string + "asn=" + query_params["pulsar_asn"] + "&"
        query_string = query_string[:-1]

        # pulsar general account wide
        if key == "pulsar":
            query_string = "?"
            # for "pulsar" group of endpoints, override settings and always use period = 2d
            # to get properly sumarized stats
            query_string = query_string + "period=2d&"
            if query_params:
                if "pulsar_geo" in query_params:
                    query_string = query_string + "geo=" + query_params["pulsar_geo"] + "&"
                if "pulsar_asn" in query_params:
                    query_string = query_string + "asn=" + query_params["pulsar_asn"] + "&"
                # if "pulsar_agg" in query_params:
                #     query_string = query_string + "agg=" + query_params["pulsar_agg"] + "&"
            query_string = query_string[:-1]

            tags = [""]
            metric_record = "pulsar.decisions"
            metric_type = "count"

            # pulsar decisions account wide
            # url = "/v1/pulsar/query/decision/customer"
            urlpath = "/v1/pulsar/query/decision/customer"
            url = "{apiendpoint}{path}{query}".format(apiendpoint=self.api_endpoint, path=urlpath, query=query_string)
            urlList["pulsar.decisions"] = [url, metric_record, tags, metric_type]

            # pulsar insufficient decision data for account
            # url = "/v1/pulsar/query/decision/customer/undetermined"
            urlpath = "/v1/pulsar/query/decision/customer/undetermined"
            metric_record = "pulsar.decisions.insufficient"
            url = "{apiendpoint}{path}{query}".format(apiendpoint=self.api_endpoint, path=urlpath, query=query_string)
            urlList["pulsar.decisions.insufficient"] = [url, metric_record, tags, metric_type]

            # pulsar all route map hits
            # url = "/v1/pulsar/query/routemap/hit/customer"
            urlpath = "/v1/pulsar/query/routemap/hit/customer"
            metric_record = "pulsar.routemap.hit"
            url = "{apiendpoint}{path}{query}".format(apiendpoint=self.api_endpoint, path=urlpath, query=query_string)
            urlList["pulsar.routemap.hit"] = [url, metric_record, tags, metric_type]

            # pulsar all route map misses
            # url = "/v1/pulsar/query/routemap/miss/customer"
            metric_record = "pulsar.routemap.miss"
            urlpath = "/v1/pulsar/query/routemap/miss/customer"
            url = "{apiendpoint}{path}{query}".format(apiendpoint=self.api_endpoint, path=urlpath, query=query_string)
            urlList["pulsar.routemap.miss"] = [url, metric_record, tags, metric_type]

        elif key == "pulsar_by_app":
            metric_type = "gauge"
            # pulsar by app

            for app in val:
                # apps[app["appid"]] = [app["name"],jobs]
                for appid, v in app.items():
                    app_name = pulsar_apps[appid][0]
                    for job in pulsar_apps[appid][1]:
                        jobid = job["jobid"]
                        if jobid == v:
                            tags = [
                                "pulsar_app:{pulsar_app_name}".format(pulsar_app_name=app_name),
                                "pulsar_job:{job_name}".format(job_name=job["name"]),
                            ]
                            # pulsar aggregate performance data
                            # /v1/pulsar/apps/{{app_id}}/jobs/{{job_id}}/data?period=30s
                            url = "{apiendpoint}/v1/pulsar/apps/{app_id}/jobs/{job_id}/data{query}".format(
                                apiendpoint=self.api_endpoint, app_id=appid, job_id=jobid, query=query_string
                            )
                            metric_record = "pulsar.performance"
                            k = "pulsar.performance.{app_id}.{job_id}".format(app_id=appid, job_id=jobid)
                            urlList[k] = [url, metric_record, tags, metric_type]

                            # pulsar availability data
                            # /v1/pulsar/apps/{{app_id}}/jobs/{{job_id}}/availability?period=30s
                            url = "{apiendpoint}/v1/pulsar/apps/{app_id}/jobs/{job_id}/availability{query}".format(
                                apiendpoint=self.api_endpoint, app_id=appid, job_id=jobid, query=query_string
                            )
                            metric_record = "pulsar.availability"
                            k = "pulsar.availability.{app_id}.{job_id}".format(app_id=appid, job_id=jobid)
                            urlList[k] = [url, metric_record, tags, metric_type]

        elif key == "pulsar_by_record":
            query_string = "?period=2d&"
            if query_params:
                if "pulsar_geo" in query_params:
                    query_string = query_string + "geo=" + query_params["pulsar_geo"] + "&"
                if "pulsar_asn" in query_params:
                    query_string = query_string + "asn=" + query_params["pulsar_asn"] + "&"
                # if "pulsar_agg" in query_params:
                #     query_string = query_string + "agg=" + query_params["pulsar_agg"] + "&"
            query_string = query_string[:-1]

            for record in val:
                for domain, rectype in record.items():
                    tags = ["record:{record}".format(record=domain)]
                    metric_type = "count"
                    metric_record = "pulsar.decisions.record"
                    # pulsar decisions for record
                    # /v1/pulsar/query/decision/record/{{record_name}}/{{record_type}}?period=30d
                    url = "{apiendpoint}/v1/pulsar/query/decision/record/{rec_name}/{rec_type}{query}".format(
                        apiendpoint=self.api_endpoint, rec_name=domain, rec_type=rectype, query=query_string
                    )
                    k = "pulsar.decisions.{rec_name}.{rec_type}".format(rec_name=domain, rec_type=rectype)
                    urlList[k] = [url, metric_record, tags, metric_type]

                    metric_record = "pulsar.routemap.hit.record"
                    # View route map hits by record
                    # /v1/pulsar/query/routemap/miss/record/{{record_name}}/{{record_type}}
                    url = "{apiendpoint}/v1/pulsar/query/routemap/hit/record/{rec_name}/{rec_type}{query}".format(
                        apiendpoint=self.api_endpoint, rec_name=domain, rec_type=rectype, query=query_string
                    )
                    k = "pulsar.routemap.hit.{rec_name}.{rec_type}".format(rec_name=domain, rec_type=rectype)
                    urlList[k] = [url, metric_record, tags, metric_type]
                    metric_record = "pulsar.routemap.miss.record"
                    # View route map misses by record
                    # /v1/pulsar/query/routemap/miss/record/{{record_name}}/{{record_type}}?period=30d
                    url = "{apiendpoint}/v1/pulsar/query/routemap/miss/record/{rec_name}/{rec_type}{query}".format(
                        apiendpoint=self.api_endpoint, rec_name=domain, rec_type=rectype, query=query_string
                    )
                    k = "pulsar.routemap.miss.{rec_name}.{rec_type}".format(rec_name=domain, rec_type=rectype)
                    urlList[k] = [url, metric_record, tags, metric_type]

        return urlList

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

    def sendMetrics(self, metricName, metricValue, tags, metric_type):
        if metricName == "billing":
            for k, v in metricValue.items():
                # {"usage": 1234, "limit": 500000}
                # tag as either usage or limit
                tags = ["billing:{btype}".format(btype=k)]
                if metric_type == "gauge":
                    self.gauge('ns1.billing', v, tags)
                elif metric_type == "count":
                    self.count('ns1.billing', v, tags)
        elif isinstance(metricValue, dict):
            for k, v in metricValue.items():
                # urlList["{key}.zones.{domain}"] = url
                # zoneTtl[zone["domain"]] = zone["ttl"]
                # self.count('ns1.{name}.{record}'.format(name=metricName, record=k), v)
                # we need tags on domain level, not zone level, override supplied values
                # {"usage": 1234, "limit": 500000}
                tags = ["record:{domain}".format(domain=k)]
                if metric_type == "gauge":
                    self.gauge('ns1.{name}'.format(name=metricName), v, tags)
                elif metric_type == "count":
                    self.count('ns1.{name}.{record}'.format(name=metricName, record=k), v, tags)
        else:
            if metric_type == "gauge":
                self.gauge('ns1.{}'.format(metricName), metricValue, tags)
            elif metric_type == "count":
                self.count('ns1.{}'.format(metricName), metricValue, tags)
