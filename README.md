# 🏦 Automated Financial Auditor Agent

### FinTech Compliance Pipeline (LLM + LangChain + Structured Validation)

---

## 📌 Overview

This project implements a **production-style AI auditing pipeline** designed for highly regulated financial environments.

It simulates a real-world compliance system used by fintech companies to **analyze credit applications**, detect inconsistencies, and generate **traceable, structured audit reports**.

The system enforces **strict output schemas, deterministic AI behavior, and full observability**, ensuring that every decision is explainable and auditable.

---

## 🎯 Objective

To design and implement a **compliance-safe AI pipeline** that:

* Processes multi-format financial data (PDF, JSON, CSV)
* Detects hidden financial risks (e.g., income discrepancies)
* Produces **strictly structured outputs**
* Maintains **full traceability and auditability**
* Adheres to **enterprise-grade LLM constraints**

---

## 🧠 Core Design Principle

> “In regulated environments, AI must adapt to the system — not the other way around.”

This project enforces:

* Deterministic outputs (`temperature = 0`)
* Schema validation using **Pydantic**
* Controlled reasoning scope
* Explicit rule-based validation + LLM reasoning

---

## 🏗️ Architecture

The system follows a **modular, Clean Architecture-inspired design**:

```
app/
├── loaders/        # Multi-format data ingestion (PDF, JSON, CSV)
├── processors/     # Business rules & validation logic
├── chains/         # LangChain LLM pipelines (LCEL)
├── schemas/        # Structured output validation (Pydantic)
├── utils/          # Config, logging, environment setup
```

### 🔄 Data Flow

```
Raw Data → Loaders → Validation → LLM Chain → Structured Output → Storage
```

---

## ⚙️ Tech Stack

| Layer             | Technology       |
| ----------------- | ---------------- |
| LLM Orchestration | LangChain (LCEL) |
| Model Provider    | OpenAI API       |
| Data Processing   | Pandas, PyPDF    |
| Validation        | Pydantic         |
| Observability     | LangSmith        |
| Language          | Python 3.10+     |

---

## 📥 Input Data Pipeline

Each client dossier contains:

* 📄 **PDF** → Credit bureau history
* 🧾 **JSON** → User-declared financial profile
* 📊 **CSV** → Banking transaction history

---

## 🧠 Risk Detection Logic

The system detects critical compliance risks such as:

* Income mismatch:

  * Declared income (JSON)
  * Actual deposits (CSV)

If discrepancies exceed threshold → flagged as **Non-Compliant**

---

## 📤 Output Schema (STRICT)

All outputs are validated against a Pydantic schema:

```json
{
  "overall_compliance_status": "Compliant | Non-Compliant",
  "findings_count": 0,
  "executive_summary": "Max 300 characters"
}
```

### 🔒 Guarantees

* No unstructured LLM output
* Schema-enforced responses
* Deterministic behavior

---

## 🔍 Observability (LangSmith)

The system integrates **LangSmith tracing** for full auditability:

* Trace execution flow
* LLM call logs
* Token usage
* Latency metrics
* Error tracking

---

## 📊 Logging

A persistent log file is generated:

```
logs/langchain_demo.log
```

Tracks:

* Data processing steps
* Client-level execution
* Errors and exceptions

---

## 🚀 Installation & Setup

### 1. Clone repository

```bash
git clone https://github.com/your-username/fintech-compliance-auditor.git
cd fintech-compliance-auditor
```

---

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure environment variables

Create `.env`:

```env
OPENAI_API_KEY=your_openai_key
LANGCHAIN_API_KEY=your_langsmith_key
```

---

### 5. Run the pipeline

```bash
python main.py
```

---

## 📁 Output

Results are stored in:

```
output/results.json
```

Each entry contains a validated audit result.

---

## 🧪 Example Execution

```
Processing client 001...
✔ Income mismatch detected
✔ LLM evaluation completed
✔ Structured output saved
```

---

## 📦 Deliverables

* ✅ Full pipeline source code
* ✅ Structured audit output (JSON)
* ✅ Log file (execution trace)
* ✅ LangSmith dashboard (telemetry)

---

## 🤖 AI Usage Strategy

This project leverages AI under strict control:

* LLM used for **reasoning, not decision authority**
* Rule-based validation handles critical checks
* Outputs validated via schema enforcement

---

## 🔐 Compliance Considerations

* Deterministic LLM configuration
* Explicit validation rules
* No hallucination-prone free text
* Full traceability for audits

---

## 🚀 Future Improvements

* Advanced fraud detection models
* Multi-client batch processing (100+ dossiers)
* Real-time streaming audits
* PostgreSQL integration
* Docker deployment
* Role-based compliance dashboards

---

## 🧠 Key Learnings

* How to design **LLM systems for regulated industries**
* Combining **rule-based + AI reasoning**
* Enforcing **structured outputs**
* Building **observable AI pipelines**

---

## 📄 License

MIT License

---

## ⭐ Final Note

This project demonstrates how AI can be safely integrated into high-risk financial systems by **prioritizing control, structure, and observability over creativity**.
