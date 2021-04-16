from typing import Any, Dict
import pytest
from datadog_checks.base.stubs.aggregator import AggregatorStub
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.ns1 import Ns1Check
from datadog_checks.base import ConfigurationError


def test_check(aggregator, instance_empty):
    # type: (AggregatorStub, Dict[str, Any]) -> None
    check = Ns1Check('ns1', {}, [instance_empty])
    # check.check(instance)
    with pytest.raises(ConfigurationError):
        check.check(instance_empty)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
