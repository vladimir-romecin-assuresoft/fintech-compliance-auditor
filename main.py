import os
import json
import logging
from typing import List
from datetime import datetime

import pandas as pd
from pypdf import PdfReader
from pydantic import BaseModel, Field
from typing import Literal

from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate


# =========================
# 🔐 ENV CONFIG (LangSmith)
# =========================
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "YOUR_LANGSMITH_KEY"
os.environ["LANGCHAIN_PROJECT"] = "FinTech_Compliance_Project"

os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"


# =========================
# 🧾 LOGGING SETUP
# =========================
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/langchain_demo.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# =========================
# 📦 PYDANTIC SCHEMA
# =========================
class AuditResult(BaseModel):
    overall_compliance_status: Literal["Compliant", "Non-Compliant"]
    findings_count: int
    executive_summary: str = Field(max_length=300)


# =========================
# 📥 DATA LOADERS
# =========================
def load_pdf(path: str) -> str:
    reader = PdfReader(path)
    return " ".join([page.extract_text() or "" for page in reader.pages])


def load_json(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


# =========================
# 🧠 BUSINESS VALIDATION
# =========================
def detect_income_mismatch(json_data: dict, csv_data: pd.DataFrame) -> List[str]:
    findings = []

    declared_income = json_data.get("income", 0)
    actual_deposits = csv_data["deposit"].sum() if "deposit" in csv_data else 0

    if actual_deposits < declared_income * 0.6:
        findings.append(
            f"Income mismatch: declared={declared_income}, actual={actual_deposits}"
        )

    return findings


# =========================
# 🤖 LLM CHAIN SETUP
# =========================
def create_llm_chain():
    llm = ChatOpenAI(temperature=0)

    parser = PydanticOutputParser(pydantic_object=AuditResult)

    prompt = PromptTemplate(
        template="""
You are a financial compliance auditor.

Analyze the following data:

PDF DATA:
{pdf_data}

DECLARED PROFILE (JSON):
{json_data}

TRANSACTIONS (CSV SUMMARY):
{csv_summary}

DETECTED FINDINGS:
{findings}

Rules:
- If any findings exist → Non-Compliant
- Otherwise → Compliant
- Keep executive summary under 300 characters
- Be precise and deterministic

{format_instructions}
""",
        input_variables=["pdf_data", "json_data", "csv_summary", "findings"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    return prompt | llm | parser


# =========================
# 🔄 PROCESS ONE CLIENT
# =========================
def process_client(client_id: str, pdf_path: str, json_path: str, csv_path: str, chain):
    logging.info(f"Processing client {client_id}")

    try:
        pdf_data = load_pdf(pdf_path)
        json_data = load_json(json_path)
        csv_data = load_csv(csv_path)

        findings = detect_income_mismatch(json_data, csv_data)

        csv_summary = {
            "total_deposits": float(csv_data["deposit"].sum()) if "deposit" in csv_data else 0
        }

        result = chain.invoke({
            "pdf_data": pdf_data[:1000],  # limit text size
            "json_data": json.dumps(json_data),
            "csv_summary": json.dumps(csv_summary),
            "findings": findings
        })

        logging.info(f"Client {client_id} processed successfully")

        return result.dict()

    except Exception as e:
        logging.error(f"Error processing client {client_id}: {str(e)}")
        return {
            "overall_compliance_status": "Non-Compliant",
            "findings_count": 1,
            "executive_summary": "Processing error occurred."
        }


# =========================
# 🚀 MAIN PIPELINE
# =========================
def main():
    os.makedirs("output", exist_ok=True)

    chain = create_llm_chain()

    results = []

    # ⚠️ Simulación de clientes (ajusta a tu dataset real)
    clients = [
        {
            "id": "001",
            "pdf": "data/pdfs/client_001.pdf",
            "json": "data/json/client_001.json",
            "csv": "data/csv/client_001.csv",
        },
        # Añade más clientes aquí...
    ]

    for client in clients:
        result = process_client(
            client["id"],
            client["pdf"],
            client["json"],
            client["csv"],
            chain
        )

        results.append(result)

    # =========================
    # 💾 SAVE OUTPUT
    # =========================
    with open("output/results.json", "w") as f:
        json.dump(results, f, indent=4)

    print("✅ Processing complete. Results saved to output/results.json")


# =========================
# ▶️ RUN
# =========================
if __name__ == "__main__":
    main()