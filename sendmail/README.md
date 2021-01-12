# Agent Check: Sendmail

## Overview

This check monitors [Sendmail][1] through the Datadog Agent.

## Setup

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Sendmail check on your host. See our dedicated Agent guide for [installing community integrations][2] to install checks with the [Agent prior v6.8][3] or the [Docker Agent][4]: your `ddev` config with the `integrations-extras/` path:

   ```shell
   ddev config set extras ./integrations-extras
   ```

4. To build the `sendmail` package, run:

   ```shell
   ddev -e release build sendmail
   ```

1. [Download and launch the Datadog Agent][6].
2. Run the following command to install the integrations wheel with the Agent:

   ```shell
   datadog-agent integration install -w <PATH_OF_SENDMAIL_ARTIFACT_>/<SENDMAIL_ARTIFACT_NAME>.whl
   ```

3. Configure your integration like [any other packaged integration][7].

### Configuration

1. Edit the `sendmail.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your sendmail performance data. See the [sample sendmail.d/conf.yaml][8] for all available configuration options.

2. [Restart the Agent][9].

### Validation

[Run the Agent's status subcommand][10] and look for `sendmail` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][11] for a list of metrics provided by this check.

### Service Checks

`sendmail.returns.output`: Returns CRITICAL if the sendmail command does not return any output, OK otherwise.

### Events

Sendmail does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][12].

[1]: https://www.proofpoint.com/us/open-source-email-solution
[2]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[4]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[5]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[6]: https://app.datadoghq.com/account/settings#agent
[7]: https://docs.datadoghq.com/getting_started/integrations/
[8]: https://github.com/DataDog/integrations-extras/blob/master/sendmail/datadog_checks/sendmail/data/conf.yaml.example
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[11]: https://github.com/DataDog/integrations-extras/blob/master/sendmail/metadata.csv
[12]: https://docs.datadoghq.com/help/
