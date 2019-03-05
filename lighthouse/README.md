# dd lighthouse custom agent check
a google chrome lighthouse custom agent check for datadog

## Overview

Get metrics from [Google Chrome Lighthouse][1] as a custom agent check in your [Datadog](https://www.datadoghq.com/) app in real time to:
* Visualize and monitor Lighthouse stats
* Track and Audit scores for yours websites Accessibility, Best Practices, Performance, PWA, SEO, and more (eventually)

![example lighthouse dashboard](./example_lighthouse_dd.png)

## Setup

At the moment this is just a [Custom Agent Check][2] for Datadog.  It's **not** included in the Datadog Agent package.

## Installation and Configuration

To install the Lighthouse Custom Agent Check on your host:

1. [Download the Datadog Agent][3]
2. Download the `custom_lighthouse.py` file for Lighthouse
3. Place it in your Agent's `checks.d` directory (in Linux, this would be found in `/etc/datadog-agent/checks.d/`)
4. Create a `custom_lighthouse.yaml` file in your Agent's `conf.d` directory (in Linux, this would be found in `/etc/datadog-agent/conf.d/`)
5. Reference the example `custom_lighthouse.yaml.example` file in this repository and copy it's contents into the `custom_lighthouse.yaml` file just created.
6. Edit the `custom_lighthouse.yaml` file for your use case (please note: This is a work in progress, it's unclear how resource intensive this can be, a typical lighthouse report takes about 5-10seconds to generate so it may be necessary to have a higher than usual `minimum_collection_interval` )
6. Restart the agent

## Requirements

Only tried this on Ubuntu so far. 

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

[Run the Agent's `status` subcommand][4] and look for `custom_lighthouse` under the Checks section.

## Data Collected
### Metrics
See `metadata.csv` for a list of metrics provided by this check.

### Events
The Lighthouse custom agent check does not include any events.

### Service Checks
The Light custom agent check does not include any service checks.

## Troubleshooting
This is not production ready at this time, and not meant to be used in production at this time.

[1]: https://developers.google.com/web/tools/lighthouse/
[2]: https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6#should-you-write-an-agent-check-or-an-integration
[3]: https://app.datadoghq.com/account/settings#agent
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
