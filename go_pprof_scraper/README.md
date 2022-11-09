# Agent Check: Go-pprof-scraper

## Overview

This check collects profiles from Go applications which expose the [`/debug/pprof`][1] endpoint.

**NOTE**: Prefer instrumenting services with the [dd-trace-go][12] profiling client library. The client library
offers better integration with other Datadog services, such as through [code hotspots and endpoint filtering][13].
Use this integration for services for which you do not control the source code.

**NOTE**: Using this integration results in billing for hosts under Datadog's [Continuous Profiler][10] service.
For more on Continuous Profiler billing, consult our [billing documentation][11].

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][3] for guidance on applying these instructions.

### Installation

If you are using an Agent version >= 7.21/6.21, follow the instructions below to install the RedisEnterprise check on your host. See the dedicated Agent guide for [installing community integrations][14] to install checks with an [Agent version < v7.21/v6.21][15] or the [Docker Agent][16]:

1. [Download and launch the Datadog Agent][2].
2. Run the following command to install the integrations wheel with the Agent:

   ```shell
   datadog-agent integration install -t datadog-go-pprof-scraper==<INTEGRATION_VERSION>
   ```
  You can find the latest version on the [Datadog Integrations Release Page][17]

   **Note**: If necessary, prepend `sudo -u dd-agent` to the install command.

### Configuration

1. Edit the `go_pprof_scraper.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your go_pprof_scraper performance data. See the [sample go_pprof_scraper.d/conf.yaml][4] for all available configuration options.

2. [Restart the Agent][5].

### Validation

[Run the Agent's status subcommand][6] and look for `go_pprof_scraper` under the Checks section.

## Data Collected

### Metrics

The Go-pprof-scraper integration does not create any metrics.

### Events

The Go-pprof-scraper integration does not include any events.

### Service Checks

The Go-pprof-scraper integration does not include any service checks.

See [service_checks.json][8] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][9].


[1]: https://pkg.go.dev/net/http/pprof
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[4]: https://github.com/DataDog/integrations-extras/blob/master/go_pprof_scraper/datadog_checks/go_pprof_scraper/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/go_pprof_scraper/metadata.csv
[8]: https://github.com/DataDog/integrations-extras/blob/master/go_pprof_scraper/assets/service_checks.json
[9]: https://docs.datadoghq.com/help/
[10]: https://docs.datadoghq.com/profiler/
[11]: https://docs.datadoghq.com/account_management/billing/apm_tracing_profiler/
[12]: https://docs.datadoghq.com/profiler/enabling/go/
[13]: https://docs.datadoghq.com/profiler/connect_traces_and_profiles/
[14]: https://docs.datadoghq.com/agent/guide/use-community-integrations/?tab=agentv721v621
[15]: https://docs.datadoghq.com/agent/guide/use-community-integrations/?tab=agentearlierversions
[16]: https://docs.datadoghq.com/agent/guide/use-community-integrations/?tab=docker
[17]: https://github.com/DataDog/integrations-extras/tags
