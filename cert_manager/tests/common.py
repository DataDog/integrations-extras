# (C) Datadog, Inc. 2019
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from datadog_checks.base.stubs import aggregator

EXPECTED_METRICS = {
    'cert_manager.certificate.ready_status': aggregator.GAUGE,
    'cert_manager.certificate.expiration_timestamp': aggregator.GAUGE,
    'cert_manager.http_acme_client.request.count': aggregator.MONOTONIC_COUNT,
    'cert_manager.http_acme_client.request.duration.sum': aggregator.GAUGE,
    'cert_manager.http_acme_client.request.duration.count': aggregator.GAUGE,
    'cert_manager.http_acme_client.request.duration.quantile': aggregator.GAUGE,
    'cert_manager.controller.sync_call.count': aggregator.MONOTONIC_COUNT,
    'cert_manager.prometheus.health': aggregator.GAUGE,
}

MOCK_INSTANCE = {
    'prometheus_url': 'http://fake.tld/prometheus',
}
