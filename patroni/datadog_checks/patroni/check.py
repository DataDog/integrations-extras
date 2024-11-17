# (C) Datadog, Inc. 2022-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import time
from collections import ChainMap
import requests
import json
import os

from datadog_checks.base import ConfigurationError, OpenMetricsBaseCheckV2
from datadog_checks.base.checks.openmetrics.v2.scraper import (
    OpenMetricsCompatibilityScraper,
)

from .metrics import (
    ALERT_TYPE_INFO,
    API_METRICS,
    ENDPOINTS,
    METRIC_MAP,
    construct_metrics_config,
)


class PatroniCheck(OpenMetricsBaseCheckV2):
    DEFAULT_METRIC_LIMIT = 0
    STATE_FILE = "/tmp/patroni_check_state.json"

    def __init__(self, name, init_config, instances):
        super(PatroniCheck, self).__init__(name, init_config, instances)
        self.check_initializations.appendleft(self._parse_config)
        self.previous_leader = None

    def _parse_config(self):
        self.scraper_configs = []
        self.base_url = self.instance.get("openmetrics_endpoint")
        if self.base_url.endswith("/metrics"):
            self.base_url = self.base_url.rstrip("/metrics")
        patroni_namespace = self.instance.get("namespace", "patroni")
        self.scraper_configs.append(
            self._generate_config(self.base_url, METRIC_MAP, patroni_namespace)
        )

    def _generate_config(self, endpoint, metrics, namespace):
        metrics = construct_metrics_config(metrics)
        metrics.append(METRIC_MAP)
        config = {
            "openmetrics_endpoint": endpoint,
            "metrics": metrics,
            "namespace": namespace,
        }
        config.update(self.instance)
        return config

    def load_state(self):
        """Load shared state from a file."""
        if os.path.exists(self.STATE_FILE):
            try:
                with open(self.STATE_FILE, "r") as f:
                    state = json.load(f)
                    self.previous_leader = state.get("previous_leader", None)
                    self.log.debug(
                        "Loaded previous leader from state file: %s",
                        self.previous_leader,
                    )
            except Exception as e:
                self.log.error("Failed to load state from file: %s", e)
                self.previous_leader = None
        else:
            self.previous_leader = None

    def save_state(self):
        """Save shared state to a file."""
        try:
            with open(self.STATE_FILE, "w") as f:
                json.dump({"previous_leader": self.previous_leader}, f)
            self.log.debug(
                "Saved previous leader to state file: %s", self.previous_leader
            )
        except Exception as e:
            self.log.error("Failed to save state to file: %s", e)

    def get_config_with_defaults(self, config):
        return ChainMap(
            config,
            {"metrics": config.pop("metrics"), "namespace": config.pop("namespace")},
        )

    def check(self, instance):
        self.load_state()
        super().check(instance)
        self.process_custom_metrics(instance)

    def process_custom_metrics(self, instance):
        """
        Process the scraped metrics to calculate custom values (e.g., dcs.last_seen).
        """
        self.log.debug("Starting process_custom_metrics")

        for endpoint, scraper in self.scrapers.items():  # Access the scraper instances
            self.log.debug("Processing metrics from scraper: %s", endpoint)
            runtime_data = {}
            for metric in scraper.consume_metrics(runtime_data):
                if metric.name == "patroni_dcs_last_seen":
                    try:
                        # Extract the current time and calculate the difference
                        current_time = int(time.time())
                        last_seen_time = int(metric.samples[0].value)
                        time_diff = current_time - last_seen_time

                        parsed_tags = [
                            f"{key}:{value}"
                            for key, value in metric.samples[0].labels.items()
                        ]
                        for tag in scraper.static_tags:
                            parsed_tags.append(tag)
                        self.gauge(
                            "patroni.dcs_last_seen_diff",
                            time_diff,
                            tags=parsed_tags,
                        )
                    except Exception as e:
                        self.log.error("Error processing dcs.last_seen: %s", str(e))
                elif (
                    metric.name == "patroni_primary" and metric.samples[0].value == 1.0
                ):
                    try:
                        parsed_tags = {
                            f"{key}": f"{value}"
                            for key, value in metric.samples[0].labels.items()
                        }
                        self.handle_failover_event(parsed_tags["name"])
                    except Exception as e:
                        self.log.error("Error processing primary: %s", str(e))

    def handle_failover_event(self, current_leader):
        """Checks for a leader change and submits a Datadog event if a failover occurred."""
        if current_leader != self.previous_leader:
            if self.previous_leader is not None:
                self.event(
                    {
                        "msg_title": "Patroni Failover Detected",
                        "msg_text": f"Failover occurred: Leader changed from {self.previous_leader} to {current_leader}",
                        "alert_type": "info",
                        "source_type_name": "patroni",
                        "tags": [
                            f"previous_leader:{self.previous_leader}",
                            f"new_leader:{current_leader}",
                        ],
                    }
                )
            # Update the previous leader to the current one
            self.log.debug("Setting current leader: %s", current_leader)
            self.previous_leader = current_leader
            self.save_state()
