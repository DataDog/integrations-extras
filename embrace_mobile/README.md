# Agent Check: Embrace Mobile

## Overview

This check monitors [Embrace Mobile][1].

## Setup

### Installation

To install the Embrace Mobile check on your host:


1. Install the [developer toolkit]
(https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit)
 on any machine.

2. Run `ddev release build embrace_mobile` to build the package.

3. [Download the Datadog Agent](https://app.datadoghq.com/account/settings#agent).

4. Upload the build artifact to any host with an Agent and
 run `datadog-agent integration install -w
 path/to/embrace_mobile/dist/<ARTIFACT_NAME>.whl`.

### Configuration

1. <List of steps to setup this Integration>

### Validation

<Steps to validate integration is functioning as expected>

## Data Collected

### Metrics

Embrace Mobile does not include any metrics.

### Service Checks

Embrace Mobile does not include any service checks.

### Events

Embrace Mobile does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][2].

[1]: https://embrace.io/
[2]: https://docs.datadoghq.com/help/
