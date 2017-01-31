# Nsq Integration

## Overview

Get metrics from nsq service in real time to:

* Visualize and monitor nsq states
* Be notified about nsq failovers and events.

## Installation

Install the `dd-check-nsq` package manually or with your favorite configuration manager

## Configuration

Edit the `nsq.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        nsq
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The nsq check is compatible with all major platforms
