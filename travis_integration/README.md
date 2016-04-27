# Travis_integration Integration

## Overview

Get metrics from travis_integration service in real time to:

* Visualize and monitor travis_integration states
* Be notified about travis_integration failovers and events.

## Installation

Install the `dd-check-travis_integration` package manually or with your favorite configuration manager

## Configuration

Edit the `travis_integration.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        travis_integration
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The travis_integration check is compatible with all major platforms
