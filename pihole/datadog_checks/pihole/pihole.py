import json

from datadog_checks.base import AgentCheck, ConfigurationError

V6_METRIC_NAMES = [
    # Clients
    'pihole.clients.active',
    'pihole.clients.total',
    # Gravity
    'pihole.gravity.domains_being_blocked',
    'pihole.gravity.last_update',
    # Summary
    'pihole.queries.blocked',
    'pihole.queries.cached',
    'pihole.queries.forwarded',
    'pihole.queries.frequency',
    'pihole.queries.percent_blocked',
    'pihole.queries.total',
    'pihole.queries.unique_domains',
    'pihole.took',
    # Replies
    'pihole.queries.replies.BLOB',
    'pihole.queries.replies.CNAME',
    'pihole.queries.replies.DNSSEC',
    'pihole.queries.replies.DOMAIN',
    'pihole.queries.replies.IP',
    'pihole.queries.replies.NODATA',
    'pihole.queries.replies.NONE',
    'pihole.queries.replies.NOTIMP',
    'pihole.queries.replies.NXDOMAIN',
    'pihole.queries.replies.OTHER',
    'pihole.queries.replies.REFUSED',
    'pihole.queries.replies.RRNAME',
    'pihole.queries.replies.SERVFAIL',
    'pihole.queries.replies.UNKNOWN',
    # Status
    'pihole.queries.status.CACHE',
    'pihole.queries.status.CACHE_STALE',
    'pihole.queries.status.DBBUSY',
    'pihole.queries.status.DENYLIST',
    'pihole.queries.status.DENYLIST_CNAME',
    'pihole.queries.status.EXTERNAL_BLOCKED_EDE15',
    'pihole.queries.status.EXTERNAL_BLOCKED_IP',
    'pihole.queries.status.EXTERNAL_BLOCKED_NULL',
    'pihole.queries.status.EXTERNAL_BLOCKED_NXRA',
    'pihole.queries.status.FORWARDED',
    'pihole.queries.status.GRAVITY',
    'pihole.queries.status.GRAVITY_CNAME',
    'pihole.queries.status.IN_PROGRESS',
    'pihole.queries.status.REGEX',
    'pihole.queries.status.REGEX_CNAME',
    'pihole.queries.status.RETRIED',
    'pihole.queries.status.RETRIED_DNSSEC',
    'pihole.queries.status.SPECIAL_DOMAIN',
    'pihole.queries.status.UNKNOWN',
    # Types
    'pihole.queries.types.A',
    'pihole.queries.types.AAAA',
    'pihole.queries.types.ANY',
    'pihole.queries.types.DNSKEY',
    'pihole.queries.types.DS',
    'pihole.queries.types.HTTPS',
    'pihole.queries.types.MX',
    'pihole.queries.types.NAPTR',
    'pihole.queries.types.NS',
    'pihole.queries.types.OTHER',
    'pihole.queries.types.PTR',
    'pihole.queries.types.RRSIG',
    'pihole.queries.types.SOA',
    'pihole.queries.types.SRV',
    'pihole.queries.types.SVCB',
    'pihole.queries.types.TXT',
]


