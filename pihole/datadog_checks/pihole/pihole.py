from datadog_checks.base import AgentCheck
from datadog_checks.base import ConfigurationError

import requests


class PiholeCheck(AgentCheck):
    def check(self, instance):
        host = instance.get('host')
        custom_tags = instance.get("tags", [])
        custom_tags.append("target_host:{}".format(host))

        if not host:  # Check if a host parameter exsists in conf.yaml
            raise ConfigurationError('Configuration error, please fix pihole.d/conf.yaml, A host parameter is required for this integration')

        url = 'http://' + host + '/admin/api.php'  # adding the rest of the URL to the given host parameter
        response = requests.get(url)
        if response.status_code == 200:  # else is after all the metrics
            try:
                data = response.json()  # try to decode the json response, throw generic error if its not a valid json response
            except simplejson.errors.JSONDecodeError:
                raise ConfigurationError('unexpected response from server, is pihole running?')
                self.service_check('pihole.running', self.CRITICAL)
                # Metrics:
                # before submitting any metric, we ensure the expected key:value pair is in the decoded response
                # if any individual metrc wasn't in the last response, we dont need to worry.

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
                self.gauge("pihole.dns_queries_today", dns_queries_all_types, custom_tags)

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

            if data.get("privacy_level"):
                privacy_level = data["privacy_level"]
                self.gauge("pihole.privacy_level", privacy_level, custom_tags)

            if data.get("status"):
                if data["status"] == 'enabled':
                    self.service_check('pihole.running', self.OK)
                else:
                    self.service_check('pihole.running', self.CRITICAL)
            else:
                self.service_check('pihole.running', self.CRITICAL)

        else:
            raise ConfigurationError('Unexpected response from server')  # if we dont get a response code of '200' raise server side issue
            self.service_check('pihole.running', self.CRITICAL)
            self.log.warning("not collecting pihole metrics for url %s runtimeError response code was %s",
                host,
                response.status_code,
            )

        pass  # one run has been completed at this point !
