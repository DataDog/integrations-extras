# (C) Datadog, Inc. 2019
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from datadog_checks.stubs import aggregator

EXPECTED_METRICS = {
    'cert_manager.certificate_ready_status': aggregator.GAUGE,
    'cert_manager.certificate_expiration_timestamp': aggregator.GAUGE,
    'cert_manager.acme_client_request_count': aggregator.MONOTONIC_COUNT,
    'cert_manager.acme_client_request_duration.sum': aggregator.GAUGE,
    'cert_manager.acme_client_request_duration.count': aggregator.GAUGE,
    'cert_manager.acme_client_request_duration.quantile': aggregator.GAUGE,
    'cert_manager.controller_sync_call_count': aggregator.MONOTONIC_COUNT,
    'cert_manager.prometheus.health': aggregator.GAUGE,
}

MOCK_INSTANCE = {
    'prometheus_url': 'http://fake.tld/prometheus',
}
