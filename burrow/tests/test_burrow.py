import pytest

from datadog_checks.base.stubs.aggregator import AggregatorStub
from datadog_checks.burrow import BurrowCheck
from datadog_checks.base import ConfigurationError


@pytest.mark.integration
@pytest.mark.usefixtures("dd_environment")
def test_check(aggregator, instance):
    c = BurrowCheck("burrow", {}, [instance])

    with pytest.raises(ConfigurationError):
        c.check(instance)

    aggregator.assert_all_metrics_covered()
