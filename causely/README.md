# Causely - Assure Continuous Application Reliability using Causal AI

## Overview

The [Causal AI platform][1] supercharges your observability stack by leveraging built-in intelligence to analyze your telemetry data. It enables self-managed, resilient applications by integrating observability with automated orchestration.

Causely delivers instant value with no complex setup or configuration. It helps shift your organization from a reactive to a proactive mode of operation. Instead of flood of alerts, Causely tells you exactly what you need to know about all active and emerging application failures. With Causely, understand why a failure happened, what the root cause was, and how to fix it.

Use Causely to:

- **Assure continuous application reliability**: Guarantee that KPIs, SLAs, SLOs, and SLIs are consistently met to maintain application reliability and performance.
- **Improve operational efficiency**: Reduce labor, data, and tooling costs by focusing on faster Mean Time to Repair (MTTR) and implementing efficient operational processes.
- **Accelerate the delivery of features and innovations**: Enhance the speed and reliability of shipping new services and features to market, ensuring a competitive edge and meeting customer demands promptly.

Causely integrates with Datadog to provide automated root cause analysis for Datadog Watchdog events. Causely uses the Datadog API key to fetch the configured monitors and use the triggered Watchdog events as input to the Causal AI reasoning platform and identifies the root cause of the anomalies and alerts. Causely sends back the remediated root cause as events to Datadog which can be viewed in the Causely Datadog dashboard.

## Setup

Causely uses the [Datadog API key][2] to fetch the configured monitors and use the triggered Watchdog events as input to the Causal AI reasoning platform. Causely analyzes the events and identifies the root cause of the anomalies and alerts.  To learn how to configure the Causely integration for Datadog, see the [Causely documentation][4].

## Data Collected

### Events

Causely identified and remediated root causes display in your Causely dashboard.

## Support

Need help? Contact [Causely support](mailto:support@causely.ai).

## Further reading

Additional helpful documentation, links, and articles:
- [Request a demo][5] to experience automated root cause analysis with Causely first-hand
- [Read the blog][6]: DevOps may have cheated death, but do we all need to work for the king of the underworld?
- [Watch the video][7]: Causely for asynchronous communication

[1]: https://www.causely.ai
[2]: https://app.datadoghq.com/organization-settings/api-keys
[3]: https://docs.datadoghq.com/monitors/
[4]: https://docs.causely.ai/getting-started/overview/
[5]: https://www.causely.ai/try
[6]: https://www.causely.ai/blog/devops-may-have-cheated-death-but-do-we-all-need-to-work-for-the-king-of-the-underworld/
[7]: https://www.causely.ai/blog/causely-for-asynchronous-communication