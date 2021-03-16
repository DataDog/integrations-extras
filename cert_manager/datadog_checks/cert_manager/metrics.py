# (C) Datadog, Inc. 2019
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

METRIC_MAP = {
    'certmanager_certificate_ready_status': 'certificate.ready_status',
    'certmanager_certificate_expiration_timestamp_seconds': 'certificate.expiration_timestamp',
    'certmanager_http_acme_client_request_count': 'http_acme_client.request.count',
    'certmanager_http_acme_client_request_duration_seconds': 'http_acme_client.request.duration',
    'certmanager_controller_sync_call_count': 'controller.sync_call.count',
}
