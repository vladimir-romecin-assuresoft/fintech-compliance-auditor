from pydantic import BaseModel, Field
from typing import Literal


class AuditResult(BaseModel):
    overall_compliance_status: Literal["Compliant", "Non-Compliant"]
    findings_count: int
    executive_summary: str = Field(max_length=300)