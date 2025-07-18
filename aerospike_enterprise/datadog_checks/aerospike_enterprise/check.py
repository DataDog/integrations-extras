# (C) Datadog, Inc. 2022-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import re
from collections import defaultdict

from datadog_checks.base import OpenMetricsBaseCheckV2

from .config_models import ConfigMixin
from .metrics import METRIC_NAME_PATTERN

RENAMED_LABELS = {"cluster_name": "aerospike_cluster", "service": "aerospike_service"}


class AerospikeEnterpriseCheck(OpenMetricsBaseCheckV2, ConfigMixin):
    __NAMESPACE__ = "aerospike"

    DEFAULT_METRIC_LIMIT = 0

    def __init__(self, name, init_config, instances):
        super().__init__(name, init_config, instances)

        self.check_initializations.append(self.configure_additional_transformers)

    def get_default_config(self):
        config = {
            "rename_labels": RENAMED_LABELS,
        }

        return config

    def configure_additional_transformers(self):
        # we are setting up the transformer for the metrics that are defined in the METRIC_NAME_PATTERN
        # Objective is to apply transformer to rename metric in datadog standard pattern
        # so we dont need to add a static mapping for each metric
        # Example:
        # aerospike_namespace_master_objects -> aerospike.namespace.master_objects

        for metric, data in METRIC_NAME_PATTERN.items():
            self.scrapers[self.instance["openmetrics_endpoint"]].metric_transformer.add_custom_transformer(
                metric,
                self.configure_transformer_for_metric(metric, **data),
                pattern=True,
            )

    def configure_transformer_for_metric(self, metric_pattern, metric_type):
        # We are doing this to modify the exporter metric-name to datadog standard pattern
        # exporter metric-name pattern: aerospike_namespace_master_objects
        # datadog metric-name pattern: aerospike.namespace.master_objects

        # Datadog counter is a monitonic_counter, which always gives delta between current and previous values
        method = getattr(self, metric_type)  # Always use gauge
        cached_patterns = defaultdict(lambda: re.compile(metric_pattern))

        def transform(metric, sample_data, runtime_data):
            for sample, tags, hostname in sample_data:
                new_metric_name = sample.name

                # Remove _total suffix if present
                if new_metric_name.endswith("_total"):
                    new_metric_name = new_metric_name[:-6]

                match = cached_patterns[metric_pattern].match(new_metric_name)

                if match:
                    new_metric_name = f"{match.groups(1)[0]}.{match.groups(1)[1]}"
                    method(new_metric_name, sample.value, tags=tags, hostname=hostname)
                else:
                    method(new_metric_name, sample.value, tags=tags, hostname=hostname)

        return transform
