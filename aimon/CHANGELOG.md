# CHANGELOG - AIMon

## 1.0.0 / 2025-05-15

# AIMon Datadog Integration – Release Notes (v1.0.0)

## Overview  
This initial release introduces the **AIMon integration with Datadog**, enabling observability for **LLM response evaluation** through structured metrics and log ingestion. The integration helps teams monitor the quality, safety, and reliability of large language model outputs in real time.

## Features

### Metrics Integration
Publishes a suite of LLM evaluation metrics under the `AIMon.*` namespace:
- `aimon.hallucination` – Detects fabricated or inaccurate responses
- `aimon.toxicity` – Flags offensive or unsafe language
- `aimon.completeness` – Measures how fully the model answered the query
- `aimon.conciseness` – Evaluates response clarity and brevity
- `aimon.retrieval_relevance` – Scores context relevance to the input query, with domain-adaptable re-ranking
- `aimon.instruction_adherence` – Checks if the output follows instructions
- `aimon.context_classification` – Verifies correct use of context in responses
- `aimon.health_check` – Simple heartbeat metric for service monitoring

### Log Ingestion Support
- Logs capture evaluation events and model outputs in structured JSON
- Compatible with log list widget in Datadog

## Use Cases
- Continuously monitor LLM response quality and safety in production environments
- Detect hallucinated, toxic, or incomplete outputs in real time for immediate visibility and triage
- Evaluate context relevance and instruction adherence to ensure reliable, task-aligned generation

## Documentation  
Full documentation available at: [https://docs.aimon.ai](https://docs.aimon.ai)
