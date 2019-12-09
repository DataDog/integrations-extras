# Portworx Integration

## Overview

Get metrics from Portworx service in real time to:

- Monitor health and performance of your Portworx Cluster
- Track disk usage, latency and throughput for Portworx volumes

## Setup

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Portworx check on your host. See our dedicated Agent guide for [installing community integrations][1] to install checks with the [Agent prior to version 6.8][2] or the [Docker Agent][3]:

1. Install the [developer toolkit][4].
2. Clone the integrations-extras repository:

    ```
    git clone https://github.com/DataDog/integrations-extras.git.
    ```

3. Update your `ddev` config with the `integrations-extras/` path:

    ```
    ddev config set extras ./integrations-extras
    ```

4. To build the `portworx` package, run:

    ```
    ddev -e release build portworx
    ```

5. [Download and launch the Datadog Agent][5].
6. Run the following command to install the integrations wheel with the Agent:

    ```
    datadog-agent integration install -w <PATH_OF_PORTWORX_ARTIFACT_>/<PORTWORX_ARTIFACT_NAME>.whl
    ```

7. Configure your integration like [any other packaged integration][6].

### Configuration

1. Edit the `portworx.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][7] to start collecting your Portworx [metrics](#metric-collection).
  See the [sample portworx.d/conf.yaml][8] for all available configuration options.

2. [Restart the Agent][9]

#### Metric Collection

- Add this configuration setup to your `portworx.yaml` file to start gathering your portworx metrics:

```
init_config:

instances:
 # url of the metrics endpoint of prometheus
 - prometheus_endpoint: http://localhost:9001/metrics
```

Configure it to point to your server and port.

See the [sample portworx.yaml][10] for all available configuration options.

* [Restart the Agent][11] to begin sending Portworx metrics to Datadog.

### Validation

[Run the Agent's `info` subcommand][12], you should see something like the following:

## Compatibility

The Portworx check is compatible with Portworx 1.4.0 and possible earlier versions.

## Data Collected

### Metrics

See [metadata.csv][13] for a list of metrics provided by this integration.

### Events

The Portworx check does not include any events.

## Troubleshooting

### Agent cannot connect

```
    portworx
    -------
      - instance #0 [ERROR]: "('Connection aborted.', error(111, 'Connection refused'))"
      - Collected 0 metrics, 0 events & 0 service check
```

Check that the `url` in `portworx.yaml` is correct.

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog][14].

[1]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent
[2]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[4]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[5]: https://app.datadoghq.com/account/settings#agent
[6]: https://docs.datadoghq.com/getting_started/integrations
[7]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[8]: https://github.com/DataDog/integrations-extras/blob/master/portworx/datadog_checks/portworx/data/conf.yaml.example
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[10]: https://github.com/DataDog/integrations-extras/blob/master/portworx/datadog_checks/portworx/data/conf.yaml.example
[11]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[12]: https://docs.datadoghq.com/agent/faq/agent-status-and-information
[13]: https://github.com/DataDog/integrations-extras/blob/master/portworx/metadata.csv
[14]: https://www.datadoghq.com/blog
