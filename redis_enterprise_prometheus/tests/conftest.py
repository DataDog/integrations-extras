import os

import mock
import pytest

from .support import ENDPOINT

CHECK = "redis_enterprise_prometheus"


@pytest.fixture(scope="session")
def dd_environment():
    instances = {"instances": [{"openmetrics_endpoint": ENDPOINT}, {"tls_verify": "false"}]}

    yield instances


@pytest.fixture(scope="session")
def instance():
    return {"openmetrics_endpoint": ENDPOINT, "tags": ["instance"], "tls_verify": "false"}


@pytest.fixture()
def mock_http_response():
    f_name = os.path.join(os.path.dirname(__file__), "data", "metrics.txt")
    with open(f_name, "r") as f:
        text_data = f.read()

    mock_response = mock.MagicMock()
    mock_response.status_code = 200
    mock_response.content = text_data
    mock_response.text = text_data
    mock_response.iter_lines = lambda **kwargs: text_data.split("\n")
    mock_response.headers = {"Content-Type": "text/plain"}

    with (
        mock.patch("requests.get", return_value=mock_response),
        mock.patch("requests.Session.get", return_value=mock_response),
    ):
        yield
