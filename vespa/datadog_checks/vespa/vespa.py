import logging
from datadog_checks.base import AgentCheck
from datadog_checks.base.errors import CheckException
from requests.exceptions import Timeout, HTTPError, InvalidURL, ConnectionError
from simplejson import JSONDecodeError

logging.basicConfig(level=logging.INFO)


class VespaCheck(AgentCheck):

    METRICS_SERVICE_CHECK = 'vespa.metrics_health'
    PROCESS_SERVICE_CHECK = 'vespa.process_health'
    VESPA_SERVICE_TAG = 'vespa-service:'
    URL = 'http://localhost:19092/metrics/v1/values'

    metric_count = 0
    services_up = 0

    def check(self, instance):
        self.metric_count = 0
        self.services_up = 0

        instance_tags = instance.get('tags', [])
        consumer = instance.get('consumer')
        if not consumer:
            raise CheckException("The consumer must be specified in the configuration.")
        url = self.URL + '?consumer=' + consumer
        try:
            json = self._get_metrics_json(url)
            if 'services' not in json:
                self.service_check(self.METRICS_SERVICE_CHECK, AgentCheck.WARNING, tags=instance_tags,
                                   message="No services in response from metrics proxy on {}".format(url))
                return

            for service in json['services']:
                service_name = service['name']
                self._report_service_status(instance_tags, service_name, service)
                for metrics in service['metrics']:
                    self._emit_metrics(service_name, metrics, instance_tags)

            self.log.info("Forwarded %s metrics to hq for %s services", self.metric_count, self.services_up)
            self.service_check(self.METRICS_SERVICE_CHECK, AgentCheck.OK, tags=instance_tags)
        except Timeout as e:
            self._report_metrics_error("Timed out connecting to Vespa's node metrics api: {}".format(e),
                                       AgentCheck.CRITICAL, instance_tags)
        except (HTTPError, InvalidURL, ConnectionError) as e:
            self._report_metrics_error("Could not connect to Vespa's node metrics api: {}".format(e),
                                       AgentCheck.CRITICAL, instance_tags)
        except JSONDecodeError as e:
            self._report_metrics_error("Error parsing JSON from Vespa's node metrics api: {}".format(e),
                                       AgentCheck.CRITICAL, instance_tags)
        except Exception as e:
            self._report_metrics_error("Unexpected error: {}".format(e),
                                       AgentCheck.WARNING, instance_tags)

    def _report_metrics_error(self, msg, level, instance_tags):
        self.log.warning(msg)
        self.service_check(self.METRICS_SERVICE_CHECK, level, tags=instance_tags,
                           message=msg if level != self.OK else "")
        self.service_check(self.PROCESS_SERVICE_CHECK, AgentCheck.WARNING, tags=instance_tags,
                           message="Problem getting metrics from Vespa's node metrics api")
        self.log.warning("Issued a warning to " + self.PROCESS_SERVICE_CHECK +
                         " service check, as there is a problem getting metrics from Vespa.")

    def _emit_metrics(self, service_name, metrics_elem, instance_tags):
        """
        Emit one metrics packet, which consists of a set of metrics that share the same set of dimensions.
        :param metrics_elem: A (values, dimensions) tuple from the 'metrics' json array.
        """
        if 'values' not in metrics_elem:
            return
        metric_tags = self._get_tags(metrics_elem, service_name)
        for name, value in metrics_elem['values'].items():
            full_name = "vespa." + name
            self._emit_metric(full_name, value, metric_tags + instance_tags)

    def _emit_metric(self, name, value, tags):
        self.log.debug("Emitting metric: %s, dimensions: %s", name, tags)
        self.gauge(name, value, tags)
        self.metric_count += 1

    def _get_metrics_json(self, url):
        """ Send rest request to metrics api and return the response as JSON
        """
        self.log.info("Sending request to %s", url)
        response = self.http.get(url)
        response.raise_for_status()
        return response.json()

    def _get_tags(self, metrics_elem, service_name):
        """
        Returns the tags from the dimensions in the given metrics element, or an empty array if there are no dimensions.
        :param metrics_elem: A (values, dimensions) tuple from the 'metrics' json array.
        """
        tags = []
        if 'dimensions' in metrics_elem:
            dimensions = metrics_elem['dimensions']
            for dim, dim_val in dimensions.items():
                tags.append(dim + ":" + dim_val)
        tags.append(self.VESPA_SERVICE_TAG + service_name)
        return tags

    def _report_service_status(self, instance_tags, service_name, service):
        code = service["status"]["code"]
        description = service["status"]["description"]
        tags = []
        if 'metrics' in service:
            tags = self._get_tags(service['metrics'][0], service_name)

        tags = tags + instance_tags
        if code == "up":
            self.service_check(self.PROCESS_SERVICE_CHECK, AgentCheck.OK, tags=tags)
            self.services_up += 1
        elif code == "down":
            self.service_check(self.PROCESS_SERVICE_CHECK, AgentCheck.CRITICAL, tags=tags,
                               message="Service {} reports down: {}".format(service_name, description))
            self.log.warning("Service %s reports down: %s", service_name, description)
        else:
            self.service_check(self.PROCESS_SERVICE_CHECK, AgentCheck.WARNING, tags=tags,
                               message="Service {} reports unknown status: {}".format(service_name, description))
            self.log.warning("Service %s reports unknown status: %s", service_name, description)
