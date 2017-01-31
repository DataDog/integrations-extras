# Unbound Integration

## Overview

Get metrics from unbound service in real time to:

* Visualize and monitor unbound states
* Be notified about unbound failovers and events.

## Installation

Install the `dd-check-unbound` package manually or with your favorite configuration manager

## Configuration

Edit the `unbound.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        unbound
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The unbound check is compatible with all major platforms
