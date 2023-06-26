## Overview

[JFrog][1] is the world’s universal, hybrid and end-to-end DevOps platform. This integration helps any JFrog self-hosted customer seamlessly stream logs, violations and metrics from JFrog Artifactory and JFrog Xray straight into your Datadog tool. This integration comes ready with in-built support for Datadog [log pipelines][2] which enriches and indexes the logs and makes them more searchable and treatable using Datadog [facets][3].  

Please let JFrog know how we can improve the integration. Feel free to visit our GitHub for more detailed documentation at: [github.com/jfrog/log-analytics-datadog][4].

## Setup
### Requirements

* Your [Datadog API key][5].

### Fluentd Installation

#### OS / Virtual Machine
Ensure you have access to the Internet from VM. Recommended install is through fluentd's native OS based package installs:

| OS             | Package Manager        | Link                                                 |
|----------------|------------------------|------------------------------------------------------|
| CentOS/RHEL    | Linux - RPM (YUM)      | https://docs.fluentd.org/installation/install-by-rpm |
| Debian/Ubuntu  | Linux - APT            | https://docs.fluentd.org/installation/install-by-deb |
| MacOS/Darwin   | MacOS - DMG            | https://docs.fluentd.org/installation/install-by-dmg |
| Windows        | Windows - MSI          | https://docs.fluentd.org/installation/install-by-msi |
| Gem Install**	 | MacOS & Linux - Gem			 | https://docs.fluentd.org/installation/install-by-gem | 


```text
** For Gem based install, Ruby Interpreter has to be setup first, following is the recommended process to install Ruby

1. Install Ruby Version Manager (RVM) as described in https://rvm.io/rvm/install#installation-explained, ensure to follow all the onscreen instructions provided to complete the rvm installation
	* For installation across users a SUDO based install is recommended, the installation is as described in https://rvm.io/support/troubleshooting#sudo

2. Once rvm installation is complete, verify the RVM installation executing the command 'rvm -v'

3. Now install ruby v2.7.0 or above executing the command 'rvm install <ver_num>', ex: 'rvm install 2.7.5'

4. Verify the ruby installation, execute 'ruby -v', gem installation 'gem -v' and 'bundler -v' to ensure all the components are intact

5. Post completion of Ruby, Gems installation, the environment is ready to further install new gems, execute the following gem install commands one after other to setup the needed ecosystem

	'gem install fluentd'

```

After FluentD is successfully installed, the below plugins are required to be installed

````text
gem install fluent-plugin-concat
gem install fluent-plugin-datadog
gem install fluent-plugin-jfrog-siem
gem install fluent-plugin-jfrog-metrics
gem install fluent-plugin-jfrog-send-metrics
````

##### Configure Fluentd
We rely heavily on environment variables so that the correct log files are streamed to your observability dashboards. Ensure that you fill in the .env file with correct values. Download the .env file from [here][6]

