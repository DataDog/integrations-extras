# Federator.ai Integration

## Overview

[ProphetStor Federator.ai][1] is an AI-based solution that helps enterprise manage, optimize, auto-scale resources for any applications on Kubernetes. Using advanced machine learning algorithms to predict application workload, Federator.ai scales the right amount of resources at the right time for optimized application performance.

* AI-based workload prediction for Kafka or any applications
* Resource recommendation based on workload prediction, application, Kubernetes and other related metrics
* Automatic scaling of application containers through [Datadog Watermark Pod Autoscaler (WPA)][4]

With integration of ProphetStor Federator.ai, users can easily track the Kafka message production/consumption rate, as well as the prediction of message production rate from Federator.ai dashboard. Based on the prediction or message production rate, Federator.ai automatically scales Kafka consumer replicas to handle the workload. This can be visualized from Federator.ai dashboard where the recommended consumer replicas and the current number of consumer replicas are shown. Additionally, overall consumer lags as well as the average latency in the queue before a message is received by a consumer are also shown on the dashboard for better performance monitoring.


**ProphetStor Federator.ai Cluster Overview**

![cluster_overview_dashboard][13]

* Cluster Resource Usage Predictions and Recommendations
   - This table shows the maximum/minimum/average value of the CPU/memory workload prediction and the recommended CPU/memory resource usage from the Federator.ai for the cluster resource planning.

* Cluster Node Resource Usage Predictions and Recommendations
   - This table shows the maximum/minimum/average value of the CPU/memory workload prediction and the recommended CPU/memory resource usage from the Federator.ai for the node resource planning.

* Node Current/Predicted Memory Usage (Daily)
   - This graph shows daily predicted memory usage from the Federator.ai and the memory usage of the nodes.

* Node Current/Predicted Memory Usage (Weekly)
   - This graph shows weekly predicted memory usage from the Federator.ai and the memory usage of the nodes.

* Node Current/Predicted Memory Usage (Monthly)
   - This graph shows monthly predicted memory usage from the Federator.ai and the memory usage of the nodes.

* Node Current/Predicted CPU Usage (Daily)
   - This graph shows daily predicted CPU usage from the Federator.ai and the CPU usage of the nodes.

* Node Current/Predicted CPU Usage (Weekly)
   - This graph shows weekly predicted CPU usage from the Federator.ai and the CPU usage of the nodes.

* Node Current/Predicted CPU Usage (Monthly)
   - This graph shows monthly predicted CPU usage from the Federator.ai and the CPU usage of the nodes.


**ProphetStor Federator.ai Application Overview**

![application_overview_dashboard][14]

* Workload Prediction for Next 24 Hours
   - This table shows the maximum/minimum/average value of the CPU/memory workload prediction and the recommended CPU/memory resource usage from the Federator.ai for the controller resource planning in the next 24 hours.

* Workload Prediction for Next 7 Days
   - This table shows the maximum/minimum/average value of the CPU/memory workload prediction and the recommended CPU/memory resource usage from the Federator.ai for the controller resource planning in the next 7 days.

* Workload Prediction for Next 30 Days
   - This table shows the maximum/minimum/average value of the CPU/memory workload prediction and the recommended CPU/memory resource usage from the Federator.ai for the controller resource planning in the next 30 days.

* Current/Predicted CPU Usage (Daily)
   - This graph shows daily predicted CPU usage from the Federator.ai and the CPU usage of the controllers.

* Current/Predicted CPU Usage (Weekly)
   - This graph shows weekly predicted CPU usage from the Federator.ai and the CPU usage of the controllers.

* Current/Predicted CPU Usage (Monthly)
   - This graph shows monthly predicted CPU usage from the Federator.ai and the CPU usage of the controllers.

* Current/Predicted Memory Usage (Daily)
   - This graph shows daily predicted memory usage from the Federator.ai and the memory usage of the controllers.

* Current/Predicted Memory Usage (Weekly)
   - This graph shows weekly predicted memory usage from the Federator.ai and the memory usage of the controllers.

* Current/Predicted Memory Usage (Monthly)
   - This graph shows monthly predicted memory usage from the Federator.ai and the memory usage of the controllers.

* Current/Desired/Recommended Replicas
   - This graph shows the recommended replicas from the Federator.ai and the desired and current replicas of the controllers.

