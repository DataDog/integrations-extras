# Powerdns_authoritative Integration

## Overview

Get metrics from powerdns_authoritative service in real time to:

* Visualize and monitor powerdns_authoritative states
* Be notified about powerdns_authoritative failovers and events.

## Installation

Install the `dd-check-powerdns_authoritative` package manually or with your favorite configuration manager

## Configuration

Edit the `powerdns_authoritative.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        powerdns_authoritative
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The powerdns_authoritative check is compatible with all major platforms
