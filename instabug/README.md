# Instabug Integration

## Overview

[Instabug][1] is a mobile-focused platform that empowers mobile teams to monitor, prioritize, and debug performance and stability issues throughout the mobile app development lifecycle.

The Instabug integration for Datadog provides comprehensive mobile app monitoring and analytics through the Datadog App Builder. The integration offers:

- Frustration-free sessions tracking and analysis
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
- An Instabug account with access to your project's App Health dashboard
- Instabug API token and email (Contact [Instabug Support][2] to obtain these)

### Installation

1. Contact [Instabug Support][2] to get your API credentials and follow [the SDK integration guide][4] to add Instabug to your mobile app.
2. In Datadog, navigate to [App Builder Blueprints][3].
3. Search for and select the **Instabug blueprint**.
4. Under "Setup your connection":
   - If you have an existing Instabug connection, select it from the dropdown
   - To create a new connection:
     1. Click **+ New Connection** and select "HTTP Connection"
     2. Configure the following:
        - Base URL: `https://dashboard-api.instabug.com`
        - Authentication Type: Token Auth
        - Token fields:
          - `token`: Your Instabug API token
          - `email`: Your registered Instabug email
        - Request Headers:
          ```
          authorization: Token token="{{ token }}", email="{{ email }}"
          ```
     3. Click **Next** and set appropriate access permissions
     4. Click **Create**
5. Click **Open in Editor**
6. Click **Save as a new app**
7. Click **Publish** and confirm access settings
8. Your Instabug integration will now be available in the [App Builder List][6].

## Data Collected
The Instabug integration does not include any metrics.

### Service Checks
The Instabug integration does not include any service checks.

## Support
For support, contact [Instabug Support][2].

## Further Reading
Additional helpful documentation, links, and articles:
- [Leverage user context to debug mobile performance issues with the Instabug Datadog Marketplace offering][5]

[1]: http://instabug.com
[2]: mailto:support@instabug.com
[3]: /app-builder/blueprints
[4]: https://docs.instabug.com/docs/introduction
[5]: https://www.datadoghq.com/blog/instabug-mobile-usability/
[6]: /app-builder/apps/list