* Memory Usage/Request/Limit vs Rec Memory Limit
   - This graph shows the recommended memory limit from the Federator.ai and the requested, limited and current memory usage of the controllers.

* CPU Usage/Request/Limit vs Rec CPU Limit
   - This graph shows the recommended CPU limit from the Federator.ai and the requested, limited and current CPU usage of the controllers.

* CPU Usage/Limit Utilization
   - This graph shows the CPU utilization of the controller and visualizes if the CPU utilization is over the limit or under the limit.


**ProphetStor Federator.ai Kafka Overview**

![dashboard_overview][7]

* Recommended Replicas vs Current/Desired Replicas
   - This timeseries graph shows the recommended replicas from the Federator.ai and the desired and current replicas in the system.

* Production vs Consumption vs Production Prediction
   - This timeseries graph shows the Kafka message production rate and consumption rate and the production rate predicted by Federator.ai.

* Kafka Consumer Lag
   - This timeseries graph shows the sum of consumer lags from all partitions.

* Consumer Queue Latency (msec)
   - This timeseries graph shows the average latency of a message in the message queue before it is received by a consumer.

* Deployment Memory Usage
   - This timeseries graph shows the memory usage of consumers.

* Deployment CPU Usage
   - This timeseries graph shows the CPU usage of consumers.


**ProphetStor Federator.ai Cost Analysis Overview**

![cost_analysis_overview][15]

* Current Cluster Cost and Current Cluster Configuration
   - These tables show the current cost and the environment configuration of the clusters.

* Recommended Cluster - AWS and Recommended Cluster Configuration - AWS
   - These tables show the recommended AWS instances configuration from Federator.ai and the cost of the recommended AWS instances.

* Recommended Cluster - Azure and Recommended Cluster Configuration - Azure
   - These tables show the recommended Azure instances configuration from Federator.ai and the cost of the recommended Azure instances.

* Recommended Cluster - GCP and Recommended Cluster Configuration - GCP
   - These tables show the recommended GCP instances configuration from Federator.ai and the cost of the recommended GCP instances.

* Namespace with Highest Cost ($/day)
   - This graph shows the highest daily cost of the namespaces in the current cluster.

* Namespace with Highest Predicted Cost ($/month)
   - This graph shows the highest predicted monthly cost of the namespaces in the current cluster.


## Setup

### Installation

1. Log in to OpenShift/Kubernetes cluster
2. Install the Federator.ai for OpenShift/Kubernetes by the following command

   ```shell
   $ curl https://raw.githubusercontent.com/containers-ai/federatorai-operator/master/deploy/federatorai-launcher.sh | bash
   ```

   ```shell
   curl https://raw.githubusercontent.com/containers-ai/federatorai-operator/master/deploy/federatorai-launcher.sh | bash
   Please input Federator.ai version tag: datadog
   
   Downloading scripts ...
   Done
   Do you want to use private repository URL? [default: n]:
   Do you want to launch Federator.ai installation script? [default: y]:
   
   Executing install.sh ...
   Checking environment version...
   ...Passed
   Enter the namespace you want to install Federator.ai [default: federatorai]:
   .........
   (snipped)
   .........
   All federatorai pods are ready.
   
   ========================================
   You can now access GUI through https://<YOUR IP>:31012
   Default login credential is admin/admin
   
   Also, you can start to apply alamedascaler CR for the target you would like to monitor.
   Review administration guide for further details.Review administration guide for further details.
   ========================================
   .........
   (snipped)
   .........
   Install Federator.ai successfully
   Do you want to monitor this cluster? [default: y]:
   Use "cluster-demo" as cluster name and DD_TAGS
   Applying file alamedascaler_federatorai.yaml ...
   alamedascaler.autoscaling.containers.ai/clusterscaler created
   Done
   
   Downloaded YAML files are located under /tmp/install-op 
   ```

3. Verify Federator.ai pods are running properly

   ```shell
   $ kubectl get pod -n federatorai
   ```
4. Log in to Federator.ai GUI, URL and login credential could be found in the output of Step 2.


### Configuration

1. A Datadog account is required for connecting and using Datadog. If you don't have an account, visit the [Datadog website][10] and sign up for a free trial account.

2. Log in to Datadog with your account and get an [API key and Application key][11] for using Datadog API.

