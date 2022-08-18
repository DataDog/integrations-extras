# Sqreen Integration

## Overview

The Sqreen integration enables you to monitor your service security activity with dashboards, security rules, log facets, and saved views in Datadog.

This integration is only available to Datadog and Sqreen design partners, and requires the Sqreen microagent to be deployed in the web services to be secured.

![Sqreen Insights in Datadog][1]

### Security rules

This integration contains 2 security rules:
* Security Incident Detected by Sqreen
* User Logged into an Application from a New Country

Once set up, you can review these rules' full definitions from the [Security Rules list][2].

## Setup

### Configure the Sqreen -> Datadog data pipeline

Sqreen streams your services security activity to Datadog as logs.

To set it up:

1. Go to the [Sqreen Dashboard > Organization settings > Integrations][3].
2. Connect a new Datadog account.
3. Choose the corresponding intake server URL. For Datadog US, use `http-intake.logs.datadoghq.com`. For Datadog EU, use `http-intake.logs.datadoghq.eu`.
4. In the **API Key** field, provide a [Datadog API key][4] which streams the Sqreen data as logs.

After a few seconds, logs with `source:sqreen` should begin to appear.

The assets bundled in this integration are deployed into your Datadog account.

![Sqreen -> Datadog data pipeline configuration][5]

## Payload reference

The log format is fully documented in the [Sqreen documentation][6].

## Data Collected

### Logs

This integration collects Sqreen events as logs.

### Metrics

No metrics is collected for this integration.

### Service Checks

No service checks are included in this integration.

### Events

No events are collected in this integration.

## Troubleshooting

For support, reach out to [Datadog Support](/help).

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/sqreen/images/sqreen_dashboard.png
[2]: https://app.datadoghq.com/security/configuration/rules?sort=rule&query=source%3Asqreen
[3]: https://my.sqreen.com/profile/organization/integrations
[4]: https://app.datadoghq.com/organization-settings/api-keys
[5]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/sqreen/images/sqreen_datadog_configuration.png
[6]: https://docs.sqreen.com/integrations/datadog-integration/
