# Agent Check: PureFB

## Overview

This check monitors the [Pure Storage FlashBlade][3] through the [Datadog Agent][2] and the [Pure Storage FlashBlade OpenMetrics exporter][1]. 

The integration can provide performance data at the array, client, share, and bucket level, as well as high-level capacity and configuration information.

You can monitor multiple FlashBlades and aggregate these into a single dashboard, or group them together by customer-defined environment.

**This integration requires the following**:

 - FlashBlade Purity 3.2.x+
 - Datadog Agent v7.26.x+ to use OpenMetricsBaseCheckV2
 - Python 3
 - The Pure Storage FlashBlade OpenMetrics exporter is installed and running in a containerized environment. Refer to the [Pure Storage GitHub repo][1] for installation instructions.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][13] for guidance on applying these instructions.

### Installation

1. [Download and launch the Datadog Agent][9].
2. Manually install the Pure FlashBlade integration. See [Use Community Integrations][10] for more details based on your environment.


#### Host

To configure this check for an Agent running on a host, run `datadog-agent integration install -t datadog-purefb==1.0.2`.

Note:  `<INTEGRATION_VERSION>` can be found within the [CHANGELOG.md][13] for Datadog Integration Extras. 
  * e.g. `datadog-agent integration install -t datadog-purefb==1.0.2`

### Configuration

1. Create a user on your FlashBlade with the Read-Only role and generate an API token for this user.

2. Add the following configuration block to the `purefb.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory, to start collecting your PureFB performance data. See the sample [purefb.d/conf.yaml][4] for all available configuration options.

**Note**: The `/array` endpoint is required as an absolute minimum when creating your configuration file.

```yaml
init_config:
   timeout: 120

instances:

  - openmetrics_endpoint: http://<exporter_ip_or_fqdn>:<port>/metrics/array?endpoint=<array_ip_or_fqdn>
    tags:
       - env:<env>
       - fb_array_name:<full_fqdn>
       - host:<full_fqdn>
    headers:
       Authorization: Bearer <api_token>
    min_collection_interval: 120

  - openmetrics_endpoint: http://<exporter_ip_or_fqdn>:<port>/metrics/clients?endpoint=<array_ip_or_fqdn>
    tags:
       - env:<env>
       - fb_array_name:<full_fqdn>
       - host:<full_fqdn>
    headers:
       Authorization: Bearer <api_token>
    min_collection_interval: 600

  - openmetrics_endpoint: http://<exporter_ip_or_fqdn>:<port>/metrics/usage?endpoint=<array_ip_or_fqdn>
    tags:
       - env:<env>
       - fb_array_name:<full_fqdn>
       - host:<full_fqdn>
    headers:
       Authorization: Bearer <api_token>
    min_collection_interval: 600

```

2. [Restart the Agent][5].

### Validation

[Run the Agent's status subcommand][6] and look for `purefb` under the Checks section.

### Troubleshooting

#### Arrays are not showing in dashboard

The dashboards included in this integration use the tags `env`, `host`, and `fb_array_name`. Make sure that these are set per instance.

```yaml
 tags:
    - env:<env>
    - fb_array_name:<full_fqdn>
    - host:<full_fqdn>
```

#### Increasing collection interval

For the `/array` endpoint, the Pure Storage FlashBlade check sets `min_collection_interval` to `120` by default, and the minimum recommended value is `15`. You may increase or decrease `min_collection_interval` in the `purefb.d/conf.yaml` file if necessary:

```yaml
min_collection_interval: 120
```

For the `/clients`, and `/usage` endpoints, the Pure Storage FlashBlade check sets `min_collection_interval` to `600` by default , and the minimum recommended value is `120`. You may increase or decrease `min_collection_interval` in the `purefb.d/conf.yaml` file if necessary:

```yaml
min_collection_interval: 600
```


## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this check.

### Events

The PureFB integration does not include any events.

### Service Checks

See [service_checks.json][12] for a list of service checks provided by this integration.

## Support

For support or feature requests, contact Pure Storage through the following methods:
* Email: pure-observability@purestorage.com
* Slack: [Pure Storage Code// Observability Channel][11].

[1]: https://github.com/PureStorage-OpenConnect/pure-fb-openmetrics-exporter
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://www.purestorage.com/products.html
[4]: https://github.com/DataDog/integrations-extras/blob/master/purefb/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/purefb/metadata.csv
[9]: https://app.datadoghq.com/account/settings#agent
[10]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent
[11]: https://code-purestorage.slack.com/messages/C0357KLR1EU
[12]: https://github.com/DataDog/integrations-extras/blob/master/purefb/assets/service_checks.json
[13]: https://docs.datadoghq.com/agent/kubernetes/integrations/