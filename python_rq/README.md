# Python_rq Integration

## Overview

Get metrics from python_rq service in real time to:

* Visualize and monitor python_rq states
* Be notified about python_rq failovers and events.

## Installation

Install the `dd-check-python_rq` package manually or with your favorite configuration manager

## Configuration

Edit the `python_rq.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        python_rq
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The python_rq check is compatible with all major platforms
