# Lighthouse Integration

## Overview

Get metrics from [Google Chrome Lighthouse][1] in real time to:

- Visualize and monitor Lighthouse stats.
- Track and audit scores for your websites accessibility, best practices, performance, PWA, and SEO audit scores.

## Setup

The Lighthouse check is not included in the [Datadog Agent][2] package, so you will need to install it yourself.

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Google Chrome Lighthouse check on your host. See our dedicated Agent guide for [installing community integrations][3] to install checks with the [Agent prior to version 6.8][4] or the [Docker Agent][5]:

1. [Download and launch the Datadog Agent][7].
2. Run the following command to install the integrations wheel with the Agent:

   ```shell
   datadog-agent integration install -t datadog-<INTEGRATION_NAME>==<INTEGRATION_VERSION>
   ```

3. Configure your integration like [any other packaged integration][8].

### Configuration

1. Edit the `lighthouse.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][9] to start collecting your Lighthouse [metrics](#metrics).
   See the [sample lighthouse.d/conf.yaml][10] for all available configuration options.

2. [Restart the Agent][11]

### Requirements

1. Node.js LTS (8.9+). 
   - Check if Node.js and npm installed:

   ```shell
   node -v
   npm -v
   ```

   - If not, [install Node.js and npm][12].

2. [Lighthouse][13]:
   - Check if installed.

   ```shell
   # example
   root@hostname:~# npm list -g --depth=0 | grep 'lighthouse'
   └── lighthouse@5.6.0
   ```

   - Install if not (no output from above command):
   ```shell
   npm install -g lighthouse
   ```


3. Either Google Chrome/Chromium or Puppeteer.

   - [Chromium][18]
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

   - [Puppeteer][14]
      + Check if installed.

      ```shell
      # example
      root@hostname:~# npm list -g --depth=0 | grep 'puppeteer'
      └── puppeteer@1.12.2
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

[Run the Agent's status subcommand][15] and look for `lighthouse` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][16] for a list of metrics provided by this check.

### Events

The Lighthouse integration does not include any events.

### Service Checks

The Lighthouse integration does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog support][17].

[1]: https://developers.google.com/web/tools/lighthouse
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/
[4]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[5]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[6]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[7]: https://app.datadoghq.com/account/settings#agent
[8]: https://docs.datadoghq.com/getting_started/integrations/
[9]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[10]: https://github.com/DataDog/integrations-extras/blob/master/lighthouse/datadog_checks/lighthouse/data/conf.yaml.example
[11]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[12]: https://nodejs.org/en/download
[13]: https://github.com/GoogleChrome/lighthouse
[14]: https://github.com/GoogleChrome/puppeteer
[15]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[16]: https://github.com/DataDog/integrations-extras/blob/master/lighthouse/datadog_checks/lighthouse/metadata.csv
[17]: https://docs.datadoghq.com/help/
[18]: https://www.chromium.org/
