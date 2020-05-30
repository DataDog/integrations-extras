# Federator.ai Integration

## Overview

This check monitors [ProphetStor Federator.ai][1].

ProphetStor Federator.ai is an AI-based solution that helps enterprise manage, optimize, auto-scale resources for any applications on Kubernetes. Using advanced machine learning algorithms to predict application workload, Federator.ai scales the right amount of resources at the right time for optimized application performance.

* AI-based workload prediction for Kafka or any applications
* Resource recommendation based on workload prediction, application, Kubernetes and other related metrics
* Automatic scaling of application containers through [Datadog Watermark Pod Autoscaler (WPA)][4]

![federatorai dashboard][7]

## Setup

### Installation

1. Log in OpenShift/Kubernetes cluster
2. Install the Federator.ai for OpenShift/Kubernetes by the following command

   ```shell
   $ curl https://raw.githubusercontent.com/containers-ai/federatorai-operator/v4.2.785/deploy/install.sh |bash
   ```

   ```shell
   $ curl https://raw.githubusercontent.com/containers-ai/federatorai-operator/v4.2.785/deploy/install.sh |bash
   Checking environment version...
   ...Passed
   Please input Federator.ai Operator tag: v4.2.785
   Enter the namespace you want to install Federator.ai [default: federatorai]:
   .........
   (snipped)
   .........
   You can now access GUI through https://federatorai-dashboard-frontend-federatorai.apps.jc-ocp4.172-31-17-84.nip.io
   Default login credential is admin/admin

   Also, you can start to apply alamedascaler CR for the namespace you would like to monitor.
   Review administration guide for further details.
   ========================================
   .........
   (snipped)
   .........
   Install Alameda v4.2.785 successfully

   Downloaded YAML files are located under /tmp/install-op
   ```

3. Verify Federator.ai pods are running properly

   ```shell
   $ kubectl get pod -n federatorai
   ```
4. Log in to Federator.ai GUI, URL and login credential could be found in the output of Step 2.


### Configuration

1. A Datadog account is required for connecting and using Datadog Cloud Service. If you don't have an account, visit Datadog website and sign up for a free trial account.
   - https://www.datadoghq.com/

2. Log in Datadog Cloud Service with your account and get an API key and Application key for using Datadog API
   - https://docs.datadoghq.com/account_management/api-app-keys/

3. Configure Federator.ai Data-Adapter
   - Download Data-Adapter configuration script from Github

   ```shell
   $ curl https://raw.githubusercontent.com/containers-ai/federatorai-operator/4.2-husky/deploy/federatorai-setup-for-datadog.sh -O
   ```

   - Change execution permission

   ```shell
   $ chomd +x federatorai-setup-for-datadog.sh
   ```

   - Prepare .kubeconfig (sh -c "export KUBECONFIG=.kubeconfig; oc login <K8s_LOGIN_URL>") or use existing one. For example,

   ```shell
   $ sh -c "export KUBECONFIG=.kubeconfig; oc login https://api.ocp4.example.com:6443"
   ```

   - Run configuration script and follow the steps to fill in configuration parameters

   ```shell
   $ ./federatorai-setup-for-datadog.sh -k .kubeconfig
   ```

   ```shell
   $ ./federatorai-setup-for-datadog.sh -k .kubeconfig
   You are connecting to cluster: https://api.jc-ocp4.172-31-17-84.nip.io:6443

   Getting Datadog info...
   Input a Datadog API Key []:7c8475872d97cbc155b893a8311111xx
   Input a Datadog Application Key []:a4c3f7620db747800d3dcb7c325fcb08a11111xx

   Getting the Kafka info... No.1
   Input Kafka consumer deployment name []: consumer
   Input Kafka consumer deeployment namespace []: myproject
   Input Kafka consumer minimum replica number []: 1
   Input Kafka consumer maximum replica number []: 30
   Input Kafka consumer group name []: group0001
   Input Kafka consumer group namespace []: myproject
   Input Kafka consumer topic name []: topic0001
   Input Kafka consumer topic namespace []: myproject

   Do you want to input another set? [default: n]:
   Warning: kubectl apply should be used on resource created by either kubectl create --save-config or kubectl apply
   secret/federatorai-data-adapter-secret configured
   Warning: kubectl apply should be used on resource created by either kubectl create --save-config or kubectl apply
   configmap/federatorai-data-adapter-config configured

   Setup Federator.ai for datadog successfully
   ```

4. Please refer to [Federator.ai and Datadog Integration - Installation and Configuration Guide][6] for more details.


## Data Collected

### Metrics

The metrics in [metadata.csv][9] will be tracked by this integration:


### Service Checks

federatorai does not include any service checks.

### Events

federatorai does not include any events.

## Troubleshooting

Need help? Read [ProphetStor Federator.ai documentations][5] or Contact ProphetStor support(<supports@prophetstor.com>).

[1]: https://www.prophetstor.com/federator-ai-for-aiops/federator-ai-datadog-integration/
[2]: https://github.com/containers-ai/federatorai-operator/blob/master/docs/quickstart.md
[3]: https://docs.datadoghq.com/integrations/kafka/
[4]: https://github.com/DataDog/watermarkpodautoscaler
[5]: https://github.com/containers-ai/federatorai-operator
[6]: http://www.prophetstor.com/wp-content/uploads/2020/05/Federator.ai%20for%20Datadog%20-%20Installation%20and%20Configuration%20Guide.pdf
[7]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/federatorai/images/federatorai-dashboard.png
[8]: https://docs.datadoghq.com/agent/cluster_agent/setup
[9]: https://github.com/DataDog/integrations-extras/blob/master/federatorai/metadata.csv
