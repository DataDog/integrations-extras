from datadog_checks.dev import get_docker_hostname

URL = 'http://{}:8000'.format(get_docker_hostname())


# fmt: off
INSTANCE = {
    'url': URL,
    'octo_api_key': 'FOO_KEY'
}

MOCK_EMPTY_JOB_RESPONSE = {
    "job": {
        "file": {
            "name": None,
            "origin": None,
            "size": None,
            "date": None,
        },
        "estimatedPrintTime": None,
        "filament": {
            "tool0": {
                "length": None,
                "volume": None,
            }
        }
    },
    "progress": {
        "completion": None,
        "filepos": None,
        "printTime": None,
        "printTimeLeft": None,
    },
    "state": "Operational"
}

MOCK_ACTIVE_JOB_RESPONSE = {
    "job": {
        "file": {
            "name": "whistle_v2.gcode",
            "origin": "local",
            "size": 1468987,
            "date": 1378847754
        },
        "estimatedPrintTime": 8811,
        "filament": {
            "tool0": {
                "length": 810,
                "volume": 5.36
            }
        }
    },
    "progress": {
        "completion": 0.22,
        "filepos": 337942,
        "printTime": 276,
        "printTimeLeft": 912
    },
    "state": "Printing"
}

MOCK_EXTRUDER_RESPONSE = {
    "tool0": {
        "actual": 25.0,
        "offset": 0,
        "target": 200.0
    }
}

MOCK_BED_RESPONSE = {
    "bed": {
        "actual": 24.77,
        "offset": 0,
        "target": 70.0
    }
}
# fmt: on
