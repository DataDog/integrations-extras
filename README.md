# Datadog Agent Integrations

[![Build Status][1]][2]
[![Code style - black][9]][10]

Collecting data is cheap; not having it when you need it can be very expensive. So we recommend instrumenting as much of your systems and applications as possible. This integrations repository will help you do that by making it easier to create and share new integrations for [Datadog][3].

**Note:** Integrations in this repo are not included with the Agent, and are not currently packaged.

## Building Integrations

For more information about how to build a new integration, please see [the guide at docs.datadoghq.com][4].

Also see the [agent integrations developer documentation][11] for more information on guidelines, tutorials, and metadata.

## Community Maintenance

Please note that integrations in this repository are maintained by the community. The current maintainer is listed in `manifest.json` and will address the pull requests and issues opened for that integration. Additionally, Datadog will assist on a best-effort basis, and will support the current maintainer whenever possible. When submitting a new integration, please indicate in the PR that you're willing to become the maintainer. For current maintainers, we understand circumstances change. If you're no longer able to maintain an integration, please notify us so we can find a new maintainer or mark the integration as orphaned. If you have any questions about the process, don't hesitate to contact us.

## Submitting Your Integration

Once you have completed the development of your integration, submit a [pull request][5] to have Datadog review your integration. Once we've reviewed your integration, we will approve and merge your pull request or provide feedback and next steps required for approval.

## Reporting Issues

For more information on integrations, please reference our [documentation][6] and [knowledge base][7]. You can also visit our [help page][8] to connect with us.

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/badges/test-results.svg
[2]: https://github.com/DataDog/integrations-extras/actions/workflows/master.yml
[3]: https://www.datadoghq.com
[4]: https://docs.datadoghq.com/developers/integrations/
[5]: https://github.com/DataDog/integrations-extras/compare
[6]: http://docs.datadoghq.com
[7]: https://help.datadoghq.com/hc/en-us
[8]: http://docs.datadoghq.com/help/
[9]: https://img.shields.io/badge/code%20style-black-000000.svg
[10]: https://github.com/ambv/black
[11]: https://datadoghq.dev/integrations-core/
