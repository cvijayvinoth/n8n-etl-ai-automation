# Nodes and Node Types in n8n

A **Node** is an atomic execution unit in n8n. Each node receives an input data stream, performs a specific operation (network call, logic routing, file conversion, database query), and emits an output stream to downstream nodes.

---

## Core Classification of Nodes

n8n categorizes nodes into four structural archetypes:

```text
                             +-------------------+
                             |     n8n Nodes     |
                             +-------------------+
                                       |
        +------------------+-----------+-----------+------------------+
        |                  |                       |                  |
+-------v-------+  +-------v-------+       +-------v-------+  +-------v-------+
| Trigger Nodes |  | Action Nodes  |       | Routing/Logic |  | Code/Transform|
+---------------+  +---------------+       +---------------+  +---------------+
| Inbound start |  | Outbound APIs |       | Flow control  |  | JS / Python   |
| Webhook, Form |  | Slack, Postgres|      | If, Switch    |  | Data cleaning |
| Cron, Schedule|  | S3, OpenAI    |       | Filter, Loop  |  | Schema mapping|
+---------------+  +---------------+       +---------------+  +---------------+
```

---

## 1. Trigger Nodes
Trigger nodes initiate workflow execution. A workflow can have multiple triggers, but each run is catalyzed by a single trigger event.
- **Polling / Scheduled**: Triggers on a timer or interval (e.g., `Schedule Trigger` running every morning at 08:00 AM).
- **Inbound Event-Driven**: Listens on an HTTP endpoint (e.g., `Webhook`, `n8n Form Trigger`).
- **App Triggers**: Subscribes to events from SaaS ecosystems via long-polling or registered webhooks (e.g., `GitHub Trigger: On Pull Request`, `Slack Trigger: On Channel Message`).

---

## 2. Action Nodes (SaaS & Databases)
Action nodes interact with third-party software, internal databases, or cloud infrastructure.
- **Database Nodes**: `PostgreSQL`, `MySQL`, `Redis`, `MongoDB`, `Snowflake`. Perform CRUD queries, inserts, and transaction rollbacks.
- **Communication & CRM**: `Slack`, `Gmail`, `HubSpot`, `Salesforce`, `Notion`. Send notifications, update CRM leads, and manage records.
- **AI & LLMs**: `OpenAI`, `Anthropic`, `LangChain Agent`, `Weaviate Vector Store`. Generate embeddings, query LLMs, and structure AI prompts.

---

## 3. Flow & Logic Nodes
Control execution branching and item filtering:
- **If Node**: Evaluates boolean conditions and splits the item flow into `True` and `False` output branches.
- **Filter Node**: Evaluates condition sets and selectively discards items that fail conditions, letting surviving items continue down the pipeline.
- **Switch Node**: Multi-way routing based on string equality, regex rules, or numeric ranges.
- **Loop / Split In Batches**: Chunks large arrays into batches to respect third-party API rate limits.

---

## 4. Transformation & Custom Code Nodes
Manipulates JSON payloads, structural schemas, and binary files:
- **Code Node**: Execute native JavaScript or Python in a sandboxed runtime to clean, reformat, and calculate values.
- **Edit Fields (Set)**: Renames, adds, or removes attributes from items without writing scripts.
- **Extract from File / Convert to File**: Handles binary-to-JSON parsing (CSV, XLSX, PDF, JSON) and reciprocal JSON-to-file conversions.
