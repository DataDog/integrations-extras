from json import JSONDecodeError
from urllib.parse import urlparse

from requests.exceptions import ConnectionError, HTTPError, InvalidURL, Timeout

from datadog_checks.base import AgentCheck, errors

SCALR_DD_METRICS_ENDPOINT = "{}/api/iacp/v3/accounts/{}/metrics"
SCALR_FIND_ACCOUNT_ENDPOINT = "{}/api/iacp/v3/accounts?filter[name]={}"
SCALR_URL_PARAM = "url"
SCALR_ACCESS_TOKEN_PARAM = "access_token"


class ScalrCheck(AgentCheck):

    __NAMESPACE__ = "scalr"

    SERVICE_CHECK_NAME = "can_connect"

    SCALR_ACCOUNT_METRICS = {
        "environments-count": "environments.count",
        "workspaces-count": "workspaces.count",
        "runs-count": "runs.count",
        "runs-successful": "runs.successful",
        "runs-failed": "runs.failed",
        "runs-awaiting-confirmation": "runs.awaiting_confirmation",
        "runs-concurrency": "runs.concurrency",
        "runs-queue-size": "runs.queue_size",
        "quota-max-concurrency": "quota.max_concurrency",
        "billings-runs-count": "billing.runs.count",
        "billings-run-minutes-count": "billing.run_minutes.count",
        "billings-flex-runs-count": "billing.flex_runs.count",
        "billings-flex-runs-minutes-count": "billing.flex_run_minutes.count",
    }

    def __init__(self, name, init_config, instances):
        super(ScalrCheck, self).__init__(name, init_config, instances)

        self.url = self.instance.get(SCALR_URL_PARAM)
        self.token = self.instance.get(SCALR_ACCESS_TOKEN_PARAM)
        self.account_id = self._get_account_id()

    def check(self, instance):

        try:
            response_json = self._get_json(SCALR_DD_METRICS_ENDPOINT.format(self.url, self.account_id))

            for key, name in self.SCALR_ACCOUNT_METRICS.items():
                if response_json.get(key) is not None:
                    self.gauge(name, response_json[key], tags=instance.get('tags', []))

            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.OK)
        except Timeout as e:
            self.service_check(
                self.SERVICE_CHECK_NAME,
                AgentCheck.CRITICAL,
                message="Request timeout: {}, {}".format(self.url, e),
            )
            self.log.exception("Communication with Scalr timed out. %s", e)

        except (HTTPError, InvalidURL, ConnectionError) as e:
            self.service_check(
                self.SERVICE_CHECK_NAME,
                AgentCheck.CRITICAL,
                message="Request failed: {}, {}".format(self.url, e),
            )
            self.log.exception("Couldn't reach Scalr. %s", e)

        except JSONDecodeError as e:
            self.service_check(
                self.SERVICE_CHECK_NAME,
                AgentCheck.CRITICAL,
                message="JSON Parse failed: {}, {}".format(self.url, e),
            )
            self.log.exception("Unexpected response from Scalr. %s", e)

        except ValueError as e:
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.CRITICAL, message=str(e))
            self.log.exception(str(e))

    def _get_account_id(self) -> str:
        parsed_url = urlparse(self.url)
        loc = parsed_url.netloc.find('.')
        domain_name = parsed_url.netloc[:loc]
        if -1 == loc or not domain_name:
            raise errors.ConfigurationError(
                f"Scalr instance configuration '{SCALR_URL_PARAM}' is not correct. "
                "Value should be in format https://<account_name>.scalr.io"
            )

        res: dict = self._get_json(SCALR_FIND_ACCOUNT_ENDPOINT.format(self.url, domain_name))
        data = res.get("data", [])
        if type(data) is not list or len(data) != 1:
            raise errors.CheckException("SCALR account not found.")

        acc_id = data[0]['id']

        return acc_id

    def _get_json(self, endpoint) -> dict:
        response = self.http.get(
            endpoint,
            extra_headers=self._get_extra_headers(),
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def _get_extra_headers(self) -> dict:
        return {
            "Accept": "application/vnd.api+json, application/json",
            "Authorization": "Bearer {}".format(self.token),
            "Prefer": "profile=preview",
        }
