import pytest

pytestmark = [pytest.mark.usefixtures("dd_environment"), pytest.mark.e2e]


def test_e2e(aggregator, dd_run_check):
    pass
