# (C) Datadog, Inc. 2026-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import copy

import pytest

from .common import INSTANCE


@pytest.fixture
def instance():
    return copy.deepcopy(INSTANCE)
