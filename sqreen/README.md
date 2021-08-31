# Sqreen Integration

## Overview

The Sqreen integration enables you and your team to monitor your service security activity from Datadog.

It provides you with dashboards, security rules, log facets, and saved views.

This integration is only available to Datadog and Sqreen design partners. 

It requires the Sqreen microagent to be deployed in the web services to be secured. 

![Sqreen Insights in Datadog][1]

### Security rules

This integration contains 2 security rules: 
* Security Incident Detected by Sqreen
* User Logged into an Application from a New Country

Once set up, you'll be able to review these rules' full definitions from the [Security Rules list][2].

## Setup

### Configure the Sqreen -> Datadog data pipeline

Sqreen streams your services security activity to Datadog as logs.

To set it up:

1. Go to the [Sqreen Dashboard > Organization settings > Integrations][3].
2. Connect a new Datadog accounts
3. Choose the corresponding intake server URL. For Datadog US: `http-intake.logs.datadoghq.com`. For Datadog EU: `http-intake.logs.datadoghq.eu`.
4. In the "API Key" field, provide a [Datadog API key][4] used to stream the Sqreen data as logs.

After a few seconds, the first logs with `source:sqreen` should be flowing in. 

The assets bundled in this integration are deployed into your Datadog account.

![Sqreen -> Datadog data pipeline configuration][5]

### Troubleshooting

For support, reach out to [Datadog Support](/help).

## Payload reference documentation

The log format is fully documented in the [Sqreen documentation][6].

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/sqreen/images/sqreen_dashboard.png
[2]: https://app.datadoghq.com/security/configuration/rules?sort=rule&query=source%3Asqreen
[3]: https://my.sqreen.com/profile/organization/integrations
[4]: https://app.datadoghq.com/account/settings#api 
[5]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/sqreen/images/sqreen_datadog_configuration.png
[6]: https://docs.sqreen.com/integrations/datadog-integration/

## Data Collected

### Logs

This integration collects Sqreen events as logs.

### Metrics

No metrics is collected for this integrations

### Service Checks

No service checks are included in this integrations

### Events

No events are collected in this integration
