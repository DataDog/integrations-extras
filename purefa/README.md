# Agent Check: PureFA

## Overview

This check monitors the [Pure Storage FlashArray][3] through the [Datadog Agent][2] and the [Pure Storage OpenMetrics exporter][1]. 

The integration can provide performance data at the array, host, volume and pod level, as well as high-level capacity and configuration information.

You can monitor multiple FlashArrays and aggregate these into a single dashboard, or group them together by customer defined environment.

**This integration requires the following**:

 - Agent v7.26.x+ to utilize OpenMetricsBaseCheckV2
 - Python 3
 - The Pure Storage OpenMetrics exporter is installed and running in a containerized environment. Refer to the [GitHub repo][1] for installation instructions.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the Autodiscovery Integration Templates for guidance on applying these instructions.

### Installation

1. [Download and launch the Datadog Agent][9].
2. Manually install the Pure FlashArray integration. See [Use Community Integrations][10] for more details based on your environment.


#### Host

To configure this check for an Agent running on a host, run `datadog-agent integration install -t datadog-purefa==<INTEGRATION_VERSION>`.

Note:  `<INTEGRATION_VERSION>` can be found within the [CHANGELOG.md][13] for Datadog Integration Extras. 
  * e.g. `datadog-agent integration install -t datadog-purefa==1.1.0`

### Configuration

1. Create a local user on your FlashArray with the Read-Only role and generate an API token for this user.
   ![Generate an API Key](https://raw.githubusercontent.com/DataDog/integrations-extras/master/purefa/images/API.png) 
2. Add the following configuration block to the `purefa.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your PureFA performance data. See the sample [purefa.d/conf.yaml][4] for all available configuration options.

**Note**: The `/array` endpoint is required as an absolute minimum when creating your configuration file.

```yaml
init_config:
   timeout: 60

instances:

  - openmetrics_endpoint: http://<exporter_ip_or_fqdn>:<port>/metrics/array?endpoint=<array_ip_or_fqdn>
    tags:
       - env:<env>
       - fa_array_name:<full_fqdn>
       - host:<full_fqdn>
    headers:
       Authorization: Bearer <api_token>
    min_collection_interval: 120

  - openmetrics_endpoint: http://<exporter_ip_or_fqdn>:<port>/metrics/volumes?endpoint=<array_ip_or_fqdn>
    tags:
       - env:<env>
       - fa_array_name:<full_fqdn>
    headers:
       Authorization: Bearer <api_token>
    min_collection_interval: 120

  - openmetrics_endpoint: http://<exporter_ip_or_fqdn>:<port>/metrics/hosts?endpoint=<array_ip_or_fqdn>
    tags:
       - env:<env>
       - fa_array_name:<full_fqdn>
    headers:
       Authorization: Bearer <api_token>
    min_collection_interval: 120

  - openmetrics_endpoint: http://<exporter_ip_or_fqdn>:<port>/metrics/pods?endpoint=<array_ip_or_fqdn>
    tags:
       - env:<env>
       - fa_array_name:<full_fqdn>
       - host:<full_fqdn>
    headers:
       Authorization: Bearer <api_token>
    min_collection_interval: 120

  - openmetrics_endpoint: http://<exporter_ip_or_fqdn>:<port>/metrics/directories?endpoint=<array_ip_or_fqdn>
    tags:
       - env:<env>
       - fa_array_name:<full_fqdn>
       - host:<full_fqdn>
    headers:
       Authorization: Bearer <api_token>
    min_collection_interval: 120
```

2. [Restart the Agent][5].

### Validation

[Run the Agent's status subcommand][6] and look for `purefa` under the Checks section.



### Upgrading to new versions of this integration

#### From PureFA Agent Check 1.0.x to 1.1.x

1.1.x supports both the [Pure Storage OpenMetrics exporter][1] and the deprecated [Pure Storage Prometheus exporter][14].

The dashboard for the deprecated [Pure Storage Prometheus exporter][14] has been renamed to `Pure FlashArray - Overview (Legacy Exporter)`.

A listing of metrics that are both shared and unique to the different exporters are listed in [metrics.py][15]. You may need to update your dashboards and/or your alerts to match the new metric names when migrating from the [Pure Storage Prometheus exporter][14] to the [Pure Storage OpenMetrics exporter][1]. Please contact Pure Storage with the information in the Support tab if you have any questions.

When migrating from [Pure Storage Prometheus exporter][14] to the [Pure Storage OpenMetrics exporter][1], the endpoints no longer have `/flasharray` in the endpoint URI.

In future versions the PureFA Agent Check, the metric names from the Pure Storage Prometheus exporter will be removed.



### Troubleshooting

#### Arrays are not showing in dashboard

The dashboards included in this integration use the tags `env`, and `fa_array_name`. Make sure that these are set per instance. `host` must also be set for the `/array` and `/pods` endpoints in `purefa.d/conf.yaml`.

```yaml
- tags:
   - env:<env>
   - fa_array_name:<full_fqdn>
   - host:<full_fqdn>
```

#### Increasing collection interval

The Pure Storage FlashArray check sets `min_collection_interval` to `120` by default, and the minimum recommended value is `20`. You may increase/decrease `min_collection_interval` in the `purefa.d/conf.yaml` file if necessary:

```yaml
min_collection_interval: 120
```


## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this check.

### Events

The PureFA integration does not include any events.

### Service Checks

See [service_checks.json][12] for a list of service checks provided by this integration.

## Support

For support or feature requests, contact Pure Storage through the following methods:
* Email: pure-observability@purestorage.com
* Slack: [Pure Storage Code// Observability Channel][11].

[1]: https://github.com/PureStorage-OpenConnect/pure-fa-openmetrics-exporter
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://www.purestorage.com/products.html
[4]: https://github.com/datadog/integrations-extras/blob/master/purefa/datadog_checks/purefa/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/purefa/metadata.csv
[9]: https://app.datadoghq.com/account/settings#agent
[10]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent
[11]: https://code-purestorage.slack.com/messages/C0357KLR1EU
[12]: https://github.com/DataDog/integrations-extras/blob/master/purefa/assets/service_checks.json
[13]: https://github.com/DataDog/integrations-extras/blob/master/purefa/CHANGELOG.md
[14]: https://github.com/PureStorage-OpenConnect/pure-exporter
[15]: https://github.com/datadog/integrations-extras/blob/master/purefa/datadog_checks/purefa/metrics.py