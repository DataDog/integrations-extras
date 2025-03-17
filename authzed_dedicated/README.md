# Authzed Dedicated

## Overview

[Authzed Dedicated][1] is an open-core, [Google Zanzibar][2]-inspired database system for creating and managing security-critical application permissions.

Developers create a schema that models their permissions requirements. Then, they use any of the official or community maintained client libraries to apply the schema to the database and insert data into the database. They can query the data to efficiently check permissions in their applications.

Authzed Dedicated metrics allow developers and SREs to monitor their Authzed Dedicated deployments, including request latency metrics, cache metrics such as size and hit/miss metrics, and datastore connection and query metrics. These metrics allow developers and SREs to diagnose performance problems and tune performance characteristics of their SpiceDB clusters.

Piping these metrics to Datadog allows Datadog users to leverage their existing metrics stack and correlate metrics from Authzed Dedicated with other events in their system.

## Setup

The Datadog integration is available in the Authzed Dashboard under the "Settings" tab on a Permission System.

1.  Go to the dashboard homepage.
2.  Select a Permission System for which to submit metrics.
2.  Click on the "Settings" tab.
3.  Scroll down to the "Datadog Metrics" block of the settings UI.
4.  Enter your Datadog account **API key**.
5.  Enter your [Datadog Site][3] if different from the default.
6.  Click **Save**.

You should see metrics start to flow to Datadog shortly thereafter. If you don't, contact [our support][4].

## Uninstallation

The Datadog integration is available in the Authzed Dashboard under the "Settings" tab on a Permission System.

1.  Go to the dashboard homepage.
2.  Select a Permission System for which to submit metrics.
2.  Click on the "Settings" tab.
3.  Scroll down to the "Datadog Metrics" block of the settings UI.
4.  Click "Remove."

This will disable the Datadog integration in your Authzed Dedicated cluster. Please note that this could take several minutes.

## Support

If you have problems with your integration, reach out to our support team via email. We'll respond with further instructions and troubleshooting steps.


[1]: https://authzed.com/products/authzed-dedicated
[2]: https://authzed.com/zanzibar
[3]: https://docs.datadoghq.com/getting_started/site/
[4]: support@authzed.com