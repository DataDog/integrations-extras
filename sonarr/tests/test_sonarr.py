import pytest
from requests.exceptions import ConnectionError, HTTPError

from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.sonarr import SonarrCheck


def test_check(aggregator, instance):
    check = SonarrCheck('sonarr', {}, [instance])

    with pytest.raises(ConnectionError):
        check.check(instance)
        aggregator.assert_all_metrics_covered()
        aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_emits_critical_service_check_when_service_is_down(aggregator, instance):
    check = SonarrCheck('sonarr', {}, [instance])

    with pytest.raises(ConnectionError):
        check.check(instance)
        aggregator.assert_service_check('sonarr.can_connect', SonarrCheck.CRITICAL)


def test_process_series(aggregator, instance):
    check = SonarrCheck('sonarr', {}, [instance])

    series = [
        {
            "title": "A title",
            "seasons": [
                {
                    "seasonNumber": 1,
                    "monitored": False,
                    "statistics": {
                        "episodeFileCount": 0,
                        "episodeCount": 0,
                        "totalEpisodeCount": 10,
                        "sizeOnDisk": 0,
                        "percentOfEpisodes": 0.0,
                    },
                },
                {
                    "seasonNumber": 2,
                    "monitored": True,
                    "statistics": {
                        "episodeFileCount": 3,
                        "episodeCount": 10,
                        "totalEpisodeCount": 20,
                        "sizeOnDisk": 2069274913,
                        "percentOfEpisodes": 30.0,
                    },
                },
            ],
            "monitored": True,
            "statistics": {
                "seasonCount": 2,
                "episodeFileCount": 3,
                "episodeCount": 10,
                "totalEpisodeCount": 30,
                "sizeOnDisk": 2069274913,
                "percentOfEpisodes": 30.0,
            },
            "id": i,
        }
        for i in range(5)
    ]
    metrics = check._init_metrics()
    check._process_series(series, metrics)

    assert metrics["series.total"] == 5
    assert metrics["series.monitored"] == 5
    assert metrics["series.unmonitored"] == 0
    assert metrics["series.downloaded"] == 0
    assert metrics["seasons.total"] == 10
    assert metrics["episodes.total"] == 150
    assert metrics["episodes.downloaded"] == 15
    assert metrics["series.file_size"] == 10346374565
    assert metrics["seasons.monitored"] == 5
    assert metrics["seasons.unmonitored"] == 5
    assert metrics["seasons.downloaded"] == 0


def test_process_episodes(aggregator, instance):
    check = SonarrCheck('sonarr', {}, [instance])

    episodes = [
        {
            "seriesId": 1,
            "tvdbId": 1234,
            "episodeFileId": 0,
            "seasonNumber": 0,
            "episodeNumber": 4,
            "title": "A title",
            "hasFile": False,
            "monitored": False,
            "id": 4,
        },
        {
            "seriesId": 1,
            "tvdbId": 4321,
            "episodeFileId": 0,
            "seasonNumber": 0,
            "episodeNumber": 2,
            "title": "Another title",
            "hasFile": False,
            "monitored": False,
            "id": 2,
        },
        {
            "seriesId": 1,
            "tvdbId": 5678,
            "episodeFileId": 0,
            "seasonNumber": 0,
            "episodeNumber": 2,
            "title": "Another title",
            "overview": "Desc",
            "hasFile": True,
            "monitored": True,
            "id": 3,
        },
    ]
    metrics = check._init_metrics()
    check._process_episodes(episodes, metrics)

    assert metrics["episodes.monitored"] == 1
    assert metrics["episodes.unmonitored"] == 2


def test_process_missing(aggregator, instance):
    check = SonarrCheck('sonarr', {}, [instance])

    missing = {
        "page": 1,
        "pageSize": 10,
        "sortKey": "airDateUtc",
        "sortDirection": "descending",
        "totalRecords": 128,
        "records": [],
    }
    metrics = check._init_metrics()
    check._process_missing(missing, metrics)

    assert metrics["episodes.missing"] == 128


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_emits_critical_service_check_when_api_key_is_invalid(aggregator, instance):
    # invalid API key: the check should send CRITICAL
    instance['api_key'] = 'cafecafe'
    check = SonarrCheck('sonarr', {}, [instance])

    with pytest.raises(HTTPError):
        check.check(instance)
        aggregator.assert_service_check('sonarr.can_connect', SonarrCheck.CRITICAL)


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_service_check(aggregator, instance):
    check = SonarrCheck('sonarr', {}, [instance])

    # the check should send OK
    check.check(instance)

    aggregator.assert_service_check('sonarr.can_connect', SonarrCheck.OK)
