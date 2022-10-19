# Twingate

## Overview
[Twingate][1] is a zero trust network access platform that allows fast growing companies to quickly and easily provide secure access to their AWS environment. Incorporating modern technologies like NAT traversal, QUIC, private proxies, and split tunneling, Twingate can replace a traditional or cloud VPN while improving user performance and overall security.

This integration allows organizations to monitor a user's resource access activities in real-time.

## Setup
### Pre-requisite
1. You must have the Datadog Agent installed on the Twingate Connector server. You also must be able to connect to that host and be able to edit the files so as to configure the Agent and YAML Integration Configs. Refer to [these instructions](https://docs.datadoghq.com/getting_started/agent/) to install the Datadog Agent.
2. You must deploy the Twingate Connector. Refer to [these instructions] to enable Real-time Connection Logs.[3]

### Configure the Datadog Agent:
#### Systemd
1. Set up [Datadog journald integration][5]
2. Replace `journald.d/conf.yaml` with the configuration below:
    ````
    logs:
      - type: journald
        container_mode: true
        include_units:
          - twingate-connector.service
        log_processing_rules:
        - type: include_at_match
          name: analytics
          pattern: ANALYTICS
            - type: mask_sequences
          name: remove_analytics
          replace_placeholder: ""
          pattern: "ANALYTICS "
    ````
3. Add the `dd-agent` user to the `systemd-journal` group using the command `usermod -a -G systemd-journal dd-agent`
4. Restart agent `service datadog-agent restart`
5. Confirm the Twingate Analytic log can be found in the [Datadog Logs](https://app.datadoghq.com/logs)

### Configure Datadog Logs
1. Create a new Datadog [Pipeline][7] with
   * Filter `Service:twingate-connector`
   * Name `Twingate Analytics`
2. Create new Grok Parser Processor within the Pipeline with
    * Name `Remove Client IP Port`
    * Rule `rule %{ipv4:connection.client_ip}%{regex(".*")}`
3. Create new GeoIP Parser Processor within the Pipeline with
    * Name `GeoIP Parser`
    * Geo IP `connection.client_ip`
    *  Target Path `connection.client_geo`
4. [Create Datadog facets][6] for the following fields
   * Client IP `@connection.client_ip` 
   * Connector ID `@connector.id`
   * Connector `@connector.name`
   * Resource ID `@resource.id`
   * Resource `@resource.address`
   * Applied Rule `@resource.applied_rule`
   * User ID `@user.id`
   * User `@user.email`
   * Connection ID `@connection.id`
   * Bytes Received `@connection.rx`
   * Bytes Sent `@connection.tx`
   * Protocol `@connection.protocol`
   * Port `@connection.resource_port`
   * Remote Network ID `@remote_network.id`
   * Remote Network `@remote_netowrk_name`
   * Device ID `@device.id`
   * Error `@connection.error_message`
   * Location `@connection.client_geo.country.iso_code`





## Troubleshooting
Need help? Contact [Twingate Support][2]

[1]: https://www.twingate.com/
[2]: https://help.twingate.com/hc/en-us
[3]: https://docs.twingate.com/docs/connector-real-time-logs
[4]: https://app.datadoghq.com/account/settings#agent
[5]: https://docs.datadoghq.com/agent/logs/?tab=journald
[6]: https://docs.datadoghq.com/logs/explorer/facets/#manage-facets
[7]: https://docs.datadoghq.com/logs/log_configuration/pipelines/?tab=source#create-a-pipeline
