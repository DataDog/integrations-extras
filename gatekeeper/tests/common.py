# (C) Datadog, Inc. 2020
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from datadog_checks.base.stubs import aggregator

EXPECTED_AUDIT_METRICS = {
    'gatekeeper.audit.duration.seconds.sum': aggregator.MONOTONIC_COUNT,
    'gatekeeper.audit.duration.seconds.count': aggregator.MONOTONIC_COUNT,
    'gatekeeper.audit.last_run_time': aggregator.GAUGE,
    'gatekeeper.constraint_template_ingestion.duration.seconds.sum': aggregator.MONOTONIC_COUNT,
    'gatekeeper.constraint_template_ingestion.duration.seconds.count': aggregator.MONOTONIC_COUNT,
    'gatekeeper.constraint_template_ingestion.count': aggregator.MONOTONIC_COUNT,
    'gatekeeper.violations': aggregator.GAUGE,
    'gatekeeper.constraints': aggregator.GAUGE,
    'gatekeeper.constraint_templates': aggregator.GAUGE,
    'gatekeeper.sync': aggregator.GAUGE,
    'gatekeeper.sync.last_run_time': aggregator.GAUGE,
    'gatekeeper.sync.duration.seconds.sum': aggregator.MONOTONIC_COUNT,
    'gatekeeper.sync.duration.seconds.count': aggregator.MONOTONIC_COUNT,
    'gatekeeper.watch.intended': aggregator.GAUGE,
    'gatekeeper.watch.watched': aggregator.GAUGE,
}

EXPECTED_CONTROLLER_METRICS = {
    'gatekeeper.request.duration.seconds.sum': aggregator.MONOTONIC_COUNT,
    'gatekeeper.request.duration.seconds.count': aggregator.MONOTONIC_COUNT,
    'gatekeeper.constraint_template_ingestion.duration.seconds.sum': aggregator.MONOTONIC_COUNT,
    'gatekeeper.constraint_template_ingestion.duration.seconds.count': aggregator.MONOTONIC_COUNT,
    'gatekeeper.constraints': aggregator.GAUGE,
    'gatekeeper.constraint_templates': aggregator.GAUGE,
    'gatekeeper.constraint_template_ingestion.count': aggregator.MONOTONIC_COUNT,
    'gatekeeper.request.count': aggregator.MONOTONIC_COUNT,
    'gatekeeper.sync': aggregator.GAUGE,
    'gatekeeper.sync.last_run_time': aggregator.GAUGE,
    'gatekeeper.sync.duration.seconds.sum': aggregator.MONOTONIC_COUNT,
    'gatekeeper.sync.duration.seconds.count': aggregator.MONOTONIC_COUNT,
    'gatekeeper.watch.intended': aggregator.GAUGE,
    'gatekeeper.watch.watched': aggregator.GAUGE,
    'gatekeeper.validation.request.count': aggregator.MONOTONIC_COUNT,
    'gatekeeper.validation.request.duration.seconds.sum': aggregator.MONOTONIC_COUNT,
    'gatekeeper.validation.request.duration.seconds.count': aggregator.MONOTONIC_COUNT,
    'gatekeeper.mutator.ingestion.count': aggregator.MONOTONIC_COUNT,
    'gatekeeper.mutator.ingestion.duration.seconds.sum': aggregator.MONOTONIC_COUNT,
    'gatekeeper.mutator.ingestion.duration.seconds.count': aggregator.MONOTONIC_COUNT,
    'gatekeeper.mutators': aggregator.GAUGE,
    'gatekeeper.mutator.conflicting.count': aggregator.GAUGE,
}


EXPECTED_CHECKS = {
    'gatekeeper.health',
    'gatekeeper.prometheus.health',
}

MOCK_INSTANCE = {
    'prometheus_url': 'http://fake.tld/metrics',
    'gatekeeper_health_endpoint': 'http://fake.tld',
}
