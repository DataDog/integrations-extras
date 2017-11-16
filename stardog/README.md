# Stardog Integration

## Overview

Get metrics from stardog service in real time to:

* Visualize and monitor stardog states
* Be notified about stardog failovers and events.

## Installation

Install the `dd-check-stardog` package manually or with your favorite configuration manager

## Configuration

Edit the `stardog.yaml` file to point to your server and set the admin username and password

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        stardog
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The stardog check is compatible with all major platforms
