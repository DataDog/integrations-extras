import mock
import pytest


from datadog_checks.sendmail import SendmailCheck


def test_mailqueue_output(aggregator, mock_queue_output):
    check = SendmailCheck('sendmail', {}, {})
    tags = ['test:sendmail']
    check.check({'tags': tags})

    aggregator.assert_all_metrics_covered()
