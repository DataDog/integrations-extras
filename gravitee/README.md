# Gravitee APIM

## Overview

Gravitee APIM is an enterprise-class agentic AI, API, and event stream management platform. It enables you to manage event streams and agentic AI as securely and easily as traditional APIs, bringing all your APIs together in a unified, full lifecycle management solution.

This integration allows you to monitor API and event stream performance, connection details, and API Gateway metrics, providing insights into the health and behavior of your Gravitee infrastructure. You can track top APIs, request and response times, content sizes, latency, slow performing APIs, gateway performance metrics, logs, and more.

This integration includes a pre-built Datadog dashboard to support comprehensive monitoring and observability of Gravitee APIM.

## Setup

### Download and install

1. Download the Datadog Reporter plugin [here][1].
2. Add the downloaded ZIP file to your [Gateway(s)][2] `{GRAVITEE_HOME}/plugins` folder.
3. Or, if you are installing the Gravitee Gateway via Helm, add the following entry in the `additionalPlugins` section (changing the version as needed):
  ```yaml
gateway:
  additionalPlugins:
    - https://download.gravitee.io/graviteeio-ee/apim/plugins/reporters/gravitee-reporter-datadog/gravitee-reporter-datadog-4.3.0.zip
```
4. Create a [Datadog API Key][3].  You will need this when _configuring_ the Reporter in Gravitee.

> **Note**: As with other reporter plugins, the Datadog Reporter plugin only needs to be installed on the Gateway container, not the Management API container.

> **Note**: If you want to collect system metrics and logs from the Management API service, use the [Datadog Agent][4] to tail the Management API logs, or collect them from stdout.

### Configuration

1. To configure the Datadog Reporter plugin on the Gateway, enable the `reporters` section in your Gravitee `values.yaml` file. See the example below:

```yaml
reporters:
  datadog:
    enabled: true
    site: "datadoghq.eu"
    authentication:
      #apiKeyPrefix: ""
      apiKey: "YOUR_API_KEY"
      #appKey: "YOUR_APP_KEY"
      #tokenScheme: ""
      #token: "YOUR_TOKEN"
      #username: "YOUR_USERNAME"
      #password: "YOUR_PASSWORD"
```
> **Note**: You can obscure the value of this API key by using [configuration-level secrets][5] in your Gravitee `values.yaml` file.

### Data Type Mapping

Gravitee has different types of reporting data, and each type maps to a different resource type in Datadog. The mapping is as follows:

| Gravitee Convention                      | Examples                      | Datadog Convention |
| ---------------------------------------- | ----------------------------- | ------------------ |
| Metadata                                 | API name, user agent          | Tags               |
| Monitoring                               | CPU, memory usage             | Metrics            |
| EndpointStatus                           | Health check status           | Events             |
| [Metrics][6] | Response time, content length | Metrics            |
| [Logs][7]   | Request body, response body   | Log                |

## Uninstallation

### In Gravitee

1. To delete the Reporter, delete the `gravitee-reporter-datadog-4.3.0.zip` from your Gateway `{GRAVITEE_HOME}/plugins` folder.
2. To disable the Reporter, change the `reporters.datadog.enabled` attribute to `false` (in your Gravitee `values.yaml` file).

### In Datadog
1. Click **Uninstall** on the integration tile to remove the dashboard.

## Support

Need help? Contact [Gravitee support][8].

Have feedback about the integration? Email Gravitee at <contact@graviteesource.com>.


[1]: https://download.gravitee.io/#graviteeio-ee/apim/plugins/reporters/gravitee-reporter-datadog/
[2]: https://documentation.gravitee.io/apim/4.3/overview/plugins#deployment
[3]: https://docs.datadoghq.com/account_management/api-app-keys/#add-an-api-key-or-client-token
[4]: https://docs.datadoghq.com/agent/?tab=Linux
[5]: https://documentation.gravitee.io/apim/configure-apim/sensitive-data-management/configuration-level-secrets
[6]: https://documentation.gravitee.io/apim/gravitee-gateway/reporters#metrics-sent-via-reporters
[7]: https://documentation.gravitee.io/apim/gravitee-gateway/reporters#log-data-sent-via-reporters
[8]: https://www.gravitee.io/contact-us