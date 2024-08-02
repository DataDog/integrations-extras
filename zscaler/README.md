# Agent Check: Zscaler Internet Access

## Overview

[Zscaler Internet Access][1] (ZIA) is a secure internet and web gateway delivered as a service from the cloud. ZIA logs are sent to Datadog through HTTPS using [Cloud NSS][8]. Datadog ingests ZIA telemetry, enabling you to apply security rules or visualize your data in dashboards.

## Requirements

A Zscaler Cloud NSS subscription is required.

## Setup

### ZIA Web Logs

1. From the ZIA console, go to **Administration** > **Nanolog Streaming Service**.
2. Select the **Cloud NSS Feeds** tab. Then, click on **Add Cloud NSS Feed**.
3. In the dialog box, enter or select the following values:
   * Feed Name: `<YOUR_FEED_NAME>`
   * NSS Type: `NSS for Web`
   * SIEM Type: `Other`
   * Batch Size: `16`
   * API URL: `{{< region-param key="http_endpoint" code="true" >}}/v1/input?ddsource=zscaler`
   * HTTP headers:
      * Key: `Content-Type`; Value: `application/json`
      * Key: `DD-API-KEY`; Value: `<YOUR_DATADOG_API_KEY>`
4. In the **Formatting** section, enter or select the following values:
   * Log Type: `Web log`
   * Output Type: `JSON`
   * Feed Escape Character: `\",`
   * Feed Output Format:
      ```
      \{ "sourcetype" : "zscalernss-web", "event" : \{"datetime":"%d{yy}-%02d{mth}-%02d{dd} %02d{hh}:%02d{mm}:%02d{ss}","reason":"%s{reason}","event_id":"%d{recordid}","protocol":"%s{proto}","action":"%s{action}","transactionsize":"%d{totalsize}","responsesize":"%d{respsize}","requestsize":"%d{reqsize}","urlcategory":"%s{urlcat}","serverip":"%s{sip}","clienttranstime":"%d{ctime}","requestmethod":"%s{reqmethod}","refererURL":"%s{ereferer}","useragent":"%s{eua}","product":"NSS","location":"%s{elocation}","ClientIP":"%s{cip}","status":"%s{respcode}","user":"%s{elogin}","url":"%s{eurl}","vendor":"Zscaler","hostname":"%s{ehost}","clientpublicIP":"%s{cintip}","threatcategory":"%s{malwarecat}","threatname":"%s{threatname}","filetype":"%s{filetype}","appname":"%s{appname}","pagerisk":"%d{riskscore}","department":"%s{edepartment}","urlsupercategory":"%s{urlsupercat}","appclass":"%s{appclass}","dlpengine":"%s{dlpeng}","urlclass":"%s{urlclass}","threatclass":"%s{malwareclass}","dlpdictionaries":"%s{dlpdict}","fileclass":"%s{fileclass}","bwthrottle":"%s{bwthrottle}","servertranstime":"%d{stime}","contenttype":"%s{contenttype}","unscannabletype":"%s{unscannabletype}","deviceowner":"%s{deviceowner}","devicehostname":"%s{devicehostname}"\}\}
      ```
5. Click **Save**.
6. **Activate** your changes.

### ZIA Firewall Logs

1. From the ZIA console, go to **Administration** > **Nanolog Streaming Service**.
2. Select the **Cloud NSS Feeds** tab. Then, click on **Add Cloud NSS Feed**.
3. In the dialog box, enter or select the following values:
   * Feed Name: `<YOUR_FEED_NAME>`
   * NSS Type: `NSS for Firewall`
   * SIEM Type: `Other`
   * Batch Size: `16`
   * API URL: `https://http-intake.logs.datadoghq.com/v1/input?ddsource=zscaler`
   * HTTP headers:
      * Key: `Content-Type`; Value: `application/json`
      * Key: `DD-API-KEY`; Value: `<YOUR_DATADOG_API_KEY>`
