# Sidekiq Integration

## Overview

Get metrics from sidekiq service in real time to:

* Visualize and monitor sidekiq states
* Be notified about sidekiq failovers and events.

## Installation

Install the `dd-check-sidekiq` package manually or with your favorite configuration manager

## Configuration

Edit the `sidekiq.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        sidekiq
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The sidekiq check is compatible with all major platforms
