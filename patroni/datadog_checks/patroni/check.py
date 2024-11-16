# (C) Datadog, Inc. 2022-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import time
from collections import ChainMap
import requests

from datadog_checks.base import ConfigurationError, OpenMetricsBaseCheckV2
from datadog_checks.base.checks.openmetrics.v2.scraper import OpenMetricsCompatibilityScraper

from .metrics import ALERT_TYPE_INFO, API_METRICS, ENDPOINTS, METRIC_MAP, construct_metrics_config



class PatroniCheck(OpenMetricsBaseCheckV2):
    DEFAULT_METRIC_LIMIT = 0

    def __init__(self, name, init_config, instances):
        super(PatroniCheck, self).__init__(name, init_config, instances)
        self.check_initializations.appendleft(self._parse_config)

    def _parse_config(self):
        self.scraper_configs = []
        base_url = self.instance.get("openmetrics_endpoint")
        if base_url.endswith("/metrics"):
            base_url = base_url.rstrip("/metrics")
        patroni_namespace = self.instance.get("namespace", "patroni")
        self.scraper_configs.append(self._generate_config(base_url, METRIC_MAP, patroni_namespace))

    def check(self, instance):
        # Call the parent OpenMetrics scraping logic
        super().check(instance)

        # Process custom metrics after scraping
        self.process_custom_metrics()


    def process_custom_metrics(self):
        """
        Process the scraped metrics to calculate custom values (e.g., dcs.last_seen).
        """
        self.log.debug("Starting process_custom_metrics")

        for endpoint, scraper in self.scrapers.items():  # Access the scraper instances
            self.log.debug("Processing metrics from scraper: %s", endpoint)
            runtime_data = {}
            self.log.debug("scarper obj is %s", scraper)
            for metric in scraper.consume_metrics(runtime_data):
                if metric.name == "patroni_dcs_last_seen":
                    self.log.debug("scarper consume is %s", scraper.consume_metrics(runtime_data))
                    #metric_par
                    # Log the metric data for debugging
                    self.log.debug("Found metric: %s with samples: %s, sameple type is %s", metric.name, metric.samples, type(metric.samples[0]))
                    #self.log.debug("Metric value is %s for metric %s", metric.name, metric.value)
                    try:
                        # Extract the current time and calculate the difference
                        current_time = int(time.time())
                        last_seen_time = int(metric.samples[0].value)
                        time_diff = current_time - last_seen_time

                        self.log.debug("metric labels are %s of type %s", metric.samples[0].labels, type(metric.samples[0].labels))

                        parsed_tags = [f"{key}:{value}" for key, value in metric.samples[0].labels.items()]
                        for tag in scraper.static_tags:
                            parsed_tags.append(tag)
                        self.log.debug("parsed tags = %s of type %s", parsed_tags, type(parsed_tags))
                        self.gauge(
                            "patroni.dcs_last_seen_diff",
                            time_diff,
                            tags=parsed_tags,
                        )
                        self.log.debug(
                            "Submitted patroni.dcs_last_seen_diff: Current time: %s, Last seen: %s, Diff: %s",
                            current_time,
                            last_seen_time,
                            time_diff,
                        )
                    except Exception as e:
                        self.log.error("Error processing dcs.last_seen: %s", str(e))



    def _generate_config(self, endpoint, metrics, namespace):
        metrics = construct_metrics_config(metrics)
        metrics.append(METRIC_MAP)
        config = {
            'openmetrics_endpoint': endpoint,
            'metrics': metrics,
            'namespace': namespace,
        }
        config.update(self.instance)
        return config


    def get_config_with_defaults(self, config):
        return ChainMap(config, {'metrics': config.pop('metrics'), 'namespace': config.pop('namespace')})

