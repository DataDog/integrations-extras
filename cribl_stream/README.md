# Cribl Stream

## Overview
[Cribl Stream][1] helps you process machine data – logs, instrumentation data, application data, metrics, etc. – in real time, and deliver them to your analysis platform of choice. It allows you to:

- Add context to your data, by enriching it with information from external data sources.
- Help secure your data, by redacting, obfuscating, or encrypting sensitive fields.
- Optimize your data, per your performance and cost requirements.

This integration allows you to visualize your Cribl Stream metrics in Datadog with our dashoard.
Screenshots should be absent for this section, instead put them in the media carousel with captions.

### Metrics

This will expose the following metrics:
- cribl.logstream.host.(in_bytes,in_events,out_bytes,out_events)
- cribl.logstream.index.(in_bytes,in_events,out_bytes,out_events)
- cribl.logstream.source.(in_bytes,in_events,out_bytes,out_events)
- cribl.logstream.sourcetype.(in_bytes,in_events,out_bytes,out_events)

For a complete list, please see the [metadata.csv][5] .


### Dashboards

Here we’ve set up a Datadog dashboard that can be shared with your organization. You can see base metrics like events per second, bytes per second, input types, output types, and infrastructure metrics used to monitor the performance of Stream. We also can monitor the percentage of reduction by events or bytes. This is useful if you are trying to improve search performance or licensing and infrastructure costs for the systems of analysis.

## Setup
Cribl Stream now has the ability to expose internal metrics as a data source :http://docs.cribl.io/logstream/sources-cribl-internal/. If you are using Datadog to monitor your applications and infrastructure this data source will send Stream metrics to the Datadog API bypassing the agent. 

# Installation

### Datadog
Navigate to the _API Keys_ under _Organization Settings_ and create an API Key for use by Cribl to send data.

### Cribl
1. In Cribl, navigate to _Quick Connects_ and click the _+Add Source_ button. 
![step1](/images/cribl_dd_1.png)
2. Scroll down to _System Internal_ and hover over _Cribl Internal_ and select _Select Existing_ and enable both _CriblLogs_ and _CriblMetrics_  
 - Make sure that both sources have Quick Connect enabled instead of Routes
![step3](/images/cribl_dd_3.png)

3. Now, click on _+Add Destination_ button.
4. Scroll to the _Datadog_ tile and click _+Add New_
5. Give a name to the input (e.g. Cribl_Datadog) 
![step4](/images/cribl_dd_4.png)

6. Next, enter your _Datadog API Key_ and make sure your site is either _US_ or _Europe_  
7. Finally add any Datadog tags, Message Field, Source or Host information [Cribl Datadog Destination Docs][3].
8. Click Save
10. Connect Cribl Metrics to your Datadog destination, select _Passthru_
![step5](/images/cribl_dd_6.png)

![complete](/images/cribl_dd_5.png)


## Uninstallation
To uninstall the Cribl Stream Dashboard, please use the instructions found here [delete dashboard][4]. 

## Support
Information about how and where to go for support for this integration.

[1]: https://cribl.io/stream
[2]: https://docs.cribl.io/stream/sources-datadog-agent
[3]: https://docs.cribl.io/stream/destinations-datadog
[4]: https://docs.datadoghq.com/dashboards/#delete-dashboard
[5]: https://github.com/DataDog/integrations-extras/blob/master/cribl_stream/metadata.csv