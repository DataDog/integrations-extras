# Twingate

## Overview

[Twingate][1] is a zero trust network access platform that allows fast growing companies to quickly and easily provide secure access to their AWS environment. By incorporating modern technologies such as NAT traversal, QUIC, private proxies, and split tunneling, Twingate can replace a traditional or cloud VPN while improving user performance and overall security.

This integration allows organizations to monitor a user's resource access activities in real time.

## Setup
### Prerequisites
1. You have the Datadog Agent installed on the Twingate Connector server. You must be able to connect to that host and edit the files to configure the Agent and YAML Integration Configs. To install the Datadog Agent, see [Getting Started with the Agent][11].
2. You must deploy the Twingate Connector. To enable real-time connection logs, see the [Twingate documentation][3].

### Configure the Datadog Agent
#### Systemd Connector
1. Set up [Datadog journald integration][5].
2. Replace `journald.d/conf.yaml` with the following configuration:
   ```yaml
    logs:
      - type: journald
        container_mode: true
        include_units:
          - twingate-connector.service
        service: Twingate Connection
        source: Twingate
        log_processing_rules:
        - type: include_at_match
          name: analytics
          pattern: ANALYTICS
        - type: mask_sequences
          name: remove_analytics
          replace_placeholder: ""
          pattern: "ANALYTICS "
   ```
3. Add the `dd-agent` user to the `systemd-journal` group by using `usermod -a -G systemd-journal dd-agent`.
4. Restart the Datadog Agent by running `service datadog-agent restart`.
5. Confirm that the Twingate Analytic log appears in the [Log Explorer][10].


#### Docker Connector
##### Set up Datadog Docker integration for the Host Agent
Add the following lines to the `datadog.yaml` configuration file:
```yaml
logs_enabled: true
listeners:
- name: docker
config_providers:
- name: docker
polling: true
logs_config:
container_collect_all: true
container_exclude: ["image:.*"]
container_include: ["image:twingate/connector"]
```
- Add the `dd-agent` user to the `docker` group by using `usermod -a -G docker dd-agent`.
- Restart the Datadog Agent by running `service datadog-agent restart`.

##### Set up Datadog Docker integration for the Container Agent
Add additional parameters `-e DD_CONTAINER_EXCLUDE="image:.*"` and `-e DD_CONTAINER_INCLUDE="image:twingate/connector"` in the docker run command.
```shell
docker run -d --name datadog-agent \
           --cgroupns host \
           --pid host \
           -e DD_API_KEY=xxx \
           -e DD_LOGS_ENABLED=true \
           -e DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true \
           -e DD_CONTAINER_EXCLUDE="image:.*" \
           -e DD_CONTAINER_INCLUDE="image:twingate/connector" \
           -v /var/run/docker.sock:/var/run/docker.sock:ro \
           -v /var/lib/docker/containers:/var/lib/docker/containers:ro \
           -v /proc/:/host/proc/:ro \
           -v /opt/datadog-agent/run:/opt/datadog-agent/run:rw \
           -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
           gcr.io/datadoghq/agent:latest
```

##### Set up Twingate Connector with additional docker parameters
Add the label `com.datadoghq.ad.logs` to the Twingate Connector docker run command:
```shell
docker run -d --sysctl net.ipv4.ping_group_range="0 2147483647" \
  -l "com.datadoghq.ad.logs"='[{"service":"Twingate Connection","source":"Twingate","log_processing_rules":[{"type":"include_at_match","name":"analytics","pattern":"ANALYTICS"},{"type":"mask_sequences","name":"remove_analytics","replace_placeholder":"","pattern":"ANALYTICS "}]}]' \
  --env TENANT_URL="https://xxx.twingate.com" \
  --env ACCESS_TOKEN="xxx" \
  --env REFRESH_TOKEN="xxx" \
  --env TWINGATE_LABEL_HOSTNAME="`hostname`" \
  --name "twingate-golden-seal" \
  --restart=unless-stopped \
  $(docker run --help | grep -- --pull >/dev/null && echo "--pull=always") twingate/connector:1
```
**Note**: The Twingate Connector container needs to be recreated to add the new label 

### Twingate Analytics Dashboard
1. Go to the Datadog [Dashboard List][12].
2. Search for the Twingate Analytics dashboard.

## Troubleshooting
Need help? Contact [Twingate Support][2].

[1]: https://www.twingate.com/
[2]: https://help.twingate.com/hc/en-us
[3]: https://docs.twingate.com/docs/connector-real-time-logs
[4]: https://app.datadoghq.com/account/settings#agent
[5]: https://docs.datadoghq.com/agent/logs/?tab=journald
[6]: https://docs.datadoghq.com/logs/explorer/facets/#manage-facets
[7]: https://docs.datadoghq.com/logs/log_configuration/pipelines/?tab=source#create-a-pipeline
[8]: https://raw.githubusercontent.com/Twingate-Labs/datadog-integrations-extras/master/twingate/images/dashboard.png
[9]: https://docs.datadoghq.com/logs/explorer/facets/#measures
[10]: https://app.datadoghq.com/logs
[11]: https://docs.datadoghq.com/getting_started/agent/
[12]: https://app.datadoghq.com/dashboard/lists