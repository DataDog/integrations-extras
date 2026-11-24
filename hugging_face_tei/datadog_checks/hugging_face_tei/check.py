from datadog_checks.base import OpenMetricsBaseCheckV2

from .metrics import METRIC_MAP, RENAME_LABELS_MAP


class HuggingFaceTeiCheck(OpenMetricsBaseCheckV2):
    __NAMESPACE__ = 'hugging_face_tei'
    DEFAULT_METRIC_LIMIT = 0

    def get_default_config(self):
        return {
            'metrics': [METRIC_MAP],
            'rename_labels': RENAME_LABELS_MAP,
        }
