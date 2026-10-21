# Enterprise ETL & AI Automation with n8n and Python

An end-to-end reference repository demonstrating automated Extract, Transform, Load (ETL) data engineering pipelines using both low-code orchestration (**n8n**) and code-first scripting (**Python / Pandas**). 

This project covers core workflow automation principles—from canvas navigation and node taxonomy to webhook ingress, schema sanitization, conditional routing, and automated file artifact generation.

---

## 📑 Table of Contents

- [Architectural Overview](#-architectural-overview)
- [Repository Structure](#-repository-structure)
- [Core Concepts & Architecture](#-core-concepts--architecture)
  - [n8n Editor Tour](#1-n8n-editor-tour)
  - [What is a Node? & Node Taxonomy](#2-what-is-a-node--node-taxonomy)
  - [HTTP Request vs. Webhook Node](#3-http-request-vs-webhook-node)
- [ETL Pipeline Implementation](#-etl-pipeline-implementation)
  - [Pipeline A: n8n Workflow](#pipeline-a-n8n-workflow-native-orchestration)
  - [Pipeline B: Python Script](#pipeline-b-python-script-code-first)
- [Data Transformation Rules](#-data-transformation-rules)
- [Quick Start & Setup](#-quick-start--setup)
  - [Importing into n8n](#importing-into-n8n)
  - [Running the Python Pipeline](#running-the-python-pipeline)
- [License](#-license)

---

## 🏛 Architectural Overview

The ETL pipeline accepts tabular student enrollment records, ingests the binary payload, cleans/normalizes attributes via custom logic, filters entries based on operational criteria, and outputs an export-ready binary report.

```text
[Data Ingress]                  [Extraction]                  [Transformation]                 [Routing / Load]
┌──────────────────┐           ┌──────────────────┐          ┌──────────────────────┐         ┌──────────────────────┐
│  Form Trigger /  │ ────────► │ Extract from File│ ───────► │ JavaScript / Pandas  │ ──────► │ Filter & Export Node │
│  Inbound Webhook │  (Binary) │   (CSV -> JSON)  │  (Items) │  Sanitization Engine │ (Items) │   (CSV File Output)  │
└──────────────────┘           └──────────────────┘          └──────────────────────┘         └──────────────────────┘
```

---

## 📂 Repository Structure

```text
.
├── README.md                           # Main architecture and documentation guide
├── docs/
│   ├── 01-n8n-editor-tour.md           # Interface anatomy, canvas, execution inspector
│   ├── 02-nodes-and-node-types.md      # Node taxonomies (Triggers, Actions, Logic)
│   ├── 03-node-types-full-overview.md  # Deep dive into data streaming, items, & binary mode
│   ├── 04-http-vs-webhook-node.md      # Inbound push vs. outbound pull architectural guide
│   ├── 05-etl-ai-automation-n8n.md     # In-depth n8n pipeline breakdown & JS code logic
│   ├── 06-etl-ai-automation-python.md  # Vectorized Pandas & regular expressions comparison
│   └── 07-etl-ai-automation-demo.md    # End-to-end execution walkthrough and verification
├── workflows/
│   └── student-etl-pipeline.json       # Production-ready n8n workflow export
├── scripts/
│   ├── etl_pipeline.py                 # Pure Python implementation of the ETL logic
│   └── requirements.txt                # Python environment dependencies
└── data/
    └── sample-students.csv             # Reference raw dataset for testing
```

---

## 🧠 Core Concepts & Architecture

### 1. n8n Editor Tour
- **Canvas Interface**: Vector-based infinite workflow canvas supporting drag-and-drop orchestration, branch splitting, and sub-workflow routing.
- **Node Configuration**: Dedicated parameters pane providing direct JSON path mapping, JavaScript expression toggling (`={{ $json.property }}`), and binary data viewers.
- **Execution History & Pin Data**: Allows freezing deterministic test states (`pinData`) at any stage to iterate on downstream transformations without re-running trigger events.

### 2. What is a Node? & Node Taxonomy
In n8n, a **Node** is a modular computational step that consumes an array of JSON objects (and optional binary payloads), applies business or network logic, and outputs transformed items to downstream connections.

| Node Class | Purpose | Examples |
| :--- | :--- | :--- |
| **Trigger Nodes** | Initiate workflow execution upon external or temporal events. | `Webhook`, `Form Trigger`, `Schedule Trigger` |
| **Transform Nodes** | Parse, reshape, calculate, or format data structures. | `Code (JS/Python)`, `Extract from File`, `Convert to File` |
| **Logic Nodes** | Route execution branches conditionally or merge concurrent data streams. | `Filter`, `If`, `Switch`, `Merge` |
| **Action Nodes** | Perform outbound operations or interact with external APIs/Databases. | `HTTP Request`, `Postgres`, `Slack`, `Google Sheets` |

### 3. HTTP Request vs. Webhook Node

Understanding the communication protocol difference is crucial for designing event-driven systems:

```text
           [Inbound Event: Push]                              [Outbound Request: Pull]
      Client ────────────────► [Webhook Node]          [HTTP Request Node] ────────────────► External API
 (Listens passively for external calls)            (Actively initiates network requests)
```

| Dimension | Webhook Node (`n8n-nodes-base.webhook`) | HTTP Request Node (`n8n-nodes-base.httpRequest`) |
| :--- | :--- | :--- |
| **Direction** | **Inbound** (Ingress / Passive Receiver) | **Outbound** (Egress / Active Requester) |
| **Trigger Role** | Acts as the entry point / workflow trigger | Acts as an intermediary action step |
| **Networking** | Requires public URL exposure (e.g., tunnel/domain) | Requires outbound network egress / DNS resolution |
| **Execution** | Fires instantaneously on receipt of HTTP payload | Executes synchronously when upstream node passes control |

---

## ⚡ ETL Pipeline Implementation

### Pipeline A: n8n Workflow (Native Orchestration)
The n8n workflow file is located at `workflows/student-etl-pipeline.json`. It defines an end-to-end file processing engine:

1. **On form submission (`formTrigger`)**: Displays a web form to ingest tabular `.csv` student files as binary uploads.
2. **Extract from File (`extractFromFile`)**: Ingests the binary stream and parses rows into discrete n8n JSON item streams (`{ "Student_ID": "...", "Name": "..." }`).
3. **Code in JavaScript (`code`)**: Performs procedural data cleansing, regular expression evaluations, title casing, and normalization.
4. **Filter (`filter`)**: Enforces validation gating:
   $$\text{Filter Condition} = (\text{is\_valid\_email} == \text{true}) \lor (\text{Fee\_Paid} == \text{"Yes"})$$
5. **Convert to File (`convertToFile`)**: Reconstructs valid, sanitized items into an exportable CSV file.

### Pipeline B: Python Script (Code-First)
The standalone script `scripts/etl_pipeline.py` mirrors the n8n pipeline logic using vectorized **Pandas**:
- Ingests raw CSV data into memory via `pd.read_csv()`.
- Validates emails using regex: `^[^@\s]+@[^@\s]+\.[^@\s]+$`.
- Cleans and normalizes course strings and phone number structures.
- Writes the cleaned dataset to `data/cleaned_students.csv`.

---

## 🛠 Data Transformation Rules

Both the JavaScript node and Python scripts execute the following data hygiene standards:

1. **Name & City Fields**: Converted to Title Case; missing cities default to `"Not Provided"`.
2. **Course Standardization**:
   - `python` $\rightarrow$ `Python`
   - `ml` or `machine learning` $\rightarrow$ `Machine Learning`
3. **Phone Number Verification**: Checks for exact 10-digit formats; invalid lengths are flagged as `"Invalid/Missing"`.
4. **Email Address RFC Validation**: Evaluated against standard regex patterns, setting a boolean flag `is_valid_email`.
5. **Fee Status Normalization**: Case-insensitive check resolving strictly to `"Yes"` or `"No"`.

---

## 🚀 Quick Start & Setup

### Importing into n8n
1. Open your n8n workspace canvas.
2. Click **Workflow Settings** (or the top-right menu `...`) and select **Import from File**.
3. Choose `workflows/student-etl-pipeline.json`.
4. Save and toggle the workflow or click **Test workflow**.
5. Upload `data/sample-students.csv` into the form trigger to execute the end-to-end run.

### Running the Python Pipeline
```bash
# Clone the repository
git clone https://github.com/cvijayvinoth/n8n-etl-ai-automation.git
cd cvijayvinoth

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r scripts/requirements.txt

# Execute ETL script
python scripts/etl_pipeline.py
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
```

This `README.md` provides complete repository documentation, clarifies all key conceptual topics without referencing internal assignments, and gives you a professional front page for your GitHub repository.

<FollowUp label="Would you like a sample CI/CD GitHub Actions workflow to run automated tests on the Python ETL pipeline?" query="Generate a GitHub Actions CI workflow to test the Python ETL pipeline with pytest."/>
