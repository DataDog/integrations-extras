# Mendix

## Overview

[Mendix][1] is a [low-code IDE][2] and a visual model-driven development environment that developers can use to build apps on the Mendix Platform.

With Mendix, you can easily create, change, integrate, test, and deploy your applications. You can manage branch lines and security as well as extend your app with custom code by using the built-in editors.

[The Mendix integration][3] allows you to monitor your Mendix ecosystem, including Mendix Runtime metrics, Java Virtual Machine (JVM) metrics, database, SaaS(Software as a Service) environment metrics. Customize the metrics you send to Datadog in Mendix Studio Pro.

**Note**: This integration is applicable to Mendix Cloud and Mendix Cloud Dedicated deployment models.

## Setup

To enable the Datadog integration for Mendix applications running on Mendix Cloud, see the [Datadog for Mendix cloud documentation][5].


## Data Collected

### Metrics

For a list of metrics available once the integration is enabled, see the [official Mendix documentation][6].

### Events

The Mendix integration does not include any events.

### Service Checks

The Mendix integration does not include any service checks.


## Troubleshooting

Need help? Contact [Mendix support][4].

**Known Issue with host count:**
* When Mendix Cloud previously ran on CloudFoundry, the host count was registered incorrectly. Mendix Cloud has since transitioned to Kubernetes and corrected the registration of hosts. Customers may notice an increase in hosts since this change. For more information, see [Datadog for Mendix: Datadog Host Billing][7]. 
* If you encounter issues affecting host billing, reach out to [Mendix support][4] for assistance. 

[1]: https://mendix.com/
[2]: https://www.mendix.com/blog/a-low-code-leader-composing-the-modern-enterprise-with-mendix/
[3]: https://docs.mendix.com/developerportal/operate/monitoring-with-apm/
[4]: https://support.mendix.com/hc/en-us
[5]: https://docs.mendix.com/developerportal/operate/datadog-metrics/#2-setting-up-datadog-for-your-mendix-app
[6]: https://docs.mendix.com/developerportal/operate/monitoring-with-apm/#environment
[7]: https://docs.mendix.com/developerportal/operate/datadog-metrics/#datadog-host-billing
