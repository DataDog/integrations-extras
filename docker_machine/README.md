# Docker_machine Integration

## Overview

Get metrics from docker_machine service in real time to:

* Visualize and monitor docker_machine states
* Be notified about docker_machine failovers and events.

## Installation

Install the `dd-check-docker_machine` package manually or with your favorite configuration manager

## Configuration

Edit the `docker_machine.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        docker_machine
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The docker_machine check is compatible with all major platforms
