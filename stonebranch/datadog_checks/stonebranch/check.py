from __future__ import annotations

from typing import Any

from datadog_checks.base import ConfigurationError, OpenMetricsBaseCheckV2

from .metrics import ADDITIONAL_METRICS, DEFAULT_METRICS


class StonebranchCheck(OpenMetricsBaseCheckV2):
    __NAMESPACE__ = "stonebranch"

    def __init__(self, name, init_config, instances):
        super().__init__(name, init_config, instances)
        self.instance.setdefault("tls_verify", True)
        self.check_initializations.appendleft(self._parse_config)

    def _parse_config(self) -> None:
        self.scraper_configs = []

        endpoint = self.instance.get("openmetrics_endpoint")
        if not endpoint:
            raise ConfigurationError("`openmetrics_endpoint` must be set")

        user_metrics = self.instance.get("metrics")

        # Precedence:
        # 1) explicit allowlist `metrics` (override)
        # 2) DEFAULT_METRICS + opt-in metric_groups - exclude_metric_names
        if user_metrics:
            metrics = self._coerce_metrics(user_metrics)
        else:
            metrics = list(DEFAULT_METRICS)

            groups = self.instance.get("metric_groups") or []
            for group in groups:
                if group not in ADDITIONAL_METRICS:
                    raise ConfigurationError(f"invalid group in metric_groups: {group}")
                metrics.extend(ADDITIONAL_METRICS[group])

            excludes = set(self.instance.get("exclude_metric_names") or [])
            if excludes:
                metrics = [m for m in metrics if next(iter(m.keys())) not in excludes]

        # Build config: start with instance pass-through, then enforce computed fields
        config: dict[str, Any] = dict(self.instance)
        config.update(
            {
                "openmetrics_endpoint": endpoint,
                "namespace": self.__NAMESPACE__,
                "metrics": metrics,
                "metadata_label_map": {
                    "build": "build",
                    "build_date": "build_date",
                    "release": "release",
                },
            }
        )

        self.scraper_configs.append(config)

    @staticmethod
    def _coerce_metrics(value: Any) -> list[dict[str, str]]:
        """
        Accept either:
        - list[str] (metric names) -> convert to OpenMetrics mapping format
        - list[dict] (OpenMetrics v2 mappings) -> pass through
        """
        if isinstance(value, list) and all(isinstance(x, str) for x in value):
            return [{n: n} for n in value]
        if isinstance(value, list) and all(isinstance(x, dict) for x in value):
            return value

        raise ConfigurationError(
            "`metrics` must be a list of metric names (strings) or a list of OpenMetrics mappings (dicts)"
        )
