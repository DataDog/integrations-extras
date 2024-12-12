from .util import get_expected_non_histogram_metrics, get_expected_histogram_metrics

def test_metrics(dd_agent_check, instance):
    aggregator = dd_agent_check(instance, rate=True)

    for metric in get_expected_non_histogram_metrics():
        aggregator.assert_metric(f"spicedb.{metric}", at_least=0)

    for metric in get_expected_histogram_metrics():
        aggregator.assert_metric(f"spicedb.{metric}", at_least=0)
