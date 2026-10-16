# (C) Datadog, Inc. 2025-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import re

from requests.exceptions import HTTPError, RequestException

from datadog_checks.base import OpenMetricsBaseCheckV2

from .api_metrics import API_ENDPOINTS, BOOL, DEFAULT_ENDPOINTS, DURATION, NUMBER
from .config_models import ConfigMixin
from .metrics import METRIC_MAP

# KurrentDB durations look like `0:00:00:00.9254789` (d:hh:mm:ss.fraction) or `739876.19:46:44.5430170`
DURATION_PATTERN = re.compile(r'^(?:(\d+)[.:])?(\d+):(\d{2}):(\d{2})(?:\.(\d+))?$')


def parse_duration(value):
    """Convert a KurrentDB duration string to seconds, or None if it is not one."""
    match = DURATION_PATTERN.match(value) if isinstance(value, str) else None
    if not match:
        return None
    days, hours, minutes, seconds, fraction = match.groups()
    total = int(days or 0) * 86400 + int(hours) * 3600 + int(minutes) * 60 + int(seconds)
    return total + (float('0.' + fraction) if fraction else 0.0)


def lookup(obj, path):
    for key in path.split('.') if path else ():
        if not isinstance(obj, dict) or key not in obj:
            return None
        obj = obj[key]
    return obj


def convert(value, kind):
    if value is None:
        return None
    if kind == NUMBER:
        return None if isinstance(value, bool) or not isinstance(value, (int, float)) else float(value)
    if kind == BOOL:
        return float(bool(value)) if isinstance(value, bool) else None
    if kind == DURATION:
        return parse_duration(value)
    if isinstance(kind, tuple) and kind[0] == 'equals':
        return float(value == kind[1]) if isinstance(value, str) else None
    return None


class KurrentdbCheck(OpenMetricsBaseCheckV2, ConfigMixin):
    __NAMESPACE__ = 'kurrentdb'

    DEFAULT_METRIC_LIMIT = 0

    def get_default_config(self):
        return {'metrics': [METRIC_MAP], 'exclude_labels': ['otel_scope_name', 'otel_scope_version']}

    def check(self, _):
        super().check(_)
        self.collect_api_metrics()

    def api_base_url(self):
        if self.config.url:
            return self.config.url.rstrip('/')
        endpoint = self.config.openmetrics_endpoint.rstrip('/')
        return endpoint[: -len('/metrics')] if endpoint.endswith('/metrics') else endpoint

    def collect_api_metrics(self):
        base_url = self.api_base_url()
        endpoints = self.config.endpoints if self.config.endpoints is not None else DEFAULT_ENDPOINTS

        for endpoint in endpoints:
            groups = API_ENDPOINTS.get(endpoint)
            if groups is None:
                self.warning('Unknown KurrentDB API endpoint `%s`, expected one of: %s', endpoint, list(API_ENDPOINTS))
                continue

            url = base_url + endpoint
            tags = list(self.config.tags or ())
            if self.config.tag_by_endpoint:
                tags.append(f'endpoint:{url}')

            payload = self.fetch_json(url, tags)
            if payload is None:
                continue

            for group in groups:
                self.submit_group(payload, group, tags)

    def fetch_json(self, url, tags):
        try:
            response = self.http.get(url)
            response.raise_for_status()
            payload = response.json()
        except HTTPError as e:
            if e.response is not None and e.response.status_code == 404:
                self.log.debug('KurrentDB API endpoint %s is not available on this node, skipping', url)
                return None
            return self.fail(url, tags, e)
        except (RequestException, ValueError) as e:
            return self.fail(url, tags, e)

        self.service_check('api.can_connect', self.OK, tags=tags)
        return payload

    def fail(self, url, tags, error):
        message = f'Unable to collect from KurrentDB API endpoint {url}: {error}'
        self.warning(message)
        self.service_check('api.can_connect', self.CRITICAL, tags=tags, message=message)

    def submit_group(self, payload, group, tags):
        target = lookup(payload, group['path'])
        if isinstance(target, list):
            items = target
        elif isinstance(target, dict) and group.get('many'):
            items = list(target.values())
        else:
            items = [target]

        for item in items:
            if not isinstance(item, dict):
                continue

            item_tags = list(tags)
            for tag_name, field in group.get('tags', {}).items():
                tag_value = lookup(item, field)
                if tag_value not in (None, ''):
                    item_tags.append(f'{tag_name}:{tag_value}')

            for field, name, kind in group['metrics']:
                value = convert(lookup(item, field), kind)
                if value is not None:
                    self.gauge(name, value, tags=item_tags)
