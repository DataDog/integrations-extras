# AIMon

## Overview

**AIMon helps teams evaluate and monitor LLM responses at scale**

This integration surfaces key response metrics, including hallucination, instruction adherence, context relevance, completeness, conciseness, and toxicity; to help teams improve output quality and build more reliable AI-driven systems.

With Datadog, AIMon metrics are visualized in real-time or asynchronously, enabling faster detection of anomalies, better prompt evaluation, and continuous tuning of LLM pipelines. Whether you're deploying in production or testing in R&D, this integration brings AI observability directly into your monitoring stack.

## Setup

1. Log in to your account on the [AIMon app][1].
2. Navigate to the Integrations tab.
3. Toggle on the Datadog integration. You may be prompted to log in to Datadog to authorize the connection.

> Note:If your organization already has a Datadog API key and an AIMon account, you **must** register under the **same company name** in AIMon; typically the one set up by your organization's admin. Using a different company name will result in an error, as AIMon enforces one-to-one mapping between companies and Datadog organizations.


When the integration is active and the AIMon API key is in use, the platform will automatically transmit:
-   Evaluation metrics (e.g., hallucination scores, instruction adherence etc.)
-   Evaluation logs with relevant metadata, such as user prompts and model responses

## Uninstallation

1. Log in to your account on the [AIMon app][1].
2. Navigate to the Integrations tab.
3. Toggle Datadog integration off.

## Support

For support, please reach out to the AIMon team at info@aimon.ai


[1]: https://www.app.aimon.ai/