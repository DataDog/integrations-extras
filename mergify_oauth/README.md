# Mergify

## Overview

This integration monitors merge queue length for each configured repository in [Mergify][1] and tracks Mergify's global availability. By sending metrics to your Datadog account, you can set up monitors for anomaly alerts and analyze merge queue performance. You can maintain awareness of Mergify service availability and optimize your development workflow using this Datadog integration.

## Setup

- **In Datadog**: Go to **Integrations**, select the Mergify tile and click **Install Integration**.
- Click **Connect Accounts** to begin authorization of this integration. You will be redirected to the [Mergify dashboard][3].
- **In the Mergify dashboard**: Log in, select the organization you would like to set up the **Datadog Integration** for and click **Connect the integration**.

Your Mergify statistics now appear in Datadog.

## Uninstallation

1. Go to the [Mergify dashboard][3], log in, and navigate to **Integrations**.
2. Click the **Disconnect** button in the **Datadog** tile.

Once this integration has been uninstalled, any previous authorizations are revoked.

Note: Ensure that all API keys associated with this integration have been disabled by searching for the integration name on the Datadog [API Keys page][4].

## Data Collected

### Metrics

See [metadata.csv][2] for a list of metrics provided by this check.

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

Mergify does not include any service checks.

### Events

Mergify does not include any events.

## Support

Need help? Contact [Mergify support][1].

[1]: https://mergify.com
[2]: https://github.com/DataDog/integrations-extras/blob/master/mergify/metadata.csv
[3]: https://dashboard.mergify.com
[4]: https://app.datadoghq.com/organization-settings/api-keys?filter=Mergify
