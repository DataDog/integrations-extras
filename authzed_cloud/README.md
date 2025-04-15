# AuthZed Cloud

## Overview

[Authzed Cloud][1] is an open-core, [Google Zanzibar][2]-inspired database system for creating and managing security-critical application permissions.

Developers define a schema that models their permissions requirements. They then use any of the official or community-maintained client libraries to apply the schema and insert data into the database. They can query this data to efficiently check permissions within their applications.

Authzed Cloud metrics allow developers and SREs to monitor their deployments, including request latency, cache metrics (such as size and hit/miss rates), and datastore connection and query performance. These metrics help diagnose performance issues and fine-tune the performance of their SpiceDB clusters.

Sending these metrics to Datadog enables users to leverage their existing observability stack and correlate Authzed Cloud metrics with other system events.

## Setup

The Datadog integration is available in the AuthZed Dashboard under the "Settings" tab on a Permission System.

1.  Go to the dashboard homepage.
2.  Select a Permission System for which to submit metrics.
2.  Click on the **Settings** tab.
3.  Scroll down to the **Datadog Metrics** block of the settings UI.
4.  Enter your Datadog account **API key**.
5.  Enter your [Datadog site][3] if different from the default.
6.  Click **Save**.

To ensure that the dashboard graph for latency correctly shows the p50, p95, and p99 latencies, you'll also need to set the **Percentiles** setting for the `authzed.grpc.server_handling` metric in the **Metrics Summary** view to **ON**. 

You should see metrics start to flow to Datadog shortly thereafter. If you don't, contact [our support][4].

## Uninstallation

The Datadog integration is available in the AuthZed Dashboard under the **Settings** tab on a Permission System.

1.  Go to the dashboard homepage.
2.  Select a Permission System for which to submit metrics.
2.  Click on the **Settings** tab.
3.  Scroll down to the **Datadog Metrics** block of the settings UI.
4.  Click **Remove**.

This disables the Datadog integration in your AuthZed Cloud cluster. Note that this could take several minutes.

## Support

Need help? Contact [AuthZed support][5].


[1]: https://authzed.com/products/authzed-dedicated
[2]: https://authzed.com/zanzibar
[3]: https://docs.datadoghq.com/getting_started/site/
[4]: support@authzed.com
[5]: mailto:support@authzed.com