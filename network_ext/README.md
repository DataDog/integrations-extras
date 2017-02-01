# Network_ext Integration

## Overview

Get metrics from network_ext service in real time to:

* Visualize and monitor network_ext states
* Be notified about network_ext failovers and events.

## Installation

Install the `dd-check-network_ext` package manually or with your favorite configuration manager

## Configuration

Edit the `network_ext.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        network_ext
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The network_ext check is compatible with all major platforms
