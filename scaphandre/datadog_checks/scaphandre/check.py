# (C) Datadog, Inc. 2024-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from datadog_checks.base import OpenMetricsBaseCheckV2

from .config_models import ConfigMixin
from .metrics import METRIC_MAP, RENAME_LABELS_MAP

SCAPHANDRE_VERSION = {'scaph_self_version': {'name': 'version'}}


class ScaphandreCheck(OpenMetricsBaseCheckV2, ConfigMixin):
    DEFAULT_METRIC_LIMIT = 0
    __NAMESPACE__ = 'scaphandre'

    def __init__(self, name, init_config, instances):
        super(ScaphandreCheck, self).__init__(name, init_config, instances)
        self.check_initializations.appendleft(self._configure_additional_transformers)
        self.check_initializations.append(self.get_default_config)

    def get_default_config(self):
        metrics = [METRIC_MAP]
        metrics.append(SCAPHANDRE_VERSION)
        return {
            'metrics': metrics,
            'rename_labels': RENAME_LABELS_MAP,
        }

    def _configure_additional_transformers(self):
        self.scrapers = {}
        self.scrapers[self.instance['openmetrics_endpoint']] = self.create_scraper(self.instance)
        metric_transformer = self.scrapers[self.instance['openmetrics_endpoint']].metric_transformer
        metric_transformer.add_custom_transformer('scaph_self_version', self.configure_version_metadata_transformer)

    def configure_version_metadata_transformer(self, metric, sample_data):
        for sample, *_ in sample_data:
            SCAPHANDRE_VERSION['scaph_self_version']['type'] = 'metadata'
            SCAPHANDRE_VERSION['scaph_self_version']['label'] = sample.value
