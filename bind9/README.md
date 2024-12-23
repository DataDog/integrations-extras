## Overview

[Bind 9][19] is a complete, highly portable implementation of the Domain Name System (DNS) protocol. The Bind 9 name server (named), can act as an authoritative name server, recursive resolver, DNS forwarder, or all three simultaneously.


This integration provides enrichment and visualization for Query, Query Errors, Network, Lame Servers, Notify, and Security log types. It helps to visualize detailed insights into DNS request patterns, DNS communication, proper server configurations, and DNS attacks, ensuring a robust and reliable DNS environment through the out-of-the-box dashboards. Additionally, this integration provides out-of-the-box detection rules. Also, it will collect Bind 9 stats in form of metrics that can be used for visualizations as needed.


## Setup

### Installation

To install the Bind 9 integration, run the following Agent installation command and the steps below. For more information, see the [Integration Management][14] documentation.

**Note**: This step is not necessary for Agent version >= 7.58.0.

Linux command
  ```shell
  sudo -u dd-agent -- datadog-agent integration install datadog-bind9==1.1.0
  ```

#### Log collection

#### File Monitoring

1. Log in to your Bind 9 device.
2. Open the `named.conf` file to add a logging clause:
    ```
    logging {
     channel <example_channel> {
          file "/folder_path/file_name.log" versions <unlimited | <integer>> size <size> suffix <increment | timestamp>;
          print-time (yes | local | iso8601 | iso8601-utc);
          print-category yes;
          print-severity yes;
     };
     category <example-category> { <example_channel>; };
    }
    ```
    **NOTE**: Recommended value for `print-time` is `iso8601-utc` because datadog expects all logs to be in the UTC time zone by default. If the timezone of your Bind 9 logs is not UTC please make sure to follow [the steps for using a different time zone][21]. Also, [check the categories defined by Bind 9][16].
    
    Example logging channel:
    ```
    logging {
     channel default_log {
          file "/var/log/named/query.log" versions 3 size 10m;
          print-time iso8601-utc;
          print-category yes;
          print-severity yes;
     };
       category default { default_log; };
    }
    ```
3. Save and exit the file.
4. Restart the service
    ```
    service named restart
    ```

#### Syslog
1. Log in to your Bind 9 device.
2. Open `named.conf` file to add a logging clause:
    ```
    logging {
     channel <example_channel> {
          syslog <syslog_facility>;
          severity (critical | error | warning | notice | info | debug [level ] | dynamic);
          print-time (yes | local | iso8601 | iso8601-utc);
          print-category yes;
          print-severity yes;
     };
     category <example-category> { <example_channel>; };
    }
    ```
    **NOTE**: Recommended value for `print-time` is `iso8601-utc` because Datadog expects all logs to be in the UTC time zone by default. If the timezone of your Bind 9 logs is not UTC please make sure to follow [the steps for using a different time zone][21]. Also, [check the categories defined by Bind 9][16].
    
    Example logging channel:
    ```
    logging {
     channel default_log {
          syslog local3;
          print-time iso8601-utc;
          print-category yes;
          print-severity yes;
     };
       category default { default_log; };
    }
    ```

3. Save and exit the file.
4. Edit the syslog/rsyslog configuration to log to Datadog using the facility you selected in Bind 9:
    ```
    <syslog_facility>.* @@<DATADOG_AGENT_IP_ADDRESS>:<PORT>
    ```
5. Restart the following services.
    ```
    service syslog/rsyslog restart
    service named restart
    ```

**Note**: Make sure `print-category` and `print-severity` are set to `yes` in the channels configured for Bind 9 application.

### Configuration

#### Metric collection

