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
                            # try to pass the value as an int
                            domains_being_blocked = int(data["domains_being_blocked"])
                        except ValueError:
                            # If we can't pass it as an int, we know it is a string
                            domains_being_blocked = data["domains_being_blocked"].replace(",", "")
                        self.gauge("pihole.domains_being_blocked", float(domains_being_blocked), custom_tags)

                    if data.get("dns_queries_today"):
                        try:
                            dns_queries_today = int(data["dns_queries_today"])
                        except ValueError:
                            dns_queries_today = data["dns_queries_today"].replace(",", "")
                        self.gauge("pihole.dns_queries_today", float(dns_queries_today), custom_tags)

                    if data.get("ads_blocked_today"):
                        try:
                            ads_blocked_today = int(data["ads_blocked_today"])
                        except ValueError:
                            ads_blocked_today = data["ads_blocked_today"].replace(",", "")
                        self.gauge("pihole.ads_blocked_today", float(ads_blocked_today), custom_tags)

                    if data.get("ads_percentage_today"):
                        try:
                            ads_percentage_today = int(data["ads_percentage_today"])
                        except ValueError:
                            # Since it is a string, pass and pray
                            ads_percentage_today = data["ads_percentage_today"]
                        self.gauge("pihole.ads_percent_blocked", float(ads_percentage_today), custom_tags)

                    if data.get("unique_domains"):
                        try:
                            unique_domains = int(data["unique_domains"])
                        except ValueError:
                            unique_domains = data["unique_domains"].replace(",", "")
                        self.gauge("pihole.unique_domains", float(unique_domains), custom_tags)

                    if data.get("queries_forwarded"):
                        try:
                            queries_forwarded = int(data["queries_forwarded"])
                        except ValueError:
                            queries_forwarded = data["queries_forwarded"].replace(",", "")
                        self.gauge("pihole.queries_forwarded", float(queries_forwarded), custom_tags)

                    if data.get("queries_cached"):
                        try:
                            queries_cached = int(data["queries_cached"])
                        except ValueError:
                            queries_cached = data["queries_cached"].replace(",", "")
                        self.gauge("pihole.queries_cached", float(queries_cached), custom_tags)

                    if data.get("clients_ever_seen"):
                        try:
                            clients_ever_seen = int(data["clients_ever_seen"])
                        except ValueError:
                            clients_ever_seen = data["clients_ever_seen"].replace(",", "")
                        self.gauge("pihole.clients_ever_seen", float(clients_ever_seen), custom_tags)

                    if data.get("unique_clients"):
                        try:
                            unique_clients = int(data["unique_clients"])
                        except ValueError:
                            unique_clients = data["unique_clients"].replace(",", "")
                        self.gauge("pihole.unique_clients", float(unique_clients), custom_tags)

                    if data.get("dns_queries_all_types"):
                        try:
                            dns_queries_all_types = int(data["dns_queries_all_types"])
                        except ValueError:
                            dns_queries_all_types = data["dns_queries_all_types"].replace(",", "")
                        self.gauge("pihole.dns_queries_all_types", float(dns_queries_all_types), custom_tags)

                    if data.get("reply_NODATA"):
                        try:
                            reply_NODATA = int(data["reply_NODATA"])
                        except ValueError:
                            reply_NODATA = data["reply_NODATA"].replace(",", "")
                        self.gauge("pihole.reply_nodata", float(reply_NODATA), custom_tags)

                    if data.get("reply_NXDOMAIN"):
                        try:
                            reply_NXDOMAIN = int(data["reply_NXDOMAIN"])
                        except ValueError:
                            reply_NXDOMAIN = data["reply_NXDOMAIN"].replace(",", "")
                        self.gauge("pihole.reply_nxdomain", float(reply_NXDOMAIN), custom_tags)

                    if data.get("reply_CNAME"):
                        try:
                            reply_CNAME = int(data["reply_CNAME"])
                        except ValueError:
                            reply_CNAME = data["reply_CNAME"].replace(",", "")
                        self.gauge("pihole.reply_cname", float(reply_CNAME), custom_tags)

                    if data.get("reply_IP"):
                        try:
                            reply_IP = int(data["reply_IP"])
                        except ValueError:
                            reply_IP = data["reply_IP"].replace(",", "")
                        self.gauge("pihole.reply_ip", float(reply_IP), custom_tags)

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
