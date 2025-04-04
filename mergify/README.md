# Agent Check: Mergify

## Overview

**Important**: starting October 10th 2024, this integration is no longer supported. You should use the [new integration](https://app.datadoghq.com/integrations/mergify-oauth).

This integration monitors merge queue length for each configured repository in
[Mergify][1] and tracks Mergify's global availability. By sending metrics to your
Datadog account, you can set up monitors for anomaly alerts and analyze merge
queue performance. You can maintain awareness of Mergify service availability
and optimize your development workflow using this Datadog integration.

## Setup

### Installation

#### From release

Run `datadog-agent integration install -t datadog-mergify==<INTEGRATION_VERSION>`.

#### From source

To install the Mergify check on your host:

1. Install the [developer tool][8] on any machine.

2. Run `ddev release build mergify` to build the package.

3. [Download the Datadog Agent][2].

4. Upload the build artifact to any host with an Agent and
 run `datadog-agent integration install -w
 path/to/mergify/dist/<ARTIFACT_NAME>.whl`.

### Configuration

1. Edit the `mergify.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][9] to start collecting your Mergify [metrics](#metrics).

   See the sample [mergify.d/conf.yaml.example][3] file for all available configuration options.

2. [Restart the Agent][4].

### Validation

Run the [Agent's status subcommand][5] and look for `mergify` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][6] for a list of metrics provided by this check.

For the metric `mergify.queue_checks_outcome`, the available `outcome_type` tags are :

- `PR_DEQUEUED`: The number of PRs that have been manually removed from the queue
- `PR_AHEAD_DEQUEUED`: The number of PRs that have been removed from the queue because a PR ahead of it was removed from the queue
- `PR_AHEAD_FAILED_TO_MERGE`: The number of PRs that have been removed from the queue because a PR ahead of it failed to merge
- `PR_WITH_HIGHER_PRIORITY_QUEUED`: The number of PRs that have been removed from the queue because a PR with higher priority has been queued
- `PR_QUEUED_TWICE`: The number of PRs that have been removed from the queue because they have been queued twice
- `SPECULATIVE_CHECK_NUMBER_REDUCED`: The number of PRs that have been removed from the queue because the number of speculative checks in the config was changed
- `CHECKS_TIMEOUT`: The number of PRs that have been removed from the queue because the speculative checks have timed out
- `CHECKS_FAILED`: The number of PRs that have been removed from the queue because the speculative checks have failed
- `QUEUE_RULE_MISSING`: The number of PRs that have been removed from the queue because the queue rule that was used to queue the PR has been removed from the config
- `UNEXPECTED_QUEUE_CHANGE`: The number of PRs that have been removed from the queue because a user made an operation on the queued pull request
- `PR_FROZEN_NO_CASCADING`: The number of PRs that have been removed from the queue because they were frozen by a freeze with no cascading effect
- `TARGET_BRANCH_CHANGED`: The number of PRs that have been removed from the queue because the PR's target branch was changed
- `TARGET_BRANCH_MISSING`: The number of PRs that have been removed from the queue because the PR's target branch does not exist anymore
- `PR_UNEXPECTEDLY_FAILED_TO_MERGE`: The number of PRs that have been removed from the queue because they unexpectedly failed to get merged
- `BATCH_MAX_FAILURE_RESOLUTION_ATTEMPTS`: The number of PRs that have been removed from the queue because the maximum batch failure resolution attempts have been reached

### Service Checks

See [service_checks.json][7] for a list of service checks provided by this integration.

### Events

Mergify does not include any events.

## Troubleshooting

Need help? Contact [Mergify support][1].

[1]: https://mergify.com
[2]: https://app.datadoghq.com/account/settings/agent/latest
[3]: https://github.com/DataDog/integrations-extras/blob/master/mergify/datadog_checks/mergify/data/conf.yaml.example
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[6]: https://github.com/DataDog/integrations-extras/blob/master/mergify/metadata.csv
[7]: https://github.com/DataDog/integrations-extras/blob/master/mergify/assets/service_checks.json
[8]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#configure-the-developer-tool
[9]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
