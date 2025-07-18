import requests
from datadog_checks.base import AgentCheck, ConfigurationError
from prometheus_client.parser import text_string_to_metric_families

class StonebranchUniversalControllerCheck(AgentCheck):
    def check(self, instance):
        url = instance.get('url')
        username = instance.get('username')
        password = instance.get('password')
        disable_tags = instance.get('disable_tags', False)
        labels_to_include = instance.get('labels_to_include', [])

        if not url:
            raise ConfigurationError("Missing 'url' in configuration for Stonebranch check")

        # Fetch the Prometheus endpoint
        try:
            response = requests.get(url, auth=(username, password), timeout=10)
            response.raise_for_status()
        except Exception as e:
            self.service_check("stonebranch_uc.can_connect", self.CRITICAL, message=str(e))
            self.log.error("Request to %s failed: %s", url, e)
            return

        # Mark service check OK
        self.service_check("stonebranch_uc.can_connect", self.OK)

        # Parse and submit metrics
        for family in text_string_to_metric_families(response.text):
            for sample in family.samples:
                prom_name, labels, value = sample.name, sample.labels, sample.value

                # Build the Datadog metric name
                dd_metric_name = f"stonebranch_uc.{prom_name}"

                # Build tags according to disable_tags / labels_to_include
                if disable_tags:
                    tags = []
                elif labels_to_include:
                    # only include requested labels
                    tags = [f"{k}:{v}" for k, v in labels.items() if k in labels_to_include]
                else:
                    # include *all* labels
                    tags = [f"{k}:{v}" for k, v in labels.items()]

                # Submit as a gauge (or counter if you prefer)
                self.gauge(dd_metric_name, value, tags=tags)
