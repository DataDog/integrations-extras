# (C) Datadog, Inc. 2022-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import datetime
import time
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

import requests_unixsocket
from requests.exceptions import ConnectionError, HTTPError, InvalidURL, Timeout

from datadog_checks.base import AgentCheck, ConfigurationError

try:
    from urllib.parse import quote, urljoin, urlparse
except ImportError:
    # Use Python 2 imports
    from urllib import quote

    from urlparse import urljoin, urlparse


try:
    import datadog_agent
except ImportError:
    from datadog_checks.stubs import datadog_agent


VALID_PROFILE_TYPES = {"cpu", "heap", "mutex", "block", "goroutine"}
DEFAULT_PROFILE_DURATION = 30  # TODO: something more sensible
DEFAULT_PROFILES = ["cpu", "heap"]


def _timeformat(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


class GoPprofScraperCheck(AgentCheck):

    # This will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = "go_pprof_scraper"

    def __init__(self, name, init_config, instances):
        super(GoPprofScraperCheck, self).__init__(name, init_config, instances)

        self._get_apm_config()
        self.runtime_id = uuid4()

        self.service = self.instance.get("service")
        if not self.service:
            raise ConfigurationError("service is required")
        self.env = self.instance.get("env", datadog_agent.get_config("env"))

        self.url = self.instance.get("pprof_url")
        if not self.url:
            raise ConfigurationError("pprof_url is required")
        self.hostname = urlparse(self.url).hostname
        # TODO: What if self.hostname == "localhost" (or 127.0.0.1 or whatever?)

        self.duration = self.instance.get("duration", DEFAULT_PROFILE_DURATION)
        if self.duration > self.instance.get("min_collection_interval", 60):
            raise ConfigurationError(
                "duration ({}) is be longer than min_collection_interval ({})".format(
                    self.duration, self.instance.get("min_collection_interval")
                )
            )

        self.profiles = self.instance.get("profiles", DEFAULT_PROFILES)
        for profile in self.profiles:
            if profile not in VALID_PROFILE_TYPES:
                raise ConfigurationError(
                    "{} is not a valid profile type, must be one of {}".format(profile, VALID_PROFILE_TYPES)
                )
        self.profiles = list(set(self.profiles))

        self.cumulative = self.instance.get("cumulative", True)
        self.tags = self.instance.get("tags", [])
        self.tags.extend(self.init_config.get("tags", []))

    def _get_apm_config(self):
        # TODO: for some reason the config I get here doesn't match the real
        # config when I run "ddev env start --dev go_pprof_scraper py38". Here,
        # I see apm_config with enabled: True, the default receiver_port, etc.
        # But in the agent logs ("docker logs dd_go_pprof_scraper_py38") I see
        # stuff like
        #
        #   [date] TRACE | INFO | (run.go:103 in Run) | trace-agent not enabled. Set the environment variable
        #   DD_APM_ENABLED=true or add "apm_config.enabled: true" entry
        #   to your datadog.yaml. Exiting...
        apm_config = datadog_agent.get_config("apm_config")
        if not apm_config:
            self.apm_enabled = False
            return

        self.apm_enabled = apm_config["enabled"]
        self.trace_agent_port = apm_config["receiver_port"]
        # XXX: Will the hostname ever *not* be localhost? I don't think so since
        # this is being run by the agent
        self.trace_agent_url = "http://localhost:{}/profiling/v1/input".format(self.trace_agent_port)

        self.trace_agent_socket = quote(apm_config.get("receiver_socket", "").encode())
        if self.trace_agent_socket:
            self.trace_agent_socket = "http+unix://{}/profiling/v1/input".format(self.trace_agent_socket)

    def _get_profile(self, profile):
        query_params = {}
        if profile != "cpu" and self.cumulative:
            # cumulative profiles should still be collected *after*
            # self.duration so that all of the returned profiles reflect the
            # change in program state over the same time period
            time.sleep(self.duration)
        else:
            query_params["seconds"] = self.duration
        url = urljoin(self.url, "profile" if profile == "cpu" else profile)

        response = self.http.get(
            url,
            params=query_params,
            # We want to stream the response so that we can forward it to the
            # upload, ideally without having to actually read the whole profile
            # into memory
            stream=True,
            # We can get bit by the default timeout here when passing the "seconds"
            # query parameter. By design, the request takes that long to finish.
            #
            # requests supports a timeout parameter, which can be a tuple
            # (connect_timeout, read_timeout). The connect_timeout can be short, but
            # the read_timeout needs to be longer than the profile duration.
            timeout=(3.05, self.duration + 3),
        )

        response.raise_for_status()
        if profile == "cpu" or self.cumulative:
            name = profile
        else:
            name = "delta-{}".format(profile)
        return name, response

    def check(self, _):
        if not self.apm_enabled:
            self.service_check("can_connect", AgentCheck.CRITICAL, message="the trace agent is not enabled")
            return

        try:
            start = datetime.datetime.utcnow()
            with ThreadPoolExecutor() as executor:
                profiles = list(executor.map(self._get_profile, self.profiles))

            files = [
                # We want response.raw, because we're going to take the response
                # and feed it straight into the profile upload (see
                # self._get_profile)
                ("data[%s.pprof]" % name, ("pprof-data", response.raw, "application/octet-stream"))
                for name, response in profiles
            ]

            def add_form_field(name, value):
                files.append((name, (None, value)))

            add_form_field("host", self.hostname)
            add_form_field("version", "3")
            add_form_field("format", "pprof")
            add_form_field("family", "go")
            add_form_field("start", _timeformat(start))
            add_form_field("end", _timeformat(start + datetime.timedelta(seconds=self.duration)))
            add_form_field("tags[]", "runtime:go")
            add_form_field("tags[]", "service:{}".format(self.service))
            add_form_field("tags[]", "runtime-id:{}".format(self.runtime_id))
            if self.env:
                add_form_field("tags[]", "env:{}".format(self.env))
            for tag in self.tags:
                add_form_field("tags[]", tag)

            # TODO: container ID? If we can get it, it should be added as a
            # "Datadog-Container-ID" header to the request.

            if self.trace_agent_socket:
                session = requests_unixsocket.Session()
                r = session.post(self.trace_agent_socket, files=files)
            else:
                r = self.http.post(self.trace_agent_url, files=files)
            r.raise_for_status()
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
        except Exception as e:
            self.service_check(
                "can_connect",
                AgentCheck.CRITICAL,
                message="Request failed: {}, {}".format(self.url, e),
            )
            raise

        # If your check ran successfully, you can send the status.
        # More info at
        # https://datadoghq.dev/integrations-core/base/api/#datadog_checks.base.checks.base.AgentCheck.service_check
        self.service_check("can_connect", AgentCheck.OK, tags=[])
