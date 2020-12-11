import mock
import pytest

from datadog_checks.octoprint import OctoPrintCheck


class MockOctoPrint:
    @staticmethod
    def octoprintInit():
        pass

    @staticmethod
    def get_bed_temp():
        return 20


@pytest.mark.unit
def test_check(aggregator, instance):
    with mock.patch('datadog_checks.octoprint.OctoPrintCheck', MockOctoPrint):
        check = OctoPrintCheck('octoprint', {}, [instance])
        check.check(instance)
    aggregator.assert_metric('octoprint.get_bed_temp', count=1)

    aggregator.assert_all_metrics_covered()
