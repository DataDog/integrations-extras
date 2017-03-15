# Apt Integration

## Overview

Get metrics from apt service in real time to:

* Visualize and monitor apt states
* Be notified about apt failovers and events.

## Installation

Install the `dd-check-apt` package manually or with your favorite configuration manager

## Configuration

Edit the `apt.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        apt
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The apt check is compatible with all major platforms
