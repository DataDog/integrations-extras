# PagerDuty

## Overview

PagerDuty is a real-time operations platform which is continuously processing, analyzing,
and routing event data. The system acts as an aggregation point for data coming from multiple 
monitoring tools and can provide a holistic view of your current state of operations. PagerDuty 
allows Datadog customers to enable more effective incident response while increasing visibility 
and accountability throughout the incident lifecycle. PagerDuty delivers two new apps that will 
give you all the capabilities of our real-time operations platform, wherever you work
without the need to switch tools. Add new widgets, Status Dashboard by PagerDuty 
and Incidents by PagerDuty, directly to your dashboard to see the service status dashboard and respond 
to high-urgency incidents directly from Datadog in real time.

### Status Dashboard by PagerDuty

Status Dashboard by PagerDuty provides technical responders, business responders, 
and technical and business leaders a live, shared view of system health to improve 
awareness of operational issues. It displays the current service status and sends 
notifications to alert users when business services are being impacted. This feature
improves communication between response teams and stakeholders during incidents.

#### Key Features

- Teams can view the service status dashboard directly from Datadog to get a quick, real-time view of their team’s system health.
- Users can manually trigger an incident from the PagerDuty Datadog App if they identify an issue that they know the engineering team will want to look at right away.
- The Widget displays the current status of key business services and their impacting business services to get complete context while working on incidents.
- Improves communication between response teams and stakeholders during incidents.


#### Requirements
- The integration is available to all PagerDuty customers. However, the following feature is only available for Pagerduty Business Plan and up customers.

### Incidents by PagerDuty

Incidents by PagerDuty allows you to take incident action directly from the 
Datadog interface. It arms you with knowledge of ongoing incidents within PagerDuty 
along with the ability to acknowledge and resolve all with a seamless navigation back into
PagerDuty without having to context switch between tools.

#### Features include
- Display up to 20 high urgency and active incidents for your teams
- Ability acknowledge and resolve incidents for your teams
- Ability to navigate into PagerDuty to view individual incidents and their services as well as into your incident list


## Setup

1. In your Datadog account, navigate to Dashboards. Select the dashboard that you would like to add the Status Dashboard widget to, or [create a new dashboard][1].

2. In the dashboard, click **+Add Widgets** to the right of the dashboard title. Scroll to the right through the widgets, and then drag and drop the **PagerDuty** widget(s) into your desired position on your dashboard.

3. In the Custom Widget Editor modal, click **Connect**. Select your **service region** and then **log in** to your PagerDuty account. Upon redirection to the Custom Widget Editor, a preview of how the widget will appear. Below the preview, under **Widget options**, optionally select which additional capabilities that you would like the dashboard to default to. You may also optionally change the **Widget title**. Click **Done** to add the widget to your dashboard.

## Support

- The Incident widget is available for all PagerDuty Customers.
[Contact the PagerDuty Sales Team][2] if you would like to become a 
PagerDuty customer or [Datadog Support][3] for any troubleshooting. 

- The status dashboard widget is only available on Business plans and up. 
[Contact the Pagerduty Sales Team](https://www.pagerduty.com/contact-sales/) if you would like to
upgrade to a plan including the status dashboard feature and incidents by Pagerduty.

[1]: https://docs.datadoghq.com/dashboards/#new-dashboard
[2]: https://www.pagerduty.com/contact-sales/
[3]: https://www.datadoghq.com/support/
