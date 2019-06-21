from datadog_checks.sendmail import SendmailCheck


def test_check(aggregator, instance):
    check = SendmailCheck('sendmail', {}, {})
    check.check(instance)

    aggregator.assert_all_metrics_covered()
