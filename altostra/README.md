# Agent Check: altostra

## Overview

Altostra integrates with cloud computing services to provide your development teams with end-to-end workflows. From designing infrastructure and writing code to deploying and managing your applications and services across multiple accounts and environments.

With the Altostra Datadog integration, you can automatically instrument your Altostra projects during deployment to send logs and metrics to your Datadog account. Control the integration configuration as policy per deployment-environment and free your engineering teams from manual instrumentation.

## Setup

### Installation

The Datadog Altostra integration is built-in. No installation is required.

### Configuration

The Datadog Altostra integration is available under [integrations](https://app.altostra.com/team/settings/integrations/logging) on the account settings page.

1. Go to the [Integrations](https://app.altostra.com/team/settings/integrations/logging) section in your Altostra account settings.
2. Click on **Connect** for the **Datadog** integration.
3. Enter a **display name** for the integration.
4. Enter your Datadog account **API key**.
5. Click **OK** to finish configuring the integration.
6. Go to the [Environments](https://app.altostra.com/environments) and click on the environment for which you wish to configure log shipping.
7. Under _Settings_, select the integration you configured in the previous steps from the **Log shipping** selection.
8. Click **Save Changes**.

### Validation

1. Deploy any project that contains Lambda functions to any environment you've configured for log shipping to Datadog.
2. Invoke the Lambda function.
3. Look at the logs on your Datadog account, it should show the logs collected from the Lambda function shortly after.

## Troubleshooting

Need help? Contact Altostra [support@altostra.com](mailto:support@altostra.com).