from datadog_checks.windows_docker import WindowsDockerCheck


def test_check(aggregator, instance):
    check = WindowsDockerCheck('windows_docker', {}, {})
    check.check(instance)

    aggregator.assert_all_metrics_covered()
