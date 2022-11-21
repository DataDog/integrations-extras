# Twingate

## Overview

[Twingate][1] is a zero trust network access platform that allows fast growing companies to quickly and easily provide secure access to their AWS environment. By incorporating modern technologies such as NAT traversal, QUIC, private proxies, and split tunneling, Twingate can replace a traditional or cloud VPN while improving user performance and overall security.

This integration allows organizations to monitor a user's resource access activities in real-time.

## Setup
### Pre-requisite
1. You must have the Datadog Agent installed on the Twingate Connector server. You also must be able to connect to that host and be able to edit the files so as to configure the Agent and YAML Integration Configs. Refer to [these instructions](https://docs.datadoghq.com/getting_started/agent/) to install the Datadog Agent.
2. You must deploy the Twingate Connector. Refer to [these instructions][3] to enable Real-time Connection Logs.

### Configure the Datadog Agent
#### Systemd
1. Set up [Datadog journald integration][5]
2. Replace `journald.d/conf.yaml` with the configuration below:
    ````
    logs:
      - type: journald
        container_mode: true
        include_units:
          - twingate-connector.service
        service: Twingate Connection
        source: Twingate Connection
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
4. Restart the agent `service datadog-agent restart`
5. Confirm the Twingate Analytic log can be found in the [Datadog Logs][10]



## Troubleshooting
Need help? Contact [Twingate Support][2]

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