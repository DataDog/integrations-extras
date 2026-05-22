# (C) Typeform Platform 2026-present
# Unofficial integration. Not affiliated with Anthropic, PBC.
# Licensed under a 3-clause BSD style license (see LICENSE)
import pytest


@pytest.fixture(scope='session')
def dd_environment():
    yield


@pytest.fixture
def instance():
    return {
        "anthropic_api_key": "test-key-not-real",
        "org_id": "test-org",
        "lag_days": 3,
    }
