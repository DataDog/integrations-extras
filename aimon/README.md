# AIMon

## Overview

AIMon provides tools that help organizations evaluate, monitor, and improve the quality and reliability of their AI applications. It surfaces key response metrics such as groundedness, instruction adherence, context relevance, and toxicity to help teams improve output quality and build more reliable AI systems.

The Datadog integration enables real-time or asynchronous visualization of these metrics, supporting faster anomaly detection, prompt evaluation, and tuning of LLM pipelines. AIMon also logs evaluation metadata such as user prompts, model responses, timestamps, and evaluation scores for traceability and debugging at scale.

## Setup

1. Within Datadog, navigate to the **Integrations** page and select **AIMon**.
2. Click **Install Integration**, then select **Connect Accounts**. You will be redirected to [AIMon][1] login page.
3. Log in to your AIMon account using your credentials or continue with Google. You will be redirected to the `/integrations` tab on AIMon.
4. Toggle on the **Datadog** integration to enable the connection.

**Note**: If your organization already has a Datadog API key and an AIMon account, make sure you register under the **same company name** in AIMon. AIMon requires a one-to-one mapping between companies and Datadog organizations. Using a different company name results in an error.

When the integration is active and the AIMon API key is in use, the platform will automatically transmit:
-   Evaluation metrics, such as hallucination scores and instruction adherence.
-   Evaluation logs with relevant metadata, such as user prompts and model responses.

## Uninstallation

1. Log in to your account on the [AIMon app][1] and navigate to the Integrations tab.
2. Disable the Datadog integration.
3. Log in to [Datadog][3] and navigate to the Integrations tab.
4. Disable the AIMon integration.
5. Search for the integration name on the [API Keys page][4] and disable any associated API keys to fully revoke access.

## Support

For support, please reach out to the [AIMon team][5].



[1]: https://www.app.aimon.ai/
[3]: https://app.datadoghq.com/account/login
[4]: https://app.datadoghq.com/organization-settings/api-keys
[5]: mailto:info@aimon.ai