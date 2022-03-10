from .ns1_api_url import NS1_ENDPOINTS


class Ns1Url:
    def __init__(self, api_endpoint, check):
        self.check = check
        self.api_endpoint = api_endpoint

    # generate url for QPS and usages statistics
    # returns dictionary in form of <metric name>:<metric url>}
    def get_stats_url_usage(self, key, val, networknames):
        urlList = {}
        query_string = ""

        metric_name = "usage"
        metric_zone = "usage.zone"
        metric_record = "usage.record"
        metric_type = "count"
        query_string = "?period=1h&expand=false"
        url = NS1_ENDPOINTS["qps.usage"].format(apiendpoint=self.api_endpoint, key=key, query=query_string)
        # get account wide stats
        tags = [""]
        urlList[key] = [url, metric_name, tags, metric_type]

        # if list of networks is supplied, query account-wide for each network as well
        if networknames and len(networknames) > 0:
            for k, v in networknames.items():
                query_string = "?period=1h&expand=false&networks={networks}".format(networks=k)
                url = NS1_ENDPOINTS["qps.usage"].format(apiendpoint=self.api_endpoint, key=key, query=query_string)
                tags = ["network:{network}".format(network=v)]
                urlList["{key}.{netid}".format(key=key, netid=k)] = [url, metric_name, tags, metric_type]

        if not val:
            return urlList

        for zoneDict in val:
            # zone is again dictionary, with zone name as key and records as list of objects
            for domain, records in zoneDict.items():
                # here, domain is zone name, records is list of records and record types
                # if list of networks is supplied, query zone for each network as well
                if networknames and len(networknames) > 0:
                    for k, v in networknames.items():
                        query_string = "?period=1h&expand=false&networks={networks}".format(networks=k)
                        url = NS1_ENDPOINTS["qps.usage.zone"].format(
                            apiendpoint=self.api_endpoint, key=key, domain=domain, query=query_string
                        )
                        tags = ["network:{network}".format(network=v), "zone:{zone}".format(zone=domain)]
                        urlkey = "{key}.{domain}.{netid}".format(key=key, domain=domain, netid=k)
                        urlList[urlkey] = [url, metric_name, tags, metric_type]
                else:
                    query_string = "?period=1h&expand=false"
                    url = NS1_ENDPOINTS["qps.usage.zone"].format(
                        apiendpoint=self.api_endpoint, key=key, domain=domain, query=query_string
                    )
                    tags = ["zone:{zone}".format(zone=domain)]

                    urlList["{key}.{domain}".format(key=key, domain=domain)] = [url, metric_zone, tags, metric_type]

                if not records:
                    # if records are not specified, get all records for the zone, then build url for each record
                    records = self.check.get_zone_records(domain)

                # for each record, either specified or queried from zone
                if records:
                    for rec in records:
                        for rname, rtype in rec.items():
                            if networknames and len(networknames) > 0:
                                for k, v in networknames.items():
                                    query_string = "?period=1h&expand=false&networks={networks}".format(networks=k)
                                    url = NS1_ENDPOINTS["qps.usage.record"].format(
                                        apiendpoint=self.api_endpoint,
                                        key=key,
                                        domain=domain,
                                        record=rname,
                                        rectype=rtype,
                                        query=query_string,
                                    )
                                    tags = [
                                        "network:{network}".format(network=v),
                                        "zone:{zone}".format(zone=domain),
                                        "record:{record}".format(record=rname),
                                        "type:{rectype}".format(rectype=rtype),
                                    ]
                                    urlkey = "{key}.{record}.{rectype}.{netid}".format(
                                        key=key, record=rname, rectype=rtype, netid=k
                                    )
                                    urlList[urlkey] = [url, metric_record, tags, metric_type]
                            else:
                                query_string = "?period=1h&expand=false"
                                url = NS1_ENDPOINTS["qps.usage.record"].format(
                                    apiendpoint=self.api_endpoint,
                                    key=key,
                                    domain=domain,
                                    record=rname,
                                    rectype=rtype,
                                    query=query_string,
                                )
                                tags = [
                                    "zone:{zone}".format(zone=domain),
                                    "record:{record}".format(record=rname),
                                    "type:{rectype}".format(rectype=rtype),
                                ]
                                urlkey = "{key}.{record}.{rectype}".format(key=key, record=rname, rectype=rtype)
                                urlList[urlkey] = [url, metric_record, tags, metric_type]

        return urlList

    # generate url for QPS statistics
    # returns dictionary in form of <metric name>:<metric url>}
    def get_stats_url_qps(self, key, val):
        urlList = {}
        query_string = ""
        metric_name = "qps"
        metric_zone = "qps.zone"
        metric_record = "qps.record"
        metric_type = "gauge"
        url = NS1_ENDPOINTS["qps.usage"].format(apiendpoint=self.api_endpoint, key="qps", query=query_string)
        # get account wide stats
        tags = [""]
        urlList[key] = [url, metric_name, tags, metric_type]

        if not val:
            return urlList
        for zoneDict in val:
            # zone is again dictionary, with zone name as key and records as list of objects
            for domain, records in zoneDict.items():
                # here, domain is zone name, records is list of records and record types
                url = NS1_ENDPOINTS["qps.usage.zone"].format(
                    apiendpoint=self.api_endpoint, key=key, domain=domain, query=query_string
                )
                tags = ["zone:{zone}".format(zone=domain)]
                urlList["{key}.{domain}".format(key=key, domain=domain)] = [url, metric_zone, tags, metric_type]

                if not records:
                    # if records are not specified, get all records for the zone, then build url for each record
                    records = self.check.get_zone_records(domain)
                    for rec in records:
                        for k, v in rec.items():
                            print("{k} = {v}".format(k=k, v=v))

                if records:
                    for rec in records:
                        for rname, rtype in rec.items():
                            url = NS1_ENDPOINTS["qps.usage.record"].format(
                                apiendpoint=self.api_endpoint,
                                key=key,
                                domain=domain,
                                record=rname,
                                rectype=rtype,
                                query=query_string,
                            )
                            tags = [
                                "zone:{zone}".format(zone=domain),
                                "record:{record}".format(record=rname),
                                "type:{rectype}".format(rectype=rtype),
                            ]
                            urlkey = "{key}.{record}.{rectype}".format(key=key, record=rname, rectype=rtype)
                            urlList[urlkey] = [url, metric_record, tags, metric_type]
                else:
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
        url = NS1_ENDPOINTS["ddi.leases"].format(apiendpoint=self.api_endpoint)
        urlList["leases"] = [url, metric_lease, tags, metric_type_count]

        url = NS1_ENDPOINTS["ddi.lps"].format(apiendpoint=self.api_endpoint)
        urlList["peak_lps"] = [url, metric_lps, tags, metric_type_gauge]

        # if scope groups are specified, get stats for those requested
        if not val:
            return urlList

        for scope_id in val:
            if scope_id in scopegroups:

                tags = ["scope_group:{scope_name}".format(scope_name=scopegroups[scope_id])]
                url = NS1_ENDPOINTS["ddi.leases.scope"].format(apiendpoint=self.api_endpoint, scope_group_id=scope_id)
                urlList["leases.{scope_group_id}".format(scope_group_id=scope_id)] = [
                    url,
                    metric_lease,
                    tags,
                    metric_type_count,
                ]
                url = NS1_ENDPOINTS["ddi.lps.scope"].format(apiendpoint=self.api_endpoint, scope_group_id=scope_id)
                urlList["peak_lps.{scope_group_id}".format(scope_group_id=scope_id)] = [
                    url,
                    metric_lps,
                    tags,
                    metric_type_gauge,
                ]

        return urlList

    def get_zone_info_url(self, key, val):
        urlList = {}

        if not val:
            return urlList
        for accDict in val:
            for _, domainList in accDict.items():
                metric_record = "ttl"
                metric_type = "gauge"
                if domainList:
                    for domain in domainList:
                        tags = ["record:{zone}".format(zone=domain)]
                        url = NS1_ENDPOINTS["ttl"].format(apiendpoint=self.api_endpoint, domain=domain)
                        urlList["{key}.ttl.{domain}".format(key=key, domain=domain)] = [
                            url,
                            metric_record,
                            tags,
                            metric_type,
                        ]
        return urlList

    def get_plan_details_url(self, key, val):
        urlList = {}

        # get account plan limits
        url = NS1_ENDPOINTS["billing"].format(apiendpoint=self.api_endpoint)
        tags = [""]
        metric_record = "billing"
        metric_type = "gauge"
        urlList["{key}.billing".format(key=key)] = [url, metric_record, tags, metric_type]

        return urlList

    def get_pulsar_by_record_url(self, val, query_params):
        urlList = {}
        query_string = "?period=1h&"
        if query_params:
            if "pulsar_geo" in query_params and query_params["pulsar_geo"] != "*":
                query_string = query_string + "geo=" + query_params["pulsar_geo"] + "&"
                if "pulsar_asn" in query_params and query_params["pulsar_asn"] != "*":
                    query_string = query_string + "asn=" + query_params["pulsar_asn"] + "&"
        query_string = query_string[:-1]

        for record in val:
            for domain, rectype in record.items():
                tags = ["record:{record}".format(record=domain)]
                metric_type = "count"
                metric_record = "pulsar.decisions.record"
                # pulsar decisions for record
                url = NS1_ENDPOINTS["pulsar.decisions.record"].format(
                    apiendpoint=self.api_endpoint, query=query_string + "&agg=jobid&record=" + domain + "_" + rectype
                )
                k = "pulsar.decisions.{rec_name}.{rec_type}".format(rec_name=domain, rec_type=rectype)
                urlList[k] = [url, metric_record, tags, metric_type]

                metric_record = "pulsar.routemap.hit.record"
                # route map hits by record
                url = NS1_ENDPOINTS["pulsar.routemap.hit.record"].format(
                    apiendpoint=self.api_endpoint, rec_name=domain, rec_type=rectype, query=query_string
                )
                k = "pulsar.routemap.hit.{rec_name}.{rec_type}".format(rec_name=domain, rec_type=rectype)
                urlList[k] = [url, metric_record, tags, metric_type]
                metric_record = "pulsar.routemap.miss.record"
                # route map misses by record
                url = NS1_ENDPOINTS["pulsar.routemap.miss.record"].format(
                    apiendpoint=self.api_endpoint, rec_name=domain, rec_type=rectype, query=query_string
                )
                k = "pulsar.routemap.miss.{rec_name}.{rec_type}".format(rec_name=domain, rec_type=rectype)
                urlList[k] = [url, metric_record, tags, metric_type]
        return urlList

    def get_pulsar_by_app_url(self, val, pulsar_apps, query_params):
        # pulsar by app
        urlList = {}
        metric_type = "gauge"
        query_string = "?"
        if query_params:
            if "pulsar_period" in query_params:
                query_string = query_string + "period=" + query_params["pulsar_period"] + "&"
            if "pulsar_geo" in query_params and query_params["pulsar_geo"] != "*":
                query_string = query_string + "geo=" + query_params["pulsar_geo"] + "&"
                if "pulsar_asn" in query_params and query_params["pulsar_asn"] != "*":
                    query_string = query_string + "asn=" + query_params["pulsar_asn"] + "&"
        query_string = query_string[:-1]

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
                        url = NS1_ENDPOINTS["pulsar.performance"].format(
                            apiendpoint=self.api_endpoint, app_id=appid, job_id=jobid, query=query_string
                        )
                        metric_record = "pulsar.performance"
                        k = "pulsar.performance.{app_id}.{job_id}".format(app_id=appid, job_id=jobid)
                        urlList[k] = [url, metric_record, tags, metric_type]

                        # pulsar availability data
                        url = NS1_ENDPOINTS["pulsar.availability"].format(
                            apiendpoint=self.api_endpoint, app_id=appid, job_id=jobid, query=query_string
                        )
                        metric_record = "pulsar.availability"
                        k = "pulsar.availability.{app_id}.{job_id}".format(app_id=appid, job_id=jobid)
                        urlList[k] = [url, metric_record, tags, metric_type]
        return urlList

    def get_pulsar_url(self, query_params):
        urlList = {}
        query_string = "?"
        # for "pulsar" group of endpoints, override settings and always use period = 1h
        # to get properly sumarized stats
        query_string = query_string + "period=1h&"
        if query_params:
            if "pulsar_geo" in query_params and query_params["pulsar_geo"] != "*":
                query_string = query_string + "geo=" + query_params["pulsar_geo"] + "&"
                if "pulsar_asn" in query_params and query_params["pulsar_asn"] != "*":
                    query_string = query_string + "asn=" + query_params["pulsar_asn"] + "&"
        query_string = query_string[:-1]

        tags = [""]
        metric_record = "pulsar.decisions"
        keyname = "pulsar.decisions"
        metric_type = "count"

        # pulsar decisions account wide
        url = NS1_ENDPOINTS[keyname].format(apiendpoint=self.api_endpoint, query=query_string + "&agg=jobid")
        urlList[keyname] = [url, metric_record, tags, metric_type]

        tags = [""]

        # pulsar insufficient decision data for account
        metric_record = "pulsar.decisions.insufficient"
        keyname = "pulsar.decisions.insufficient"
        url = NS1_ENDPOINTS[keyname].format(
            apiendpoint=self.api_endpoint, query=query_string + "&agg=jobid&result=ERR_INSUF"
        )
        urlList[keyname] = [url, metric_record, tags, metric_type]

        # pulsar all route map hits
        metric_record = "pulsar.routemap.hit"
        keyname = "pulsar.routemap.hit"
        url = NS1_ENDPOINTS[keyname].format(apiendpoint=self.api_endpoint, query=query_string)
        urlList[keyname] = [url, metric_record, tags, metric_type]

        # pulsar all route map misses
        metric_record = "pulsar.routemap.miss"
        keyname = "pulsar.routemap.miss"
        url = NS1_ENDPOINTS[keyname].format(apiendpoint=self.api_endpoint, query=query_string)
        urlList[keyname] = [url, metric_record, tags, metric_type]
        return urlList
