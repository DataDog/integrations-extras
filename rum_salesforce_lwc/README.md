# Salesforce Integration

## Overview

Instrument Salesforce Lightning Apps and Experience Cloud sites with Datadog Real User Monitoring using the Datadog RUM Salesforce bundle.

The integration supports Lightning Apps, Experience Cloud Head Markup, and Experience Cloud components. Use only one deployment path per Salesforce app or Experience Cloud site.

## Setup

### Prerequisites

Before you begin, gather the following Datadog RUM values:

- A Datadog RUM Application ID
- A Datadog RUM Client Token
- A Datadog site, such as `datadoghq.com`

You can get those values in Datadog under **Digital Experience > Real User Monitoring > Manage Applications > Set Up Manually**.

You should also enable [Lightning Web Security](https://developer.salesforce.com/docs/platform/lightning-components-security/guide/lws-enable.html) in the Salesforce org.

### Prepare your Salesforce site

All deployment paths must allow connections to the Datadog browser intake. Lightning App Utility Bar and Experience Cloud Component deployments load the bundle from a Salesforce Static Resource. Experience Cloud Head Markup can load it from either Salesforce Static Resources or the Datadog CDN.

#### 1. Add Salesforce Static Resources

This step is required for Lightning App Utility Bar and Experience Cloud Component deployments. For Experience Cloud Head Markup, follow it only if you want to host the SDK in Salesforce; skip it when using the Datadog CDN.

<!-- xxx tabs xxx -->
<!-- xxx tab "RUM only" xxx -->

For Lightning App Utility Bar, Experience Cloud Component, or Head Markup without Session Replay, download the Salesforce bundle:

```shell
mkdir -p staticresources
curl -fL -o staticresources/datadog_rum.js https://www.datadoghq-browser-agent.com/us1/v7/datadog-rum-salesforce.js
```

Register `datadog_rum.js` as the `datadog_rum` static resource.

<!-- xxz tab xxx -->
<!-- xxx tab "RUM with Session Replay (Head Markup only)" xxx -->

Download the Salesforce bundle and its matching chunks from the same version of the `@datadog/browser-rum` npm package. The following example uses version `7.15.0`. Run these commands in an empty working directory with `curl`, `tar`, and `zip` installed:

```shell
curl -fL -o browser-rum.tgz https://registry.npmjs.org/@datadog/browser-rum/-/browser-rum-7.15.0.tgz
tar -xzf browser-rum.tgz package/bundle
mkdir -p staticresources
cp package/bundle/datadog-rum-salesforce.js staticresources/datadog_rum.js
zip -j staticresources/chunks.zip package/bundle/chunks/*-datadog-rum-salesforce.js
```

Register `datadog_rum.js` as the `datadog_rum` static resource and `chunks.zip` as the `chunks` static resource. The ZIP must contain the chunk files at its root, with their original filenames, without a wrapping `chunks/` directory.

<!-- xxz tab xxx -->
<!-- xxz tabs xxx -->

For source-controlled Salesforce projects, copy the downloaded files into your project's static resources directory before adding the metadata below.

<!-- xxx tabs xxx -->
<!-- xxx tab "Project metadata" xxx -->

##### Project metadata

Use this option when your Salesforce project is managed from source control. Commit the metadata file with the downloaded bundle.

`staticresources/datadog_rum.resource-meta.xml`

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<StaticResource xmlns="http://soap.sforce.com/2006/04/metadata">
  <cacheControl>Public</cacheControl>
  <contentType>application/javascript</contentType>
</StaticResource>
```

For Head Markup with Session Replay, also add the `chunks` ZIP and its metadata:

`staticresources/chunks.resource-meta.xml`

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<StaticResource xmlns="http://soap.sforce.com/2006/04/metadata">
  <cacheControl>Public</cacheControl>
  <contentType>application/zip</contentType>
</StaticResource>
```

<!-- xxz tab xxx -->
<!-- xxx tab "Salesforce UI" xxx -->

##### Salesforce UI

Use this option when you configure the static resource directly in Salesforce Setup.

1. Go to **Setup > Static Resources**.
2. Click **New**.
3. Set **Name** to `datadog_rum`.
4. Upload the downloaded RUM JavaScript bundle.
5. Set **Cache Control** to **Public**, then save.

For Head Markup with Session Replay, repeat these steps to upload the matching chunks ZIP with **Name** set to `chunks`.

<!-- xxz tab xxx -->
<!-- xxz tabs xxx -->

#### 2. Configure CSP

Allow Salesforce to connect to the Datadog browser intake endpoint for your [Datadog site](https://docs.datadoghq.com/getting_started/site/#access-the-datadog-site).

<!-- xxx tabs xxx -->
<!-- xxx tab "Project metadata" xxx -->

##### Project metadata

Use this option when your Salesforce project is managed from source control.

`cspTrustedSites/browser_intake_datadoghq_com.cspTrustedSite-meta.xml`

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<CspTrustedSite xmlns="http://soap.sforce.com/2006/04/metadata">
  <context>All</context>
  <description>Datadog browser RUM intake for US1</description>
  <endpointUrl>https://browser-intake-datadoghq.com</endpointUrl>
  <isActive>true</isActive>
  <isApplicableToConnectSrc>true</isApplicableToConnectSrc>
</CspTrustedSite>
```

For non-US1 Datadog sites, update `endpointUrl` to match the correct Datadog browser intake endpoint for your region.

<!-- xxz tab xxx -->
<!-- xxx tab "Salesforce UI" xxx -->

##### Salesforce UI

Use this option when you configure the trusted endpoint directly in Salesforce Setup.

1. Go to **Setup > Security > Trusted URLs**.
2. Click **New Trusted URL**.
3. Set **API Name** to `browser_intake_datadoghq_com`.
4. Set **URL** to `https://browser-intake-datadoghq.com` for US1. For other regions, use the endpoint for your [Datadog site](https://docs.datadoghq.com/getting_started/site/#access-the-datadog-site).
5. Make sure **Active** is checked.
6. Set **CSP Context** to **All**.
7. Under **CSP Directives**, check **connect-src (scripts)**, then save.

<!-- xxz tab xxx -->
<!-- xxz tabs xxx -->

### Configuration

Choose the deployment path that matches your Salesforce app or Experience Cloud site.

<!-- xxx tabs xxx -->
<!-- xxx tab "Lightning App" xxx -->

#### Lightning App Utility Bar

Use for Salesforce Lightning Apps. This path loads a Datadog initializer LWC from the Utility Bar.

##### 1. Create Init Component

Create a Lightning Web Component that loads the Datadog Browser SDK and manually starts views as users navigate within the Lightning application.

A Lightning Web Component bundle requires an HTML template. Create the following file first.

File location: `lwc/datadogInit/datadogInit.html`

```html
<template></template>
```

Create the component JavaScript at `lwc/datadogInit/datadogInit.js`:

```javascript
import { LightningElement, wire } from 'lwc'
import { NavigationMixin, CurrentPageReference } from 'lightning/navigation'
import datadogRum from '@salesforce/resourceUrl/datadog_rum'
import { loadScript } from 'lightning/platformResourceLoader'

let datadogInitialization
let lastStartedUrl

export default class DatadogInit extends NavigationMixin(LightningElement) {
  connectedCallback() {
    this.initialize()
  }

  @wire(CurrentPageReference)
  handleCurrentPageReference(pageReference) {
    if (!pageReference) {
      return
    }

    this.initialize()

    if (window.DD_RUM) {
      this.startViewForPageReference(pageReference)
    }
  }

  startViewForPageReference(pageReference) {
    const urlPromise = this[NavigationMixin.GenerateUrl](pageReference)
    urlPromise.then((url) => {
      if (url === lastStartedUrl) {
        return
      }
      lastStartedUrl = url
      const absoluteUrl = new URL(url, window.location.origin).href
      window.DD_RUM.startView({ name: url, url: absoluteUrl })
    })
  }

  initialize() {
    if (!datadogInitialization) {
      datadogInitialization = this.loadDatadogRum()
    }
  }

  loadDatadogRum() {
    return loadScript(this, datadogRum).then(() => {
      const initConfig = {
        applicationId: '<YOUR_DATADOG_APPLICATION_ID>',
        clientToken: '<YOUR_DATADOG_CLIENT_TOKEN>',
        env: '<YOUR_ENV_NAME>',
        service: '<YOUR_SERVICE_NAME>',
        site: '<YOUR_DATADOG_SITE>',
        sessionSampleRate: 100,
        sessionReplaySampleRate: 0, // Session Replay is not supported inside Lightning Web Security (LWS).
        trackViewsManually: true,
        trackLongTasks: true,
        trackResources: true,
        trackUserInteractions: true,
      }
      window.DD_RUM.init(initConfig)
      lastStartedUrl = window.location.pathname + window.location.search + window.location.hash
      window.DD_RUM.startView({
        name: lastStartedUrl,
        url: window.location.href,
      })
    })
  }
}
```

##### 2. Add to Utility Bar

Expose the component to the Lightning Utility Bar, then add it to your app's Utility Bar with `eager` set to `true`.

`lwc/datadogInit/datadogInit.js-meta.xml`

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
  <apiVersion>64.0</apiVersion>
  <isExposed>true</isExposed>
  <masterLabel>Datadog Init</masterLabel>
  <targets>
    <target>lightning__UtilityBar</target>
  </targets>
</LightningComponentBundle>
```

Add the following `componentInstance` excerpt to your app's existing Utility Bar FlexiPage metadata, for example in `flexipages/MyApp_UtilityBar.flexipage-meta.xml`.

```xml
<componentInstance>
  <componentInstanceProperties>
    <name>eager</name>
    <type>decorator</type>
    <value>true</value>
  </componentInstanceProperties>
  <componentName>datadogInit</componentName>
  <identifier>datadogInit</identifier>
</componentInstance>
```

<!-- xxz tab xxx -->
<!-- xxx tab "Experience Cloud" xxx -->

#### Experience Cloud

Choose Head Markup to load the SDK from Salesforce Static Resources or the Datadog CDN. Use a Lightning Web Component when Head Markup is unavailable.

Head Markup runs outside Lightning Web Security (LWS) and is the only Salesforce deployment path that supports Session Replay.

<!-- xxx tabs xxx -->
<!-- xxx tab "Head Markup (CDN)" xxx -->

- **CDN async (recommended)**: Does not block page rendering, but it can miss events that occur before the SDK loads.
- **CDN sync**: Loads the SDK before subsequent scripts, so it collects earlier events, but it can affect page load performance.

For more information, see [Browser Monitoring Setup](https://docs.datadoghq.com/real_user_monitoring/application_monitoring/browser/setup/).

##### 1. Configure CSP for CDN Loading

Allow Salesforce to connect to the Datadog browser intake by completing the [Configure CSP](#2-configure-csp) section on this page. Then, in Experience Builder:

1. Open the site in Experience Builder from **Setup > Digital Experiences > All Sites > Builder**.
2. Go to **Settings > Security & Privacy**.
3. Change the security level from **Strict CSP** to **Relaxed CSP**. This is required because the Head Markup snippets contain inline initialization scripts. See [Select a Security Level in Experience Builder Sites](https://help.salesforce.com/s/articleView?id=experience.networks_security_csp_scriptlevel.htm&type=5).
4. Under **Trusted Sites for Scripts**, click **Add Trusted Site**.
5. Add `https://www.datadoghq-browser-agent.com` and make sure it is active.

For more information, see [Where to Allowlist Third-Party Hosts for Experience Builder Sites](https://help.salesforce.com/s/articleView?id=experience.networks_security_csp_allow.htm&type=5).

##### 2. Add CDN Head Markup

In Experience Builder, go to **Settings > Advanced > Edit Head Markup**, paste one of the following snippets, and replace the placeholder values with your Datadog RUM configuration. Set `sessionReplaySampleRate` to a value greater than `0` to enable Session Replay. Save the change, then publish the site.

<!-- xxx tabs xxx -->
<!-- xxx tab "CDN async (recommended)" xxx -->

```html
<script>
  ;(function (h, o, u, n, d) {
    h = h[d] = h[d] || {
      q: [],
      onReady: function (c) {
        h.q.push(c)
      },
    }
    d = o.createElement(u)
    d.async = 1
    d.src = n
    d.crossOrigin = 'anonymous'
    n = o.getElementsByTagName(u)[0]
    n.parentNode.insertBefore(d, n)
  })(window, document, 'script', 'https://www.datadoghq-browser-agent.com/us1/v7/datadog-rum-salesforce.js', 'DD_RUM')
</script>
<script>
  window.DD_RUM.onReady(function () {
    window.DD_RUM.init({
      applicationId: '<YOUR_DATADOG_APPLICATION_ID>',
      clientToken: '<YOUR_DATADOG_CLIENT_TOKEN>',
      env: '<YOUR_ENV_NAME>',
      service: '<YOUR_SERVICE_NAME>',
      site: '<YOUR_DATADOG_SITE>',
      sessionSampleRate: 100,
      sessionReplaySampleRate: 100,
      trackLongTasks: true,
      trackResources: true,
      trackUserInteractions: true,
    })
  })
</script>
```

<!-- xxz tab xxx -->
<!-- xxx tab "CDN sync" xxx -->

```html
<script
  src="https://www.datadoghq-browser-agent.com/us1/v7/datadog-rum-salesforce.js"
  type="text/javascript"
  crossorigin
></script>
<script>
  window.DD_RUM &&
    window.DD_RUM.init({
      applicationId: '<YOUR_DATADOG_APPLICATION_ID>',
      clientToken: '<YOUR_DATADOG_CLIENT_TOKEN>',
      env: '<YOUR_ENV_NAME>',
      service: '<YOUR_SERVICE_NAME>',
      site: '<YOUR_DATADOG_SITE>',
      sessionSampleRate: 100,
      sessionReplaySampleRate: 100,
      trackLongTasks: true,
      trackResources: true,
      trackUserInteractions: true,
    })
</script>
```

<!-- xxz tab xxx -->
<!-- xxz tabs xxx -->

<!-- xxz tab xxx -->
<!-- xxx tab "Head Markup (Static Resource)" xxx -->

Loads synchronously and hosts the SDK and its lazy-loaded chunks in Salesforce.

##### 1. Configure CSP for Static Resources

Allow Salesforce to connect to the Datadog browser intake by completing the [Configure CSP](#2-configure-csp) section on this page. Then, in Experience Builder:

1. Open the site in Experience Builder from **Setup > Digital Experiences > All Sites > Builder**.
2. Go to **Settings > Security & Privacy**.
3. Change the security level from **Strict CSP** to **Relaxed CSP**. This is required because the Head Markup snippet contains an inline initialization script. See [Select a Security Level in Experience Builder Sites](https://help.salesforce.com/s/articleView?id=experience.networks_security_csp_scriptlevel.htm&type=5).

##### 2. Add Static Resource Head Markup

In Experience Builder, go to **Settings > Advanced > Edit Head Markup**, paste the following snippet, and replace the placeholder values with your Datadog RUM configuration. Set `sessionReplaySampleRate` to a value greater than `0` to enable Session Replay. Save the change, then publish the site.

Use this after uploading the bundle and its chunks as described in the [Add Salesforce Static Resources](#1-add-salesforce-static-resources) section.

```html
<script src="/sfsites/c/resource/datadog_rum" type="text/javascript"></script>
<script>
  window.DD_RUM.onReady(function () {
    window.DD_RUM.init({
      applicationId: '<YOUR_DATADOG_APPLICATION_ID>',
      clientToken: '<YOUR_DATADOG_CLIENT_TOKEN>',
      site: '<YOUR_DATADOG_SITE>',
      service: '<YOUR_SERVICE_NAME>',
      env: '<YOUR_ENV_NAME>',
      sessionSampleRate: 100,
      sessionReplaySampleRate: 100,
      trackLongTasks: true,
      trackResources: true,
      trackUserInteractions: true,
    })
  })
</script>
```

<!-- xxz tab xxx -->
<!-- xxx tab "Lightning Web Component" xxx -->

#### Experience Cloud Component

Place an initializer LWC in a shared site region.

##### 1. Create Init Component

Create an LWC that loads the Datadog Browser SDK and manually starts views as users navigate within the Experience Cloud site.

A Lightning Web Component bundle requires an HTML template.

File location: `lwc/datadogInit/datadogInit.html`

```html
<template></template>
```

Create the component JavaScript at `lwc/datadogInit/datadogInit.js`:

```javascript
import { LightningElement, wire } from 'lwc'
import { NavigationMixin, CurrentPageReference } from 'lightning/navigation'
import datadogRum from '@salesforce/resourceUrl/datadog_rum'
import { loadScript } from 'lightning/platformResourceLoader'

let datadogInitialization
let lastStartedUrl

export default class DatadogInit extends NavigationMixin(LightningElement) {
  connectedCallback() {
    this.initialize()
  }

  @wire(CurrentPageReference)
  handleCurrentPageReference(pageReference) {
    if (!pageReference) {
      return
    }

    this.initialize()

    if (window.DD_RUM) {
      this.startViewForPageReference(pageReference)
    }
  }

  startViewForPageReference(pageReference) {
    const urlPromise = this[NavigationMixin.GenerateUrl](pageReference)
    urlPromise.then((url) => {
      if (url === lastStartedUrl) {
        return
      }
      lastStartedUrl = url
      const absoluteUrl = new URL(url, window.location.origin).href
      window.DD_RUM.startView({ name: url, url: absoluteUrl })
    })
  }

  initialize() {
    if (!datadogInitialization) {
      datadogInitialization = this.loadDatadogRum()
    }
  }

  loadDatadogRum() {
    return loadScript(this, datadogRum).then(() => {
      const initConfig = {
        applicationId: '<YOUR_DATADOG_APPLICATION_ID>',
        clientToken: '<YOUR_DATADOG_CLIENT_TOKEN>',
        env: '<YOUR_ENV_NAME>',
        service: '<YOUR_SERVICE_NAME>',
        site: '<YOUR_DATADOG_SITE>',
        sessionSampleRate: 100,
        sessionReplaySampleRate: 0, // Session Replay is not supported inside Lightning Web Security (LWS).
        trackViewsManually: true,
        trackLongTasks: true,
        trackResources: true,
        trackUserInteractions: true,
      }
      window.DD_RUM.init(initConfig)
      lastStartedUrl = window.location.pathname + window.location.search + window.location.hash
      window.DD_RUM.startView({
        name: lastStartedUrl,
        url: window.location.href,
      })
    })
  }
}
```

##### 2. Add to Experience Builder

Expose the component to Experience Builder and place it in a shared region, page template, global header, global footer, or theme/layout area that loads on every page.

`lwc/datadogInit/datadogInit.js-meta.xml`

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
  <apiVersion>64.0</apiVersion>
  <isExposed>true</isExposed>
  <masterLabel>Datadog Init</masterLabel>
  <targets>
    <target>lightningCommunity__Page</target>
    <target>lightningCommunity__Default</target>
  </targets>
</LightningComponentBundle>
```

<!-- xxz tab xxx -->
<!-- xxz tabs xxx -->

<!-- xxz tab xxx -->
<!-- xxz tabs xxx -->

### Validate the Installation

1. Open the configured Lightning app or published Experience Cloud site in a new browser session.
2. Open browser developer tools.
3. Confirm that the Datadog static resource loads successfully and that no CSP errors appear for the Datadog browser intake endpoint.
4. Navigate between pages.
5. In Datadog RUM Explorer, filter by the configured service and env, then confirm that view events appear as you navigate.

## Salesforce Feature Support Matrix

The following table outlines SDK feature support within the Lightning Web Security (LWS) sandbox environment.

<table>
  <thead>
    <tr><th>Feature Area</th><th>Supported</th><th>Notes</th></tr>
  </thead>
  <tbody>
    <tr><td colspan="3"><strong>View Events</strong></td></tr>
    <tr><td>Initial View</td><td>Yes</td><td>Automatic on init.</td></tr>
    <tr><td>Manual Tracking</td><td>Yes</td><td>Supported through <code>startView</code>.</td></tr>
    <tr><td>Navigation Timings</td><td>Yes</td><td>Collected via performance API.</td></tr>
    <tr><td>Web Vitals</td><td>Yes</td><td></td></tr>
    <tr><td colspan="3"><strong>Resource Events</strong></td></tr>
    <tr><td>Fetch / XHR</td><td>Limited (2)</td><td>Context payload inaccessible.</td></tr>
    <tr><td>Other Resources</td><td>Yes</td><td>CSS, images, etc.</td></tr>
    <tr><td>APM Correlation</td><td>Limited (2)</td><td>Requires header injection.</td></tr>
    <tr><td colspan="3"><strong>Action Events</strong></td></tr>
    <tr><td>Custom Actions</td><td>Yes</td><td>Supported through <code>addAction</code>.</td></tr>
    <tr><td>Click Actions</td><td>Yes</td><td>(3) Shadow DOM boundaries apply.</td></tr>
    <tr><td>Frustration Signals</td><td>Yes</td><td></td></tr>
    <tr><td>Loading Time</td><td>Limited (1)</td><td>Network detection may be incomplete.</td></tr>
    <tr><td colspan="3"><strong>Error Events</strong></td></tr>
    <tr><td>Console / Custom</td><td>Yes</td><td>Captured via instrumentation.</td></tr>
    <tr><td>Runtime Errors</td><td>Limited (4)</td><td>Often redacted as "Script error."</td></tr>
    <tr><td>Unhandled Rejection</td><td>No</td><td>Event not supported in LWS.</td></tr>
    <tr><td colspan="3"><strong>Other</strong></td></tr>
    <tr><td>Vital Events</td><td>Yes</td><td></td></tr>
    <tr><td>Long Task Events</td><td>Yes</td><td></td></tr>
    <tr><td>Session Replay</td><td>Head Markup only</td><td>Unsupported inside LWS; use the Salesforce bundle in Head Markup.</td></tr>
  </tbody>
</table>

Footnotes:

1. **Loading Time**: Ends when no pending network requests are detected. LWS may hide some fetch/XHR activity.
2. **Limited Context**: Inaccessible sandbox objects mean `beforeSend` cannot access response bodies or full XHR objects.
3. **Selectors**: Due to shadow boundaries, `event.target` may reflect the component host rather than the inner element.
4. **Runtime Errors**: Errors passing through the Lightning shell may lose stack traces and original error objects.

## Troubleshooting

Need help? Contact [Datadog Support](https://docs.datadoghq.com/help/).
