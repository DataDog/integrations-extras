# (C) Datadog, Inc. 2020
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from datadog_checks.base.stubs import aggregator

EXPECTED_METRICS = {
    'open_policy_agent.request.duration.sum': aggregator.MONOTONIC_COUNT,
    'open_policy_agent.request.duration.count': aggregator.MONOTONIC_COUNT,
    'open_policy_agent.policies': aggregator.GAUGE,
}

EXPECTED_CHECKS = {
    'open_policy_agent.health',
    'open_policy_agent.plugins_health',
    'open_policy_agent.bundles_health',
}

MOCK_INSTANCE = {
    'prometheus_url': 'http://fake.tld/metrics',
    'opa_url': 'http://fake.tld',
}
