# Agent Check: Genesys Cloud MOS

## Overview

This check reports [Genesys Cloud][1] conversation call quality metrics, the Mean
Opinion Score (MOS), to Datadog.

MOS is a measure of perceived call quality on a scale of roughly 1.0 (unusable) to
approximately 4.9
(toll quality). Genesys Cloud computes it per conversation and exposes it directly through
the [Analytics Conversation Detail Query API][2] as the `mediaStatsMinConversationMos`
dimension (the minimum MOS observed on the conversation). This check queries ended
conversations on a trailing interval and reports the average and worst MOS, the number of
conversations, and how many fall at or below a configurable quality threshold.

## Setup

### Installation

The Genesys Cloud MOS check is not included in the [Datadog Agent][3] package, so you need
to install it.

For Agent v7.21+ / v6.21+, follow the instructions below to install the check on your
host. See [Use Community Integrations][4] to install with the Docker Agent or earlier
versions of the Agent.

1. Run the following command to install the integration's wheel with the Agent:

   ```shell
   datadog-agent integration install -w /path/to/genesys_mos/dist/datadog_genesys_mos-1.0.0-py3-none-any.whl
   ```

   This also installs the check's dependency, the Genesys Cloud Python SDK
   (`PureCloudPlatformClientV2`), into the Agent's embedded environment.

2. Configure your integration similar to core [integrations][5].

### Configuration

1. In Genesys Cloud, create an [OAuth client][6] using the **Client Credentials** grant.
   Assign it a role that grants the **Analytics > Conversation Detail > View** permission.
   Note the Client ID and Client Secret.

2. Edit the `genesys_mos.d/conf.yaml` file, in the `conf.d/` folder at the root of your
   Agent's configuration directory, to start collecting your Genesys Cloud MOS data. See
   the [sample genesys_mos.d/conf.yaml][7] for all available configuration options.

   ```yaml
   instances:
     - region: mypurecloud.com
       client_id: "<CLIENT_ID>"
       client_secret: "<CLIENT_SECRET>"
       min_collection_interval: 300
   ```

   Set `region` to the API host for your organization (for example `mypurecloud.com`,
   `usw2.pure.cloud`, or `mypurecloud.ie`), without the `api.` prefix.

3. [Restart the Agent][8].

### Secrets management

The `client_secret` (and optionally `client_id`) is sensitive, so avoid writing it in
plaintext in `conf.yaml`. The Agent resolves [secret handles][13] in check configuration
before the check runs, so you can store the credentials in a secret backend and reference
them with `ENC[]`. No changes to the check are required.

The example below uses the Agent's built-in JSON file backend (Agent v7.70+):

1. Create a JSON file, one level deep, readable only by the Agent user (`dd-agent` by
   default):

   ```json
   {
     "genesys_client_id": "<CLIENT_ID>",
     "genesys_client_secret": "<CLIENT_SECRET>"
   }
   ```

   ```shell
   sudo chown dd-agent:dd-agent /etc/datadog-agent/genesys_secrets.json
   sudo chmod 600 /etc/datadog-agent/genesys_secrets.json
   ```

2. Point the Agent at the file in `datadog.yaml`:

   ```yaml
   secret_backend_type: file.json
   secret_backend_config:
     file_path: /etc/datadog-agent/genesys_secrets.json
   ```

3. Reference the handles from `genesys_mos.d/conf.yaml` instead of the literal values. The
   handle in `ENC[...]` is the top-level key in the JSON file:

   ```yaml
   instances:
     - region: mypurecloud.com
       client_id: ENC[genesys_client_id]
       client_secret: ENC[genesys_client_secret]
       min_collection_interval: 300
   ```

4. Restart the Agent, then confirm the handles resolved with `sudo datadog-agent secret`,
   which lists each handle and its resolution status without printing the secret values.

Any other supported backend (for example `aws.secrets`, `azure.keyvault`, or a custom
`secret_backend_command`) works the same way; only `datadog.yaml` changes.

### Validation

[Run the Agent's status subcommand][9] and look for `genesys_mos` under the Checks section.

## Data collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this integration.

### Service checks

See [service_checks.json][11] for a list of service checks provided by this integration.

### Events

The Genesys Cloud MOS integration does not include any events.

## Troubleshooting

- `genesys_mos.can_connect` reports `CRITICAL`: verify the `region`, `client_id`, and
  `client_secret`, and confirm the OAuth client's role has the
  **Analytics > Conversation Detail > View** permission.
- No conversations reported: MOS is only present on conversations that used media with
  measurable quality (for example voice), and only after they have ended and been indexed.
  Increase `collection_lag_seconds` if conversations appear to be missed near the window
  boundary.

## Support

This integration is maintained by the community. For questions, issues, or feature
requests, contact the maintainer at ed.ferron@datadoghq.com or open an issue in the
[integrations-extras repository][12].

[1]: https://www.genesys.com/genesys-cloud
[2]: https://developer.genesys.cloud/analyticsdatamanagement/analytics/detail/conversation-query
[3]: https://app.datadoghq.com/account/settings/agent/latest
[4]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[5]: https://docs.datadoghq.com/getting_started/integrations/
[6]: https://help.mypurecloud.com/articles/create-an-oauth-client/
[7]: https://github.com/DataDog/integrations-extras/blob/master/genesys_mos/datadog_checks/genesys_mos/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[10]: https://github.com/DataDog/integrations-extras/blob/master/genesys_mos/metadata.csv
[11]: https://github.com/DataDog/integrations-extras/blob/master/genesys_mos/assets/service_checks.json
[12]: https://github.com/DataDog/integrations-extras/issues
[13]: https://docs.datadoghq.com/agent/configuration/secrets-management/
