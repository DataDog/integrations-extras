# This file is autogenerated.
# To change this file you should edit assets/configuration/spec.yaml and then run the following commands:
#     ddev -x validate config -s <INTEGRATION_NAME>
#     ddev -x validate models -s <INTEGRATION_NAME>

from datadog_checks.base.utils.models.fields import get_default_field_value


def shared_service(field, value):
    return 'kamailio'


def instance_disable_generic_tags(field, value):
    return False


def instance_empty_default_hostname(field, value):
    return False


def instance_get_modules_from_mmaps(field, value):
    return False


def instance_jsonrpc_config(field, value):
    return get_default_field_value(field, value)


def instance_metric_patterns(field, value):
    return get_default_field_value(field, value)


def instance_min_collection_interval(field, value):
    return 60


def instance_service(field, value):
    return get_default_field_value(field, value)


def instance_tags(field, value):
    return get_default_field_value(field, value)
