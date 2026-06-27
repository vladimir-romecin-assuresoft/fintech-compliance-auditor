from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate

from app.schemas.audit_schema import AuditResult


def create_audit_chain():
    llm = ChatOpenAI(temperature=0)

    parser = PydanticOutputParser(pydantic_object=AuditResult)

    prompt = PromptTemplate(
        template="""
You are a financial compliance auditor.

Analyze the following:

PDF DATA:
{pdf_data}

JSON DATA:
{json_data}

CSV SUMMARY:
{csv_summary}

FINDINGS:
{findings}

Rules:
- If findings exist → Non-Compliant
- Else → Compliant
- Keep summary under 300 chars

{format_instructions}
""",
        input_variables=["pdf_data", "json_data", "csv_summary", "findings"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    return prompt | llm | parser