3. Configure the Federator.ai Data-Adapter.
   - Data-Adapter configuration script should already be downloaded in /tmp/federatorai-scripts/datadog/ directory. If not, re-run the federatorai-launcher.sh script described in the installation step 2 without launching Federator.ai installation script again.

   ```shell
   $ curl https://raw.githubusercontent.com/containers-ai/federatorai-operator/master/deploy/federatorai-launcher.sh | bash
   Please input Federator.ai version tag: datadog
   
   Downloading scripts ...
   Done
   Do you want to use private repository URL? [default: n]:
   Do you want to launch Federator.ai installation script? [default: y]: n
   ```

   - Change the execution permission.

   ```shell
   $ chomd +x /tmp/federatorai-scripts/datadog/federatorai-setup-for-datadog.sh
   ```

   - Run the configuration script and follow the steps to fill in configuration parameters:

   ```shell
   $ ./federatorai-setup-for-datadog.sh -k .kubeconfig
   Checking environment version...
   ...Passed
   You are connecting to cluster: https://<YOUR IP>:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
   
   Getting Datadog info...
   Input a Datadog API Key []:xxxxx9273dxxcbc155xx3a7331xxxxx
   Input a Datadog Application Key []:xxxxx7220db1478xxxxxcb5c323fcb02a11xxxxx
   
   Getting Kafka info... No.1
   
   You can use command "kubectl get cm cluster-info -n <namespace> --template={{.metadata.uid}}" to get cluster name
   Where '<namespace>' is either 'default' or 'kube-public' or 'kube-service-catalog'.
   If multiple cluster-info exist, pick either one would work as long as you always use the same one to configure Datadog Agent/Cluster Agent/WPA and other data source agents.
   Input cluster name []: cluster-demo
   Input Kafka exporter namespace []: myproject
   Input Kafka consumer group kind (Deployment/DeploymentConfig/StatefulSet) []: Deployment
   Input Kafka consumer group kind name []: consumer1-topic0001-group-0001
   Input Kafka consumer group namespace []: myproject
   Input Kafka consumer topic name []: topic0001
   
   You can use Kafka command-line tool 'kafka-consumer-group.sh' (download separately or enter into a broker pod, in /bin directory) to list consumer groups.
   e.g.: "/bin/kafka-consumer-groups.sh --bootstrap-server <kafka-bootstrap-service>:9092 --describe --all-groups --members"
   The first column of output is the 'kafkaConsumerGroupId'.
   Input Kafka consumer group id []: group0001
   Input Kafka consumer minimum replica number []: 1
   Input Kafka consumer maximum replica number []: 20
   
   Do you want to input another set? [default: n]: 
   .........
   (snipped)
   .........
   ```
    
4. Please refer to [Federator.ai and Datadog Integration - Installation and Configuration Guide][6] for more details.


## Data Collected

### Metrics

See [metadata.csv][9] for a list of metrics provided by this integration.


### Service Checks

Federator.ai does not include any service checks.

### Events

Federator.ai does not include any events.

## Troubleshooting

Need help? Read [ProphetStor Federator.ai documentations][5] or contact [Datadog support][12].

[1]: https://www.prophetstor.com/federator-ai-for-aiops/federator-ai-datadog-integration/
[2]: https://github.com/containers-ai/federatorai-operator/blob/master/docs/quickstart.md
[3]: https://docs.datadoghq.com/integrations/kafka/
[4]: https://github.com/DataDog/watermarkpodautoscaler
[5]: https://github.com/containers-ai/federatorai-operator
[6]: http://www.prophetstor.com/wp-content/uploads/2020/05/Federator.ai%20for%20Datadog%20-%20Installation%20and%20Configuration%20Guide.pdf
[7]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/federatorai/images/dashboard_overview.png
[8]: https://docs.datadoghq.com/agent/cluster_agent/setup
[9]: https://github.com/DataDog/integrations-extras/blob/master/federatorai/metadata.csv
[10]: https://www.datadoghq.com/
[11]: https://docs.datadoghq.com/account_management/api-app-keys/
[12]: https://docs.datadoghq.com/help/
[13]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/federatorai/images/cluster_overview_dashboard.png
[14]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/federatorai/images/application_overview_dashboard.png
[15]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/federatorai/images/cost_analysis_overview.png
