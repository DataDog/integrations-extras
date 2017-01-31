# Proxysql Integration

## Overview

Get metrics from proxysql service in real time to:

* Visualize and monitor proxysql states
* Be notified about proxysql failovers and events.

## Installation

Install the `dd-check-proxysql` package manually or with your favorite configuration manager

## Configuration

Edit the `proxysql.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        proxysql
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The proxysql check is compatible with all major platforms
