# Logstash Integration

## Overview

Get metrics from logstash service in real time to:

* Visualize and monitor logstash states
* Be notified about logstash failovers and events.

## Installation

Install the `dd-check-logstash` package manually or with your favorite configuration manager

## Configuration

Edit the `logstash.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        logstash
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The logstash check is compatible with all major platforms