class PiholeCheck(AgentCheck):
    def __init__(self, name, init_config, instances):
        super(PiholeCheck, self).__init__(name, init_config, instances)
        self.host = self.instance.get('host')
        if not self.host:  # Check if a host parameter exists in conf.yaml
            raise ConfigurationError('Error, please fix pihole.d/conf.yaml, host parameter is required')
        self.web_password = self.instance.get('web_password')
        self.v5_pihole = self.instance.get('legacy_check')
        self.custom_tags = self.instance.get("tags", [])
        self.custom_tags.append("target_host:{}".format(self.host))

    def _collect_response(self, url):
        response = self.http.get(url)
        data = response.json()
        status_code = response.status_code
        return data, status_code

    def _legacy_check(self, host, custom_tags):
        url = 'http://' + host + '/admin/api.php'  # adding the rest of the URL to the given host parameter
        data, status_code = self._collect_response(url)
        if status_code == 200:  # else is after all the metrics
            if data.get("status"):
                if data["status"] == 'enabled':
                    self.service_check('pihole.running', self.OK)

                    if data.get("domains_being_blocked"):
                        domains_being_blocked = data["domains_being_blocked"]
                        self.gauge("pihole.domains_being_blocked", domains_being_blocked, custom_tags)

                    if data.get("dns_queries_today"):
                        dns_queries_today = data["dns_queries_today"]
                        self.gauge("pihole.dns_queries_today", dns_queries_today, custom_tags)

                    if data.get("ads_blocked_today"):
                        ads_blocked_today = data["ads_blocked_today"]
                        self.gauge("pihole.ads_blocked_today", ads_blocked_today, custom_tags)

                    if data.get("ads_percentage_today"):
                        ads_percentage_today = data["ads_percentage_today"]
                        self.gauge("pihole.ads_percent_blocked", ads_percentage_today, custom_tags)

                    if data.get("unique_domains"):
                        unique_domains = data["unique_domains"]
                        self.gauge("pihole.unique_domains", unique_domains, custom_tags)

                    if data.get("queries_forwarded"):
                        queries_forwarded = data["queries_forwarded"]
                        self.gauge("pihole.queries_forwarded", queries_forwarded, custom_tags)

                    if data.get("queries_cached"):
                        queries_cached = data["queries_cached"]
                        self.gauge("pihole.queries_cached", queries_cached, custom_tags)

                    if data.get("clients_ever_seen"):
                        clients_ever_seen = data["clients_ever_seen"]
                        self.gauge("pihole.clients_ever_seen", clients_ever_seen, custom_tags)

                    if data.get("unique_clients"):
                        unique_clients = data["unique_clients"]
                        self.gauge("pihole.unique_clients", unique_clients, custom_tags)

                    if data.get("dns_queries_all_types"):
                        dns_queries_all_types = data["dns_queries_all_types"]
                        self.gauge("pihole.dns_queries_all_types", dns_queries_all_types, custom_tags)

                    if data.get("reply_NODATA"):
                        reply_NODATA = data["reply_NODATA"]
                        self.gauge("pihole.reply_nodata", reply_NODATA, custom_tags)

                    if data.get("reply_NXDOMAIN"):
                        reply_NXDOMAIN = data["reply_NXDOMAIN"]
                        self.gauge("pihole.reply_nxdomain", reply_NXDOMAIN, custom_tags)

                    if data.get("reply_CNAME"):
                        reply_CNAME = data["reply_CNAME"]
                        self.gauge("pihole.reply_cname", reply_CNAME, custom_tags)

                    if data.get("reply_IP"):
                        reply_IP = data["reply_IP"]
                        self.gauge("pihole.reply_ip", reply_IP, custom_tags)

                else:
                    self.log.warning(
                        "Pi-hole disabled on host: %s runtimeError",
                        host,
                    )
                    self.service_check('pihole.running', self.CRITICAL)
                    raise Exception('Pi-hole is disabled')  # if we dont get a status parameter
            else:
                self.log.warning(
                    "no status returned for host: %s runtimeError",
                    host,
                )
                self.service_check('pihole.running', self.CRITICAL)
                raise Exception('Unexpected response from server - No status returned')  # if we dont get a valid status
        else:
            self.service_check('pihole.running', self.CRITICAL)
            self.log.warning(
                "no metrics for %s runtimeError response code: %s",
                host,
                status_code,
            )
            raise Exception('Unexpected response from server')  # if we dont get a response code of '200'

    # Supports generating a SID and CSRF using a pihole web password
    def _auth_v6_session(self, host, web_password):
        authUrl = 'http://' + host + '/api/auth'
        payload = {"password": web_password}
        json_payload = json.dumps(payload)
        response = self.http.post(authUrl, data=json_payload)
        return response.text, response.status_code

    # flattens the returned summary result from raw json to metric format, and prepends the namespace
    def _flatten_dict(self, d, parent_key='pihole', sep='.'):
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}"
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    # Helper function to submit a single metric safely, verifying it is present in the collected output
    def submit_metrics(self, metric_name, metrics, custom_tags):
        value = metrics.get(metric_name)
        if value is not None:
            self.gauge(metric_name, value, custom_tags)

    # Collect all metrics retunred from the /stats/summary endpoint and submit
    def _collect_v6_metrics(self, host, headers, custom_tags):
        statsUrl = 'http://' + host + '/api/stats/summary'
        stats_resp = self.http.get(statsUrl, headers=headers)
        metrics = self._flatten_dict(stats_resp.json())
        for metric_name in V6_METRIC_NAMES:
            self.submit_metrics(metric_name, metrics, custom_tags)
        return stats_resp

    # End session by submitting a delete request with our created SID
    def _end_v6_session(self, host, headers):
        delete_url = "http://" + host + "/api/auth"
        delete_response = self.http.delete(delete_url, headers=headers, verify=False)
        return delete_response

    # Logic for version 6+ of the pihole API
    def _v6_check(self, host, web_password, custom_tags):
        response, status_code = self._auth_v6_session(host, web_password)
        if status_code == 200:
            self.service_check('pihole.running', self.OK)
            resp_json = json.loads(response)
            sid, csrf = (
                resp_json["session"]["sid"],
                resp_json["session"]["csrf"],
            )  # Extract SID and CSRF from the json upon a sucesful auth request
            headers = {
                "X-FTL-SID": sid,
                "X-FTL-CSRF": csrf,
                "Accept": "application/json",
            }  # Set headers needed for further requests
            try:
                stats_resp = self._collect_v6_metrics(host, headers, custom_tags)
            except Exception:
                self.log.error(
                    "ERROR %e",
                    stats_resp,
                )
            logout_resp = self._end_v6_session(host, headers)
            self.log.debug("logout status %s", logout_resp)
        else:
            self.service_check('pihole.running', self.CRITICAL)
            raise Exception('Unexpected response from server')

    def check(self, instance):
        if self.v5_pihole:
            self._legacy_check(self.host, self.custom_tags)
        else:
            self._v6_check(self.host, self.web_password, self.custom_tags)
