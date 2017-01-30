# Mysql Integration

## Overview

Get metrics from mysql service in real time to:

* Visualize and monitor mysql states
* Be notified about mysql failovers and events.

## Installation

Install the `dd-check-mysql` package manually or with your favorite configuration manager

## Configuration

Edit the `mysql.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        mysql
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The mysql check is compatible with all major platforms
