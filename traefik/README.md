# Traefik Integration

## Overview

Get metrics from traefik in real time to:

* Visualize and monitor requests and error served by traefik

## Installation

Install the `dd-check-traefik` package manually or with your favorite configuration manager

## Configuration

Edit the `traefik.yaml` file to point to your server and port, set the masters to monitor. Alternatively you can setup [auto discovery](http://docs.datadoghq.com/guides/autodiscovery/) to configure the check automatically.

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        traefik
        -----------
          - instance #0 [OK]
          - Collected 7 metrics, 0 events & 0 service checks

## Compatibility

The traefik check is compatible with all major platforms
