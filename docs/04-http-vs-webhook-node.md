# HTTP Request Node vs. Webhook Node

Both nodes deal with HTTP protocols, but they serve fundamentally opposite roles in distributed network architectures.

---

## High-Level Comparison

| Feature | Webhook Node | HTTP Request Node |
| :--- | :--- | :--- |
| **Direction** | **Inbound** (Passive listener) | **Outbound** (Active initiator) |
| **Role** | Receiver / Trigger | Client / Action |
| **Initiator** | External system calls n8n | n8n calls external API |
| **Execution Trigger** | Yes (workflow begins here) | No (runs inside a sequence) |
| **Network Requirement** | Requires public URL / Ingress | Needs outbound internet access |
| **Typical Use Cases** | GitHub webhooks, Stripe events, form submissions | Querying REST APIs, calling microservices |

---

## 1. Webhook Node (Inbound Event-Driven)

The Webhook node binds a unique URL endpoint to n8n, transforming incoming POST, GET, PUT, or DELETE payloads into an actionable workflow event.

```text
External System (Stripe, GitHub, Custom App)
                    │
                    ▼ HTTP POST https://n8n.domain.com/webhook/test-event
          +───────────────────+
          |   Webhook Node    | -> Captures headers, body, query parameters
          +───────────────────+
                    │
                    ▼ Emits parsed JSON to workflow
```

### URLs: Test vs. Production
- **Test Webhook URL** (`/webhook-test/...`): Listens for a single payload when you click **Listen for Test Event** in the canvas editor.
- **Production Webhook URL** (`/webhook/...`): Only active when the workflow is toggled to **Active**. Runs reliably in the background without UI interaction.

---

## 2. HTTP Request Node (Outbound Polling/Calls)

The HTTP Request node is an outbound REST client capable of making requests to any external HTTP/HTTPS service.

```text
       +────────────────────────+
       |   HTTP Request Node    |
       +────────────────────────+
                    │
                    ▼ GET / POST / PUT / PATCH / DELETE
           External REST API (OpenAI, GitHub API, Database Microservice)
```

### Key Configurations
- **Authentication**: Supports Pre-built OAuth2, Bearer Token, Basic Auth, and Custom Header signing.
- **Pagination Handling**: Can automatically iterate through paginated responses (cursor-based, offset/limit, link headers).
- **Body Content**: Supports `JSON`, `Form-Data`, `Raw`, and `Binary` uploads.

---

## When to Use Which?

```text
Does an external system need to notify n8n when something happens?
  ├── YES -> Use Webhook Node (Event-driven, instantaneous, zero idle resource waste)
  └── NO  -> Do you need to fetch, query, or mutate an external API?
               └── YES -> Use HTTP Request Node
```
