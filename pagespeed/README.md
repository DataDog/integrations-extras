# Pagespeed Integration

## Overview

Get metrics from pagespeed service in real time to:

* Visualize and monitor pagespeed states
* Be notified about pagespeed failovers and events.

## Installation

Install the `dd-check-pagespeed` package manually or with your favorite configuration manager

## Configuration

Edit the `pagespeed.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        pagespeed
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The pagespeed check is compatible with all major platforms
