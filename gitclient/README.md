# Agent Check: GitClient

## Overview

This check monitors that a [Git client][1] can connect to a target http/https repo url.  The host running the Datadog agent must already have a git client installed and configured for authentication.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][2] for guidance on applying these instructions.

### Installation

To install the "GitClient" check on your host:

1. Install the [developer toolkit](https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit) on any machine.
2. Run `ddev release build gitclient` to build the package.
3. [Download the Datadog Agent](https://app.datadoghq.com/account/settings#agent).
4. Upload the build artifact to any host with an Agent and run `datadog-agent integration install -w path/to/gitclient/dist/<ARTIFACT_NAME>.whl`.

### Configuration

1. Edit the `gitclient.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your gitclient performance data. See the [sample gitclient.d/conf.yaml][3] for all available configuration options.

2. [Restart the Agent][4].

### Validation

[Run the Agent's status subcommand][5] and look for `gitclient` under the Checks section.

## Data Collected

### Metrics

GitClient does not collect any [metrics][6].

### Service Checks

GitClient collects a single status check for a target Git repository.

* `OK` is returned if `git ls-remote` returns a `0` exit code
* `CRITICAL` is returned if `git ls-remote` returns a non-zero exit code

### Events

GitClient does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][7].

[1]: https://git-scm.com/
[2]: https://docs.datadoghq.com/agent/autodiscovery/integrations
[3]: https://github.com/DataDog/integrations-core/blob/master/gitclient/datadog_checks/gitclient/data/conf.yaml.example
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[6]: https://github.com/DataDog/integrations-core/blob/master/gitclient/metadata.csv
[7]: https://docs.datadoghq.com/help
