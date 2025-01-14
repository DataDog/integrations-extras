import pytest
from requests.exceptions import ConnectionError, HTTPError

from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.radarr import RadarrCheck


def test_check(aggregator, instance):
    check = RadarrCheck('radarr', {}, [instance])

    with pytest.raises(ConnectionError):
        check.check(instance)


def test_emits_critical_service_check_when_service_is_down(aggregator, instance):
    check = RadarrCheck('radarr', {}, [instance])

    with pytest.raises(ConnectionError):
        check.check(instance)
        aggregator.assert_service_check('radarr.can_connect', RadarrCheck.CRITICAL)


def test_process_movies(aggregator, instance):
    check = RadarrCheck("radarr", {}, [instance])

    movies = [
        {
            "id": 0,
            "title": "A cool movie",
            "sizeOnDisk": 64334621,
            "hasFile": True,
            "monitored": True,
            "isAvailable": True,
        },
        {
            "id": 1,
            "title": "Another cool movie",
            "sizeOnDisk": 0,
            "hasFile": False,
            "monitored": True,
            "isAvailable": True,
        },
        {
            "id": 2,
            "title": "An ok movie",
            "sizeOnDisk": 0,
            "hasFile": False,
            "monitored": True,
            "isAvailable": False,
        },
    ]

    metrics = check._init_metrics()
    check._process_movies(movies, metrics)

    assert metrics["movies.total"] == 3
    assert metrics["movies.monitored"] == 3
    assert metrics["movies.unmonitored"] == 0
    assert metrics["movies.downloaded"] == 1
    assert metrics["movies.wanted"] == 1
    assert metrics["movies.missing"] == 1
    assert metrics["movies.filesize_bytes"] == 64334621


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_emits_critical_service_check_when_api_key_is_invalid(aggregator, instance):
    # invalid API key: the check should send CRITICAL
    instance['api_key'] = 'cafecafe'
    check = RadarrCheck('radarr', {}, [instance])

    with pytest.raises(HTTPError):
        check.check(instance)
        aggregator.assert_service_check('radarr.can_connect', RadarrCheck.CRITICAL)


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_service_check(aggregator, instance):
    check = RadarrCheck('radarr', {}, [instance])

    # the check should send OK
    check.check(instance)

    aggregator.assert_service_check('radarr.can_connect', RadarrCheck.OK)

    aggregator.assert_metric("radarr.movies.total")
    aggregator.assert_metric("radarr.movies.monitored")
    aggregator.assert_metric("radarr.movies.unmonitored")
    aggregator.assert_metric("radarr.movies.downloaded")
    aggregator.assert_metric("radarr.movies.wanted")
    aggregator.assert_metric("radarr.movies.missing")
    aggregator.assert_metric("radarr.movies.filesize_bytes")

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
