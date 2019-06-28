import mock

from datadog_checks.sendmail import SendmailCheck


def mailqueue_mock():
    return """MSP Queue status...
/var/spool/mqueue-client is empty
Total requests: 0
MTA Queue status...
/var/spool/mqueue is empty
Total requests: 0"""


def test_queue_output(aggregator):
    check = SendmailCheck('sendmail', {}, {})

    tags = ['test:sendmail']

    with mock.patch('os.path.exists', return_value=True):
        with mock.patch(
            'datadog_checks.sendmail.sendmail.get_subprocess_output', return_value=(mailqueue_mock(), '', 0)
        ):
            check.check({'tags': tags})
            aggregator.assert_metric('sendmail.queue.size', value=0, tags=tags + ['queue:total'])
