import json
from datetime import datetime

import requests


def get_response(url):
    def wrapper(func):
        def inner_wrapper(self):
            initiate_pull_time = datetime.now()
            url1 = "{}://{}{}".format(self.protocol, self.hostname, url)
            resp = requests.get(url1, auth=(self.username, self.password), verify=False)
            return func(self, resp, initiate_pull_time, datetime.now())

        return inner_wrapper

    return wrapper


def add_latency_to_response(data, event_time, initiate_pull_time, recieve_time):
    response = data
    response["event_time"] = event_time
    response["initiate_pull_time"] = initiate_pull_time
    response["recieve_time"] = recieve_time
    return response


def _get_token_and_cookie_headers(token, vmanage_cookie):
    return {'Cookie': "JSESSIONID={}".format(vmanage_cookie), 'X-XSRF-TOKEN': token}


class vManageApi:
    def __init__(self, instance: dict) -> None:
        self.hostname = instance.get('hostname')
        self.username = instance.get('username')
        self.password = instance.get('password')
        self.protocol = instance.get('protocol')

    @get_response('/dataservice/client/token')
    def _get_token_and_cookie(self, resp, initiate_pull_time, recieve_time):
        for cookie in resp.cookies:
            if cookie.name == 'JSESSIONID':
                cookie_value = cookie.value
        return resp.text, cookie_value

    @get_response('/dataservice/network/connectionssummary')
    def get_connection_summary(self, resp, initiate_pull_time, recieve_time):
        response = {}
        connection_summary = []
        if resp.status_code == 200:
            connections_response = json.loads(resp.text)
            event_time = connections_response["header"]["generatedOn"]
            for conn in connections_response["data"]:
                connection = {"device": conn["name"], "total": conn["count"], "error": conn["statusList"][0]["count"]}
                connection_summary.append(connection)
                response["connection_summary"] = connection_summary
            response = add_latency_to_response(response, event_time, initiate_pull_time, recieve_time)
        return response

    @get_response('/dataservice/certificate/stats/summary')
    def get_certificate_summary(self, resp, initiate_pull_time, recieve_time):
        response = {}
        if resp.status_code == 200:
            response = resp.json()["data"][0]
            response["initiate_pull_time"] = initiate_pull_time
            response["recieve_time"] = recieve_time
        return response

    @get_response('/dataservice/network/issues/rebootcount')
    def get_reboot_count(self, resp, initiate_pull_time, recieve_time):
        response = {}
        if resp.status_code == 200:
            response = resp.json()["data"][0]
            response["initiate_pull_time"] = initiate_pull_time
            response["recieve_time"] = recieve_time
        return response

    @get_response('/dataservice/clusterManagement/health/summary')
    def get_vmanage_count(self, resp, initiate_pull_time, recieve_time):
        response = {}
        if resp.status_code == 200:
            event_time = resp.json()["header"]["generatedOn"]
            response = add_latency_to_response(resp.json()["data"][0], event_time, initiate_pull_time, recieve_time)
        return response

    @get_response('/dataservice/device/control/count')
    def get_control_status(self, resp, initiate_pull_time, recieve_time):
        response = {}
        if resp.status_code == 200:
            event_time = resp.json()["header"]["generatedOn"]
            response["data"] = resp.json()["data"][0]["statusList"]
            response = add_latency_to_response(response, event_time, initiate_pull_time, recieve_time)
        return response

    @get_response('/dataservice/device/bfd/sites/summary')
    def get_site_health(self, resp, initiate_pull_time, recieve_time):
        response = {}
        if resp.status_code == 200:
            event_time = resp.json()["header"]["generatedOn"]
            response["data"] = resp.json()["data"][0]["statusList"]
            response = add_latency_to_response(response, event_time, initiate_pull_time, recieve_time)
        return response

    @get_response('/dataservice/device/tlocutil')
    def get_transport_interface(self, resp, initiate_pull_time, recieve_time):
        response = {}
        if resp.status_code == 200:
            event_time = resp.json()["header"]["generatedOn"]
            response["data"] = resp.json()["data"]
            response = add_latency_to_response(response, event_time, initiate_pull_time, recieve_time)
        return response

    @get_response('/dataservice/device/hardwarehealth/summary')
    def get_wan_edge_health(self, resp, initiate_pull_time, recieve_time):
        response = {}
        if resp.status_code == 200:
            event_time = resp.json()["header"]["generatedOn"]
            response["data"] = resp.json()["data"][0]["statusList"]
            response = add_latency_to_response(response, event_time, initiate_pull_time, recieve_time)
        return response

    # new end points
    @get_response('/dataservice/device/vedgeinventory/summary')
    def get_wan_edge_inventory(self, resp, initiate_pull_time, recieve_time):
        response = {}
        if resp.status_code == 200:
            event_time = resp.json()["header"]["generatedOn"]
            response["data"] = resp.json()["data"]
            response = add_latency_to_response(response, event_time, initiate_pull_time, recieve_time)
        return response

    @get_response('/dataservice/statistics/approute/transport/summary/loss_percentage')
    def get_transport_health(self, resp, initiate_pull_time, recieve_time):
        response = {}
        if resp.status_code == 200:
            response = resp.json()["data"][0]
            response["initiate_pull_time"] = initiate_pull_time
            response["recieve_time"] = recieve_time
        return response

    def get_top_application(self):
        response = {}
        token, vmanage_cookie = self._get_token_and_cookie()
        url = '/dataservice/statistics/dpi/applications/summary'
        initiate_pull_time = datetime.now()
        url1 = "{}://{}{}".format(self.protocol, self.hostname, url)
        resp = requests.get(
            url1,
            auth=(self.username, self.password),
            headers=_get_token_and_cookie_headers(token, vmanage_cookie),
            verify=False,
        )
        recieve_time = datetime.now()
        event_time = resp.json()["header"]["generatedOn"]
        response["data"] = resp.json()["data"]
        response = add_latency_to_response(response, event_time, initiate_pull_time, recieve_time)
        return response

    @get_response('/dataservice/statistics/approute/tunnels/summary/loss')
    def get_app_aware_routing(self, resp, initiate_pull_time, recieve_time):
        response = {}
        if resp.status_code == 200:
            response["data"] = resp.json()["data"]
            response["initiate_pull_time"] = initiate_pull_time
            response["recieve_time"] = recieve_time
        return response

    @get_response('/dataservice/device')
    def get_device_info(self, resp, initiate_pull_time, recieve_time):
        return resp.json()
