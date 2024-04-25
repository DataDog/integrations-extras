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
 3. Create an API Key in DataDog:
    - Go to Organizations settings
    - Click New Key
    ![Perfectscale Screenshot][5]
    - Copy your API Key for the next step
    ![Perfectscale Screenshot][6]
 4. [Create a Datadog profile][7].

    The profile configuration:
    - datadog_api_key: <API_KEY>
    - datadog_site_region: datadoghq.com

    The available datadog_site_region:
    
       | Code    | Site              |            
       |---------|-------------------|
       | US1     | datadoghq.com     |
       | US3     | us3.datadoghq.com |
       | US5     | datadoghq.com     |
       | EU      | datadoghq.eu      |
       | AP1     | ap1.datadoghq.com |
       | US1-FED | ddog-gov.com      |
5. Apply the profile to the desired cluster(s).

### Uninstallation

To stop using PerfectScale Datadog Integration, simply unassign your Datadog profile from a cluster. Check out the [full instructions][8] here.

## Troubleshooting

Need help with the integration? Contact our [support][9].

[1]: https://app.perfectscale.io/account/sign-up?_fs=16602000196-15320833110&_fsRef=https%3A%2F%2Fwww.perfectscale.io%2F
[2]: https://app.perfectscale.io/account/login
[3]: https://docs.perfectscale.io/getting-started/step-by-step-guide-to-onboard-a-cluster
[4]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/perfectscale/images/perfectscale-connect-cluster.png
[5]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/perfectscale/images/perfectscale-create-key.png
[6]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/perfectscale/images/perfectscale-copy-key.png
[7]: https://docs.perfectscale.io/customizations/communication-and-messaging/datadog-alerts-integration
[8]: https://docs.perfectscale.io/customizations/communication-and-messaging/datadog-alerts-integration
[9]: mailto:support@perfectscale.io

