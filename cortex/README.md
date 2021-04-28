# Agent Check: cortex

## Overview

This check monitors [cortex][1].

## Setup

### Installation

To install the cortex check on your host:


1. Install the [developer toolkit]
(https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit)
 on any machine.

2. Run `ddev release build cortex` to build the package.

3. [Download the Datadog Agent](https://app.datadoghq.com/account/settings#agent).

4. Upload the build artifact to any host with an Agent and
 run `datadog-agent integration install -w
 path/to/cortex/dist/<ARTIFACT_NAME>.whl`.

### Configuration

1. <List of steps to setup this Integration>

### Validation

<Steps to validate integration is functioning as expected>

## Data Collected

### Metrics

cortex does not include any metrics.

### Service Checks

cortex does not include any service checks.

### Events

cortex does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][2].

[1]: **LINK_TO_INTEGRATION_SITE**
[2]: https://docs.datadoghq.com/help/
