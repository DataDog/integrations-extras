import json
import os

import mock
import pytest

from datadog_checks.dev import get_here
from datadog_checks.dev.utils import read_file


@pytest.fixture
def mock_client():
    client = mock.MagicMock()
    client.get_products = mock.MagicMock()
    client.get_products.side_effect = lambda *args, **kwargs: json.loads(
        read_file(os.path.join(get_here(), "fixtures", "get_products.json"))
    )

    with mock.patch("boto3.client", return_value=client) as m:
        yield m, client


@pytest.fixture
def instance_good():
    instance = {"region_name": "us-east-1", "services": ["AmazonEC2"], "filters": []}
    return instance


@pytest.fixture
def instance_no_services():
    instance = {"region_name": "us-east-1", "services": [], "filters": []}
    return instance
