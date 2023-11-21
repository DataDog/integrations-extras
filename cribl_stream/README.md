# Cribl Stream

## Overview
[Cribl Stream][1] helps you process machine data logs, instrumentation data, application data, and metrics in real time, and deliver it to your analysis platform of choice. It allows you to:

- Add context to your data, by enriching it with information from external data sources.
- Help secure your data, by redacting, obfuscating, or encrypting sensitive fields.
- Optimize your data, per your performance and cost requirements.

This is for the self-hosted Cribl Stream version. 

Use the out-of-the-box dashboard to view the performance of the Stream with base metrics like events per second, bytes per second, input types, output types, and infrastructure metrics. Monitor reduction percentages by events or bytes, which is useful for improving search performance or licensing and infrastructure costs for the systems of analysis.

## Setup
You can send your Cribl Stream [internal metrics][6] to the Datadog API. 

### Installation

#### Datadog
Navigate to [_API Keys_][7] under Organization Settings and create an API Key for Cribl to send data.

#### Cribl
1. In Cribl, navigate to _Quick Connects_ and click the _+Add Source_ button. 
![step1](https://raw.githubusercontent.com/DataDog/integrations-extras/master/cribl_stream/images/images/cribl_dd_1.png)
2. Scroll down to _System Internal_ , hover over _Cribl Internal_ and choose _Select Existing_. Enable both _CriblLogs_ and _CriblMetrics_.  
 - **Note**: Both sources must have **Quick Connect** enabled instead of **Routes**.
![step3](https://raw.githubusercontent.com/DataDog/integrations-extras/master/cribl_stream/images/images/cribl_dd_3.png)

3. Click the _+Add Destination_ button.
4. Scroll to the _Datadog_ tile and click _+Add New_.
5. Give a name to the input (for example, Cribl_Datadog).
![step4](https://raw.githubusercontent.com/DataDog/integrations-extras/master/cribl_stream/images/images/cribl_dd_4.png)

6. Next, enter your _Datadog API Key_ and select your Datadog site.
7. Add any Datadog tags, a Message Field, Source, or Host information. For more information, see the [Cribl Datadog Destination documentation][3].
8. Click _Save_.
10. Select _Passthru_ to connect Cribl Metrics to your Datadog destination.
![step5](https://raw.githubusercontent.com/DataDog/integrations-extras/master/cribl_stream/images/images/cribl_dd_6.png)

![complete](https://raw.githubusercontent.com/DataDog/integrations-extras/master/cribl_stream/images/images/cribl_dd_5.png)

## Uninstallation
Use the [delete dashboard][4] option within the Cribl Stream dashboard settings to delete the Cribl Stream dashboard. Remove the Datadog destination from the Cribl Stream deployment to stop sending data.

## Data Collected
### Metrics
See [metadata.csv][5] for a list of metrics provided by this integration.
### Events
The Cribl Stream integration does not include any events.
### Service Checks
The Cribl Stream integration does not include any service checks.

## Troubleshooting
Need help? Contact [Cribl Support][8].

[1]: https://cribl.io/stream
[2]: https://docs.cribl.io/stream/sources-datadog-agent
[3]: https://docs.cribl.io/stream/destinations-datadog
[4]: https://docs.datadoghq.com/dashboards/#delete-dashboard
[5]: https://github.com/DataDog/integrations-extras/blob/master/cribl_stream/metadata.csv
[6]: http://docs.cribl.io/logstream/sources-cribl-internal/
[7]: https://app.datadoghq.com/organization-settings/api-keys
[8]: https://cribl.io/support
