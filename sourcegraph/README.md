# Sourcegraph Datadog Services Map Extension

## Overview

![Datadog Services Map Screenshot](https://raw.githubusercontent.com/DataDog/integrations-extras/master/sourcegraph/images/sourcegraph-datadog-services-map-extension.png)

The Datadog Services Map Sourcegraph Extension brings the context of Datadog APM directly into your code on Sourcegraph and on your code host through [the Sourcegraph Browser Extension][1]. 

* See which services call or are called by other services.
* Go directly to the [Datadog APM Services Map][2] for your service.

## Setup

### 1. Enable the extension 

Visit the Sourcegraph extensions registry at yourSourcegraphInstance.com/extensions and search for `datadog-service-map`. Enable the extension. 

Sourcegraph Cloud users can directly enable the extension at https://sourcegraph.com/extensions/sourcegraph/datadog-service-map. 

### 2. Add configuration keys to the preferred Sourcegraph settings level

To enable this extension for everyone on your Sourcegraph instance, add these to your global settings `/site-admin/global-settings`. 

To enable it for just users in your organization, add this to your organization settings `/organizations/orgName/settings`. 

To enable it just for yourself, add these to your user settings `/user/username/settings`. 

```json
"datadogServiceMap.apiKey": "DD_API_KEY",
"datadogServiceMap.applicationKey": "DD_APPLICATION_KEY",
"datadogServiceMap.env": "DD_SERVICE_MAP_ENVIRONMENT",
"datadogServiceMap.corsAnywhereUrl": "CORS_ANYWHERE_URL",
```

If you don't have a CORS anywhere URL, you can use the [Sourcegraph demo][5].

### 3. Visit a code file with a service tracer call

Visit any code file with a service call and hover over the call, like: 
```JS
app.get("/", (req, res) => {
  tracer.trace("ping", () => {
    res.send("ping");
  });
});
```

Hovering over `tracer.trace("ping", ...` will display your tooltip with all called and calling services, as well as a link to go directly to the Datadog services map.

## Data Collected

### Metrics

This extension does not collect any metrics. 

### Service Checks

This extension does not include any service checks.

### Events

This extension does not include any events.

## Support

## Further reading

- [Use Datadog's Sourcegraph extension to navigate code and visualize service dependencies][4]

Need help? Contact [Datadog support][3].

[1]: https://docs.sourcegraph.com/integration/browser_extension
[2]: https://docs.datadoghq.com/tracing/visualization/services_map/
[3]: https://docs.datadoghq.com/help/
[4]: https://www.datadoghq.com/blog/sourcegraph-datadog-apm-integration/
[5]: https://sourcegraph-demo-cors-anywhere.herokuapp.com
