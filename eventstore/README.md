# EventStore Integration

## Overview

Get metrics from Eventstore in real time to:

* Visualize and monitor EventStore queues
* capture all available metrics within the stats api


## Setup

### Installation

To install please see the datadog documentation: https://docs.datadoghq.com/ja/guides/installcoreextra/

### Configuration

  1. Edit the eventstore.d/conf.yaml file, in the conf.d/ folder at the root of your Agent's configuration directory to start collecting your eventstore performance data. See the sample eventstore.d/eventstore.yaml.default for all available configuration options.

  2. Restart the Agent

### Validation

[Run the Agent's `status` subcommand][4] and look for `eventstore` under the Checks section:

## Compatibility

The check is compatible with all major platforms.

## Data Collected

### Metrics

Able to collect all numeric or datetime metrics supplied by the api, it will require you to add metric_definitions for new metrics, all current metrics are listed

### Events

The eventstore check does not include any event at this time.

### Service Checks

The eventstore check does not include any service checks at this time.

## Troubleshooting

Raise a ticket for the maintainer to assist with
