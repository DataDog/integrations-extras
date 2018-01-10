# UPSC Stats Collector Integration

## Overview

Get metrics from UPSD service via upsc in real time to:

* Visualize and monitor UPS battery health and states
* Be notified about UPS failovers and events.

## Installation

Install the `dd-check-upsc` package manually or with your favorite configuration manager

## Configuration

Edit the `upsc.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        upsc
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The UPSC check is compatible with linux-based platforms.
