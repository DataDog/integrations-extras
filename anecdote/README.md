# Agent Check: Anecdote

## Overview

Anecdote continuously monitors customer feedback, such as app store reviews and customer support tickets. Anecdote then sends any feedback that is classified as a bug to Datadog. It also sends the meta information that is available (version, operating system, etc.).

For every new reported bug, Anecdote sends an event to Datadog, so developer can create a case or an incident. On top of that, the solution enables correlation analysis of machine signals (like cpu utilization), with user reported signals
Using the logs of customer feedback data, developers can significantly shorten MTTR and systematically discover hard to repoicate

Anecdote monitors customer feedback from more than 80 sources, including:

- Support tickets (Zendesk, Intercom, Freshdesk, and others)
- Public reviews (App Store, Google Play, and Trustpilot)
- Social media comments on Twitter, Reddit, and Facebook
- Customer surveys (SurveyMonkey, Typeform, Medallia, and others)

By aggregating and analyzing user-reported bugs in a unified dashboard, developers gain a comprehensive view of customer feedback, enabling them to prioritize and address issues more effectively.

## Setup

### Configuration

1. **Go to the Anecdote integration**
   - Visit the Anecdote integration page on the Datadog website.

2. **Click Install to install the integration**
   - On the Anecdote integration page, click the "Install" button to begin the installation process.

3. **Click Connect [Accounts][1]**
   - After clicking "Install," you are prompted to connect your Anecdote account with your Datadog account. Click "Connect Accounts" to proceed.

4. **Sign into your Anecdote account**
   - You are redirected to the Anecdote login page. Enter your Anecdote account credentials to sign in.

5. **Navigate to the Integrations section**
   - Once signed in, navigate to the Integrations section within your Anecdote account.

6. **Find the Datadog integration**
   - In the Integrations section, search for and select the Datadog integration.

7. **Enter the region where your Datadog Workspace is located**
   - Enter the region where your Datadog Workspace is located. This ensures that the integration points to the correct Datadog server.

8. **Authenticate your Datadog account with the integration**
   - You are redirected to the Datadog website to authenticate your Datadog account. Log in with your Datadog credentials.

9. **Install the Anecdote application within Datadog**
   - After logging into Datadog, install the Anecdote application within the Datadog environment. This adds "Anecdote: Bug Reports" to your list of Dashboards in Datadog.

10. **Verify the integration**
    - Return to Anecdote and verify that the integration is successfully connected. You should see a confirmation message or the status of the integration.

11. **Start using the integration**
    - Once the integration is verified, you can start using Anecdote to send bug reports directly to Datadog and monitor them in your Datadog Dashboards.

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

