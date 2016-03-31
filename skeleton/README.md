# Skeleton Integration

## Overview

Get metrics from skeleton service in real time to:

* Visualize and monitor skeleton states
* Be notified about skeleton failovers and events.

## Installation

Install the `dd-check-skeleton` package manually or with your favorite configuration manager

## Configuration

Edit the `skeleton.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        skeleton
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The skeleton check is compatible with all major platforms
