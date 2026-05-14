# Luciq Integration

## Overview

[Luciq][1] is a mobile-focused platform that empowers mobile teams to monitor, prioritize, and debug performance and stability issues throughout the mobile app development lifecycle.

The Luciq integration for Datadog provides comprehensive mobile app monitoring and analytics through Datadog App Builder. The integration offers:

- Session tracking and analysis
- Crash-free session and user metrics with historical trends 
- Detailed app performance metrics including:
  - Cold and hot app launch times
  - UI hangs and freezes
  - Network performance
  - Screen loading times
  - User flows
- Non-fatal error tracking
- Bug report analytics

## Setup

### Prerequisites

- A Datadog account with access to App Builder
- An Luciq account with access to your project's App Health dashboard
- An Luciq API token and email (contact [Luciq Support][2] to obtain these)

### Installation

1. Contact [Luciq Support][2] to get your API credentials and follow [the SDK integration guide][4] to add Luciq to your mobile app.
2. In Datadog, navigate to [App Builder Blueprints][3].
3. Search for and select the **Luciq blueprint**.
4. Under **Setup your connection**:
   - If you have an existing Luciq connection, select it from the dropdown
   - To create a new connection:
     1. Click **+ New Connection** and select `HTTP Connection`.
     2. Configure the following:
        - Base URL: `https://dashboard-api.instabug.com`
        - Authentication Type: Token Auth
        - Token fields:
          - `token`: Your Luciq API token
          - `email`: Your registered Luciq email
        - Request Headers:
          ```
          authorization: Token token="{{ token }}", email="{{ email }}"
          ```
     3. Click **Next** and set appropriate access permissions.
     4. Click **Create**.
5. Click **Open in Editor**.
6. Click **Save as a new app**.
7. Click **Publish** and confirm access settings.
8. Your Luciq integration is then available in the [App Builder List][6].

## Data Collected
The Luciq integration does not include any metrics.

### Service Checks
The Luciq integration does not include any service checks.

## Support
For support, contact [Luciq Support][2].

## Further Reading
Additional helpful documentation, links, and articles:
- [Leverage user context to debug mobile performance issues with the Luciq Datadog Marketplace offering][5]

[1]: http://luciq.ai
[2]: mailto:support@luciq.ai
[3]: /app-builder/blueprints
[4]: https://docs.luciq.ai/docs/introduction
[5]: https://www.datadoghq.com/blog/instabug-mobile-usability/
[6]: /app-builder/apps/list
