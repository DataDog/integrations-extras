import json
import os
from datetime import datetime, timedelta

from requests.exceptions import ConnectionError, HTTPError, Timeout
from sixgill.sixgill_actionable_alert_client import SixgillActionableAlertClient

from datadog_checks.base import AgentCheck, ConfigurationError

Channel_Id = "d5cd46c205c20c87006b55a18b106428"


class CybersixgillActionableAlertsCheck(AgentCheck):
    SERVICE_CHECK_CONNECT_NAME = 'cybersixgill.can_connect'
    SERVICE_CHECK_HEALTH_NAME = 'cybersixgill.health'

    def __init__(self, name, init_config, instances):
        super(CybersixgillActionableAlertsCheck, self).__init__(name, init_config, instances)

    def check(self, instance):
        cl_id = self.instance.get('cl_id')
        cl_secret = self.instance.get('cl_secret')
        if not cl_id and cl_secret:
            raise ConfigurationError
        alerts_limit = self.instance.get('alerts_limit')
        threat_level = self.instance.get('threat_level')
        threat_type = self.instance.get('threat_type')
        organization_id = self.instance.get('organization_id')
        if not threat_level:
            threat_level = None
        threat_type_list = None
        if not organization_id:
            organization_id = None
        if threat_type:
            threat_type_list = threat_type.split(", ")
        try:
            file_dir = os.path.dirname(__file__)
            abs_file_path = os.path.join(file_dir, "date_threshold.txt")
            if os.path.exists(abs_file_path):
                file_data = open(abs_file_path, 'r')
                req_date = file_data.read()
                date_conv = json.loads(req_date)
                time_stamp_str = date_conv["from_date"]
                if time_stamp_str is not None:
                    from_datetime = datetime.strptime(time_stamp_str, "%Y-%m-%d %H:%M:%S")
                else:
                    from_datetime = datetime.now()
                    str_from_date = from_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    str_from_date = datetime.strptime(str_from_date, "%Y-%m-%d %H:%M:%S")
                    from_datetime = str_from_date - timedelta(days=90)
            else:
                from_datetime = datetime.now()
                str_from_date = from_datetime.strftime("%Y-%m-%d %H:%M:%S")
                str_from_date = datetime.strptime(str_from_date, "%Y-%m-%d %H:%M:%S")
                from_datetime = str_from_date - timedelta(days=90)
            to_datetime = datetime.now()
            str_today = to_datetime.strftime("%Y-%m-%d %H:%M:%S")
            str_today = datetime.strptime(str_today, "%Y-%m-%d %H:%M:%S")
            to_datetime = str_today
            sixgill_client = SixgillActionableAlertClient(
                client_id=cl_id, client_secret=cl_secret, channel_id=Channel_Id, verify=True
            )
            alerts = sixgill_client.get_actionable_alerts_bulk(
                limit=alerts_limit,
                from_date=from_datetime,
                to_date=to_datetime,
                threat_type=threat_type_list,
                threat_level=threat_level,
                organization_id=organization_id,
            )
            for al in alerts:
                alert_id = al.get("id")
                portal_url = f"https://portal.cybersixgill.com/#/?actionable_alert={alert_id}"
                alert_info = sixgill_client.get_actionable_alert(alert_id)
                additional_info = alert_info.get("additional_info")
                event_dict = {
                    "event_type": al.get("threat_level"),
                    "msg_title": al.get("title"),
                    "aggregation_key": al.get("id"),
                    "source_type_name": "Cybersixgill",
                    "tags": al.get("threats", []),
                    "priority": "normal",
                    "msg_text": f"Cybersixgill Portal URL: {portal_url}\n"
                    f"Description: {alert_info.get('description')}\n"
                    f"Content Type: {alert_info.get('content_type')}\n"
                    f"Created time: {alert_info.get('create_time')}\n"
                    f"Attributes: {alert_info.get('additional_info', {}).get('asset_attributes')}\n"
                    f"Threat Level: {alert_info.get('threat_level', 'Unknown')}\n"
                    f"Threat Type: {alert_info.get('threats', [])}\n"
                    f"Matched Assets: {alert_info.get('matched_assets', {})}\n",
                }
                if al.get('content', []):
                    event_dict["msg_text"] += f"Content: {al.get('content', [])}\n"
                if alert_info.get('assessment'):
                    event_dict["msg_text"] += f"Assessment: {alert_info.get('assessment', None)}\n"
                if alert_info.get('recommendations', []):
                    event_dict["msg_text"] += f"Recommendations: {alert_info.get('recommendations', [])}\n"
                if additional_info:
                    if 'cve_id' in additional_info:
                        event_dict["msg_text"] += f'Main CVE ID: {additional_info.get("cve_id")}\n'
                        event_dict["msg_text"] += f'CVE List: {additional_info.get("cve_list", [])}\n'
                        event_dict["msg_text"] += (
                            f'CVE Link: "https://portal.cybersixgill.com/#/cve/'
                            f'{additional_info.get("cve_id", "")}"\n '
                        )
                        event_dict[
                            "msg_text"
                        ] += f'CVSS 3.1: {additional_info.get("nvd", {}).get("v3", {}).get("current")}\n'
                        event_dict[
                            "msg_text"
                        ] += f'CVSS 2.0: {additional_info.get("nvd", {}).get("v2", {}).get("current")}\n'
                        event_dict["msg_text"] += f'DVE Score: {additional_info.get("score", {}).get("current")}\n'
                        attributes = []
                        attributes_dict = {}
                        for att in additional_info.get("attributes"):
                            if att.get("value"):
                                attributes_dict["Name"] = att.get("name")
                                attributes_dict["Description"] = att.get("description")
                                attributes.append(attributes_dict)
                        event_dict["msg_text"] += f'CVE Attributes: {attributes}'
                if "sub_alerts" in al:
                    sub_alerts = al.get('sub_alerts', [])
                    for sub in sub_alerts:
                        event_dict["msg_text"] += (
                            f"Aggregate Alert ID: {sub.get('aggregate_alert_id')}\n"
                            f"Content{sub.get('content')}\n"
                            f"Date{sub.get('date')}\n"
                            f"Read{sub.get('read')}\n"
                            f"Matched Assets: {sub.get('matched_assets')}\n"
                            f"{sub.get('site')}"
                        )
                self.event(event_dict)
                last_alert_time = alert_info.get("create_time")
                # self.write_persistent_cache("from_date", last_alert_time)
                time_dict = {'from_date': last_alert_time}
                txt_file_update = open(abs_file_path, 'w')
                txt_file_update.write(json.dumps(time_dict))
                txt_file_update.close()
            self.service_check(self.SERVICE_CHECK_CONNECT_NAME, AgentCheck.OK)
            self.service_check(self.SERVICE_CHECK_HEALTH_NAME, AgentCheck.OK)
        except (Timeout, HTTPError, ConnectionError) as e:
            error_message = f"Request Timeout {e}"
            self.service_check(self.SERVICE_CHECK_CONNECT_NAME, AgentCheck.CRITICAl, message=error_message)
            raise ConfigurationError
        except Exception as e:
            self.service_check(self.SERVICE_CHECK_HEALTH_NAME, AgentCheck.CRITICAL, message=str(e))
            raise
