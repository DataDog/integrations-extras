# Federator.ai Integration

## Overview


[ProphetStor Federator.ai][1] is an AI-based solution that helps enterprises manage and optimize resources for applications on Kubernetes and virtual machines (VMs) in VMware clusters.

Using advanced machine learning algorithms to predict application workloads, Federator.ai offers:
* AI-based workload prediction for containerized applications in Kubernetes clusters as well as VMs in VMware clusters and Amazon Web Services (AWS) Elastic Compute Cloud (EC2)
* Resource recommendations based on workload prediction, application, Kubernetes, and other related metrics
* Automatic provisioning of CPU/memory for generic Kubernetes application controllers/namespaces
* Automatic scaling of Kubernetes application containers, Kafka consumer groups, and NGINX Ingress upstream services
* Multicloud cost analysis and recommendations based on workload predictions for Kubernetes clusters and VM clusters
* Actual cost and potential savings based on recommendations for clusters, Kubernetes applications, VMs, and Kubernetes namespaces

By integrating with ProphetStor Federator.ai, you can track and predict the resource usages of Kubernetes containers, namespaces, and cluster nodes to make the right recommendations to prevent costly over-provisioning or performance-impacting under-provisioning. With easy integration to CI/CD pipeline, Federator.ai enables continuous optimization of containers whenever they are deployed in a Kubernetes cluster. Utilizing application workload predictions, Federator.ai auto-scales application containers at the right time and optimizes performance with the right number of container replicas through Kubernetes HPA or [Datadog Watermark Pod Autoscaling (WPA)][3].

For additional information on Federator.ai, refer to the [ProphetStor Federator.ai Feature Demo][2] and [ProphetStor Federator.ai for Datadog][14] videos.


**ProphetStor Federator.ai Cluster Overview**

![ProphetStor Federator.ai Cluster Overview][11]

* Cluster Resource Usage Predictions and Recommendations
   - This table shows the maximum, minimum, and average value of the CPU memory workload prediction and the recommended CPU memory resource usage from Federator.ai for cluster resource planning.

* Cluster Node Resource Usage Predictions and Recommendations
   - This table shows the maximum, minimum, and average value of the CPU memory workload prediction and the recommended CPU memory resource usage from Federator.ai for node resource planning.

* Node Current/Predicted Memory Usage (Daily)
   - This graph shows daily predicted memory usage from Federator.ai and the memory usage of the nodes.

* Node Current/Predicted Memory Usage (Weekly)
   - This graph shows weekly predicted memory usage from Federator.ai and the memory usage of the nodes.

* Node Current/Predicted Memory Usage (Monthly)
   - This graph shows monthly predicted memory usage from Federator.ai and the memory usage of the nodes.

* Node Current/Predicted CPU Usage (Daily)
   - This graph shows daily predicted CPU usage from Federator.ai and the CPU usage of the nodes.

* Node Current/Predicted CPU Usage (Weekly)
   - This graph shows weekly predicted CPU usage from Federator.ai and the CPU usage of the nodes.

* Node Current/Predicted CPU Usage (Monthly)
   - This graph shows monthly predicted CPU usage from Federator.ai and the CPU usage of the nodes.


**ProphetStor Federator.ai Application Overview**

![Application Overview Dashboard][12]

* Workload Prediction for Next 24 Hours
   - This table shows the maximum, minimum, and average value of the CPU memory workload prediction and the recommended CPU memory resource usage from Federator.ai for the controller resource planning in the next 24 hours.

* Workload Prediction for Next 7 Days
   - This table shows the maximum, minimum, and average value of the CPU memory workload prediction and the recommended CPU memory resource usage from Federator.ai for the controller resource planning in the next 7 days.

* Workload Prediction for Next 30 Days
   - This table shows the maximum, minimum, and average value of the CPU memory workload prediction and the recommended CPU memory resource usage from Federator.ai for the controller resource planning in the next 30 days.

* Current/Predicted CPU Usage (Daily)
   - This graph shows daily predicted CPU usage from Federator.ai and the CPU usage of the controllers.

* Current/Predicted CPU Usage (Weekly)
   - This graph shows weekly predicted CPU usage from Federator.ai and the CPU usage of the controllers.

* Current/Predicted CPU Usage (Monthly)
   - This graph shows monthly predicted CPU usage from Federator.ai and the CPU usage of the controllers.

* Current/Predicted Memory Usage (Daily)
   - This graph shows daily predicted memory usage from Federator.ai and the memory usage of the controllers.

* Current/Predicted Memory Usage (Weekly)
   - This graph shows weekly predicted memory usage from Federator.ai and the memory usage of the controllers.

* Current/Predicted Memory Usage (Monthly)
   - This graph shows monthly predicted memory usage from Federator.ai and the memory usage of the controllers.

* Current/Desired/Recommended Replicas
   - This graph shows the recommended replicas from Federator.ai and the desired and current replicas of the controllers.

* Memory Usage/Request/Limit vs Rec Memory Limit
   - This graph shows the recommended memory limit from Federator.ai and the requested, limited and current memory usage of the controllers.

* CPU Usage/Request/Limit vs Rec CPU Limit
   - This graph shows the recommended CPU limit from Federator.ai and the requested, limited and current CPU usage of the controllers.

