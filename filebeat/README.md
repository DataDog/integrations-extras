# Filebeat Integration

## Overview

Get metrics from filebeat service in real time to:

* Visualize and monitor filebeat states
* Be notified about filebeat failovers and events.

## Installation

Install the `dd-check-filebeat` package manually or with your favorite configuration manager

## Configuration

Edit the `filebeat.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        filebeat
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The filebeat check is compatible with all major platforms
