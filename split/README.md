# Split

## Overview

<a href="http://www.split.io">Split</a> is a platform for <a href="http://www.split.io/articles/controlled-rollout">controlled rollouts</a>, helping businesses of all sizes deliver exceptional user experiences—and mitigate risk—by providing an easy, secure way to target features to customers.

Integrate Split with Datadog to:
* See feature changes in context by including Split changlelogs in your event stream
* Correlate feature impact with application performance
* Avoid critical issues before they happen. Disable features proactively based on Datadog metrics and alerts

![Split Screenshot](https://raw.githubusercontent.com/DataDog/integrations-extras/ilan/split/split/images/split-screenshot.png =500x282)

## Setup

### Configuration

**In Datadog**<br/>
* Create an API Key <span class="hidden-api-key">${api_key}</span>

**In Split**<br/>

* Go to **Admin Settings** and click **Integrations** and navigate to the Marketplace. Click Add next to Datadog.<br/>

![Split Screenshot](https://raw.githubusercontent.com/DataDog/integrations-extras/ilan/split/split/images/in-split.png =800x)

* Paste your Datadog API Key and click Save.

![Split Screenshot](https://raw.githubusercontent.com/DataDog/integrations-extras/ilan/split/split/images/integrations-datadog.png =800x)

Split data should now be flowing into Datadog.
