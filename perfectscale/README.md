# Agent Check: PerfectScale by DoiT

## Overview


PerfectScale by DoiT is a comprehensive cloud-agnostic solution that enables teams with continuous and autonomous Kubernetes optimization capabilities. Our main goal is to empower teams to effortlessly manage their infrastructure, make quick, data-driven decisions, and reach peak performance at the lowest possible cost.

PerfectScale by DoiT monitors resiliency metrics across your Kubernetes environment and sends these metrics to Datadog through the Integration. When PerfectScale by DoiT identifies under-provisioned or misconfigured workloads, it promptly pushes an alert to the Datadog dashboard detailing the issue type (such as OOM, CPU-Throttling, Eviction, and more) along with its precise location (cluster, namespace, workload, and container).

## Setup

### Create account

If you don't have a PerfectScale by DoiT account yet, sign up for a [free 30-day trial][1]. Once it is active, you can start using the PerfectScale by DoiT integration.

### Configuration

1. [Sign in to][2] PerfectScale by DoiT.
2. To start using the Datadog integration, the cluster should be connected to PerfectScale by DoiT. If this is not completed yet, add the cluster by following the instructions in the [official PerfectScale documentation][3].
![Perfectscale Screenshot][4]

3. Create an [API Key][5] in Datadog for the PerfectScale by DoiT integration.
4. [Create a Datadog profile][6].
5. Paste your API Key and select the associated [site][7].
6. Apply the profile to the desired cluster(s).

### Uninstallation

To stop using PerfectScale by DoiT Datadog Integration, simply un-assign your Datadog profile from a cluster. For more information, see the [official PerfectScale documentation][6].

## Troubleshooting

Need help with the integration? Contact [PerfectScale support][8].

[1]: https://app.perfectscale.io/account/sign-up?_fs=16602000196-15320833110&_fsRef=https%3A%2F%2Fwww.perfectscale.io%2F
[2]: https://app.perfectscale.io/account/login
[3]: https://docs.perfectscale.io/getting-started/step-by-step-guide-to-onboard-a-cluster
[4]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/perfectscale/images/perfectscale-connect-cluster.png
[5]: https://app.datadoghq.com/organization-settings/api-keys
[6]: https://docs.perfectscale.io/customizations/communication-and-messaging/datadog-alerts-integration
[7]: https://docs.datadoghq.com/getting_started/site/
[8]: mailto:support@perfectscale.io


