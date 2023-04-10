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
                        domains_being_blocked = float(data["domains_being_blocked"].replace(",", ""))
                        self.gauge("pihole.domains_being_blocked", domains_being_blocked, custom_tags)

                    if data.get("dns_queries_today"):
                        dns_queries_today = float(data["dns_queries_today"].replace(",", ""))
                        self.gauge("pihole.dns_queries_today", dns_queries_today, custom_tags)

                    if data.get("ads_blocked_today"):
                        ads_blocked_today = string(data["ads_blocked_today"].replace(",", ""))
                        self.gauge("pihole.ads_blocked_today", ads_blocked_today, custom_tags)

                    if data.get("ads_percentage_today"):
                        ads_percentage_today = float(data["ads_percentage_today"].replace(",", ""))
                        self.gauge("pihole.ads_percent_blocked", ads_percentage_today, custom_tags)

                    if data.get("unique_domains"):
                        unique_domains = float(data["unique_domains"].replace(",", ""))
                        self.gauge("pihole.unique_domains", unique_domains, custom_tags)

                    if data.get("queries_forwarded"):
                        queries_forwarded = float(data["queries_forwarded"].replace(",", ""))
                        self.gauge("pihole.queries_forwarded", queries_forwarded, custom_tags)

                    if data.get("queries_cached"):
                        queries_cached = float(data["queries_cached"].replace(",", ""))
                        self.gauge("pihole.queries_cached", queries_cached, custom_tags)

                    if data.get("clients_ever_seen"):
                        clients_ever_seen = float(data["clients_ever_seen"].replace(",", ""))
                        self.gauge("pihole.clients_ever_seen", clients_ever_seen, custom_tags)

                    if data.get("unique_clients"):
                        unique_clients = float(data["unique_clients"].replace(",", ""))
                        self.gauge("pihole.unique_clients", unique_clients, custom_tags)

                    if data.get("dns_queries_all_types"):
                        dns_queries_all_types = float(data["dns_queries_all_types"].replace(",", ""))
                        self.gauge("pihole.dns_queries_all_types", dns_queries_all_types, custom_tags)

                    if data.get("reply_NODATA"):
                        reply_NODATA = float(data["reply_NODATA"].replace(",", ""))
                        self.gauge("pihole.reply_nodata", reply_NODATA, custom_tags)

                    if data.get("reply_NXDOMAIN"):
                        reply_NXDOMAIN = float(data["reply_NXDOMAIN"].replace(",", ""))
                        self.gauge("pihole.reply_nxdomain", reply_NXDOMAIN, custom_tags)

                    if data.get("reply_CNAME"):
                        reply_CNAME = int(data["reply_CNAME"].replace(",", ""))
                        self.gauge("pihole.reply_cname", reply_CNAME, custom_tags)

                    if data.get("reply_IP"):
                        reply_IP = float(data["reply_IP"].replace(",", ""))
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
