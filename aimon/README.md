# AIMon

## Overview

**AIMon provides tools to improve large language models (LLMs) by detecting issues like hallucinations, instruction adherence, retrieval relevance in real-time. Its models help ensure LLM outputs are accurate, relevant, and safe for use in production environments.**

This integration surfaces key response metrics, including hallucination, instruction adherence, context relevance, completeness, conciseness, and toxicity; to help teams improve output quality and build more reliable AI-driven systems.

With Datadog, AIMon metrics are visualized in real-time or asynchronously, enabling faster detection of anomalies, better prompt evaluation, and continuous tuning of LLM pipelines. Whether you're deploying in production or testing in R&D, this integration brings AI observability directly into your monitoring stack.

In addition to metric visualization, the integration logs rich metadata associated with each evaluated response. This includes the user query, full model response, company ID, application ID, version, timestamp and evaluation metrics; enabling traceability, debugging, and performance analysis at scale.

## Setup

1. Ensure you're logged into the Datadog platform to streamline the integration process.
2. Log in to your account on the [AIMon app][1].
3. Navigate to the Integrations tab.
4. Toggle on the Datadog integration. If you're not already logged into Datadog, you'll be prompted to do so to authorize the connection.

> Note: If your organization already has a Datadog API key and an AIMon account, you **must** register under the **same company name** in AIMon. This is typically the one set up by your organization's admin. Using a different company name will result in an error, as AIMon requires a one-to-one mapping between companies and Datadog organizations.

When the integration is active and the AIMon API key is in use, the platform will automatically transmit:
-   Evaluation metrics (e.g., hallucination scores, instruction adherence etc.)
-   Evaluation logs with relevant metadata, such as user prompts and model responses

## Uninstallation

1. Log in to your account on the [AIMon app][1].
2. Navigate to the Integrations tab.
3. Toggle Datadog integration off.
4. Once this integration has been uninstalled, any previous authorizations are revoked.
5. Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the [API Keys page][3].

## Support

For support, please reach out to the AIMon team at [info@aimon.ai][4]


[1]: https://www.app.aimon.ai/
[3]: https://app.datadoghq.com/organization-settings/api-keys
[4]: mailto:info@aimon.ai