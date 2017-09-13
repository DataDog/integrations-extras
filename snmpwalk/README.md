# Snmpwalk Integration

## Overview

Get metrics from snmpwalk service in real time to:

* Visualize and monitor snmpwalk states
* Be notified about snmpwalk failovers and events.

## Installation

Install the `dd-check-snmpwalk` package manually or with your favorite configuration manager

## Configuration

Edit the `snmpwalk.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        snmpwalk
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The snmpwalk check is compatible with all major platforms
