import pytest
from datadog_checks.cybersixgill_actionable_alerts.config_models.shared import SharedConfig


def test_shared_config_service():

    # Test that the service field is validated
    shared_config = SharedConfig(service="my_service")
    assert shared_config.service == "my_service"

    # # Test that the service field is not validated if it is None
    # shared_config = SharedConfig(service=None)
    # assert shared_config.service is ''

# def test_shared_config_defaults():
#     # Test that the default values are applied
#     shared_config = SharedConfig()
#     assert shared_config.field1 == "default_value1"
#     assert shared_config.field2 == "default_value2"
#
# def test_shared_config_validations():
#     # Test that the validations are applied
#     shared_config = SharedConfig(service="my_service", field1="invalid_value")
#     with pytest.raises(ValueError):
#         shared_config.validate()
#
#     shared_config = SharedConfig(service="my_service", field1="valid_value")
#     shared_config.validate()
