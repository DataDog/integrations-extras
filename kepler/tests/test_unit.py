import logging
import os

# from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.kepler import KeplerCheck

from .conftest import HERE


def get_fixture_path(filename):
    return os.path.join(HERE, 'fixtures', filename)


def test_check(dd_run_check, aggregator, instance, mock_http_response, caplog):
    mock_http_response(file_path=get_fixture_path('output.txt'))

    check = KeplerCheck('kepler', {}, [instance])
    caplog.set_level(logging.DEBUG)

    dd_run_check(check)
    #aggregator.assert_all_metrics_covered()
    # aggregator.assert_metrics_using_metadata(get_metadata_metrics())
