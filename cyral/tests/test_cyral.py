import mock
import os
from os import open
import pytest

CHECK_NAME = 'cyral'


@pytest.fixture()
def test_check_all_metrics():
    f_name = os.path.join(os.path.dirname(__file__), 'fixtures', 'metrics.txt')
    with open(f_name, 'r') as f:
        text_data = f.read()
    with mock.patch('requests.get', return_value=mock.MagicMock(
            status_code=200, headers={"Content-Type": "text/plain"}, iter_lines=lambda **kw: text_data.split("\n")
    )):
        yield
