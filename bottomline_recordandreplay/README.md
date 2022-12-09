# Bottomline Mainframe Record and Replay

## Overview

This free intgration is for existing Bottomline and Datadog customers.  The integration creates a logger in Bottomline's Record and Replay using a pre-built JSON message format which can then be sent to Datadog using the standard agent. 

Bottomline's Mainframe Record and Replay solution is non-invasive in its capability to monitor 3270/5250 users via network traffic.  Bottomline helps customers monitor users and systems in ways more advanced than traditional approaches with our industry leading Fraud and Financial Crime solutions.

### Monitoring Capabilities

1. Mainframe Users: Record and Replay the users session and log information about what the user did in the session.
2. Mainframe: User Response Time
3. Mainframe: Resource Response Time 

### Monitors

This integration includes a monitor that reports when a Mainframe Resource is experiencing a problem.
### Metrics

See [metadata.csv][2] for a list of metrics provided by this check.

### Dashboards

1. Bottomline Record and Replay Overview: This dashboard gives visibility into what resources are being used, resource performance, user activity, security events, and system monitors.

## Setup

Follow the step-by-step instructions below to install and configure this check for an Agent running on a host. 

### Prerequisites

The following items are all required for this integration to run as intended:
  - You must have the Datadog Agent installed and running.
  - Access to the server running the Datadog Agent for installing Bottomline's Record and Replay and to modify the Datadog Agent configurations.
  - A supported database (Oracle or Postgres).
  - A windows desktop to install Bottomline's Enterprise Manager for configuring Record and Replay.


### Setup

If you are not already a customer of Bottomline, visit [Bottomline's Marketplace listing][3] to purchase a license.

Follow the instructions outlined [here][4] to install the integration.

## Support
For support or feature requests, contact Bottomline at [Andrew.Leon@bottomline.com](mailto:Andrew.Leon@bottomline.com).


[1]: https://www.bottomline.com/
[2]: https://github.com/DataDog/integrations-extras/blob/master/bottomline_recordandreplay/metadata.csv
[3]: /account/settings#marketplace/bottomline-mainframe
[4]: https://github.com/nbk96f1/datadog/tree/main/Documentation
