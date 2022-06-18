from datadog_checks.base import OpenMetricsBaseCheckV2
from datadog_checks.gitea.config_models import ConfigMixin
from datadog_checks.gitea.metrics import METRIC_MAP


class GiteaCheck(OpenMetricsBaseCheckV2, ConfigMixin):
    __NAMESPACE__ = "gitea"

    def get_default_config(self):
        return {
            "metrics": [METRIC_MAP],
            "rename_labels": {"version": "go-version"},
        }
