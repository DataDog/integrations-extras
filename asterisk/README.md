# Asterisk Integration

## Overview

Get metrics from asterisk service in real time to:

* Visualize and monitor asterisk states
* Be notified about asterisk failovers and events.

## Installation

Install the `dd-check-asterisk` package manually or with your favorite configuration manager

## Configuration

Edit the `asterisk.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        asterisk
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The asterisk check is compatible with all major platforms
