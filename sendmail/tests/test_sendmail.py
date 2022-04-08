import mock
import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.sendmail import SendmailCheck


def mailqueue_mock():
    return """MSP Queue status...
/var/spool/mqueue-client is empty
Total requests: 0
MTA Queue status...
/var/spool/mqueue is empty
Total requests: 306"""


def test_bad_configuration():
    instance = {}
    check = SendmailCheck('sendmail', {}, {})

    with pytest.raises(ConfigurationError):
        check.check(instance)


def test_bad_sendmail_command():
    instance = {'sendmail_command': 'something'}
    check = SendmailCheck('sendmail', {}, {})

    with pytest.raises(ConfigurationError):
        check.check(instance)


def test_queue_output(aggregator):
    check = SendmailCheck('sendmail', {}, {})

    tags = ['test:sendmail']

    with mock.patch('os.path.exists', return_value=True):
        with mock.patch(
            'datadog_checks.sendmail.sendmail.get_subprocess_output', return_value=(mailqueue_mock(), '', 0)
        ):
            check.check({'sendmail_command': '/usr/bin/mailq', 'tags': tags})
            aggregator.assert_metric('sendmail.queue.size', value=306, tags=tags + ['queue:total'])
            aggregator.assert_service_check('sendmail.returns.output', SendmailCheck.OK)
