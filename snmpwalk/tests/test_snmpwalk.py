# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

import os

from datadog_checks.snmpwalk import SnmpwalkCheck

from .common import HERE

RESULTS_TIMEOUT = 10


CHECK_NAME = 'snmpwalk'
FIXTURE_DIR = os.path.join(os.path.dirname(__file__), 'ci')

CHECK_TAGS = ['snmp_device:localhost:161']

TABULAR_OBJECTS = [
    {
        'MIB': "IF-MIB",
        'table': "ifTable",
        'symbols': ["ifInOctets", "ifOutOctets"],
        'metric_tags': [{'tag': "interface", 'column': "ifDescr"}, {'tag': "dumbindex", 'index': 1}],
    }
]


def generate_instance_config(instance_config, metrics):
    instance_config['metrics'] = metrics
    instance_config['name'] = 'localhost'
    return instance_config


def test_check(aggregator, dd_environment):
    """
    Testing Snmpwrap check.
    """
    instance = generate_instance_config(dd_environment, TABULAR_OBJECTS)
    config = {'binary': os.path.join(HERE, "script.sh")}
    check = SnmpwalkCheck(CHECK_NAME, config, {})
    check.check(instance)

    # Test metrics
    for symbol in TABULAR_OBJECTS[0]['symbols']:
        metric_name = '{}.{}'.format(CHECK_NAME, symbol)
        aggregator.assert_metric(metric_name, at_least=1)
        aggregator.assert_metric_has_tag(metric_name, CHECK_TAGS[0], at_least=1)

        for mtag in TABULAR_OBJECTS[0]['metric_tags']:
            tag = mtag['tag']
            if tag == 'dumbindex':  # unsupported
                aggregator.assert_metric_has_tag_prefix(metric_name, tag, count=0)
            else:
                aggregator.assert_metric_has_tag_prefix(metric_name, tag, at_least=1)

    # Test service check
    svcchk_name = '{}.can_check'.format(CHECK_NAME)
    aggregator.assert_service_check(
        svcchk_name, status=SnmpwalkCheck.OK, tags=[':'.join(CHECK_TAGS[0].split(':')[:-1])], count=1
    )

    aggregator.assert_all_metrics_covered()


def test_unavailable_binary(caplog):
    """
    Should log exception if binary is unavailable.
    """
    config = {'binary': '/path/to/nonexistent/snmpwalk'}
    instance = generate_instance_config({}, TABULAR_OBJECTS)

    check = SnmpwalkCheck(CHECK_NAME, config, {})
    check.check(instance)

    assert 'Cannot find executable: /path/to/nonexistent/snmpwalk' in caplog.text
