from datadog_checks.base import OpenMetricsBaseCheckV2

from .metrics import METRIC_MAP


class Resilience4jCheck(OpenMetricsBaseCheckV2):
    """Datadog Check for monitoring Resilience4j metrics via OpenMetrics."""

    __NAMESPACE__ = "resilience4j"
    DEFAULT_METRIC_LIMIT = 0  # Set an appropriate default metric limit.

    def __init__(self, name, init_config, instances):
        """Initialize the Resilience4jCheck with given configurations."""
        super().__init__(name, init_config, instances)

    def check(self, _):
        """Collect health/microservice metrics from Resilience4j's HTTP endpoint."""
        health_endpoint = self.instance.get('openmetrics_endpoint', '')

        if not health_endpoint:
            self.log.error("The 'openmetrics_endpoint' is not configured for this instance.")
            self.count("openmetrics.health", 0)
            return

        try:
            # Attempt to fetch the health endpoint response
            response = self.http.get(health_endpoint)
            response.raise_for_status()

            # Fetch metrics line by line from Prometheus output
            metrics_data = response.text.splitlines()
            for line in metrics_data:
                # Parse each metric line and map it based on METRIC_MAP
                for raw_metric, standardized_metric in METRIC_MAP.items():
                    if raw_metric in line:
                        # Extract value and tags (if available)
                        metric_value = self._extract_metric_value(line)
                        tags = self._extract_metric_tags(line)
                        self.gauge(standardized_metric, metric_value, tags=tags)

            # Report a healthy endpoint if all metrics were processed successfully
            self.count("openmetrics.health", 1)
            self.log.debug("Health endpoint '%s' is reachable.", health_endpoint)

        except Exception as error:
            # Log an error and record an unreachable status metric
            self.log.error(
                "Cannot connect to Resilience4j diagnostic HTTP endpoint '%s': %s",
                health_endpoint,
                error,
            )
            self.count("openmetrics.health", 0)
            raise

        # Call the parent class's check for metric collection
        super().check(_)


def _extract_metric_value(metric_line):
    """
    Extract the numeric value from a Prometheus metric line.
    Assumes Prometheus-style formatting: metric_name{tag1="value"} value
    """
    try:
        return float(metric_line.split()[-1])
    except (IndexError, ValueError):
        return 0.0


def _extract_metric_tags(metric_line):
    """
    Extract tags from a Prometheus metric line.
    Returns a list of tag strings in the form key:value.
    """
    if "{" in metric_line and "}" in metric_line:
        raw_tags = metric_line.split("{")[1].split("}")[0]
        return [tag.replace("=", ":") for tag in raw_tags.split(",")]
    return []
