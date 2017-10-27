# Storm Integration

## Overview

Get metrics from storm service in real time to:

* Visualize and monitor storm cluster and topology metrics.
* Be notified about storm failovers and events.

## Installation

Install the `dd-check-storm` package manually or with your favorite configuration manager

## Configuration

Edit the `storm.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        storm
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The storm check is compatible with all major platforms, and apache storm version 1.x.x line.
