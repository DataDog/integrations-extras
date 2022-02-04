# Sourcegraph Datadog Services Map Extension

## Overview

![Datadog Services Map Screenshot](images/sourcegraph-datadog-services-map-extension.png)

The Datadog Services Map Sourcegraph Extension brings the context of Datadog APM directly into your code on Sourcegraph and on your code host (via [the Sourcegraph Browser Extension](https://docs.sourcegraph.com/integration/browser_extension)). 

* See which services call or are called by other services 
* Go directly to the [Datadog APM Services Map](https://docs.datadoghq.com/tracing/visualization/services_map/) for your service 

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

> If you don't have a CORS anywhere URL, you can use the Sourcegraph demo: `https://sourcegraph-demo-cors-anywhere.herokuapp.com`

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

## Troubleshooting

If you're a an individual Sourcegraph user, email support@sourcegraph.com. 

If you're a Sourcegraph customer, use your existing support slack channel or email contact.

