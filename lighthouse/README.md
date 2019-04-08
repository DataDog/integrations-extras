## Overview

Get metrics from [Google Chrome Lighthouse][1] in real time to:
* Visualize and monitor Lighthouse stats
* Track and audit scores for your websites accessibility, best practices, performance, PWA, and SEO audit scores

## Setup

The Lighthouse check is not included in the [Datadog Agent][2] package, so you will need to install it yourself.

### Installation

1. [Download the Datadog Agent][2].
2. Download the [`lighthouse.py` file][3] for Lighthouse.
3. Place it in the Agent's `checks.d` directory.

To install the Lighthouse Check on your host:

### Configuration

1. Create a `lighthouse.d/` folder in the `conf.d/` folder at the root of your Agent's directory. 
2. Create a `conf.yaml` file in the `lighthouse.d/` folder previously created.
3. Reference the example lighthouse [`conf.yaml.example` file][4] in this repository and copy it's contents into the `conf.yaml` file just created.
4. Edit the `conf.yaml` file for your use case.  **Note**: It's unclear how resource intensive this can be, a typical lighthouse report takes 5-10seconds to generate so it may be necessary to have a higher than usual `minimum_collection_interval`.
5. Restart the Agent.

### Requirements
 
1. Check you have Node and npm installed
```
node -v
npm -v
```
Lighthouse requires Node 8 LTS (8.9) or later.

If not, [install Node and npm][5]

2. [Install Lighthouse][6]
```
npm install -g lighthouse
```
3. Make sure Google Chrome is installed or Puppeteer (this custom Agent check runs Chrome in headless mode).
```
# example
vagrant@web2:~$ npm list -g --depth=0 | grep 'puppeteer'
└── puppeteer@1.12.2
```

If not, install Chrome or [Puppeteer][7]

```
npm install -g puppeteer
```

### Validation

[Run the Agent's status subcommand][8] and look for `lighthouse` under the Checks section.

## Data Collected
### Metrics
See [metadata.csv][9] for a list of metrics provided by this check.

### Events
The Lighthouse integration does not include any events.

### Service Checks
The Lighthouse integration does not include any service checks.

## Troubleshooting
Need help? Contact [Datadog support][10].

[1]: https://developers.google.com/web/tools/lighthouse/
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://github.com/DataDog/integrations-extras/blob/master/lighthouse/datadog_checks/lighthouse/lighthouse.py
[4]: https://github.com/DataDog/integrations-extras/blob/master/lighthouse/datadog_checks/lighthouse/data/conf.yaml.example
[5]: https://nodejs.org/en/download/
[6]: https://github.com/GoogleChrome/lighthouse
[7]: https://github.com/GoogleChrome/puppeteer
[8]: https://github.com/DataDog/integrations-extras/blob/master/lighthouse/datadog_checks/lighthouse/metadata.csv
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[10]: https://docs.datadoghq.com/help/