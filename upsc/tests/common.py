# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

CHECK_NAME = 'upsc'
INSTANCES = [
    {
        'tags': ['foo:bar'],
        'string_tags': ['ups.testStringTag'],
        'excluded': ['ups.ignoreme'],
        'excluded_re': [r'ups\.ignore\..*'],
        'excluded_devices': ['ignoreme'],
        'excluded_devices_re': [r'ignore\..*']
    }
]
