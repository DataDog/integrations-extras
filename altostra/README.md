# Agent Check: altostra

## Overview

Altostra integrates with cloud computing services to provide your development teams with end-to-end workflows.

The Datadog Altostra integration enables you to automatically instrument your Altostra projects during deployment to send logs and metrics to your Datadog account. Control the integration configuration per deployment environment.

## Setup

### Installation

The Datadog Altostra integration is built-in. No installation is required.

### Configuration

The Datadog integration is available in the Altostra Web Console under [integrations](https://app.altostra.com/team/settings/integrations/logging) on the account settings page.

1. Go to the [Integrations](https://app.altostra.com/team/settings/integrations/logging) section in your Altostra account settings.
2. Click on **Connect** for the **Datadog** integration.
3. Enter a **display name** for the integration.
4. Enter your Datadog account **API key**.
5. Click **OK** to finish configuring the integration.
6. Go to the [Environments](https://app.altostra.com/environments) and click on the environment for which you wish to configure log shipping.
7. Under _Settings_, select the integration you configured in the previous steps from the **Log shipping** selection.
8. Click **Save Changes**.

### Validation

1. Deploy an Altostra project that contains a Lambda function to any environment you've configured for log shipping to Datadog.
2. Invoke the Lambda function.
3. You should see the Lambda function logs appear in the _Logs_ view in Datadog.

## Troubleshooting

Need help? Contact [Datadog Support][1].

[1]: /help