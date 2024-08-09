import pytest

from datadog_checks.qdrant import QdrantCheck


def test_empty_instance(dd_run_check):
    with pytest.raises(
        Exception,
        match="InstanceConfig`:\nopenmetrics_endpoint\n  Field required",
    ):
        check = QdrantCheck("qdrant", {}, [{}])
        dd_run_check(check)
