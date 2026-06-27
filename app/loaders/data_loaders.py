from pypdf import PdfReader
import pandas as pd
import json


def load_pdf(path: str) -> str:
    reader = PdfReader(path)
    return " ".join([page.extract_text() or "" for page in reader.pages])


def load_json(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)