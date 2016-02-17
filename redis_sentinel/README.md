# Overview

Get metrics from Redis's Sentinel service in real time to:

* Visualize sentinels states
* Be notified about failovers

# Installation

Install the `dd-check-twemproxy` package

# Configuration

Edit the `redis_sentinel.yaml` file to point to your server and port, set the masters to monitor

# Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        redis_sentinel
        --------------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks
