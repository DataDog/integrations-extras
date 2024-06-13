# Agent Check: Anecdote

## Overview

Anecdote continuously monitors customer feedback from sources like app store reviews and customer support tickets. With this integration, Anecdote sends any feedback that is classified as a bug to Datadog, in addition to the meta information that is available (version, operating system, etc.).

For every new reported bug, Anecdote sends an event to Datadog so you can create a case or an incident. On top of that, the solution enables correlation analysis of machine signals (like CPU utilization) with user-reported signals.
Using customer feedback data logs, you can significantly shorten the MTTR and systematically discover hard to replicate issues.

Anecdote monitors customer feedback from more than 80 sources, including:

- Support tickets (Zendesk, Intercom, Freshdesk, and others)
- Public reviews (App Store, Google Play, and Trustpilot)
- Social media comments on Twitter, Reddit, and Facebook
- Customer surveys (SurveyMonkey, Typeform, Medallia, and others)

By aggregating and analyzing user-reported bugs in a unified dashboard, developers gain a comprehensive view of customer feedback, enabling them to prioritize and address issues more effectively.

## Setup

### Configuration

1. In Datadog, go to **Integrations** and search for Anecdote.

2. On the Anecdote integration page, click **Install** to install the integration.

3. After installation is complete, click **Connect Accounts** to connect your Anecdote and Datadog accounts.

4. You are redirected to the Anecdote login page. Log in with your Anecdote credentials.

5. Once you are signed into Anecdote, navigate to the Integrations section.

6. In the Integrations section, search for and select the Datadog integration.

7. Enter the region where your Datadog Workspace is located. This ensures the integration points to the correct Datadog server.
   - Enter the region where your Datadog Workspace is located. This ensures that the integration points to the correct Datadog server.

8. **Authenticate your Datadog account with the integration**

9. After logging into Datadog, install the Anecdote application. This adds "Anecdote: Bug Reports" to your list of dashboards in Datadog.

10. In Anecdoate, verify the integration is successfully connected. You should see a confirmation message or the integration status.

11. Once the integration is verified, you can start using Anecdote to send bug reports directly to Datadog and monitor them in the Dashboards page.

### Validation

To validate the connection health, you can check Anecdote's dashboard, where you can see bug reports.

## Uninstallation

- Sign into your [Anecdote account][1].
- Navigate to the Integrations section.
- Find the Datadog integration and click the delete icon to remove the integration.

## Data Collected

### Metrics
See `metadata.csv` for a list of metrics provided by this integration.

## Support

Need help? Contact [Anecdote Support][2].

[1]: app.anecdoteai.com
[2]: mailto:hello@anec.app

