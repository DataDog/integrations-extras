import pytest
from datadog_checks.cybersixgill_actionable_alerts.config_models.instance import InstanceConfig

def test_instance_config_initialization():
    # Test that an instance of InstanceConfig can be initialized with valid values
    config = InstanceConfig(
        alerts_limit=10,
        cl_id='my_client_id',
        cl_secret='my_client_secret',
        organization_id='my_org_id',
        threat_level='high',
        threat_type='Malware'
    )
    assert config.alerts_limit == 10
    assert config.cl_id == 'my_client_id'
    assert config.cl_secret == 'my_client_secret'
    assert config.organization_id == 'my_org_id'
    assert config.threat_level == 'high'
    assert config.threat_type == 'Malware'
#
# def test_instance_config_missing_required_field():
#     # Test that an instance of InstanceConfig cannot be initialized without a required field
#     with pytest.raises(ValueError):
#         config = InstanceConfig(
#             alerts_limit=10,
#             cl_id='',
#             cl_secret='my_client_secret',
#             threat_level='high',
#             threat_type='Malware'
#         )
#
# def test_instance_config_invalid_field_value():
#     # Test that an instance of InstanceConfig cannot be initialized with an invalid field value
#     with pytest.raises(ValueError):
#         config = InstanceConfig(
#             alerts_limit=10,
#             cl_id='my_client_id',
#             cl_secret='my_client_secret',
#             organization_id='my_org_id',
#             threat_level='not_a_valid_threat_level',
#             threat_type='Malware'
#         )
