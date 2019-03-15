# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
from os.path import isfile


def test_ok(aggregator, check, instance_ok):
    assert isfile(instance_ok['created_at_file'])

    check.check(instance_ok)

    aggregator.assert_service_check('system.reboot_required', status=check.OK)


def test_not_present_ok(aggregator, check, instance_not_present):
    assert not isfile(instance_not_present['created_at_file'])

    check.check(instance_not_present)

    aggregator.assert_service_check('system.reboot_required', status=check.OK)


def test_warning(aggregator, check, instance_warning):
    check.check(instance_warning)

    aggregator.assert_service_check('system.reboot_required', status=check.WARNING)


def test_critical(aggregator, check, instance_critical):
    check.check(instance_critical)

    aggregator.assert_service_check('system.reboot_required', status=check.CRITICAL)
