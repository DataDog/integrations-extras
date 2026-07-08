# Mergify

## Overview

This integration sends [Mergify][1] merge queue metrics to your Datadog account, so you can monitor and alert on your merge queue alongside the rest of your observability data. It covers merge queue throughput (pull requests entered and merged, queue and batch size), queue health (exit reasons, check outcomes, CI retries, and bisections), and performance (queue time, CI runtime, and idle waits) for each configured repository. It ships with an out-of-the-box **Mergify - Merge Queue Stats** dashboard to get you started.

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

The merge queue stats metrics (prefixed `mergify.queue.`) cover three categories:

- **Throughput**: pull requests entered and merged, queue size, batch size, and concurrent running checks.
- **Queue Health**: queue exit reasons, batch check outcomes, CI check retries, and batch bisections.
- **Performance**: total queue time, CI runtime, and idle time spent waiting for capacity, schedules, or freezes.

These metrics are tagged by `repository`, `branch`, `queue`, and `priority_rule`. Duration and size averages are submitted as `sum` and `count` companions, derived in Datadog as `sum / count` (for example, `mergify.queue.total_queue_time.sum / mergify.queue.total_queue_time.count`).

#### Queue outcomes and exit reasons

`mergify.queue.check_outcome` (tag `outcome`) and the deprecated `mergify.queue_checks_outcome` (tag `outcome_type`) report the same set of values. `mergify.queue.exit_reason` (tag `exit_reason`) reports these same values plus `UNKNOWN` (no reason was recorded):

- `SUCCESS`: the pull request was merged
- `PR_DEQUEUED`: the pull request was manually dequeued
- `PR_DEQUEUED_FROM_PARTITION`: the pull request was removed from a partition
- `PR_AHEAD_DEQUEUED`: a pull request ahead in the queue was dequeued
- `BATCH_AHEAD_FAILED`: a batch ahead in the queue failed to merge
- `PR_WITH_HIGHER_PRIORITY_QUEUED`: a higher-priority pull request was queued
- `SCHEDULED_FREEZE_STATUS_CHANGED`: a scheduled freeze changed the freeze status
- `SPECULATIVE_CHECK_NUMBER_REDUCED`: the number of speculative checks was reduced
- `CHECKS_TIMEOUT`: the speculative checks timed out
- `CHECKS_FAILED`: the speculative checks failed
- `QUEUE_RULE_MISSING`: the queue rule used to queue the pull request no longer exists
- `BASE_BRANCH_MISSING`: the base branch no longer exists
- `BASE_BRANCH_CHANGED`: the pull request base branch changed
- `PR_UNEXPECTEDLY_FAILED_TO_MERGE`: the pull request unexpectedly failed to merge
- `BATCH_MAX_FAILURE_RESOLUTION_ATTEMPTS`: the maximum batch failure-resolution attempts were reached
- `PR_CHECKS_STOPPED_BECAUSE_MERGE_QUEUE_PAUSE`: checks were interrupted because the merge queue is paused
- `CONFLICT_WITH_BASE_BRANCH`: the pull request conflicts with the base branch
- `CONFLICT_WITH_PULL_AHEAD`: the pull request conflicts with a pull request ahead in the queue
- `BRANCH_UPDATE_FAILED`: the pull request branch could not be updated
- `DRAFT_PULL_REQUEST_CHANGED`: non-Mergify commits were added to the draft pull request
- `BATCH_PULL_REQUEST_CLOSED`: the batch pull request was closed
- `PULL_REQUEST_UPDATED`: the pull request was manually updated
- `MERGE_QUEUE_RESET`: the merge queue was reset
- `INCOMPATIBILITY_WITH_BRANCH_PROTECTIONS`: the pull request is incompatible with the branch protections
- `PR_MANUALLY_MERGED`: the pull request was merged manually, outside Mergify
- `DRAFT_PULL_REQUEST_CREATION_FAILED`: the draft pull request could not be created
- `DRAFT_PULL_REQUEST_CREATION_BRANCH_NOT_INDEXED`: the draft pull request could not be created because of a GitHub branch-indexing delay
- `CONFIGURATION_CHANGED`: the Mergify configuration changed
- `UNPROCESSABLE_PULL_REQUEST`: the pull request could not be processed
- `PR_MANUALLY_DEQUEUED`: the pull request was dequeued by a command
- `STACK_PREDECESSOR_DEQUEUED`: a stack predecessor was dequeued
- `INTERMEDIATE_RESULTS_SKIPPED`: intermediate results were skipped during batch promotion
- `CHECKS_RETRIED`: the checks failed and are being retried
- `SCHEDULE_BLOCKED_AHEAD_YIELDED`: a schedule-blocked pull request ahead yielded its position

### Service Checks

Mergify does not include any service checks.

### Events

Mergify does not include any events.

## Support

Need help? Contact [Mergify support][1].

[1]: https://mergify.com
[2]: https://github.com/DataDog/integrations-extras/blob/master/mergify_oauth/metadata.csv
[3]: https://dashboard.mergify.com
[4]: /organization-settings/api-keys?filter=Mergify
