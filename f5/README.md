# F5 Integration

## Overview

Get metrics from f5 service in real time to:

* Visualize and monitor f5 states
* Be notified about f5 failovers and events.

## Installation

Install the `dd-check-f5` package manually or with your favorite configuration manager

## Configuration

Edit the `f5.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        f5
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The f5 check is compatible with all major platforms
