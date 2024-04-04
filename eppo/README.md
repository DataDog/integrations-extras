# Agent Check: Eppo / Datadog RUM

## Overview

[Eppo][1]

The Datadog Eppo RUM integration enriches your RUM data with your feature flags to provide visibility into performance monitoring and behavioral changes. Determine which users are shown a user experience and if it is negatively affecting the user's performance.

## Setup

### Installation

To install the Eppo check on your host:


1. Install the [developer toolkit]
(https://docs.datadoghq.com/developers/integrations/python/)
 on any machine.

2. Run `ddev release build eppo` to build the package.

3. [Download the Datadog Agent][2].

4. Upload the build artifact to any host with an Agent and
 run `datadog-agent integration install -w
 path/to/eppo/dist/<ARTIFACT_NAME>.whl`.

### Configuration

!!! Add list of steps to set up this integration !!!

### Validation

!!! Add steps to validate integration is functioning as expected !!!

## Data Collected

### Metrics

Eppo does not include any metrics.

### Service Checks

Eppo does not include any service checks.

### Events

Eppo does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][3].

[1]: https://www.geteppo.com/
[2]: https://app.datadoghq.com/account/settings/agent/latest
[3]: https://docs.datadoghq.com/help/

