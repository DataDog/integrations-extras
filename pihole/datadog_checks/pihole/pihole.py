from datadog_checks.base import AgentCheck, ConfigurationError


class PiholeCheck(AgentCheck):
    def __init__(self, name, init_config, instances):
        super(PiholeCheck, self).__init__(name, init_config, instances)
        host = self.instance.get('host')
        if not host:  # Check if a host parameter exists in conf.yaml
            raise ConfigurationError('Error, please fix pihole.d/conf.yaml, host parameter is required')
        token = self.instance.get('token')
        if not token:
            raise ConfigurationError('Error, please fix pihole.d/conf.yaml, token parameter is required')

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

        url = 'http://' + host + '/admin/api.php?summary&auth=' + token  # Generate the properly formed url to hit a standard configuration of pihole
        data, status_code = self._collect_response(url)
        if status_code == 200:  # else is after all the metrics

            if data.get("status"):
                if data["status"] == 'enabled':
                    self.service_check('pihole.running', self.OK)

                    if data.get("domains_being_blocked"):
                        domains_being_blocked = data["domains_being_blocked"]
                        self.gauge("pihole.domains_being_blocked", float(domains_being_blocked.replace(",", "")), custom_tags)

                    if data.get("dns_queries_today"):
                        dns_queries_today = data["dns_queries_today"]
                        self.gauge("pihole.dns_queries_today", float(dns_queries_today.replace(",", "")), custom_tags)

                    if data.get("ads_blocked_today"):
                        ads_blocked_today = data["ads_blocked_today"]
                        self.gauge("pihole.ads_blocked_today", float(ads_blocked_today.replace(",", "")), custom_tags)

                    if data.get("ads_percentage_today"):
                        ads_percentage_today = data["ads_percentage_today"]
                        self.gauge("pihole.ads_percent_blocked", float(ads_percentage_today.replace(",", "")), custom_tags)

                    if data.get("unique_domains"):
                        unique_domains = data["unique_domains"]
                        self.gauge("pihole.unique_domains", float(unique_domains.replace(",", "")), custom_tags)

                    if data.get("queries_forwarded"):
                        queries_forwarded = data["queries_forwarded"]
                        self.gauge("pihole.queries_forwarded", float(queries_forwarded.replace(",", "")), custom_tags)

                    if data.get("queries_cached"):
                        queries_cached = data["queries_cached"]
                        self.gauge("pihole.queries_cached", float(queries_cached.replace(",", "")), custom_tags)

                    if data.get("clients_ever_seen"):
                        clients_ever_seen = data["clients_ever_seen"]
                        self.gauge("pihole.clients_ever_seen", float(clients_ever_seen.replace(",", "")), custom_tags)

                    if data.get("unique_clients"):
                        unique_clients = data["unique_clients"]
                        self.gauge("pihole.unique_clients", float(unique_clients.replace(",", "")), custom_tags)

                    if data.get("dns_queries_all_types"):
                        dns_queries_all_types = data["dns_queries_all_types"]
                        self.gauge("pihole.dns_queries_all_types", float(dns_queries_all_types.replace(",", "")), custom_tags)

                    if data.get("reply_NODATA"):
                        reply_NODATA = data["reply_NODATA"]
                        self.gauge("pihole.reply_nodata", float(reply_NODATA.replace(",", "")), custom_tags)

                    if data.get("reply_NXDOMAIN"):
                        reply_NXDOMAIN = data["reply_NXDOMAIN"]
                        self.gauge("pihole.reply_nxdomain", float(reply_NXDOMAIN.replace(",", "")), custom_tags)

                    if data.get("reply_CNAME"):
                        reply_CNAME = data["reply_CNAME"]
                        self.gauge("pihole.reply_cname", float(reply_CNAME.replace(",", "")), custom_tags)

                    if data.get("reply_IP"):
                        reply_IP = data["reply_IP"]
                        self.gauge("pihole.reply_ip", float(reply_IP.replace(",", "")), custom_tags)

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
