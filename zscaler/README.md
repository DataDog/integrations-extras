# Agent Check: Zscaler Internet Access

## Overview

[Zscaler Internet Access][1] (ZIA) is a secure internet and web gateway delivered as a service from the cloud. ZIA logs are sent to Datadog through HTTPS using [Cloud NSS][8]. Datadog ingests ZIA telemetry, enabling you to apply security rules or visualize your data in dashboards.

## Requirements

* Zscaler Cloud NSS subscription

## Setup

1. From the ZIA console, go to **Administration** > **Nanolog Streaming Service**.
2. Select the **Cloud NSS Feeds** tab. Then, click on **Add Cloud NSS Feed**.
3. In the dialog box, enter or select the following values:
   * Feed Name: `<YOUR_FEED_NAME>`
   * NSS Type: `NSS for Web`
   * SIEM Type: `Other`
   * Batch Size: `16`
   * API URL: `https://http-intake.logs.datadoghq.com/v1/input?ddsource=zscaler`
   * HTTP headers:
      * Key: `Content-Type`; Value: `application/json`
      * Key: `DD-API-KEY`; Value: `<YOUR_DATADOG_API_KEY>`
4. In the **Formatting** section, enter or select the following values:
   * Log Type: `Web log`
   * Output Type: `JSON`
   * Feed Escape Character: `\",`
   * Feed output format:
      ```
      \{ "sourcetype" : "zscalernss-web", "event" : \{"datetime":"%d{yy}-%02d{mth}-%02d{dd} %02d{hh}:%02d{mm}:%02d{ss}","reason":"%s{reason}","event_id":"%d{recordid}","protocol":"%s{proto}","action":"%s{action}","transactionsize":"%d{totalsize}","responsesize":"%d{respsize}","requestsize":"%d{reqsize}","urlcategory":"%s{urlcat}","serverip":"%s{sip}","clienttranstime":"%d{ctime}","requestmethod":"%s{reqmethod}","refererURL":"%s{ereferer}","useragent":"%s{eua}","product":"NSS","location":"%s{elocation}","ClientIP":"%s{cip}","status":"%s{respcode}","user":"%s{elogin}","url":"%s{eurl}","vendor":"Zscaler","hostname":"%s{ehost}","clientpublicIP":"%s{cintip}","threatcategory":"%s{malwarecat}","threatname":"%s{threatname}","filetype":"%s{filetype}","appname":"%s{appname}","pagerisk":"%d{riskscore}","department":"%s{edepartment}","urlsupercategory":"%s{urlsupercat}","appclass":"%s{appclass}","dlpengine":"%s{dlpeng}","urlclass":"%s{urlclass}","threatclass":"%s{malwareclass}","dlpdictionaries":"%s{dlpdict}","fileclass":"%s{fileclass}","bwthrottle":"%s{bwthrottle}","servertranstime":"%d{stime}","contenttype":"%s{contenttype}","unscannabletype":"%s{unscannabletype}","deviceowner":"%s{deviceowner}","devicehostname":"%s{devicehostname}"\}\}
      ```
5. Click **Save**.
6. **Activate** your changes.

### Installation

The zscaler check is included in the [Datadog Agent][2] package.
No additional installation is needed on your server.

### Configuration

1. Edit the `zscaler.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your zscaler performance data. See the [sample zscaler.d/conf.yaml][3] for all available configuration options.

2. [Restart the Agent][4].

### Validation

[Run the Agent's status subcommand][5] and look for `zscaler` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][6] for a list of metrics provided by this check.

### Service Checks

zscaler does not include any service checks.

### Events

zscaler does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][7].

[1]: https://www.zscaler.com/products/zscaler-internet-access
[2]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[3]: https://github.com/DataDog/integrations-core/blob/master/zscaler/datadog_checks/zscaler/data/conf.yaml.example
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[6]: https://github.com/DataDog/integrations-core/blob/master/zscaler/metadata.csv
[7]: https://docs.datadoghq.com/help/
[8]: https://help.zscaler.com/zia/about-nanolog-streaming-service
