# Split

## Overview

<a href="http://www.split.io">Split</a> is a platform for <a href="http://www.split.io/articles/controlled-rollout">controlled rollouts</a>, helping businesses of all sizes deliver exceptional user experiences and mitigate risk by providing an easy, secure way to target features to customers.

Integrate Split with Datadog to:

 * See feature changes in context by including Split changlelogs in your event stream
 * Correlate feature impact with application performance
 * Avoid critical issues before they happen. Disable features proactively based on Datadog metrics and alerts

## Setup

### Configuration

**In Datadog**

 * Create an API Key <span class="hidden-api-key">${api_key}</span>

**In Split**

 * Go to **Admin Settings** and click **Integrations** and navigate to the Marketplace. Click Add next to Datadog.<br/>

![Split Screenshot](https://raw.githubusercontent.com/DataDog/integrations-extras/ilan/split-integration/split/images/in-split.png)

 * Paste your Datadog API Key and click Save.

![Split Screenshot](https://raw.githubusercontent.com/DataDog/integrations-extras/ilan/split-integration/split/images/integrations-datadog.png)

Split data should now be flowing into Datadog.
