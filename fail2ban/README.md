# Fail2ban Integration

## Overview

Get metrics from fail2ban service in real time to:

* Visualize and monitor fail2ban states
* Be notified about fail2ban failovers and events.

## Installation

Install the `dd-check-fail2ban` package manually or with your favorite configuration manager

## Configuration

Edit the `fail2ban.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        fail2ban
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The fail2ban check is compatible with all major platforms
