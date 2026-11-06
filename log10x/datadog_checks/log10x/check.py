# (C) Datadog, Inc. 2026-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from datadog_checks.base import OpenMetricsBaseCheckV2

from .metrics import METRIC_MAP


class Log10xCheck(OpenMetricsBaseCheckV2):
    # This will be the prefix of every metric the integration sends
    __NAMESPACE__ = 'log10x'
    DEFAULT_METRIC_LIMIT = 0

    def __init__(self, name, init_config, instances):
        super(Log10xCheck, self).__init__(name, init_config, instances)

    def get_default_config(self):
        return {
            'metrics': [METRIC_MAP],
            # Neither label adds identity, so dropping them never merges series.
            # `tenx_hash` is the hash of the `message_pattern` value, one hash per
            # pattern name. `tenx_pipeline_uuid` is the scraped process's id, one value
            # per endpoint; engines since 1.1.140 no longer put it on these metrics.
            'exclude_labels': ['tenx_pipeline_uuid', 'tenx_hash'],
        }

    def check(self, instance):
        # Emitted on every run, whether or not the engine is reachable or any event has
        # flowed, so the integration itself is always visible.
        self.gauge('check.up', 1)
        super().check(instance)
