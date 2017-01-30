# Http_json Integration

## Overview

Get metrics from http_json service in real time to:

* Visualize and monitor http_json states
* Be notified about http_json failovers and events.

## Installation

Install the `dd-check-http_json` package manually or with your favorite configuration manager

## Configuration

Edit the `http_json.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        http_json
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The http_json check is compatible with all major platforms
