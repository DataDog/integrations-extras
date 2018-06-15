# Sortdb Integration

## Overview

Get metrics from sortdb service in real time to:

* Visualize and monitor sortdb stats.
* Be notified about sortdb failovers.
* Check health of and get stats from multiple instances

## Installation

Install the `dd-check-sortdb` package manually or with your favorite configuration manager

## Configuration

Edit the `sortdb.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        sortdb
        -----------
          - instance #0 [OK]
          - Collected 28 metrics, 0 events & 1 service checks

## Compatibility

The sortdb check is compatible with all major platforms
