# Code Climate

## Overview

The Code Climate integration enables you to send metrics from Code Climate's Quality and Velocity products to your Datadog account. Having Quality and Velocity metrics, like days of tech debt or PR cycle time, in Datadog allows for:

1. Increased visibility of engineering process metrics when they are displayed alongside infra and application metrics on team dashboards
2. Correlating application performance metrics with code quality metrics (e.g., as tech debt has built up, has the frequency of SLO breaches also increased?)
3. Alerting (e.g., slack notifications) when engineering flow metrics fall below levels set as team objectives

The integration also comes with an out-of-the-box dashboard.

TODO: Insert screen shot

### Data visibility

Anyone with access to your Datadog account will be able to see all the metrics coming from Code Climate -- regardless of what role-based permissions you have set for those metrics within Code Climate.

### Types of metrics

The metrics fall into two broad categories:

1. State-of-the-world metrics. These metrics are submitted on a regular cadence and represent snapshots of the current state. For example: `code_climate.quality.test_coverage`, `code_climate.velocity.open_prs`, `code_climate.velocity.open_issue_age`
2. Event-based metrics. These metrics are submitted whenever a key event happens. For example: `code_climate.velocity.prs_created`, `code_climate.velocity.cycle_time`, `code_climate.velocity.issues_resolved`

## Setup

The Code Climate integration sends data directly to Datadog's API from Code Climate on your behalf. Therefore, setup is simple and only requires you to provide Code Climate with an API key and Datadog site.

1. [Create a new API key][1] in your Datadog account.
2. [Identify which Datadog site][2] your account is running in.
3. Add a Datadog integration in the [Velocity integration settings page][3], using the API key and site gathered above.

That's all! Code Climate will automatically start submitting metrics within a few minutes!

Note that no historical data is sent to Datadog; the new Code Climate metrics will only be seen going forward.

## Support

Need help? Reach out to [Code Climate Support][4].


[1]: https://docs.datadoghq.com/account_management/api-app-keys/#add-an-api-key-or-client-token
[2]: https://docs.datadoghq.com/getting_started/site/#access-the-datadog-site
[3]: https://velocity.codeclimate.com/settings/integrations/new
[4]: https://codeclimate.com/help/new
