from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict

class SocRecord(BaseModel):
    occupation_code: str
    job_type: str
    related_job_titles: List[str] = Field(default_factory=list)
    eligibility: Any = None
    rates: Any = None
    special_salary_routes: List[str] = Field(default_factory=list)
    search_text: Optional[str] = None
    source_references: List[str] = Field(default_factory=list)

class SocCandidate(BaseModel):
    occupation_code: str
    job_type: str
    score: float
    matched_terms: List[str] = Field(default_factory=list)
    eligibility: Any = None
    rates: Any = None
    special_salary_routes: List[str] = Field(default_factory=list)

class SocDecision(BaseModel):
    best_occupation_code: str
    confidence: float
    reasoning: str
    evidence_from_jd: List[str] = Field(default_factory=list)
    alternative_codes: List[str] = Field(default_factory=list)
    warning_flags: List[str] = Field(default_factory=list)
    classification_method: str = "unknown"

from .salary_models import SalaryEvaluation

class ClassificationResponse(BaseModel):
    decision: SocDecision
    selected_soc_record: SocRecord
    candidates: List[SocCandidate] = Field(default_factory=list)
    salary_evaluation: SalaryEvaluation
    disclaimer: str
    report_id: str
