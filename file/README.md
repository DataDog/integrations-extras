# File Integration

## Overview

Get metrics from file service in real time to:

* Visualize and monitor file states
* Be notified about file failovers and events.

## Installation

Install the `dd-check-file` package manually or with your favorite configuration manager

## Configuration

Edit the `file.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        file
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The file check is compatible with all major platforms
