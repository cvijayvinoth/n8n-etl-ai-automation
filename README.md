# AI-Powered Student Enrollment ETL Pipeline

An intelligent, event-driven ETL (Extract, Transform, Load) workflow built with **n8n**, **OpenAI**, and **JavaScript** that automatically ingests student enrollment CSV data, enriches and cleans records using AI and deterministic scripts, filters targeted student cohorts (students located in **Chennai** with **valid email addresses**), and exports the sanitized dataset into a formatted **Microsoft Excel (.xlsx)** file.

---

## 🎯 Objectives & Features

- **Extract**: Ingest raw student enrollment datasets from uploaded CSV files.
- **AI Processing**: Leverage OpenAI LLMs via the LangChain Basic LLM Chain to structure and contextualize records.
- **Data Standardization**: Strip leading/trailing whitespaces, enforce Title Case, and map synonymous course names (e.g., `ml` $\rightarrow$ `Machine Learning`).
- **Validation**: Validate email addresses using standard RFC regular expressions and verify 10-digit phone numbers.
- **Normalization**: Standardize fee payment indicators into strict boolean flags (`Yes` / `No`).
- **Targeted Filtering**: Route and isolate students located in **Chennai** with verified emails using strict boolean gating.
- **Load & Export**: Convert transformed JSON streams into production-ready Excel (`.xlsx`) spreadsheets.

---

## 🛠️ Technologies Used

| Technology | Role in Architecture |
| :--- | :--- |
| **n8n** | Workflow orchestration, event triggering, and node-based pipeline execution |
| **OpenAI (GPT-4o / GPT-4o-mini)** | Context-aware AI data parsing, entity classification, and anomaly cleanup |
| **JavaScript (ES6+)** | High-performance deterministic cleansing, normalization, and regex validation |
| **CSV** | Input raw tabular data format |
| **Excel (.xlsx)** | Structured business export format |
| **Git & GitHub** | Version control, documentation, and repository management |

---

## 🔄 Workflow Architecture

```text
+----------------+      +-------------------+      +---------------------+
| 1. CSV Upload  | ---> | 2. Extract File   | ---> | 3. Basic LLM Chain  |
| (Form Trigger) |      | (Parse Raw CSV)   |      | + OpenAI Chat Model |
+----------------+      +-------------------+      +---------------------+
                                                              |
                                                              v
+----------------+      +-------------------+      +---------------------+
| 7. Convert File| <--- |    6. IF Node     | <--- | 5. Code in JS Node  |
| (Export .xlsx) | (True)| (City=Chennai && |      | (Clean, Validate,   |
+----------------+      |   Valid Email)    |      |  Normalize Fees)    |
                        +-------------------+      +---------------------+
```

### Detailed Node Execution Flow

1. **CSV Upload (`n8n-nodes-base.formTrigger`)**
   - Web-accessible upload portal enabling end users or integrations to submit enrollment CSV files securely.
2. **Extract from File (`n8n-nodes-base.extractFromFile`)**
   - Ingests binary CSV data, parses headers, and streams row items as structured JSON payloads.
3. **Basic LLM Chain (`@n8n/n8n-nodes-langchain.chainLlm`)**
   - Directs record inputs into language model prompts to normalize anomalous fields and resolve inconsistencies.
4. **OpenAI Chat Model (`@n8n/n8n-nodes-langchain.lmChatOpenAi`)**
   - Sub-node providing OpenAI model connectivity (`gpt-4o-mini` with low temperature for deterministic parsing).
5. **Code in JavaScript (`n8n-nodes-base.code`)**
   - Deterministic sanitization layer:
     - Trims excess whitespace and formats `Name` and `City` to Title Case.
     - Maps `Course` values to unified naming conventions.
     - Runs RFC regex pattern checking against `Email` (`is_valid_email: true/false`).
     - Normalizes `Fee_Paid` inputs (`yes`, `paid`, `y`, `1` $\rightarrow$ `Yes`, else `No`).
     - Verifies telephone numeric lengths (10 digits).
6. **IF Node (`n8n-nodes-base.if`)**
   - Dual-condition logical filter (`AND` combinator):
     - `City` equals `Chennai` (case-insensitive)
     - `is_valid_email` is `true`
7. **Convert to File (`n8n-nodes-base.convertToFile`)**
   - Encodes filtered JSON data into an Excel spreadsheet (`chennai_verified_students.xlsx`).

---

## 📂 Repository Structure

```text
├── README.md
├── docs/
│   ├── workflow-architecture.md         # Detailed breakdown of nodes, parameters, and AI prompts
│   └── data-transformation-rules.md     # Cleansing formulas, regex rules, and normalizations
├── workflows/
│   └── student-enrollment-pipeline.json # n8n workflow export ready for 1-click import
├── scripts/
│   ├── etl_pipeline.py                  # Standalone Python script matching the pipeline logic
│   └── requirements.txt                 # Python dependencies (pandas, openpyxl)
└── data/
    └── sample_students.csv              # Test dataset containing raw, uncleaned records
```

---

## 🚀 Setup & Execution Guide

### 1. Import Workflow into n8n
1. Open your n8n workspace.
2. Select **Workflows > Import from File** and upload `workflows/student-enrollment-pipeline.json`.
3. Connect your **OpenAI API Key** inside credentials for the `OpenAI Chat Model` node.
4. Click **Save** and activate the workflow.

### 2. Run Python Alternative Pipeline
```bash
# Clone the repository
git clone https://github.com/cvijayvinoth/n8n-etl-ai-automation.git
cd cvijayvinoth/scripts

# Install dependencies
pip install -r requirements.txt

# Run ETL script (Filters for Chennai + Valid Email and outputs .xlsx)
python etl_pipeline.py --input ../data/sample_students.csv --output ../data/chennai_verified_students.xlsx
```

---

## 📊 Sample Input vs. Output

### Input (`sample_students.csv`)
```csv
Student_ID,Name,Email,Phone,Course,Fee_Paid,City,Enrolled_Date
STU1001,  rajesh kumar ,rajesh@gmail.com,9876543210,python,yes,chennai,10-01-2025
STU1002,Priya S,priya.s@yahoo.com,,ml,no,coimbatore,06-05-2025
STU1003,suresh b,suresh_invalid_at_gmail,9123456780,DS,paid,CHENNAI,12-02-2025
STU1004,ANITHA R,anitha@gmail.com,9000011111,machine learning,no,chennai,05-04-2025
STU1008,kavitha,kavitha99@gmail.com,9988776655,ml,yes,Chennai,15-01-2025
```

### Output (`chennai_verified_students.xlsx`)
| Student_ID | Name | Email | Phone | Course | Fee_Paid | City | Enrolled_Date | is_valid_email |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| STU1001 | Rajesh Kumar | rajesh@gmail.com | 9876543210 | Python | Yes | Chennai | 10-01-2025 | TRUE |
| STU1004 | Anitha R | anitha@gmail.com | 9000011111 | Machine Learning | No | Chennai | 05-04-2025 | TRUE |
| STU1008 | Kavitha | kavitha99@gmail.com | 9988776655 | Machine Learning | Yes | Chennai | 15-01-2025 | TRUE |

*(Note: STU1002 excluded due to City != Chennai; STU1003 excluded due to invalid email address format).*

---

## 📄 License
MIT License.
