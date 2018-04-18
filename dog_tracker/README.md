# Dog Tracker

## Overview

Track your dogs! Or people or devices locations.

* Visualize what city, state, country, latitude and longitude the agent is reporting from
* Setup Alerts on changes?

**Note: This can be totally creepy if used on humans, should be opt-in only, but if you have a large remote crowd that travels it could also be fun. Please don't abuse this.**

## Installation

Install the `dd-check-dog-tracker` package manually or with your favorite configuration manager

## Configuration

Edit the `dog_tracker.yaml` file with name of the `dog` you want to track.

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        dog_tracker
        -----------
          - instance #0 [OK]
          - Collected 3 metrics, 0 events & 0 service checks

## Compatibility

The dog_tracker check is compatible with all major platforms
