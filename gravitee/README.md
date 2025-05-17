# Gravitee

## Overview

Comprehensive monitoring and observability of the Gravitee API & Event Streams Management solution. This integration allows you to track API & Event Stream performance, connection details, and database metrics, providing insights into the health and behavior of your Gravitee infrastructure.

We rely on your feedback and feature requests to improve this dashboard. Please send feedback to <contact@graviteesource.com>.

## Setup

## Download and install

To configure the Datadog reporter, download the reporter plugin [here][1]. Once you've downloaded the .ZIP file, you can add it to the Gateway in the same way as [other plugins][2]. Typically, you'll install plugins in the `/plugins` directory of your installation. As with other reporters, the Datadog reporter plugin only needs to be installed on the Gateway, not the Management API.

{% hint style="info" %}
If you want to collect system metrics and logs from the Management API service, use the [Datadog agent][3] to tail the Management API logs, or collect them from stdout.
{% endhint %}

If you are installing the Gravitee Gateway via Helm, add the following entry in the `additionalPlugins` section (changing the version as needed):

```yaml
gateway:
  additionalPlugins:
    - https://download.gravitee.io/graviteeio-ee/apim/plugins/reporters/gravitee-reporter-datadog/gravitee-reporter-datadog-3.0.1.zip
```

## Configuration

To configure the Datadog reporter on the Gateway, enable the `reporters` section in `gravitee.yml`. This will look something like:

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

Authentication is required for the Gateway to send reporting data to Datadog. Gravitee sends data to Datadog as an [API client][4] over HTTP, and so needs to authenticate to Datadog. The basic way to do this is via an [API key][5], but you can also configure application keys and client tokens, depending on what your Datadog account requires.

{% hint style="info" %}
You can obscure the value of this API key by using [configuration-level secrets][6] in `gravitee.yml`.
{% endhint %}

## Data type mapping

Gravitee has different types of reporting data, and each type maps to a different resource type in Datadog. The mapping is as follows:

| Gravitee Convention                      | Examples                      | Datadog Convention |
| ---------------------------------------- | ----------------------------- | ------------------ |
| Metadata                                 | API name, user agent          | Tags               |
| Monitoring                               | CPU, memory usage             | Metrics            |
| EndpointStatus                           | Health check status           | Events             |
| [Metrics][7] | Response time, content length | Metrics            |
| [Logs][8]   | Request body, response body   | Log                |

The reporter sends metrics to Datadog with the prefix `gravitee.apim`. Metrics in Datadog appear with underscores between words, instead of the CamelCase default shown in the metrics page. For example, `proxyResponseTimeMs` appears in Datadog as `proxy_response_time_ms`.

For details on what metrics and logs are being sent, please see [documentation][9] and [plugin details][10].

## Uninstallation

## Uninstall

Simply disable or remove the DataDog Reporter plugin in your Gravitee values.yaml file.

## Support

Contact [Gravitee][11] for help


[1]: https://download.gravitee.io/#graviteeio-ee/apim/plugins/reporters/gravitee-reporter-datadog/
[2]: ../../getting-started/plugins/
[3]: https://docs.datadoghq.com/agent/?tab=Linux
[4]: https://docs.datadoghq.com/api/latest/
[5]: https://docs.datadoghq.com/account_management/api-app-keys/
[6]: ../../configure-apim/sensitive-data-management/configuration-level-secrets.md
[7]: ./#metrics-sent-via-reporters
[8]: ./#log-data-sent-via-reporters
[9]: https://documentation.gravitee.io/apim/gravitee-gateway/reporters/datadog-reporter
[10]: https://www.gravitee.io/plugins/gravitee-reporter-datadog
[11]: https://www.gravitee.io/contact-us