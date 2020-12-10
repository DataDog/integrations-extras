# (C) Datadog, Inc. 2020
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from datadog_checks.base.stubs import aggregator

EXPECTED_METRICS = {
    'opa.request.duration.sum': aggregator.MONOTONIC_COUNT,
    'opa.request.duration.count': aggregator.MONOTONIC_COUNT,
    'opa.policies': aggregator.GAUGE,
}

EXPECTED_CHECKS = {
    'opa.health',
    'opa.plugins_health',
    'opa.bundles_health',
}

MOCK_INSTANCE = {
    'prometheus_url': 'http://fake.tld/metrics',
    'opa_url': 'http://fake.tld',
}
