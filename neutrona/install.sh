#!/bin/bash

cp ./datadog_checks/neutrona/neutrona.py /etc/datadog-agent/checks.d/neutrona.py
cp ./datadog_checks/neutrona/data/conf.yaml.example /etc/datadog-agent/conf.d/neutrona.d/conf.yaml

service datadog-agent restart

