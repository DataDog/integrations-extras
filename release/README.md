# Release

## Overview

The **Release Datadog Integration** enables users to seamlessly monitor their build and deployment activity within Datadog. With this integration, users can track key metrics related to their **Applications** and **Environments**, gaining valuable insights into the health, performance, and efficiency of their software delivery pipelines.

### **Key Features:**

-   **Build Metrics**: Monitor build times, success/failure rates, and frequency of builds.
-   **Deployment Insights**: Track deployment status, duration, and trends over time.
-   **Environment Visibility**: View real-time deployment activity across different environments.
-   **Custom Dashboards & Alerts**: Configure Datadog dashboards and alerts for proactive monitoring.
-   **Seamless Integration**: Connect Release with Datadog effortlessly, ensuring visibility without additional configuration.

By integrating Release with Datadog, teams can optimize their CI/CD workflows, quickly diagnose issues, and improve the overall reliability of their software releases.

## Setup

## Prerequisites
- An active Datadog account
- A Release account with owner-level permissions
- Administrative access to your Release account

## Installation Steps

1. **Log in to Release**
   - Go to [app.release.com][1] and sign in
   - You must be an Account Owner to install integrations

2. **Navigate to Integrations**
   - Select the account you want to integrate with Datadog
   - Go to "Configuration" → "Integrations"

3. **Add Datadog Integration**
   - Click "Add Integration"
   - Select "Datadog Metrics" from the available integrations

4. **Configure OAuth Connection**
   - Click "Connect to Datadog" to authenticate via OAuth
   - You will be redirected to Datadog to authorize the connection
   - Grant the requested permissions

5. **Configure Metrics Settings**
   - Select which metrics to send:
     - Build metrics
     - Deployment metrics
   - Choose the Datadog site (US, EU, etc.)
   - Save your configuration

6. **Verify Installation**
   - Check the integration status shows "Connected"
   - Your first metrics should appear in Datadog within minutes of your next build or deployment

## Troubleshooting

- If the connection fails, ensure your Datadog API key has the correct permissions
- For connection issues, try regenerating your API key from the integration settings page

For additional support, contact Release support.

## Uninstallation

## Prerequisites
- A Release account with owner-level permissions
- Administrative access to your Release account

## Uninstallation Steps

1. **Log in to Release**
   - Go to [app.release.com][1] and sign in
   - You must be an Account Owner to uninstall integrations

2. **Navigate to Integrations**
   - Select the account with the Datadog integration
   - Go to "Configuration" → "Integrations"

3. **Locate Datadog Integration**
   - Find the Datadog Metrics integration in your list of connected integrations

4. **Uninstall the Integration**
   - Click the "Uninstall" button next to the Datadog integration
   - Confirm the uninstallation when prompted

5. **Verify Uninstallation**
   - Confirm the Datadog integration no longer appears in your list of active integrations
   - No further metrics will be sent to Datadog

## Additional Notes
- Uninstalling the integration will immediately stop all metric transmissions to Datadog
- Historical data already sent to Datadog will remain in your Datadog account unless manually removed there
- Your Datadog account will not be affected by this uninstallation

For additional support, contact Release support.

## Support

### Primary Support Channel
For timely assistance, our team prefers to connect with customers through **Slack Connect**. This allows for real-time collaboration and faster issue resolution.

### Alternative Support Channel
If Slack Connect is not available to you, please reach out via **email** at:
support@release.com

## When Contacting Support
Please include the following information when reporting issues:
- Your Release account name
- Integration configuration details
- Error messages you've encountered
- Steps to reproduce the issue

## Support Hours
Our team is available Monday through Friday, 9am-5pm PT. For urgent issues outside of business hours, please indicate "URGENT"
in your email subject line.

We aim to respond to all inquiries within 24 business hours.


[1]: https://app.release.com