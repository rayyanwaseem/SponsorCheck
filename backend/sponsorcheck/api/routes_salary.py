from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sponsorcheck.domain.salary_models import ApplicantFacts, SalaryEvaluation
from sponsorcheck.data.soc_store import get_soc_store
from sponsorcheck.salary.evaluator import evaluate_salary_routes

router = APIRouter()

class SalaryEvaluateRequest(BaseModel):
    occupation_code: str
    facts: ApplicantFacts

@router.post("/evaluate", response_model=SalaryEvaluation)
async def evaluate_salary(request: SalaryEvaluateRequest):
    store = get_soc_store()
    record = store.get_by_code(request.occupation_code)
    
    if not record:
        raise HTTPException(status_code=404, detail=f"SOC Code {request.occupation_code} not found.")
        
    evaluation = evaluate_salary_routes(record, request.facts)
    return evaluation
