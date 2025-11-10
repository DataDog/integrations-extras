from typing import Any
from datadog_checks.base import AgentCheck
import re

class StonebranchCheck(AgentCheck):
    __NAMESPACE__ = 'stonebranch'

    def __init__(self, name, init_config, instances):
        super(StonebranchCheck, self).__init__(name, init_config, instances)
        self.url = self.instance.get("url")
        self.username = self.instance.get("username")
        self.password = self.instance.get("password")
        self.verify_ssl = self.instance.get("verify_ssl", True)
        self.timeout = self.instance.get("timeout", 30)
        self.max_metrics = self.instance.get("max_metrics", 10000)

    def check(self, _):
        try:
            if self.url:
                self._check_api_connectivity()
            self.service_check('stonebranch_uc.can_connect', self.OK)
        except Exception as e:
            self.service_check('stonebranch_uc.can_connect', self.CRITICAL, message=str(e))
            self.log.error(f"Stonebranch check failed: {e}")
            raise

    def _check_api_connectivity(self):
        try:
            base_url = self.url.rstrip('/').replace('/resources/metrics', '')
            metrics_url = f"{base_url}/resources/metrics"
            self.log.debug(f"Attempting to connect to metrics endpoint: {metrics_url}")

            response = self.http.get(
                metrics_url,
                auth=(self.username, self.password),
                verify=self.verify_ssl,
                timeout=self.timeout
            )
            response.raise_for_status()

            self.gauge('stonebranch.api.response_time', response.elapsed.total_seconds())
            self.gauge('stonebranch.api.status_code', response.status_code)
            self.gauge('stonebranch.api.available', 1)

            metrics_count = self._process_prometheus_metrics(response.text)
            self.gauge('stonebranch.metrics.collected', metrics_count)
            self.log.info(f"Successfully collected {metrics_count} metrics from UC")
        except Exception as e:
            self.gauge('stonebranch.api.available', 0)
            self.log.error(f"Failed to connect to UC metrics endpoint: {e}")
            raise

    def _process_prometheus_metrics(self, metrics_text):
        """Process Prometheus-format metrics from UC, honoring TYPE comments."""
        metrics_count = 0
        lines_processed = 0
        metric_types = {}  # name -> "counter" | "gauge" | etc

        for line in metrics_text.splitlines():
            line = line.strip()
            lines_processed += 1

            # Capture TYPE declarations
            if line.startswith('# TYPE'):
                parts = line.split()
                if len(parts) >= 4:
                    _, _, name, mtype = parts[:4]
                    metric_types[name] = mtype
                continue

            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue

            # Prevent metric explosion
            if metrics_count >= self.max_metrics:
                self.log.warning(f"Reached maximum metric limit ({self.max_metrics}), stopping processing")
                break

            try:
                # Tokenize
                segments = line.split()
                if len(segments) < 2:
                    continue

                # Drop trailing UNIX timestamp tokens
                if segments[-1].isdigit() and len(segments[-1]) >= 10:
                    segments.pop()

                # Last token is the metric value
                value_str = segments[-1]
                metric_part = ' '.join(segments[:-1])

                # Convert to float
                try:
                    value = float(value_str)
                except ValueError:
                    self.log.debug(f"Skipping non-numeric value: {value_str} for metric: {metric_part}")
                    continue

                # Skip infinities/NaN
                if value == float('inf') or value == float('-inf') or value != value:
                    self.log.debug(f"Skipping infinite/NaN value: {value} for metric: {metric_part}")
                    continue

                # Extract name & labels
                if '{' in metric_part and '}' in metric_part:
                    metric_name, labels_str = metric_part.split('{', 1)
                    labels_str = labels_str.rstrip('}')
                    labels = self._parse_labels(labels_str)
                else:
                    metric_name = metric_part
                    labels = {}

                # Remove duplicate namespace
                prefix = f"{self.__NAMESPACE__}."
                if metric_name.startswith(prefix):
                    metric_name = metric_name[len(prefix):]

                if not metric_name:
                    continue

                # Build tags
                tags = self._create_tags_from_labels(labels)

                # Emit using the correct type
                mtype = metric_types.get(metric_name, 'gauge')
                if mtype == 'counter':
                    # count() reports monotonic counters
                    self.count(metric_name, value, tags=tags)
                else:
                    # default to gauge
                    self.gauge(metric_name, value, tags=tags)

                metrics_count += 1

            except Exception as e:
                self.log.debug(f"Skipping invalid metric line: {line[:100]} - {e}")
                continue

        self.log.debug(f"Processed {lines_processed} lines, emitted {metrics_count} metrics")
        return metrics_count

    def _create_tags_from_labels(self, labels):
        tags = []
        for key, val in labels.items():
            if not key:
                continue
            cleaned = self._clean_tag_value(str(val))
            if cleaned:
                tags.append(f"{key}:{cleaned}")
        return tags

    def _clean_tag_value(self, value):
        cleaned = (value.replace('"', '')
                        .replace(' ', '_')
                        .replace('/', '_')
                        .replace(':', '_')
                        .replace('\\', '_')
                        .replace('\n', '_')
                        .replace('\r', '_')
                        .replace('\t', '_'))
        cleaned = cleaned.strip('_-.')
        return cleaned[:200] if len(cleaned) > 200 else cleaned

    def _parse_labels(self, labels_str):
        labels = {}
        if not labels_str:
            return labels
        try:
            pattern = r'(\w+)="([^"\\]*(?:\\.[^"\\]*)*)"'
            for key, val in re.findall(pattern, labels_str):
                labels[key] = val.replace('\\"', '"').replace('\\\\', '\\')
            if not labels:
                labels = self._parse_labels_fallback(labels_str)
        except Exception:
            labels = self._parse_labels_fallback(labels_str)
        return labels

    def _parse_labels_fallback(self, labels_str):
        labels = {}
        current_key = None
        current_val = ''
        in_quotes = False
        for char in labels_str + ',':
            if char == '"':
                in_quotes = not in_quotes
            elif char == '=' and not in_quotes and current_key is None:
                current_key = current_val.strip()
                current_val = ''
            elif char == ',' and not in_quotes:
                if current_key:
                    labels[current_key] = current_val.strip().strip('"')
                    current_key = None
                current_val = ''
            else:
                current_val += char
        return labels