* **JF_PRODUCT_DATA_INTERNAL**: The environment variable JF_PRODUCT_DATA_INTERNAL must be defined to the correct location. For each JFrog service you will find its active log files in the `$JFROG_HOME/<product>/var/log` directory
* **DATADOG_API_KEY**: APIkey from [Datadog][5]
* **JPD_URL**: Artifactory JPD URL of the format `http://<ip_address>`
* **JPD_ADMIN_USERNAME**: Artifactory username for authentication
* **JFROG_ADMIN_TOKEN**: Artifactory [Access Token][7] for authentication
* **COMMON_JPD**: This flag should be set as true only for non-kubernetes installations or installations where JPD base URL is same to access both Artifactory and Xray (ex: https://sample_base_url/artifactory or https://sample_base_url/xray)

Apply the .env files and then run the fluentd wrapper with one argument pointed to the `fluent.conf.*` file configured.

````text
source .env_jfrog
./fluentd $JF_PRODUCT_DATA_INTERNAL/fluent.conf.<product_name>
````

#### Docker
In order to run fluentd as a docker image to send the logs, violations and metrics data to datadog, the following commands needs to be executed on the host that runs the docker.

1. Check the docker installation is functional, execute command 'docker version' and 'docker ps'.

2. Once the version and process are listed successfully, build the intended docker image for Datadog using the docker file,

   * Download Dockerfile from [here][8] to any directory which has write permissions.

3. Download the Dockerenvfile.txt file needed to run Jfrog/FluentD Docker Images for Datadog,

   * Download Dockerenvfile.txt from [here][9] to the directory where the docker file was downloaded.

```text

For Datadog as the observability platform, execute these commands to setup the docker container running the fluentd installation

1. Execute 'docker build --build-arg SOURCE="JFRT" --build-arg TARGET="DATADOG" -t <image_name> .'

    Command example

    'docker build --build-arg SOURCE="JFRT" --build-arg TARGET="DATADOG" -t jfrog/fluentd-datadog-rt .'

    The above command will build the docker image.

2. Fill the necessary information in the Dockerenvfile.txt file

    JF_PRODUCT_DATA_INTERNAL: The environment variable JF_PRODUCT_DATA_INTERNAL must be defined to the correct location. For each JFrog service you will find its active log files in the `$JFROG_HOME/<product>/var/log` directory
    DATADOG_API_KEY: APIkey from [Datadog](https://docs.datadoghq.com/account_management/api-app-keys/)
    JPD_URL: Artifactory JPD URL of the format `http://<ip_address>`
    JPD_ADMIN_USERNAME: Artifactory username for authentication
    JFROG_ADMIN_TOKEN: Artifactory [Access Token](https://jfrog.com/help/r/how-to-generate-an-access-token-video/artifactory-creating-access-tokens-in-artifactory) for authentication
    COMMON_JPD: This flag should be set as true only for non-kubernetes installations or installations where JPD base URL is same to access both Artifactory and Xray (ex: https://sample_base_url/artifactory or https://sample_base_url/xray)

3. Execute 'docker run -it --name jfrog-fluentd-datadog-rt -v <path_to_logs>:/var/opt/jfrog/artifactory --env-file Dockerenvfile.txt <image_name>' 

    The <path_to_logs> should be an absolute path where the Jfrog Artifactory Logs folder resides, i.e for an Docker based Artifactory Installation,  ex: /var/opt/jfrog/artifactory/var/logs on the docker host.

    Command example

    'docker run -it --name jfrog-fluentd-datadog-rt -v $JFROG_HOME/artifactory/var/:/var/opt/jfrog/artifactory --env-file Dockerenvfile.txt jfrog/fluentd-datadog-rt'


```

#### Kubernetes Deployment with Helm
Recommended installation for Kubernetes is to utilize the helm chart with the associated values.yaml in this repo.

| Product        | Example Values File             |
|----------------|---------------------------------|
| Artifactory    | helm/artifactory-values.yaml    |
| Artifactory HA | helm/artifactory-ha-values.yaml |
| Xray           | helm/xray-values.yaml           |

Add JFrog Helm repository:

```text
helm repo add jfrog https://charts.jfrog.io
helm repo update
```
Replace placeholders with your ``masterKey`` and ``joinKey``. To generate each of them, use the command
``openssl rand -hex 32``

##### Artifactory ⎈:
For Artifactory installation, download the .env file from [here][6]. Fill in the .env_jfrog file with correct values.

* **JF_PRODUCT_DATA_INTERNAL**: Helm based installs will already have this defined based upon the underlying docker images. Not a required field for k8s installation
* **DATADOG_API_KEY**: APIkey from [Datadog][5]
* **JPD_URL**: Artifactory JPD URL of the format `http://<ip_address>`
* **JPD_ADMIN_USERNAME**: Artifactory username for authentication
* **JFROG_ADMIN_TOKEN**: Artifactory [Access Token][7] for authentication
* **COMMON_JPD**: This flag should be set as true only for non-kubernetes installations or installations where JPD base URL is same to access both Artifactory and Xray (ex: https://sample_base_url/artifactory or https://sample_base_url/xray)

Apply the .env files and then run the helm command below

````text
source .env_jfrog
````
```text
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
For HA installation, please create a license secret on your cluster prior to installation.

```text
kubectl create secret generic artifactory-license --from-file=<path_to_license_file>artifactory.cluster.license 
```
Download the .env file from [here][6]. Fill in the .env_jfrog file with correct values.

* **JF_PRODUCT_DATA_INTERNAL**: Helm based installs will already have this defined based upon the underlying docker images. Not a required field for k8s installation
* **DATADOG_API_KEY**: APIkey from [Datadog][5]
* **JPD_URL**: Artifactory JPD URL of the format `http://<ip_address>`
* **JPD_ADMIN_USERNAME**: Artifactory username for authentication
* **JFROG_ADMIN_TOKEN**: Artifactory [Access Token][7] for authentication
* **COMMON_JPD**: This flag should be set as true only for non-kubernetes installations or installations where JPD base URL is same to access both Artifactory and Xray (ex: https://sample_base_url/artifactory or https://sample_base_url/xray)

Apply the .env files and then run the helm command below

````text
source .env_jfrog
````
```text
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

* **JF_PRODUCT_DATA_INTERNAL**: Helm based installs will already have this defined based upon the underlying docker images. Not a required field for k8s installation
* **DATADOG_API_KEY**: APIkey from [Datadog][5]
* **JPD_URL**: Artifactory JPD URL of the format `http://<ip_address>`
* **JPD_ADMIN_USERNAME**: Artifactory username for authentication
* **JFROG_ADMIN_TOKEN**: Artifactory [Access Token][7] for authentication
* **COMMON_JPD**: This flag should be set as true only for non-kubernetes installations or installations where JPD base URL is same to access both Artifactory and Xray (ex: https://sample_base_url/artifactory or https://sample_base_url/xray)

Apply the .env files and then run the helm command below

````text
source .env_jfrog
````

Use the same `joinKey` as you used in Artifactory installation to allow Xray node to successfully connect to Artifactory.

```text
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

### JFrog Platform (Self-hosted) tile 

If you have not installed the JFrog Platform (Self-hosted) tile yet, install the tile.

### JFrog dashboards

Once the JFrog Platform (Self-hosted) tile is installed, go to Dashboard -> Dashboard List, find `JFrog Artifactory Dashboard`, `Artifactory Metrics`, `Xray Metrics`, `Xray Logs`, `Xray Violations` and explore it.

#### JFrog Artifactory Dashboard
This dashboard is divided into three sections Application, Audit and Requests
* **Application** - This section tracks Log Volume(information about different log sources) and Artifactory Errors over time(bursts of application errors that may otherwise go undetected)
* **Audit** - This section tracks audit logs help you determine who is accessing your Artifactory instance and from where. These can help you track potentially malicious requests or processes (such as CI jobs) using expired credentials.
* **Requests** - This section tracks HTTP response codes, Top 10 IP addresses for uploads and downloads

#### JFrog Artifactory Metrics dashboard
This dashboard tracks Artifactory System Metrics, JVM memory, Garbage Collection, Database Connections, and HTTP Connections metrics

#### JFrog Xray Logs dashboard
Thi dashboard provides a summary of access, service and traffic log volumes associated with Xray. Additionally, customers are also able to track various HTTP response codes, HTTP 500 errors, and log errors for greater operational insight

#### JFrog Xray Violations Dashboard
This dashboard provides an aggregated summary of all the license violations and security vulnerabilities found by Xray. Information is segmented by watch policies and rules. Trending information is provided on the type and severity of violations over time, as well as, insights on most frequently occurring CVEs, top impacted artifacts and components.

#### JFrog Xray Metrics Dashboard
This dashboard tracks System Metrics, and data metrics about Scanned Artifacts and Scanned Components


### Data Collected

#### Metrics

See [metadata.csv][10] for a list of metrics provided by this integration

## Troubleshooting

**Q : Who do I reach out to if I run into problems with this integration ?**

A: You are welcome to reach out to JFrog directly by writing to us at [support@jfrog.com](support@jfrog.com) or opening a support ticket on our [Customer Support Portal][11]

**Q : I have JFrog Cloud Enterprise + license. Will I be able to use this integration?**

A: No.This integration is only built for JFrog customers who have on-prem or self-hosted JFrog subscription. JFrog is working on a SaaS Log streaming solution which will allow our SaaS customers to stream logs to Datadog. We hope to launch that solution in late 2023.

**Q : I am about to upgrade from on-prem to JFrog Cloud. Can I expect all the same logs to stream into Datadog from my SaaS instance post migration when I install the SaaS version of the integration?**

A: At launch, the SaaS version of the integration will only stream the following 3 logs from your SaaS JFrog instance to Datadog

## Support

Need help? Contact [support@jfrog.com](support@jfrog.com) or open a support ticket on JFrog [Customer Support Portal][11]

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

