# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import os

import mock
import pytest

from .common import HERE, URL


@pytest.fixture(scope="session", autouse=True)
def mock_requests():
    with open(os.path.join(HERE, "fixtures", "sample_stats.xml"), "r") as f:
        mock_data = f.read()

    with mock.patch(
        "requests.get", return_value=mock.MagicMock(text=mock_data, status_code=200)
    ):
        yield


@pytest.fixture
def instance():
    return {"url": URL}
