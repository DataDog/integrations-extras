from .ns1_api_url import NS1_ENDPOINTS


class Ns1Url:
    def __init__(self, api_endpoint):
        self.api_endpoint = api_endpoint

    # generate url for QPS and usages statistics
    # returns dictionary in form of <metric name>:<metric url>}
    def get_stats_url(self, key, val, query_params):
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

        # get account wide stats
        url = NS1_ENDPOINTS["qps.usage"].format(apiendpoint=self.api_endpoint, key=key, query=query_string)
        tags = [""]
        urlList[key] = [url, metric_name, tags, metric_type]

        if val:
            for zoneDict in val:
                # zone is again dictionary, with zone name as key and records as list of objects
                # metric_name=metric_name + ".zone"
                for domain, records in zoneDict.items():
                    # here, domain is zone name, records is list of records and record types
                    url = NS1_ENDPOINTS["qps.usage.zone"]
                    url = url.format(apiendpoint=self.api_endpoint, key=key, domain=domain, query=query_string)
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

    # generate url for DDI lease and lps statistics
    def get_ddi_url(self, key, val, scopegroups):
        urlList = {}
        metric_lease = "leases"
        metric_lps = "peak_lps"
        metric_type_count = "count"
        metric_type_gauge = "gauge"

        # first get account-wide lease and lps stats
        tags = ["scope_group:account_wide"]
        url = "{apiendpoint}/v1/stats/leases?period=24h".format(apiendpoint=self.api_endpoint)
        urlList["leases"] = [url, metric_lease, tags, metric_type_count]

        url = "{apiendpoint}/v1/stats/lps?period=24h".format(apiendpoint=self.api_endpoint)
        urlList["peak_lps"] = [url, metric_lps, tags, metric_type_gauge]

        # if scope groups are specified, get stats for those requested
        if val:
            # get scope group names to use them as tags so that we can separate metrics in dashboard
            # scopegroups = self.get_ddi_scope_groups()

            for scope_id in val:
                if scope_id in scopegroups:

                    tags = ["scope_group:{scope_name}".format(scope_name=scopegroups[scope_id])]

                    url = "{apiendpoint}/v1/stats/leases/{scope_group_id}?period=24h".format(
                        apiendpoint=self.api_endpoint, scope_group_id=scope_id
                    )
                    urlList["leases.{scope_group_id}".format(scope_group_id=scope_id)] = [
                        url,
                        metric_lease,
                        tags,
                        metric_type_count,
                    ]

                    url = "{apiendpoint}/v1/stats/lps/{scope_group_id}?period=24h".format(
                        apiendpoint=self.api_endpoint, scope_group_id=scope_id
                    )
                    urlList["peak_lps.{scope_group_id}".format(scope_group_id=scope_id)] = [
                        url,
                        metric_lps,
                        tags,
                        metric_type_gauge,
                    ]

        return urlList

    def get_zone_info_url(self, key, val):
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

    def get_plan_details_url(self, key, val):
        urlList = {}

        # just get account plan limits
        url = "{apiendpoint}/v1/account/billataglance".format(apiendpoint=self.api_endpoint)
        tags = [""]
        metric_record = "billing"
        metric_type = "gauge"
        urlList["{key}.billing".format(key=key)] = [url, metric_record, tags, metric_type]

        return urlList

    def get_pulsar_app_url(self, key, val, query_params, pulsar_apps):

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

            tags = [""]

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
                                "app:{pulsar_app_name}".format(pulsar_app_name=app_name),
                                "resource:{job_name}".format(job_name=job["name"]),
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
                    url = "{apiendpoint}/v1/pulsar/query/decision/record/{rec_name}/{rec_type}{query}".format(
                        apiendpoint=self.api_endpoint, rec_name=domain, rec_type=rectype, query=query_string
                    )
                    k = "pulsar.decisions.{rec_name}.{rec_type}".format(rec_name=domain, rec_type=rectype)
                    urlList[k] = [url, metric_record, tags, metric_type]

                    metric_record = "pulsar.routemap.hit.record"
                    # route map hits by record
                    url = "{apiendpoint}/v1/pulsar/query/routemap/hit/record/{rec_name}/{rec_type}{query}".format(
                        apiendpoint=self.api_endpoint, rec_name=domain, rec_type=rectype, query=query_string
                    )
                    k = "pulsar.routemap.hit.{rec_name}.{rec_type}".format(rec_name=domain, rec_type=rectype)
                    urlList[k] = [url, metric_record, tags, metric_type]
                    metric_record = "pulsar.routemap.miss.record"
                    # route map misses by record
                    url = "{apiendpoint}/v1/pulsar/query/routemap/miss/record/{rec_name}/{rec_type}{query}".format(
                        apiendpoint=self.api_endpoint, rec_name=domain, rec_type=rectype, query=query_string
                    )
                    k = "pulsar.routemap.miss.{rec_name}.{rec_type}".format(rec_name=domain, rec_type=rectype)
                    urlList[k] = [url, metric_record, tags, metric_type]

        return urlList
