# Helloworld Integration

## Overview

Get metrics from helloworld service in real time to:

* Visualize and monitor helloworld states
* Be notified about helloworld failovers and events.

## Installation

Install the `dd-check-helloworld` package manually or with your favorite configuration manager

## Configuration

Edit the `helloworld.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        helloworld
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The helloworld check is compatible with all major platforms
