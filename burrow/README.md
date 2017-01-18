# Burrow Integration

## Overview

Get metrics from burrow service in real time to:

* Visualize kafka09 lag metrics
* Monitor lag status of all kafka clusters and consumers

See https://github.com/linkedin/Burrow

## Installation

Install the `dd-check-burrow` package manually or with your favorite configuration manager

## Configuration

Edit the `burrow.yaml` file to point to your burrow http endpoint, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        burrow
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The burrow check is compatible with all major platforms
