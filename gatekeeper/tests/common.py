# (C) Datadog, Inc. 2020
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from datadog_checks.base.stubs import aggregator

EXPECTED_AUDIT_METRICS = {
    'audit.duration.seconds.sum': aggregator.MONOTONIC_COUNT,
    'audit.duration.seconds.count': aggregator.MONOTONIC_COUNT,
}

EXPECTED_CONTROLLER_METRICS = {
    'duration.seconds.sum': aggregator.MONOTONIC_COUNT,
    'duration.seconds.count': aggregator.MONOTONIC_COUNT,
}


EXPECTED_CHECKS = {
    'gatekeeper.health',
    'gatekeeper.prometheus.health',
}

MOCK_INSTANCE = {
    'prometheus_url': 'http://fake.tld/metrics',
    'gatekeeper_health_endpoint': 'http://fake.tld',
}
