# Pm2 Integration

## Overview

Get metrics from pm2 service in real time to:

* Visualize and monitor pm2 states
* Be notified about pm2 failovers and events.

## Installation

Install the `dd-check-pm2` package manually or with your favorite configuration manager

## Configuration

Edit the `pm2.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        pm2
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The pm2 check is compatible with all major platforms
