from json import JSONDecodeError

from requests.exceptions import ConnectionError, HTTPError, InvalidURL, Timeout

from datadog_checks.base import AgentCheck


class RadarrCheck(AgentCheck):
    # This will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = 'radarr'

    def __init__(self, name, init_config, instances):
        super(RadarrCheck, self).__init__(name, init_config, instances)

        self.url = self.instance.get("url")
        self.http.options["headers"] = {"Authorization": self.instance.get("api_key")}
        self.tags = self.instance.get("tags", [])
        self.tags.append(f"url:{self.url}")

    def check(self, _):
        metrics = self._init_metrics()

        movies = self._http_get("/api/v3/movie")

        self._process_movies(movies, metrics)

        self._report_metrics(metrics)
        self.service_check("can_connect", AgentCheck.OK)

    def _http_get(self, endpoint):
        """Perform HTTP request against radarr API endpoint"""
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
            # movies metrics
            "movies.total": 0,
            "movies.monitored": 0,
            "movies.unmonitored": 0,
            "movies.downloaded": 0,
            "movies.wanted": 0,
            "movies.missing": 0,
            "movies.filesize_bytes": 0,
        }

    def _process_movies(self, movies, metrics):
        """Compute metrics values from movies response from the radarr API"""
        metrics["movies.total"] = len(movies)
        for movie in movies:
            if movie.get("hasFile"):
                metrics["movies.downloaded"] += 1
            if not movie.get("monitored"):
                metrics["movies.unmonitored"] += 1
            else:
                metrics["movies.monitored"] += 1
                if movie.get("isAvailable") and not movie.get("hasFile"):
                    metrics["movies.missing"] += 1
                elif not movie.get("hasFile"):
                    metrics["movies.wanted"] += 1

            metrics["movies.filesize_bytes"] += movie.get("sizeOnDisk", 0)

    def _report_metrics(self, metrics):
        """Report metrics"""
        for metric, value in metrics.items():
            self.gauge(metric, value, tags=self.tags)
