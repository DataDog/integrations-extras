# Linux_vm_extras Integration

## Overview

Get metrics from linux_vm_extras in real time to visualize and monitor linux vmstat metrics.

## Installation

Install the `dd-check-linux_vm_extras` package manually or with your favorite configuration manager

## Configuration

There's no configuration necessary for this check, just copy the example file to
`/etc/dd-agent/conf.d/linux_vm_extras.py` to enable the check

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        linux_vm_extras
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 0 service checks

## Compatibility

The linux_vm_extras check is compatible with Linux platforms only
