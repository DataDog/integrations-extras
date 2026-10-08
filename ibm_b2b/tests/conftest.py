# (C) Datadog, Inc. 2026-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import os
from typing import Iterator

import pytest

from datadog_checks.base.types import InstanceType


def _get_instance() -> InstanceType | None:
    required = {
        'url': os.getenv('IBM_B2B_URL'),
        'username': os.getenv('IBM_B2B_USERNAME'),
        'password': os.getenv('IBM_B2B_PASSWORD'),
        'cd_node': os.getenv('IBM_B2B_CD_NODE'),
        'statistics_timezone': os.getenv('IBM_B2B_STATISTICS_TIMEZONE'),
    }
    if any(value is None for value in required.values()):
        return None

    return {
        **required,
        'cd_port': int(os.getenv('IBM_B2B_CD_PORT', '1363')),
        'cd_protocol': os.getenv('IBM_B2B_CD_PROTOCOL', 'TCPIP'),
        'tls_verify': os.getenv('IBM_B2B_TLS_VERIFY', 'true').lower() == 'true',
        'timeout': float(os.getenv('IBM_B2B_TIMEOUT', '10')),
        'statistics_lookback_minutes': int(os.getenv('IBM_B2B_LOOKBACK_MINUTES', '2')),
    }


@pytest.fixture(scope='session')
def dd_environment() -> Iterator[dict]:
    instance = _get_instance()
    yield {'instances': [instance] if instance is not None else []}


@pytest.fixture
def instance() -> InstanceType:
    configured_instance = _get_instance()
    if configured_instance is None:
        pytest.skip('IBM B2B e2e environment variables are not configured')
    return configured_instance
