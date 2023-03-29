from json import JSONDecodeError

from requests.exceptions import ConnectionError, HTTPError, InvalidURL, Timeout

from datadog_checks.base import AgentCheck


class SonarrCheck(AgentCheck):
    # This will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = "sonarr"

    def __init__(self, name, init_config, instances):
        super(SonarrCheck, self).__init__(name, init_config, instances)

        self.url = self.instance.get("url")
        self.http.options["headers"] = {"Authorization": self.instance.get("api_key")}
        self.tags = self.instance.get("tags", [])
        self.tags.append(f"url:{self.url}")

    def check(self, _):
        metrics = self._init_metrics()

        series = self._http_get("/api/v3/series")

        self._process_series(series, metrics)

        for show in series:
            showID = show.get("id")
            if showID is not None:
                episodes = self._http_get(f"/api/v3/episode?seriesId={showID}")
                self._process_episodes(episodes, metrics)

        missing = self._http_get("/api/v3/wanted/missing")
        self._process_missing(missing, metrics)

        self._report_metrics(metrics)
        self.service_check("can_connect", AgentCheck.OK)

    def _http_get(self, endpoint):
        """Perform HTTP request against sonarr API endpoint"""
        try:
            full_url = self.url + endpoint
            response = self.http.get(full_url)
            response.raise_for_status()
            response_json = response.json()

        except Timeout as e:
            self.service_check(
                "can_connect",
                AgentCheck.CRITICAL,
                message="Request timeout: {}, {}".format(self.url, e),
            )
            raise

        except (HTTPError, InvalidURL, ConnectionError) as e:
            self.service_check(
                "can_connect",
                AgentCheck.CRITICAL,
                message="Request failed: {}, {}".format(self.url, e),
            )
            raise

        except JSONDecodeError as e:
            self.service_check(
                "can_connect",
                AgentCheck.CRITICAL,
                message="JSON Parse failed: {}, {}".format(self.url, e),
            )
            raise

        except ValueError as e:
            self.service_check("can_connect", AgentCheck.CRITICAL, message=str(e))
            raise

        else:
            return response_json

    def _init_metrics(self):
        """Create and initialize a dictionnary to hold the gathered values
        of the metrics that will be emitted by the check"""

        return {
            # series metrics
            "series.file_size": 0,
            "series.total": 0,
            "series.downloaded": 0,
            "series.monitored": 0,
            "series.unmonitored": 0,
            # seasons metrics
            "seasons.total": 0,
            "seasons.downloaded": 0,
            "seasons.monitored": 0,
            "seasons.unmonitored": 0,
            # episodes metrics
            "episodes.total": 0,
            "episodes.downloaded": 0,
            "episodes.monitored": 0,
            "episodes.unmonitored": 0,
            "episodes.missing": 0,
        }

    def _process_series(self, series, metrics):
        """Compute metrics values from series response from the sonarr API"""
        metrics["series.total"] = len(series)
        for show in series:
            if show.get("monitored"):
                metrics["series.monitored"] += 1
            else:
                metrics["series.unmonitored"] += 1

            show_statistics = show.get("statistics", {})

            if show_statistics.get("percentOfEpisodes", 0) == 100.0:
                metrics["series.downloaded"] += 1

            metrics["seasons.total"] += show_statistics.get("seasonCount", 0)
            metrics["episodes.total"] += show_statistics.get("totalEpisodeCount", 0)
            metrics["episodes.downloaded"] += show_statistics.get("episodeFileCount", 0)
            metrics["series.file_size"] += show_statistics.get("sizeOnDisk", 0)

            for season in show.get("seasons", []):
                if season.get("monitored"):
                    metrics["seasons.monitored"] += 1
                else:
                    metrics["seasons.unmonitored"] += 1

                if season.get("statistics", {}).get("percentOfEpisodes", 0) == 100.0:
                    metrics["seasons.downloaded"] += 1

    def _process_episodes(self, episodes, metrics):
        """Compute metrics values from episodes response from the sonarr API"""
        for episode in episodes:
            if episode.get("monitored"):
                metrics["episodes.monitored"] += 1
            else:
                metrics["episodes.unmonitored"] += 1

    def _process_missing(self, missing, metrics):
        """Compute metrics values from wanted/missing response from the sonarr API"""
        metrics["episodes.missing"] = missing.get("totalRecords", 0)

    def _report_metrics(self, metrics):
        """Report metrics"""
        for metric, value in metrics.items():
            self.gauge(metric, value, tags=self.tags)
