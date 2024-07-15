import copy
from urllib.parse import urljoin, urlparse

from datadog_checks.base import AgentCheck, OpenMetricsBaseCheckV2

from .metrics import DEFAULT_METRICS


class QdrantCheck(OpenMetricsBaseCheckV2):
    """AwesomeCheck derives from AgentCheck, and provides the required check method."""

    __NAMESPACE__ = "qdrant"
    DEFAULT_METRIC_LIMIT = 0

    ALLOWED_SERVICE_CHECKS = ["readyz", "livez"]

    def check(self, instance):
        self._base_url = self._get_base_url(instance)
        self.tags = self.instance.get("tags", [])
        if self._base_url:
            super().check(instance)
            self._submit_version_metadata()
            for check_type in self.ALLOWED_SERVICE_CHECKS:
                self._check_health_endpoint(check_type)

    def get_default_config(self):
        return {"metrics": [DEFAULT_METRICS]}

    def _check_health_endpoint(self, check_type):
        service_check_name = f"{check_type}.status"
        check_url = urljoin(self._base_url, check_type)
        tags = copy.deepcopy(self.tags)
        tags.append(f"qdrant_{check_type}_url:{check_url}")

        response = self.http.get(check_url)
        if response.ok:
            self.service_check(service_check_name, AgentCheck.OK, tags)
        else:
            self.service_check(service_check_name, AgentCheck.CRITICAL, tags)
        self.log.debug("qdrant health check %s succeeded", check_type)

    @AgentCheck.metadata_entrypoint
    def _submit_version_metadata(self):
        endpoint = self._get_base_url(self.instance)
        response = self.http.get(endpoint)

        if response.ok:
            data = response.json()
            version = data.get("version", "")
            version_split = version.split(".")
            if len(version_split) >= 3:
                major, minor, patch = version_split[:3]

                version_parts = {
                    "major": major,
                    "minor": minor,
                    "patch": patch,
                }
                self.set_metadata("version", version, scheme="semver", part_map=version_parts)
            else:
                self.log.debug("Invalid Qdrant version format: %s", version)
        else:
            self.log.debug("Could not retrieve version metadata from host.")

    def _get_base_url(self, instance):
        if openmetrics_endpoint := instance.get("openmetrics_endpoint"):
            url = urlparse(openmetrics_endpoint)
            return f"{url.scheme}://{url.netloc}/"
        else:
            return None