1. Edit the `bind9.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][7] to start collecting your Bind 9 [metrics][20]. See the [sample bind9.d/conf.yaml][8] for all available configuration options.

   ```yaml
   init_config:
  
   instances:
     - url: "<BIND_9_STATS_URL>"
   ```

2. [Restart the Agent][9]

#### Log collection

1. Collecting logs is disabled by default in the Datadog Agent. Enable it in the `datadog.yaml` file:

   ```yaml
   logs_enabled: true
   ```

#### File monitoring

1. Add this configuration block to your `bind9.d/conf.yaml` file to start collecting your Bind 9 logs.

   See the [sample bind9.d/conf.yaml][8] for available configuration options.

   ```yaml
   logs:
     - type: file
       path: /var/log/named/*.log
       service: bind9
       source: bind9
   ```
   **Note**: Change the `path` variable in `conf.yaml` to the same path configured in the `file` parameter in channels for the Bind 9 application.

3. [Restart the Agent][9].

#### Syslog
1. Add this configuration block to your `bind9.d/conf.yaml` file to start collecting your Bind 9 logs.

   See the [sample bind9.d/conf.yaml][8] for available configuration options.

   ```yaml
   logs:
     - type: tcp
       port: <PORT>
       service: bind9
       source: bind9
   ```
   **Note**: Value of `port` should be the same as mentioned in `syslog.conf/rsyslog.conf`.

3. [Restart the Agent][9].

<h4 id="timezone-steps"> Specify a time zone other than UTC in the Bind 9 Datadog log pipeline</h4>

Datadog expects all logs to be in the UTC time zone by default. If the time zone of your Bind 9 logs is not UTC, specify the correct time zone in the Bind 9 Datadog pipeline.

To change the time zone in the Bind 9 pipeline:

  1. Navigate to the [Pipelines page][15] in the Datadog app. 

  2. Enter "Bind 9" in the  **Filter Pipelines** search box.

  3. Hover over the Bind 9 pipeline and click on the **clone**  button. This will create an editable clone of the Bind 9 pipeline.

  4. Edit the Grok Parser using the below steps:
      - In the cloned pipeline, find a processor with the name "Grok Parser: Parsing Bind 9 common log format" and click on the `Edit` button by hovering over the pipeline.
      - Under **Define parsing rules**,
        - Change the string `UTC` to the [TZ identifier][17] of the time zone of your Bind 9 server. For example, if your timezone is IST, you would change the value to`Asia/Calcutta`.
      - Click the **update** button.

### Validation

[Run the Agent's status subcommand][18] and look for `bind9` under the Checks section.

## Compatibility

The check is compatible with all major platforms.

## Data Collected

### Logs

The Bind 9 integration collects the following log types.

| Event Types    |
| -------------- |
| Query, Query Errors, Lame Servers, Notify, Security|

### Metrics

See [metadata.csv][11] for a list of metrics provided by this integration.

### Events

The Bind 9 check does not include any events.

### Service Checks

See [service_checks.json][12] for a list of service checks provided by this integration.

## Troubleshooting

If you see a **Permission denied** error while monitoring the log files, give the `dd-agent` user read permission on them.

  ```shell
  sudo chown -R dd-agent:dd-agent /var/log/named/
  ```

For any further assistance, contact [Datadog support][13].


[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[7]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[8]: https://github.com/DataDog/integrations-extras/blob/master/bind9/datadog_checks/bind9/data/conf.yaml.example
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[11]: https://github.com/DataDog/integrations-extras/blob/master/bind9/metadata.csv
[12]: https://github.com/DataDog/integrations-extras/blob/master/bind9/assets/service_checks.json
[13]: https://docs.datadoghq.com/help/
[14]: https://docs.datadoghq.com/agent/guide/integration-management/?tab=linux#install
[15]: https://app.datadoghq.com/logs/pipelines
[16]: https://downloads.isc.org/isc/bind9/9.18.29/doc/arm/html/reference.html#namedconf-statement-category
[17]: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
[18]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[19]: https://www.isc.org/bind/
[20]: https://docs.datadoghq.com/integrations/bind9/#metrics
[21]: https://docs.datadoghq.com/integrations/bind9/#timezone-steps