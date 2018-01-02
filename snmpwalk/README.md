# Snmpwalk Integration

## Overview

Get metrics from snmpwalk service in real time to:

* Visualize and monitor snmpwalk states
* Be notified about snmpwalk failovers and events.

## Setup
### Installation

Install the `dd-check-snmpwalk` package manually or with your favorite configuration manager

### Configuration

Edit the `snmpwalk.yaml` file to point to your server and port, set the masters to monitor

### Validation

[Run the Agent's `info` subcommand](https://docs.datadoghq.com/agent/faq/agent-status-and-information/), you should see something like the following:

    Checks
    ======

        snmpwalk
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The snmpwalk check is compatible with all major platforms

## Data Collected
### Metrics

The SNMP walk check does not include any event at this time.

### Events
The SNMP walk check does not include any event at this time.

### Service Checks
The SNMP walk check does not include any service check at this time.

## Troubleshooting
Need help? Contact [Datadog Support](http://docs.datadoghq.com/help/).

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog](https://www.datadoghq.com/blog/)