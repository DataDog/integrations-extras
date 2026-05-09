"""Run EdenCheck against a local eden-service without installing the Datadog Agent.

Usage:
    EDEN_URL=http://localhost:8000 \
    EDEN_ORG_ID=TestOrg \
    EDEN_ROBOT_USERNAME=datadog-agent \
    EDEN_ROBOT_API_KEY=... \
    python integrations/eden/tests/run_local.py
"""

import os
import sys
import types
from pprint import pprint

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
PKG_ROOT = os.path.dirname(HERE)
sys.path.insert(0, PKG_ROOT)


class _ConfigurationError(Exception):
    pass


class _StubAgentCheck:
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3

    def __init__(self, name, init_config, instances):
        self.name = name
        self.instances = instances
        self.submitted = []
        self.service_checks = []
        self.http = _Http()
        self._cache = {}

    def gauge(self, metric, value, tags=None):
        self.submitted.append(("gauge", metric, value, tuple(tags or [])))

    def monotonic_count(self, metric, value, tags=None):
        self.submitted.append(("monotonic_count", metric, value, tuple(tags or [])))

    def count(self, metric, value, tags=None):
        self.submitted.append(("count", metric, value, tuple(tags or [])))

    def service_check(self, name, status, message=None, tags=None):
        self.service_checks.append((name, status, message, tuple(tags or [])))

    def read_persistent_cache(self, key):
        return self._cache.get(key, "")

    def write_persistent_cache(self, key, value):
        self._cache[key] = value


class _Http:
    def __init__(self):
        self._session = requests.Session()

    def get(self, url, params=None, extra_headers=None):
        return self._session.get(url, params=params, headers=extra_headers, timeout=15)

    def post(self, url, json=None, extra_headers=None):
        return self._session.post(url, json=json, headers=extra_headers, timeout=15)


base_module = types.ModuleType("datadog_checks.base")
base_module.AgentCheck = _StubAgentCheck
base_module.ConfigurationError = _ConfigurationError

datadog_pkg = types.ModuleType("datadog_checks")
datadog_pkg.__path__ = [PKG_ROOT + "/datadog_checks"]
datadog_pkg.base = base_module

sys.modules["datadog_checks"] = datadog_pkg
sys.modules["datadog_checks.base"] = base_module

from datadog_checks.eden.check import EdenCheck  # noqa: E402

INSTANCE = {
    "url": os.environ.get("EDEN_URL", "http://localhost:8000"),
    "org_id": os.environ.get("EDEN_ORG_ID"),
    "org_uuid": os.environ.get("EDEN_ORG_UUID"),
    "robot_username": os.environ.get("EDEN_ROBOT_USERNAME", "datadog-agent"),
    "robot_api_key": os.environ.get("EDEN_ROBOT_API_KEY"),
    "range_seconds": int(os.environ.get("EDEN_RANGE_SECONDS", "300")),
    "limit": int(os.environ.get("EDEN_LIMIT", "5000")),
    "tags": ["env:dev"],
}


def main():
    if not (INSTANCE.get("org_id") or INSTANCE.get("org_uuid")):
        raise SystemExit("Set EDEN_ORG_ID or EDEN_ORG_UUID before running this helper.")
    if not INSTANCE.get("robot_api_key"):
        raise SystemExit("Set EDEN_ROBOT_API_KEY before running this helper.")

    check = EdenCheck("eden", {}, [INSTANCE])
    check.check(INSTANCE)

    print(f"\n=== service_checks ({len(check.service_checks)}) ===")
    for name, status, message, tags in check.service_checks:
        status_label = {0: "OK", 1: "WARNING", 2: "CRITICAL", 3: "UNKNOWN"}.get(status, str(status))
        print(f"  {name} -> {status_label}", f"({message})" if message else "", "tags:", list(tags))

    print(f"\n=== submitted metrics ({len(check.submitted)}) ===")
    by_name = {}
    for kind, metric, value, tags in check.submitted:
        by_name.setdefault(metric, []).append((kind, value, tags))

    for metric in sorted(by_name):
        samples = by_name[metric]
        kinds = {kind for kind, _, _ in samples}
        kinds_str = ",".join(sorted(kinds))
        print(f"  {metric} [{kinds_str}] x{len(samples)}")
        for kind, value, tags in samples[:2]:
            print(f"    -> {kind}={value} tags={list(tags)}")
        if len(samples) > 2:
            print(f"    ... {len(samples) - 2} more")

    print("\n=== auth cache ===")
    pprint(check._auth_cache)


if __name__ == "__main__":
    main()
