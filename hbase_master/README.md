# Hbase_master Integration

## Overview

Get metrics from hbase_master service in real time to:

* Visualize and monitor hbase_master states
* Be notified about hbase_master failovers and events.

## Installation

Install the `dd-check-hbase_master` package manually or with your favorite configuration manager

## Configuration

Edit the `hbase_master.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        hbase_master
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 0 service checks

## Compatibility

The hbase_master check is compatible with all major platforms
