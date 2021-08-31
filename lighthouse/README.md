# Lighthouse Integration

## Overview

Get metrics from [Google Chrome Lighthouse][1] in real time to:

- Visualize and monitor Lighthouse stats.
- Track and audit scores for your websites accessibility, best practices, performance, PWA, and SEO audit scores.

## Setup

The Lighthouse check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the Lighthouse check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-lighthouse==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][4].

### Configuration

1. Edit the `lighthouse.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][7] to start collecting your Lighthouse [metrics](#metrics).
   See the [sample lighthouse.d/conf.yaml][8] for all available configuration options.

2. [Restart the Agent][9]

### Requirements

1. Node.js LTS (8.9+). 
   - Check if Node.js and npm installed:

   ```shell
   node -v
   npm -v
   ```

   - If not, [install Node.js and npm][10].

2. [Lighthouse][11]:
   - Check if installed.

   ```shell
   # example
   root@hostname:~# npm list -g --depth=0 | grep 'lighthouse'
   |_ lighthouse@5.6.0
   ```

   - Install if not (no output from above command):
   ```shell
   npm install -g lighthouse
   ```


3. Either Google Chrome/Chromium or Puppeteer.

   - [Chromium][16]
      + Debian/Ubuntu
      
      ```shell
      sudo apt-get update
      sudo apt-get install -y chromium-browser
      ```

      + RHEL/CentOS
      
      ```shell
      sudo yum install -y epel-release
      sudo yum install -y chromium
      ```

      **Note**: This integration runs Chrome/Chromium in headless mode; Chrome/Chromium may require kernel 4.4+ on RHEL/CentOS for the headless mode to work properly.

   - [Puppeteer][12]
      + Check if installed.

      ```shell
      # example
      root@hostname:~# npm list -g --depth=0 | grep 'puppeteer'
      |_ puppeteer@1.12.2
      ```

      + Install if not (no output from above command):

      ```shell
      npm install -g puppeteer --unsafe-perm=true
      ```

4. Verify if `dd-agent` user is able to run the lighthouse cli.

   ```shell
   sudo -u dd-agent lighthouse <WEB_URL> --output json --quiet --chrome-flags='--headless'
   ```

### Validation

[Run the Agent's status subcommand][13] and look for `lighthouse` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][14] for a list of metrics provided by this check.

### Events

The Lighthouse integration does not include any events.

### Service Checks

The Lighthouse integration does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog support][15].

[1]: https://developers.google.com/web/tools/lighthouse
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[7]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[8]: https://github.com/DataDog/integrations-extras/blob/master/lighthouse/datadog_checks/lighthouse/data/conf.yaml.example
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[10]: https://nodejs.org/en/download
[11]: https://github.com/GoogleChrome/lighthouse
[12]: https://github.com/GoogleChrome/puppeteer
[13]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[14]: https://github.com/DataDog/integrations-extras/blob/master/lighthouse/datadog_checks/lighthouse/metadata.csv
[15]: https://docs.datadoghq.com/help/
[16]: https://www.chromium.org/
