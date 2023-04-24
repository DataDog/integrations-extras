from datadog_checks.cybersixgill_actionable_alerts.config_models.defaults import (
    instance_alerts_limit,
    instance_organization_id,
    instance_threat_level,
    instance_threat_type,
    shared_service,
)


def test_shared_service():
    field = "shared_service"
    value = "my_service"
    assert shared_service(field, value) == "my_service"


def test_instance_alerts_limit():
    field = "instance_alerts_limit"
    value = 100
    assert instance_alerts_limit(field, value) == 100


def test_instance_organization_id():
    field = "instance_organization_id"
    value = "my_organization"
    assert instance_organization_id(field, value) == "my_organization"


def test_instance_threat_level():
    field = "instance_threat_level"
    value = "high"
    assert instance_threat_level(field, value) == "high"


def test_instance_threat_type():
    field = "instance_threat_type"
    value = "malware"
    assert instance_threat_type(field, value) == "malware"
