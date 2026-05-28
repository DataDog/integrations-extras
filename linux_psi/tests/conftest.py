# (C) voseghale 2026-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import pytest


@pytest.fixture(scope='session')
def dd_environment(instance):
    """No external service to spin up - PSI is a host kernel feature."""
    yield instance


@pytest.fixture
def instance():
    return {'tags': ['integration:linux_psi_test']}
