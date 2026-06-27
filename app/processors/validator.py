from typing import List
import pandas as pd


def detect_income_mismatch(json_data: dict, csv_data: pd.DataFrame) -> List[str]:
    findings = []

    declared_income = json_data.get("income", 0)
    actual_deposits = csv_data["deposit"].sum() if "deposit" in csv_data else 0

    if actual_deposits < declared_income * 0.6:
        findings.append(
            f"Income mismatch: declared={declared_income}, actual={actual_deposits}"
        )

    return findings