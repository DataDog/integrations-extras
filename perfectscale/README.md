# Agent Check: Perfectscale

## Overview


PerfectScale is a comprehensive cloud-agnostic solution that enables teams with continuous and autonomous Kubernetes optimization capabilities. Our main goal is to empower teams to effortlessly manage their infrastructure, make quick, data-driven decisions, and reach peak performance at the lowest possible cost.

This integration enables you to receive PerfectScale Alerts directly into your Datadog dashboard, ensuring you stay informed about any resilience risks identified in your Kubernetes environment, and helping you prioritize tasks to eliminate the issues before they impact performance and user experience.


## Setup

### Create account

If you don't have a PerfectScale account yet, sign up for a [free 30-day trial][1]. Once it is active, you can start using PerfectScale integration.

### Configuration

 1. [Sign-in][2] to PerfectScale.
 2. In order to start using Datadog integration, the cluster should be connected to PerfectScale. If it is not done yet, add the cluster in 3 simple steps following the instructions in our [Documentation][3].
![Perfectscale Screenshot][4]
 3. Create an [API Key][5] in DataDog for the PerfectScale integration.
 4. [Create a Datadog profile][6].
5. Paste your API Key and select the associated [site][7].
6. Apply the profile to the desired cluster(s).

### Uninstallation

To stop using PerfectScale Datadog Integration, simply unassign your Datadog profile from a cluster. Check out the [full instructions][7] here.

## Troubleshooting

Need help with the integration? Contact our [PerfectScale support][8].

[1]: https://app.perfectscale.io/account/sign-up?_fs=16602000196-15320833110&_fsRef=https%3A%2F%2Fwww.perfectscale.io%2F
[2]: https://app.perfectscale.io/account/login
[3]: https://docs.perfectscale.io/getting-started/step-by-step-guide-to-onboard-a-cluster
[4]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/perfectscale/images/perfectscale-connect-cluster.png
[5]: https://app.datadoghq.com/organization-settings/api-keys
[6]: https://docs.perfectscale.io/customizations/communication-and-messaging/datadog-alerts-integration
[7]: https://docs.datadoghq.com/getting_started/site/
[8]: mailto:support@perfectscale.io


