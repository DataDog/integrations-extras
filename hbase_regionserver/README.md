# Hbase_regionserver Integration

## Overview

Get metrics from hbase_regionserver service in real time to:

* Visualize and monitor hbase_regionserver states
* Be notified about hbase_regionserver failovers and events.

## Installation

Install the `dd-check-hbase_regionserver` package manually or with your favorite configuration manager

## Configuration

Edit the `hbase_regionserver.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        hbase_regionserver
        -----------
          - instance #0 [OK]
          - Collected 150 metrics, 0 events & 0 service checks

## Compatibility

The hbase_regionserver check is compatible with all major platforms
