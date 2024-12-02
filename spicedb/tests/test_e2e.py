
def test_metrics(dd_agent_check, instance):
    aggregator = dd_agent_check(instance, rate=True)
    expected_metrics = []

    for metric in expected_metrics:
        aggregator.assert_metric(f"spicedb.{metric}", at_least=0)
