import mock

from datadog_checks.sendmail import SendmailCheck


def test_queue_output(aggregator, mock_queue_output):
    check = SendmailCheck('sendmail', {}, {})

    tags = ['test:sendmail']

    with mock.patch('os.path.exists', return_value=True):
        check.check({'tags': tags})
        aggregator.assert_metric('sendmail.queue.size', value=3, tags=tags + ['queue:total'])
