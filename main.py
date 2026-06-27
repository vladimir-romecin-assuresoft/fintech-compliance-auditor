from app.loaders.data_loaders import load_pdf, load_json, load_csv
from app.processors.validator import detect_income_mismatch
from app.chains.audit_chain import create_audit_chain
from app.utils.logger import logger

import json
import os


def process_client(client, chain):
    logger.info(f"Processing {client['id']}")

    pdf = load_pdf(client["pdf"])
    js = load_json(client["json"])
    csv = load_csv(client["csv"])

    findings = detect_income_mismatch(js, csv)

    result = chain.invoke({
        "pdf_data": pdf[:1000],
        "json_data": json.dumps(js),
        "csv_summary": json.dumps({
            "total_deposits": float(csv["deposit"].sum()) if "deposit" in csv else 0
        }),
        "findings": findings
    })

    return result.dict()


def main():
    os.makedirs("output", exist_ok=True)

    chain = create_audit_chain()

    clients = [
        {
            "id": "001",
            "pdf": "data/pdfs/sample.pdf",
            "json": "data/json/sample.json",
            "csv": "data/csv/sample.csv",
        }
    ]

    results = []

    for client in clients:
        results.append(process_client(client, chain))

    with open("output/results.json", "w") as f:
        json.dump(results, f, indent=4)

    print("✅ Done!")


if __name__ == "__main__":
    main()