# Aerospike Integration

## Overview

Get metrics from Aerospike Database in real time to:

* Visualize and monitor aerospike states
* Be notified about aerospike failovers and events.

## Installation

Install the `dd-check-aerospike` package manually or with your favorite configuration manager

## Configuration

Edit the `aerospike.yaml` file to point to your server and port, set the masters to monitor

## Validation

[Run the Agent's `status` subcommand][1] and look for `aerospike` under the Checks section.

[1]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information