* CPU Usage/Limit Utilization
   - This graph shows the CPU utilization of the controller and visualizes if the CPU utilization is over the limit or under the limit.


**ProphetStor Federator.ai Kafka Overview**

![Dashboard Overview][7]

* Recommended Replicas vs Current/Desired Replicas
   - This timeseries graph shows the recommended replicas from Federator.ai and the desired and current replicas in the system.

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

![Cost Analysis Overview][13]

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

* Follow the instructions below to download and set up Federator.ai.

### Installation

1. Log in to your OpenShift/Kubernetes cluster
2. Install Federator.ai for OpenShift/Kubernetes with the following command:

   ```shell
   $ curl https://raw.githubusercontent.com/containers-ai/prophetstor/master/deploy/federatorai-launcher.sh | bash
   ```

   ```shell
   $ curl https://raw.githubusercontent.com/containers-ai/prophetstor/master/deploy/federatorai-launcher.sh | bash
   ...
   Please enter Federator.ai version tag [default: latest]:latest
   Please enter the path of Federator.ai directory [default: /opt]:
   
   Downloading v4.5.1-b1562 tgz file ...
   Done
   Do you want to use a private repository URL? [default: n]:
   Do you want to launch Federator.ai installation script? [default: y]:
   
   Executing install.sh ...
   Checking environment version...
   ...Passed
   Enter the namespace you want to install Federator.ai [default: federatorai]:
   .........
   Downloading Federator.ai alamedascaler sample files ...
   Done
   ========================================
   Which storage type you would like to use? ephemeral or persistent?
   [default: persistent]:
   Specify log storage size [e.g., 2 for 2GB, default: 2]:
   Specify AI engine storage size [e.g., 10 for 10GB, default: 10]:
   Specify InfluxDB storage size [e.g., 100 for 100GB, default: 100]:
   Specify storage class name: managed-nfs-storage
   Do you want to expose dashboard and REST API services for external access? [default: y]:
   
   ----------------------------------------
   install_namespace = federatorai
   storage_type = persistent
   log storage size = 2 GB
   AI engine storage size = 10 GB
   InfluxDB storage size = 100 GB
   storage class name = managed-nfs-storage
   expose service = y
   ----------------------------------------
   Is the above information correct [default: y]:
   Processing...
   
   (snipped)
   .........
   All federatorai pods are ready.
   
   ========================================
   You can now access GUI through https://<YOUR IP>:31012
   Default login credential is admin/admin
   
   Also, you can start to apply alamedascaler CR for the target you would like to monitor.
   Review administration guide for further details. 
   ========================================
   ========================================
   You can now access Federatorai REST API through https://<YOUR IP>:31011
   The default login credential is admin/admin
   The REST API online document can be found in https://<YOUR IP>:31011/apis/v1/swagger/index.html
   ========================================
   
   Install Federator.ai v4.5.1-b1562 successfully
   
   Downloaded YAML files are located under /opt/federatorai/installation
   
   Downloaded files are located under /opt/federatorai/repo/v4.5.1-b1562
   ```

3. Verify Federator.ai pods are running properly.

   ```shell
   $ kubectl get pod -n federatorai
   ```
4. Log in to Federator.ai GUI, URL and login credential could be found in the output of Step 2.


### Configuration

1. Log in to Datadog with your account and get an [API key and application key][9] for using the Datadog API.

2. Configure Federator.ai for the metrics data source per cluster.
    - Launch Federator.ai GUI->Configuration->Clusters->Click "Add Cluster"
    - Enter API key and application key
    
	![Add Cluster Window][4] 
    
3. Refer to the [Federator.ai - Installation and Configuration Guide][6] and [User Guide][5] for more details. 


## Data Collected

### Metrics

See [metadata.csv][8] for a list of metrics provided by this integration.


### Service Checks

Federator.ai does not include any service checks.

### Events

Federator.ai does not include any events.

## Troubleshooting

Need help? Read the [Federator.ai - Installation and Configuration Guide][6] or contact [Datadog support][10].

[1]: https://prophetstor.com/federator-ai-2/
[2]: https://youtu.be/IooFJnB8bb8
[3]: https://github.com/DataDog/watermarkpodautoscaler
[4]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/federatorai/images/add_cluster_window.png
[5]: https://prophetstor.com/wp-content/uploads/documentation/Federator.ai/Latest%20Version/ProphetStor%20Federator.ai%20User%20Guide.pdf
[6]: https://prophetstor.com/wp-content/uploads/documentation/Federator.ai/Latest%20Version/ProphetStor%20Federator.ai%20Installation%20Guide.pdf
[7]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/federatorai/images/dashboard_overview.png
[8]: https://github.com/DataDog/integrations-extras/blob/master/federatorai/metadata.csv
[9]: https://docs.datadoghq.com/account_management/api-app-keys/
[10]: https://docs.datadoghq.com/help/
[11]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/federatorai/images/cluster_overview_dashboard.png
[12]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/federatorai/images/application_overview_dashboard.png
[13]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/federatorai/images/cost_analysis_overview.png
[14]: https://youtu.be/qX_HF_zZ4BA
