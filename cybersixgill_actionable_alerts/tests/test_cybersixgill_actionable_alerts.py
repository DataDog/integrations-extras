import pytest

from datadog_checks.cybersixgill_actionable_alerts.check import (
    CybersixgillActionableAlertsCheck,
)

# from ..datadog_checks.cybersixgill_actionable_alerts.check import CybersixgillActionableAlertsCheck

incidents_list = [
    {
        "alert_name": "Your organization was potentially targeted by a ransomware group",
        "content": "text",
        "date": "2021-11-08 06:01:05",
        "id": "6188bd21017198385e228437",
        "read": True,
        "severity": 1,
        "site": "rw_everest",
        "status": {"name": "in_treatment", "user": "60b604a048ce2cb294629a2d"},
        "threat_level": "imminent",
        "threats": ["Brand Protection", "Data Leak"],
        "title": "Your organization was potentially targeted by a ransomware group",
        "user_id": "5d233575f8db38787dbe24b6",
    },
    {
        "alert_name": "Gift Cards of {organization_name} are Sold on the Underground ",
        "category": "regular",
        "content": "text",
        "date": "2021-11-02 06:00:27",
        "id": "6180d4011dbb8edcb496ec8b",
        "lang": "English",
        "langcode": "en",
        "read": False,
        "threat_level": "imminent",
        "threats": ["Fraud"],
        "title": "Gift Cards of Sixgill are Sold on the Underground ",
        "user_id": "5d233575f8db38787dbe24b6",
    },
]

info_item = {
    "alert_id": "616ffed97a1b66036a138f73",
    "alert_name": "Your organization was potentially targeted by a ransomware group",
    "alert_type": "QueryBasedManagedAlertRule",
    "assessment": "text",
    "category": "regular",
    "content_type": "search_result_item",
    "description": 'A ransomware group posted on its leak site, rw_everest, focusing on "Walmart" ',
}

expected_alert_output = {
    "event_type": "imminent",
    "api_key": "c16896127b23db13ff905496e339a0bf",
    "msg_title": "Name of the alert",
    "aggregation_key": "324234234122",
    "source_type_name": "Cybersixgill",
    "tags": ["fraud", "malware"],
    "priority": "normal",
    "msg_txt": "Cybersixgill Portal URL- https://portal.cybersixgill.com/#/?actionable_alert=634\n"
    "Description- Sixgill discovered 182 Cybersixgill compromised credit cards\n"
    "Content Type- table_content_item\n"
    "Created time- 2022-10-11 05:04:52\n"
    "Attributes- None\n"
    "Threat Level- imminent\n"
    "Threat Type- ['Fraud', 'Compromised Accounts']\n"
    "Matched Assets- ['404137', '401795']",
}


def test_config_empty(aggregator):
    instance = {}
    with pytest.raises(Exception):
        c = CybersixgillActionableAlertsCheck('cybersixgill_actionable_alerts', {}, [instance])
        c.check(instance)
        aggregator.assert_service_check(
            CybersixgillActionableAlertsCheck.SERVICE_CHECK_HEALTH_NAME,
            CybersixgillActionableAlertsCheck.CRITICAL,
        )


def test_invalid_config(aggregator):
    instance = {"cl_id": "clientid", "cl_secret": "clientsecret"}
    with pytest.raises(Exception):
        c = CybersixgillActionableAlertsCheck('cybersixgill_actionable_alerts', {}, [instance])
        c.check(instance)
        aggregator.assert_service_check(
            CybersixgillActionableAlertsCheck.SERVICE_CHECK_HEALTH_NAME,
            CybersixgillActionableAlertsCheck.CRITICAL,
        )


def test_check(aggregator, instance, mocker):
    from sixgill.sixgill_actionable_alert_client import SixgillActionableAlertClient

    c = CybersixgillActionableAlertsCheck('cybersixgill_actionable_alerts', {}, [instance])
    instance["cl_id"] = "clientid"
    instance["cl_secret"] = "clientsecret"
    mocker.patch.object(SixgillActionableAlertClient, 'get_actionable_alerts_bulk', return_value=incidents_list)
    mocker.patch.object(SixgillActionableAlertClient, 'get_actionable_alert', return_value=info_item)
    c.check(instance)
    aggregator.assert_service_check(
        CybersixgillActionableAlertsCheck.SERVICE_CHECK_CONNECT_NAME,
        CybersixgillActionableAlertsCheck.OK,
    )
    aggregator.assert_all_metrics_covered()
