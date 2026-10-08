import pytest

from datadog_checks.base.constants import ServiceCheck
from datadog_checks.celerdata import CelerdataCheck

pytestmark = [pytest.mark.integration, pytest.mark.usefixtures("dd_environment")]


def test_celerdata_fe(aggregator, dd_run_check, fe_instance):
    check = CelerdataCheck('celerdata', {}, [fe_instance])
    dd_run_check(check)

    aggregator.assert_service_check('celerdata.openmetrics.health', ServiceCheck.OK)
    aggregator.assert_metric('celerdata.fe.job', value=0)


def test_table_num_given_live_fe_returns_series_for_multiple_dbs(aggregator, dd_run_check, fe_instance):
    check = CelerdataCheck("celerdata", {}, [fe_instance])
    dd_run_check(check)

    # Even a fresh FE has more than one database (at least `information_schema` and `sys`), and it
    # interleaves their `table_num` samples with `db_size_bytes`. More than one `db_name` checks the
    # gauge pin against live output, not just the reconstructed unit-test fixture.
    db_names = {
        tag for m in aggregator.metrics("celerdata.fe.table_num") for tag in m.tags if tag.startswith("db_name:")
    }
    assert len(db_names) > 1, db_names


def test_celerdata_be(aggregator, dd_run_check, be_instance):
    check = CelerdataCheck("celerdata", {}, [be_instance])
    dd_run_check(check)

    aggregator.assert_service_check("celerdata.openmetrics.health", ServiceCheck.OK)
    aggregator.assert_metric("celerdata.be.active_scan_context_count", value=0)
