# Agent Check: PagerDuty

## Overview

PagerDuty is a real-time operations platform which is continuously processing, analyzing,
and routing event data. Our system acts as an aggregation point for data coming from multiple 
monitoring tools and can provide a holistic view of your current state of operations. PagerDuty 
allows Datadog customers to enable more effective incident response while increasing visibility 
and accountability throughout the incident lifecycle. PagerDuty delivers two new apps that will 
give our customers all the capabilities of our real-time operations platform, wherever they work
without the need to switch tools. Users can easily add these new widgets, Status Dashboard by PagerDuty 
and Incidents by PagerDuty, directly to their dashboard to see the service status dashboard and respond 
to high-urgency incidents directly from Datadog in real time.

### Status Dashboard by PagerDuty

Status Dashboard by PagerDuty provides technical responders, business responders, 
and technical and business leaders a live, shared view of system health to improve 
awareness of operational issues. It displays the current service status and sends 
notifications to alert users when business services are being impacted. This feature
improves communication between response teams and stakeholders during incidents.

#### Key Features

- Teams can view the service status dashboard directly from Datadog to get a quick, real-time view of their team’s system health.
- Users can manually trigger an incident from the PagerDuty Datadog Marketplace if they identify an issue that they know the engineering team will want to look at right away.
- The Widget displays the current status of key business services and their impacting business services to get complete context while working on incidents.
- Improves communication between response teams and stakeholders during incidents.


#### Requirements
- Available to all Pagerduty Business Plan and up customers

### Incidents by PagerDuty
**PagerDuty incident response actions directly from the Datadog interface**

Incidents by PagerDuty allows users to take incident action directly from the 
Datadog interface. It arms responders with knowledge of ongoing incidents within PagerDuty 
along with the ability to acknowledge and resolve all with a seamless navigation back into
PagerDuty without having to context switch between tools.

#### Features include
- Display up to 20 high urgency and active incidents for your teams
- Ability acknowledge and resolve incidents for your teams
- Ability to navigate into PagerDuty to view individual incidents and their services as well as into your incident list

#### Requirements
- Available to all PagerDuty customers

## Setup

## Support


### Installation

To install the PagerDuty check on your host:


1. Install the [developer toolkit]
(https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit)
 on any machine.

2. Run `ddev release build pagerduty` to build the package.

3. [Download the Datadog Agent](https://app.datadoghq.com/account/settings#agent).

4. Upload the build artifact to any host with an Agent and
 run `datadog-agent integration install -w
 path/to/pagerduty/dist/<ARTIFACT_NAME>.whl`.

### Configuration

1. Edit the `pagerduty.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your pagerduty performance data. See the [sample pagerduty.d/conf.yaml][3] for all available configuration options.

2. [Restart the Agent][4].

### Validation

[Run the Agent's status subcommand][5] and look for `pagerduty` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][6] for a list of metrics provided by this check.

### Events

The PagerDuty integration does not include any events.

### Service Checks

The PagerDuty integration does not include any service checks.

See [service_checks.json][7] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][8].


[1]: **LINK_TO_INTEGRATION_SITE**
[2]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[3]: https://github.com/DataDog/integrations-extras/blob/master/pagerduty/datadog_checks/pagerduty/data/conf.yaml.example
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[6]: https://github.com/DataDog/integrations-extras/blob/master/pagerduty/metadata.csv
[7]: https://github.com/DataDog/integrations-core/blob/master/pagerduty/assets/service_checks.json
[8]: https://docs.datadoghq.com/help/
