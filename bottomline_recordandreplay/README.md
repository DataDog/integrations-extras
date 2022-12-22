# Bottomline Mainframe Record and Replay

## Overview

Bottomline's Mainframe Record and Replay solution is non-invasive in its capability to monitor 3270/5250 users via network traffic to help customers monitor users and systems.

With this integration, you can monitor Bottomline's' Record and Replay sessions in Datadog to provide visibility into resource utilization, resource performance, user activity, security events, and system monitors. Customers can also directly access user session replays through Datadog.

### Monitors

This integration includes a monitor that reports when a Mainframe Resource is experiencing a problem.

### Metrics

See [metadata.csv][2] for a list of metrics provided by this check.

### Dashboards

**Bottomline Record and Replay Overview**: This dashboard gives visibility into what resources are being used, resource performance, user activity, security events, and system monitors.

## Setup

Follow the step-by-step instructions below to install and configure this check for an Agent running on a host. 

### Prerequisites

The following items are required for this integration to run as intended:
  - You must have the Datadog Agent installed and running.
  - Access to the server running the Datadog Agent for installing Bottomline's Record and Replay and to modify the Datadog Agent configurations.
  - A supported database (Oracle or Postgres).
  - A Windows desktop to install Bottomline's Enterprise Manager for configuring Record and Replay.


### Setup

If you are not already a customer of Bottomline, visit [Bottomline's Marketplace listing][3] to purchase a license.

Follow the instructions outlined [here][4] to install the integration.

## Support
For support or feature requests, contact Bottomline at [partner.cfrm@bottomline.com](mailto:partner.cfrm@bottomline.com).


[1]: https://www.bottomline.com/
[2]: https://github.com/DataDog/integrations-extras/blob/master/bottomline_recordandreplay/metadata.csv
[3]: /marketplace/app/bottomline-mainframe
[4]: https://github.com/nbk96f1/datadog/tree/main/Documentation
