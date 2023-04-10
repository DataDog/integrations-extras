from datadog_checks.base import AgentCheck, ConfigurationError


class PiholeCheck(AgentCheck):
    def __init__(self, name, init_config, instances):
        super(PiholeCheck, self).__init__(name, init_config, instances)
        host = self.instance.get('host')
        if not host:  # Check if a host parameter exists in conf.yaml
            raise ConfigurationError('Error, please fix pihole.d/conf.yaml, host parameter is required')

    def _collect_response(self, url):
        response = self.http.get(url)
        data = response.json()
        status_code = response.status_code
        return data, status_code

    def check(self, instance):
        host = self.instance.get('host')
        token = self.instance.get('token')
        custom_tags = self.instance.get("tags", [])
        custom_tags.append("target_host:{}".format(host))
        # If a token is passed in, then use it
        if token:
            url = 'http://' + host + '/admin/api.php?summary&auth=' + token
        else:
            url = 'http://' + host + '/admin/api.php?summary'
        data, status_code = self._collect_response(url)
        if status_code == 200:  # else is after all the metrics

            if data.get("status"):
                if data["status"] == 'enabled':
                    self.service_check('pihole.running', self.OK)

                    if data.get("domains_being_blocked"):
                        try:
                            domains_being_blocked = float(data["domains_being_blocked"].replace(",", ""))
                        except AttributeError:
                            domains_being_blocked = float(data["domains_being_blocked"])
                        self.gauge("pihole.domains_being_blocked", domains_being_blocked, custom_tags)

                    if data.get("dns_queries_today"):
                        try:
                            dns_queries_today = float(data["dns_queries_today"].replace(",", ""))
                        except AttributeError:
                            dns_queries_today = float(data["dns_queries_today"])
                        self.gauge("pihole.dns_queries_today", dns_queries_today, custom_tags)

                    if data.get("ads_blocked_today"):
                        try:
                            ads_blocked_today = float(data["ads_blocked_today"].replace(",", ""))
                        except AttributeError:
                            ads_blocked_today = float(data["ads_blocked_today"])
                        self.gauge("pihole.ads_blocked_today", ads_blocked_today, custom_tags)

                    if data.get("ads_percentage_today"):
                        try:
                            ads_percentage_today = float(data["ads_percentage_today"].replace(",", ""))
                        except AttributeError:
                            ads_percentage_today = float(data["ads_percentage_today"])
                        self.gauge("pihole.ads_percent_blocked", ads_percentage_today, custom_tags)

                    if data.get("unique_domains"):
                        try:
                            unique_domains = float(data["unique_domains"].replace(",", ""))
                        except AttributeError:
                            unique_domains = float(data["unique_domains"])
                        self.gauge("pihole.unique_domains", unique_domains, custom_tags)

                    if data.get("queries_forwarded"):
                        try:
                            queries_forwarded = float(data["queries_forwarded"].replace(",", ""))
                        except AttributeError:
                            queries_forwarded = float(data["queries_forwarded"])
                        self.gauge("pihole.queries_forwarded", queries_forwarded, custom_tags)

                    if data.get("queries_cached"):
                        try:
                            queries_cached = float(data["queries_cached"].replace(",", ""))
                        except AttributeError:
                            queries_cached = float(data["queries_cached"])
                        self.gauge("pihole.queries_cached", queries_cached, custom_tags)

                    if data.get("clients_ever_seen"):
                        try:
                            clients_ever_seen = float(data["clients_ever_seen"].replace(",", ""))
                        except AttributeError:
                            clients_ever_seen = float(data["clients_ever_seen"])
                        self.gauge("pihole.clients_ever_seen", clients_ever_seen, custom_tags)

                    if data.get("unique_clients"):
                        try:
                            unique_clients = float(data["unique_clients"].replace(",", ""))
                        except AttributeError:
                            unique_clients = float(data["unique_clients"])
                        self.gauge("pihole.unique_clients", unique_clients, custom_tags)

                    if data.get("dns_queries_all_types"):
                        try:
                            dns_queries_all_types = float(data["dns_queries_all_types"].replace(",", ""))
                        except AttributeError:
                            dns_queries_all_types = float(data["dns_queries_all_types"])
                        self.gauge("pihole.dns_queries_all_types", dns_queries_all_types, custom_tags)

                    if data.get("reply_NODATA"):
                        try:
                            reply_NODATA = float(data["reply_NODATA"].replace(",", ""))
                        except AttributeError:
                            reply_NODATA = float(data["reply_NODATA"])
                        self.gauge("pihole.reply_nodata", reply_NODATA, custom_tags)

                    if data.get("reply_NXDOMAIN"):
                        try:
                            reply_NXDOMAIN = float(data["reply_NXDOMAIN"].replace(",", ""))
                        except AttributeError:
                            reply_NXDOMAIN = float(data["reply_NXDOMAIN"])
                        self.gauge("pihole.reply_nxdomain", reply_NXDOMAIN, custom_tags)

                    if data.get("reply_CNAME"):
                        try:
                            reply_CNAME = float(data["reply_CNAME"].replace(",", ""))
                        except AttributeError:
                            reply_CNAME = float(data["reply_CNAME"])
                        self.gauge("pihole.reply_cname", reply_CNAME, custom_tags)

                    if data.get("reply_IP"):
                        try:
                            reply_IP = float(data["reply_IP"].replace(",", ""))
                        except AttributeError:
                            reply_IP = float(data["reply_IP"])
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