4. In the **Formatting** section, enter or select the following values:
   * Log Type: `Firewall logs`
   * Firewall Log Type: Full Session Logs
   * Feed Output Type: `JSON`
   * Feed Escape Character: `\",`
   * Feed Output Format:
      ```
      \{ "sourcetype" : "zscalernss-fw", "event" :\{"datetime":"%s{time}","user":"%s{elogin}","department":"%s{edepartment}","locationname":"%s{elocation}","cdport":"%d{cdport}","csport":"%d{csport}","sdport":"%d{sdport}","ssport":"%d{ssport}","csip":"%s{csip}","cdip":"%s{cdip}","ssip":"%s{ssip}","sdip":"%s{sdip}","tsip":"%s{tsip}","tunsport":"%d{tsport}","tuntype":"%s{ttype}","action":"%s{action}","dnat":"%s{dnat}","stateful":"%s{stateful}","aggregate":"%s{aggregate}","nwsvc":"%s{nwsvc}","nwapp":"%s{nwapp}","proto":"%s{ipproto}","ipcat":"%s{ipcat}","destcountry":"%s{destcountry}","avgduration":"%d{avgduration}","rulelabel":"%s{erulelabel}","inbytes":"%ld{inbytes}","outbytes":"%ld{outbytes}","duration":"%d{duration}","durationms":"%d{durationms}","numsessions":"%d{numsessions}","ipsrulelabel":"%s{ipsrulelabel}","threatcat":"%s{threatcat}","threatname":"%s{ethreatname}","deviceowner":"%s{deviceowner}","devicehostname":"%s{devicehostname}"\}\}
      ```
5. Click **Save**.
6. **Activate** your changes.

### ZIA DNS Logs

1. From the ZIA console, go to **Administration** > **Nanolog Streaming Service**.
2. Select the **Cloud NSS Feeds** tab. Then, click on **Add Cloud NSS Feed**.
3. In the dialog box, enter or select the following values:
   * Feed Name: `<YOUR_FEED_NAME>`
   * NSS Type: `NSS for DNS`
   * SIEM Type: `Other`
   * Batch Size: `16`
   * API URL: `https://http-intake.logs.datadoghq.com/v1/input?ddsource=zscaler`
   * HTTP headers:
      * Key: `Content-Type`; Value: `application/json`
      * Key: `DD-API-KEY`; Value: `<YOUR_DATADOG_API_KEY>`
4. In the **Formatting** section, enter or select the following values:
   * Log Type: `DNS logs`
   * Feed Output Type: `JSON`
   * Feed Escape Character: `\",`
   * Feed output format:
      ```
      \{ "sourcetype" : "zscalernss-dns", "event" :\{"datetime":"%s{time}","user":"%s{login}","department":"%s{dept}","location":"%s{location}","reqaction":"%s{reqaction}","resaction":"%s{resaction}","reqrulelabel":"%s{reqrulelabel}","resrulelabel":"%s{resrulelabel}","dns_reqtype":"%s{reqtype}","dns_req":"%s{req}","dns_resp":"%s{res}","srv_dport":"%d{sport}","durationms":"%d{durationms}","clt_sip":"%s{cip}","srv_dip":"%s{sip}","category":"%s{domcat}","odeviceowner":"%s{odeviceowner}","odevicehostname":"%s{odevicehostname}"\}\}
      ```
5. Click **Save**.
6. **Activate** your changes.

### ZIA Tunnel Logs

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
   * Log Type: `Tunnel`
   * Feed Output Type: `JSON`
   * Feed Escape Character: `\",`
   * Feed Output Format:
      ```
      \{ "sourcetype" : "zscalernss-tunnel", "event" : \{"datetime":"%s{datetime}","Recordtype":"%s{tunnelactionname}","tunneltype":"IPSEC IKEV %d{ikeversion}","user":"%s{vpncredentialname}","location":"%s{locationname}","sourceip":"%s{sourceip}","destinationip":"%s{destvip}","sourceport":"%d{srcport}","destinationport":"%d{dstport}","lifetime":"%d{lifetime}","ikeversion":"%d{ikeversion}","spi_in":"%lu{spi_in}","spi_out":"%lu{spi_out}","algo":"%s{algo}","authentication":"%s{authentication}","authtype":"%s{authtype}","recordid":"%d{recordid}"\}\}
      ```
5. Click **Save**.
6. **Activate** your changes.

### Validation

[Run the Agent's status subcommand][5] and look for `zscaler` under the Checks section.

## Data Collected

### Metrics

Zscaler does not include any metrics.

### Service Checks

Zscaler does not include any service checks.

### Events

Zscaler does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][7].

[1]: https://www.zscaler.com/products/zscaler-internet-access
[2]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[6]: https://github.com/DataDog/integrations-extras/blob/master/zscaler/metadata.csv
[7]: https://docs.datadoghq.com/help/
[8]: https://help.zscaler.com/zia/about-nanolog-streaming-service
