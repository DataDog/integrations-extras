## Overview

[JFrog][1] is a universal, hybrid, and end-to-end DevOps platform. This integration helps any JFrog self-hosted customer seamlessly stream logs, violations and metrics from JFrog Artifactory and JFrog Xray straight into your Datadog tool. This integration comes ready with in-built support for Datadog [log pipelines][2] which enriches and indexes the logs and makes them more searchable and treatable using Datadog [facets][3].  

Let JFrog know how we can improve the integration. Feel free to visit our GitHub for more detailed documentation at: [github.com/jfrog/log-analytics-datadog][4].

### **IMPORTANT NOTE : The existing agent check to gather JFrog metrics has been replaced with Fluentd. Agent check will be deprecated by July 31st 2023.** 

## Setup

`Note! You must follow the order of the steps throughout Datadog Configuration`
1. [Requirements](#requirements)
2. [Fluentd Installation](#fluentd-installation)
   * [OS / Virtual Machine](#os--virtual-machine)
   * [Docker](#docker)
   * [Kubernetes Deployment with Helm](#kubernetes-deployment-with-helm)

### Requirements

* Your [Datadog API key][5].
* Install the JFrog Platform (Self-hosted) integration.

### Fluentd Installation

#### OS / Virtual Machine
Ensure you have access to the Internet from a virtual machine (VM). We recommend installation through FluentD's native OS based package installs:

| OS             | Package Manager        | Link                                                 |
|----------------|------------------------|------------------------------------------------------|
| CentOS/RHEL    | Linux - RPM (YUM)      | https://docs.fluentd.org/installation/install-by-rpm |
| Debian/Ubuntu  | Linux - APT            | https://docs.fluentd.org/installation/install-by-deb |
| MacOS/Darwin   | MacOS - DMG            | https://docs.fluentd.org/installation/install-by-dmg |
| Windows        | Windows - MSI          | https://docs.fluentd.org/installation/install-by-msi |
| Gem Install**	 | MacOS & Linux - Gem			 | https://docs.fluentd.org/installation/install-by-gem | 

```text
** For Gem based install, Ruby Interpreter has to be setup first, following is the recommended process to install Ruby

1. Install Ruby Version Manager (RVM) outlined in the [RVM documentation][12]. 
	* Use the `SUDO` command  for multi-user installation. For more information, see the [RVM troubleshooting documentation][13].

2. After the RVM installation is complete, execute the command 'rvm -v' to verify.

3. Install Ruby v2.7.0 or above with the command `rvm install <ver_num>`, (for example, `rvm install 2.7.5`).

4. Verify the ruby installation, execute `ruby -v`, gem installation `gem -v` and `bundler -v` to ensure all the components are intact.

5. Install the FluentD gem with the command `gem install fluentd`.

6. After FluentD is successfully installed, install the following plugins.
```
```shell
gem install fluent-plugin-concat
gem install fluent-plugin-datadog
gem install fluent-plugin-jfrog-siem
gem install fluent-plugin-jfrog-metrics
gem install fluent-plugin-jfrog-send-metrics
```

##### Configure Fluentd
We rely on environment variables to stream log files to your observability dashboards. Ensure that you fill in the `.env` file with the correct values. You can download the `.env` file [here][6].

* **JF_PRODUCT_DATA_INTERNAL**: The environment variable JF_PRODUCT_DATA_INTERNAL must be defined to the correct location. For each JFrog service, you can find its active log files in the `$JFROG_HOME/<product>/var/log` directory
* **DATADOG_API_KEY**: APIkey from [Datadog][5]
* **JPD_URL**: Artifactory JPD URL with the format `http://<ip_address>`
* **JPD_ADMIN_USERNAME**: Artifactory username for authentication
* **JFROG_ADMIN_TOKEN**: Artifactory [Access Token][7] for authentication
* **COMMON_JPD**: This flag should be set as true only for non-Kubernetes installations or installations where JPD base URL is same to access both Artifactory and Xray (for example, `https://sample_base_url/artifactory` or `https://sample_base_url/xray`)

Apply the `.env` files and run the fluentd wrapper with the following command, note that the argument points to the `fluent.conf.*` file configured.

```shell
source .env_jfrog
./fluentd $JF_PRODUCT_DATA_INTERNAL/fluent.conf.<product_name>
```

#### Docker
In order to run FluentD as a docker image to send the logs, violations, and metrics data to Datadog, execute the following commands on the host that runs the docker.

1. Execute the `docker version` and `docker ps` commands to verify that the Docker installation is functional.

2. If the version and process are listed successfully, build the intended docker image for Datadog using the docker file. You can download [this Dockerfile][8] to any directory that has write permissions.

3. Download the `Dockerenvfile.txt` file needed to run `Jfrog/FluentD` Docker Images for Datadog. You can download [this Dockerenvfile.txt][9] to the directory where the docker file was downloaded. 

4. Execute the following command to build the docker image `docker build --build-arg SOURCE="JFRT" --build-arg TARGET="DATADOG" -t <image_name>`. For example:

    ```shell
     docker build --build-arg SOURCE="JFRT" --build-arg TARGET="DATADOG" -t jfrog/fluentd-datadog-rt .'
    ```

5. Fill the necessary information in the Dockerenvfile.txt file

    * **JF_PRODUCT_DATA_INTERNAL**: The environment variable JF_PRODUCT_DATA_INTERNAL must be defined to the correct location. For each JFrog service you will find its active log files in the `$JFROG_HOME/<product>/var/log` directory
    * **DATADOG_API_KEY**: APIkey from [Datadog](https://docs.datadoghq.com/account_management/api-app-keys/)
    * **JPD_URL**: Artifactory JPD URL of the format `http://<ip_address>`
    * **JPD_ADMIN_USERNAME**: Artifactory username for authentication
    * **JFROG_ADMIN_TOKEN**: Artifactory [Access Token](https://jfrog.com/help/r/how-to-generate-an-access-token-video/artifactory-creating-access-tokens-in-artifactory) for authentication
    * **COMMON_JPD**: This flag should be set as true only for non-kubernetes installations or installations where JPD base URL is same to access both Artifactory and Xray (ex: https://sample_base_url/artifactory or https://sample_base_url/xray)

6. Execute 'docker run -it --name jfrog-fluentd-datadog-rt -v <path_to_logs>:/var/opt/jfrog/artifactory --env-file Dockerenvfile.txt <image_name>' 

   The <path_to_logs> should be an absolute path where the Jfrog Artifactory Logs folder resides, such as a Docker based Artifactory Installation. For example, `/var/opt/jfrog/artifactory/var/logs` on the docker host. For example:

    ```shell
     docker run -it --name jfrog-fluentd-datadog-rt -v $JFROG_HOME/artifactory/var/:/var/opt/jfrog/artifactory --env-file Dockerenvfile.txt jfrog/fluentd-datadog-rt
    ```


#### Kubernetes Deployment with Helm
Recommended installation for Kubernetes is to utilize the helm chart with the associated values.yaml in this repo.

| Product        | Example Values File             |
|----------------|---------------------------------|
| Artifactory    | helm/artifactory-values.yaml    |
| Artifactory HA | helm/artifactory-ha-values.yaml |
| Xray           | helm/xray-values.yaml           |

Add JFrog Helm repository:

```shell
helm repo add jfrog https://charts.jfrog.io
helm repo update
```
Replace placeholders with your ``masterKey`` and ``joinKey``. To generate each of them, use the command
``openssl rand -hex 32``

##### Artifactory ⎈:
For Artifactory installation, you can download the `.env` file [here][6]. Fill in the `.env_jfrog` file with correct values.

* **JF_PRODUCT_DATA_INTERNAL**: Helm based installs will already have this defined based upon the underlying Docker images. Not a required field for k8s installation
* **DATADOG_API_KEY**: APIkey from [Datadog][5]
* **JPD_URL**: Artifactory JPD URL of the format `http://<ip_address>`
* **JPD_ADMIN_USERNAME**: Artifactory username for authentication
* **JFROG_ADMIN_TOKEN**: Artifactory [Access Token][7] for authentication
* **COMMON_JPD**: This flag should be set as true only for non-Kubernetes installations or installations where the JPD base URL is the same to access both Artifactory and Xray (for example, `https://sample_base_url/artifactory` or `https://sample_base_url/xray`)

Apply the `.env` files and run the helm command below

```shell
source .env_jfrog
```
```shell
helm upgrade --install artifactory  jfrog/artifactory \
       --set artifactory.masterKey=FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF \
       --set artifactory.joinKey=EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE \
       --set datadog.api_key=$DATADOG_API_KEY  \
       --set jfrog.observability.jpd_url=$JPD_URL \
       --set jfrog.observability.username=$JPD_ADMIN_USERNAME \
       --set jfrog.observability.access_token=$JFROG_ADMIN_TOKEN \
       --set jfrog.observability.common_jpd=$COMMON_JPD \
       -f helm/artifactory-values.yaml
```

##### Artifactory-HA ⎈:
For an HA installation, create a license secret on your cluster prior to installation.

```shell
kubectl create secret generic artifactory-license --from-file=<path_to_license_file>artifactory.cluster.license 
```
Download the [.env file here][6]. Fill in the `.env_jfrog` file with correct values.

* **JF_PRODUCT_DATA_INTERNAL**: Helm based installs will already have this defined based upon the underlying Docker images. Not a required field for k8s installation
* **DATADOG_API_KEY**: APIkey from [Datadog][5]
* **JPD_URL**: Artifactory JPD URL of the format `http://<ip_address>`
* **JPD_ADMIN_USERNAME**: Artifactory username for authentication
* **JFROG_ADMIN_TOKEN**: Artifactory [Access Token][7] for authentication
* **COMMON_JPD**: This flag should be set as true only for non-Kubernetes installations or installations where the JPD base URL is the same to access both Artifactory and Xray (for example, `https://sample_base_url/artifactory` or `https://sample_base_url/xray`)

Apply the `.env` files and run the helm command below:

```shell
source .env_jfrog
```
```shell
helm upgrade --install artifactory-ha  jfrog/artifactory-ha \
       --set artifactory.masterKey=FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF \
       --set artifactory.joinKey=EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE \
       --set datadog.api_key=$DATADOG_API_KEY  \
       --set jfrog.observability.jpd_url=$JPD_URL \
       --set jfrog.observability.username=$JPD_ADMIN_USERNAME \
       --set jfrog.observability.access_token=$JFROG_ADMIN_TOKEN \
       --set jfrog.observability.common_jpd=$COMMON_JPD \
       -f helm/artifactory-ha-values.yaml
```

##### Xray ⎈:
For Artifactory installation, download the .env file from [here][6]. Fill in the .env_jfrog file with correct values.

* **JF_PRODUCT_DATA_INTERNAL**: Helm based installs will already have this defined based upon the underlying Docker images. Not a required field for k8s installation
* **DATADOG_API_KEY**: APIkey from [Datadog][5]
* **JPD_URL**: Artifactory JPD URL of the format `http://<ip_address>`
* **JPD_ADMIN_USERNAME**: Artifactory username for authentication
* **JFROG_ADMIN_TOKEN**: Artifactory [Access Token][7] for authentication
* **COMMON_JPD**: This flag should be set as true only for non-Kubernetes installations or installations where the JPD base URL is the same to access both Artifactory and Xray (for example, `https://sample_base_url/artifactory` or `https://sample_base_url/xray`)

Apply the `.env` files and run the helm command below

```shell
source .env_jfrog
```

Use the same `joinKey` as you used in Artifactory installation to allow Xray node to successfully connect to Artifactory.

```shell
helm upgrade --install xray jfrog/xray --set xray.jfrogUrl=http://my-artifactory-nginx-url \
       --set xray.masterKey=FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF \
       --set xray.joinKey=EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE \
       --set datadog.api_key=$DATADOG_API_KEY  \
       --set jfrog.observability.jpd_url=$JPD_URL \
       --set jfrog.observability.username=$JPD_ADMIN_USERNAME \
       --set jfrog.observability.access_token=$JFROG_ADMIN_TOKEN \
       --set jfrog.observability.common_jpd=$COMMON_JPD \
       -f helm/xray-values.yaml
```


### JFrog dashboards

Once the JFrog Platform (Self-hosted) tile is installed, go to Dashboard -> Dashboard List, find `JFrog Artifactory Dashboard`, `Artifactory Metrics`, `Xray Metrics`, `Xray Logs`, `Xray Violations` and explore it.

#### JFrog Artifactory dashboard
This dashboard is divided into three sections Application, Audit and Requests
* **Application** - This section tracks Log Volume(information about different log sources) and Artifactory Errors over time(bursts of application errors that may otherwise go undetected)
* **Audit** - This section tracks audit logs help you determine who is accessing your Artifactory instance and from where. These can help you track potentially malicious requests or processes (such as CI jobs) using expired credentials.
* **Requests** - This section tracks HTTP response codes, Top 10 IP addresses for uploads and downloads

#### JFrog Artifactory Metrics dashboard
This dashboard tracks Artifactory System Metrics, JVM memory, Garbage Collection, Database Connections, and HTTP Connections metrics

#### JFrog Xray Logs dashboard
Thi dashboard provides a summary of access, service and traffic log volumes associated with Xray. Additionally, customers are also able to track various HTTP response codes, HTTP 500 errors, and log errors for greater operational insight

#### JFrog Xray Violations dashboard
This dashboard provides an aggregated summary of all the license violations and security vulnerabilities found by Xray. Information is segmented by watch policies and rules. Trending information is provided on the type and severity of violations over time, as well as, insights on most frequently occurring CVEs, top impacted artifacts and components.

#### JFrog Xray Metrics dashboard
This dashboard tracks System Metrics, and data metrics about Scanned Artifacts and Scanned Components


### Data Collected

#### Metrics

See [metadata.csv][10] for a list of metrics provided by this integration

## Support

Need help? Contact [support@jfrog.com](support@jfrog.com) or open a support ticket on JFrog [Customer Support Portal][11]

### Troubleshooting

**Q : I have JFrog Cloud Enterprise + license. Will I be able to use this integration?**

A: No.This integration is only built for JFrog customers who have on-prem or self-hosted JFrog subscription. JFrog is working on a SaaS Log streaming solution which will allow our SaaS customers to stream logs to Datadog. We hope to launch that solution in late 2023.

**Q : I am about to upgrade from on-prem to JFrog Cloud. Can I expect all the same logs to stream into Datadog from my SaaS instance post migration when I install the SaaS version of the integration?**

A: At launch, the SaaS version of the integration will only stream the following 3 logs from your SaaS JFrog instance to Datadog


[1]: https://jfrog.com/
[2]: https://docs.datadoghq.com/logs/log_configuration/pipelines/?tab=source
[3]: https://docs.datadoghq.com/logs/explorer/facets/
[4]: https://github.com/jfrog/log-analytics-datadog
[5]: https://app.datadoghq.com/organization-settings/api-keys
[6]: https://raw.githubusercontent.com/jfrog/log-analytics-datadog/master/.env_jfrog
[7]: https://jfrog.com/help/r/how-to-generate-an-access-token-video/artifactory-creating-access-tokens-in-artifactory
[8]: https://raw.githubusercontent.com/jfrog/log-analytics-datadog/master/docker-build/Dockerfile
[9]: https://raw.githubusercontent.com/jfrog/log-analytics-datadog/master/docker-build/Dockerenvfile.txt
[10]: https://github.com/DataDog/integrations-extras/blob/master/jfrog_platform/metadata.csv
[11]: https://support.jfrog.com/s/login/?language=en_US&ec=302&startURL=%2Fs%2F
[12]: https://rvm.io/rvm/install#installation-explained
[13]: https://rvm.io/support/troubleshooting#sudo