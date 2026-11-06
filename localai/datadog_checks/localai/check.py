from datadog_checks.base import OpenMetricsBaseCheckV2

from .metrics import EXCLUDE_LABELS, METRIC_MAP, RENAME_LABELS_MAP


class LocalAICheck(OpenMetricsBaseCheckV2):
    __NAMESPACE__ = 'localai'
    DEFAULT_METRIC_LIMIT = 0

    def get_default_config(self):
        return {
            'metrics': [METRIC_MAP],
            'rename_labels': RENAME_LABELS_MAP,
            'exclude_labels': EXCLUDE_LABELS,
            # LocalAI compresses `/metrics` twice when the client accepts gzip
            # (the HTTP compression middleware wraps the already compressed
            # promhttp response), so ask for an uncompressed response.
            'extra_headers': {'Accept-Encoding': 'identity'},
        }
