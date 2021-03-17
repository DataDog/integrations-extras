# (C) Datadog, Inc. 2019
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

CERT_METRICS = {
    'certmanager_certificate_ready_status': 'certificate.ready_status',
    'certmanager_certificate_expiration_timestamp_seconds': 'certificate.expiration_timestamp',
}

CONTROLLER_METRICS = {
    'certmanager_controller_sync_call_count': 'controller.sync_call.count',
}

ACME_METRICS = {
    'certmanager_http_acme_client_request_count': 'http_acme_client.request.count',
    'certmanager_http_acme_client_request_duration_seconds': 'http_acme_client.request.duration',
}
