# Aerospike Integration

## Overview

Get metrics from Aerospike Database in real time to:

* Visualize and monitor aerospike states
* Be notified about aerospike failovers and events.

## Installation

Install the `dd-check-aerospike` package manually or with your favorite configuration manager

## Configuration

Edit the `aerospike.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        aerospike
        -----------
          - instance #0 [OK]
          - Collected 269 metrics, 0 events & 1 service checks

## Compatibility

The Aerospike check is compatible with all major platforms and Aerospike Community Edition


