# Logstats Integration

## Overview

Get metrics from logstats service in real time to:

* Visualize and monitor logstats states
* Be notified about logstats failovers and events.

## Installation

Install the `dd-check-logstats` package manually or with your favorite configuration manager

## Configuration

Edit the `logstats.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        logstats
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The logstats check is compatible with all major platforms
