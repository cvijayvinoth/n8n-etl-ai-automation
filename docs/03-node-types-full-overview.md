# Node Types: Full Architectural Deep Dive

This guide breaks down node internals, input item mapping, credential management, and execution lifecycle strategies.

---

## 1. How n8n Processes Data: The Item Stream

Unlike conventional workflow engines that execute row-by-row linearly, n8n is inherently **stream-oriented**.

### The Batch Object Format
When a node receives data, it receives an array of items:
```json
[
  {
    "json": {
      "id": "STU1002",
      "name": "Priya S",
      "course": "Machine Learning"
    },
    "binary": {
      "data": {
        "mimeType": "application/pdf",
        "fileExtension": "pdf",
        "fileName": "invoice.pdf"
      }
    }
  }
]
```

### Expression Resolution Syntax
Inside node parameters, you can reference contextual values dynamically:
- `{{ $json.field_name }}`: Resolves the value of `field_name` for the current item in iteration.
- `{{ $('Node Name').item.json.field }}`: Pulls data from a previous upstream node.
- `{{ $now.toISO() }}`: Luxon DateTime utilities for timestamp generation.

---

## 2. Credentials Architecture & Security

n8n separates workflow logic from authentication credentials:
- **Centralized Credential Store**: Credentials (API Keys, OAuth2 tokens, Basic Auth, SSH Keys) are encrypted at rest using an encryption key (`N8N_ENCRYPTION_KEY`).
- **Reuse Across Workflows**: Multiple nodes across various projects can point to a single credential instance.
- **Environment Variable Masking**: Dynamic values can be populated via `{{ $env.DATABASE_URL }}` to maintain 12-factor application security.

---

## 3. Error Handling & Resilience Patterns

Production pipelines require fault-tolerant routing:

```text
[HTTP Request Node]
       |
       +---> (On Success) ---> [Update Database]
       |
       +---> (On Error: Continue) ---> [Alert PagerDuty / Slack]
```

### Node Error Options
- **Continue on Fail**: Prevents workflow termination; outputs an error payload for downstream error handling.
- **Retry on Fail**: Automatically retries transient network failures up to $N$ times with exponential backoff intervals.
- **Error Trigger Workflow**: Designate a dedicated error-catcher workflow that triggers when any production workflow fails, receiving stack traces and payload metadata.
