from datadog_checks.base import OpenMetricsBaseCheckV2
from datadog_checks.celerdata.metrics import METRIC_MAP, SLOW_LOCK_SUMMARIES


class CelerdataCheck(OpenMetricsBaseCheckV2):
    __NAMESPACE__ = "celerdata"

    def __init__(self, name, init_config, instances):
        super(CelerdataCheck, self).__init__(name, init_config, instances)

    def get_default_config(self):
        """
        Returns the default OpenMetrics configuration.
        """
        return {
            "metrics": [METRIC_MAP],
            "exclude_metrics": [r".*8060.*"],
        }

    def configure_scrapers(self):
        """
        Register the slow-lock summary transformer on every scraper.

        See `SLOW_LOCK_SUMMARIES` in `metrics.py` for why these summaries bypass `METRIC_MAP`.
        """
        super().configure_scrapers()

        for scraper in self.scrapers.values():
            for raw_name in SLOW_LOCK_SUMMARIES:
                scraper.metric_transformer.add_custom_transformer(raw_name, self._submit_slow_lock_summary)

    def _submit_slow_lock_summary(self, metric, sample_data, runtime_data):
        """
        Submit a StarRocks slow-lock summary, omitting its unusable `_sum` sample.

        Mirrors the native summary transformer for quantiles and `_count`, but drops `_sum`,
        which StarRocks derives from a sliding window and which therefore is not monotonic.
        """
        metric_name = SLOW_LOCK_SUMMARIES[metric.name]

        for sample, tags, hostname in sample_data:
            if sample.name.endswith("_sum"):
                continue

            if sample.name.endswith("_count"):
                self.monotonic_count(
                    f"{metric_name}.count",
                    sample.value,
                    tags=tags,
                    hostname=hostname,
                    flush_first_value=runtime_data["flush_first_value"],
                )
            else:
                self.gauge(f"{metric_name}.quantile", sample.value, tags=tags, hostname=hostname)
