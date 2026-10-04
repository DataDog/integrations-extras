# (C) Datadog, Inc. 2026-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

from urllib.parse import urlparse
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def instance_url(value, **kwargs):
    parsed = urlparse(value)
    if parsed.scheme not in ('http', 'https') or not parsed.netloc:
        raise ValueError('url must be an absolute HTTP or HTTPS URL')
    return value.rstrip('/')


def instance_timeout(value, **kwargs):
    if value <= 0:
        raise ValueError('timeout must be greater than zero')
    return value


def instance_statistics_lookback_minutes(value, **kwargs):
    if value <= 0:
        raise ValueError('statistics_lookback_minutes must be greater than zero')
    return value


def instance_statistics_timezone(value, **kwargs):
    try:
        ZoneInfo(value)
    except (TypeError, ValueError, ZoneInfoNotFoundError) as err:
        raise ValueError('statistics_timezone must be a valid IANA timezone') from err
    return value
