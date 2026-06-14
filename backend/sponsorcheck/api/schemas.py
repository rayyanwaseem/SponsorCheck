from pydantic import BaseModel
from typing import Optional
from sponsorcheck.domain.salary_models import ApplicantFacts

class ClassifyRequest(BaseModel):
    job_description: str
    provider: str = "openai_compatible"
    llm_base_url: Optional[str] = "http://localhost:11434/v1"
    llm_api_key: Optional[str] = "ollama"
    llm_model: Optional[str] = "gemma4:e2b"
    top_k: int = 15
    facts: Optional[ApplicantFacts] = None
