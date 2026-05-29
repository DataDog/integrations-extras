# (C) voseghale 2026-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import pytest


@pytest.fixture(scope='session')
def dd_environment(instance):
    """No external service to spin up - PSI is a host kernel feature."""
    yield instance


@pytest.fixture(scope='session')
def instance():
    """Shared base instance config for test, Session-scoped so it can be
    consumed by 'dd_environment` (also session-scoped) without triggering
    pytest's ScopeMisMatch error. Test that need to customize the instance
    should dict-spread it (e.f. `{**instance , 'cgroup_roots': [...[]]}`)
    rather than mutate it in place.
    """
    return {'tags': ['integration:linux_psi_test']}
