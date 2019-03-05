# dd lighthouse custom agent check
a google chrome lighthouse custom agent check for datadog

## Overview

Get metrics from [Google Chrome Lighthouse][1] as a custom agent check in your [Datadog](https://www.datadoghq.com/) app in real time to:
* Visualize and monitor Lighthouse stats
* Track and Audit scores for yours websites Accessibility, Best Practices, Performance, PWA, SEO, and more (eventually)

## Setup

The Lighthouse check is not included in the [Datadog Agent][2] package, so you will
need to install it yourself.

## Installation

1. [Download the Datadog Agent][3].
2. Download the [`lighthouse.py` file][4] for Lighthouse.
3. Place it in the Agent's `checks.d` directory.

To install the Lighthouse Check on your host:

### Configuration

1. Create a `lighthouse.d/` folder in the `conf.d/` folder at the root of your Agent's directory. 
2. Create a `lighthouse.yaml` file in the `lighthouse.d/` folder previously created.
3. Reference the example lighthouse [`conf.yaml.example` file][5] in this repository and copy it's contents into the `custom_lighthouse.yaml` file just created.
4. Edit the `custom_lighthouse.yaml` file for your use case (please note: it's unclear how resource intensive this can be, a typical lighthouse report takes about 5-10seconds to generate so it may be necessary to have a higher than usual `minimum_collection_interval` )
5. Restart the agent

## Requirements
 
1. Check you have Node and NPM installed
```
node -v
npm -v
```
Lighthouse requires Node 8 LTS (8.9) or later.

If not, [install Node and npm](https://nodejs.org/en/download/)

2. [Install Lighthouse](https://github.com/GoogleChrome/lighthouse)
```
npm install -g lighthouse
```
3. Make sure Google Chrome is installed or Puppeteer (this custom agent check runs chrome in headless mode)
```
# example
vagrant@web2:~$ npm list -g --depth=0 | grep 'puppeteer'
└── puppeteer@1.12.2
```

If not, install Chrome or [Puppeteer](https://github.com/GoogleChrome/puppeteer)

```
npm install -g puppeteer
```

## Validation

[Run the Agent's `status` subcommand][6] and look for `lighthouse` under the Checks section.

## Data Collected
### Metrics
See `metadata.csv` for a list of metrics provided by this check.

### Events
The Lighthouse integration does not include any events.

### Service Checks
The Lighthouse integration does not include any service checks.

## Troubleshooting
Need help? Contact [Datadog support][7].

[1]: https://developers.google.com/web/tools/lighthouse/
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://app.datadoghq.com/account/settings#agent
[4]: https://github.com/DataDog/integrations-extras/blob/master/lighthouse/datadog_checks/lighthouse/lighthouse.py
[5]: https://github.com/DataDog/integrations-extras/blob/master/lighthouse/datadog_checks/lighthouse/data/conf.yaml.example
[6]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[7]: https://docs.datadoghq.com/help/