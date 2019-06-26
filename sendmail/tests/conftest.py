import mock
import os
import pytest

from datadog_checks.dev import get_here


@pytest.fixture
def mock_queue_output():
    with open(os.path.join(get_here(), 'fixtures', 'mail_queue'), 'r') as f:
        mail_queue = f.read()

    with mock.patch('datadog_checks.sendmail.sendmail.get_subprocess_output', return_value=(mail_queue, '', 0)):
        yield
