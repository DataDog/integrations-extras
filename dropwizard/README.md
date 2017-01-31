# Dropwizard Integration

## Overview

Get metrics from dropwizard service in real time to:

* Visualize and monitor dropwizard states
* Be notified about dropwizard failovers and events.

## Installation

Install the `dd-check-dropwizard` package manually or with your favorite configuration manager

## Configuration

Edit the `dropwizard.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        dropwizard
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The dropwizard check is compatible with all major platforms
