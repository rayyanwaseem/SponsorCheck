import uuid
from fastapi import APIRouter, HTTPException
from sponsorcheck.api.schemas import ClassifyRequest
from sponsorcheck.domain.models import ClassificationResponse
from sponsorcheck.domain.salary_models import ApplicantFacts
from sponsorcheck.classification.retriever import get_retriever
from sponsorcheck.classification.llm_classifier import classify_with_llm
from sponsorcheck.classification.rule_based_classifier import classify_rule_based
from sponsorcheck.salary.evaluator import evaluate_salary_routes
from sponsorcheck.data.soc_store import get_soc_store
from sponsorcheck.reports.store import get_report_store

router = APIRouter()

@router.post("/classify", response_model=ClassificationResponse)
async def classify_job(request: ClassifyRequest):
    retriever = get_retriever()
    candidates = retriever.retrieve(request.job_description, request.top_k)
    
    if not candidates:
        raise HTTPException(status_code=400, detail="Could not find any SOC candidates for this job description.")
        
    if request.provider == "rule_based":
        decision = classify_rule_based(request.job_description, candidates)
    else:
        decision = await classify_with_llm(
            base_url=request.llm_base_url,
            api_key=request.llm_api_key,
            model=request.llm_model,
            job_description=request.job_description,
            candidates=candidates
        )
        
    store = get_soc_store()
    selected_record = store.get_by_code(decision.best_occupation_code)
    
    if not selected_record:
        selected_record = store.get_by_code(candidates[0].occupation_code)
        decision.best_occupation_code = candidates[0].occupation_code
    
    facts = request.facts or ApplicantFacts()
    salary_eval = evaluate_salary_routes(selected_record, facts)
    
    report_id = str(uuid.uuid4())
    
    response_data = ClassificationResponse(
        decision=decision,
        selected_soc_record=selected_record,
        candidates=candidates,
        salary_evaluation=salary_eval,
        disclaimer="SponsorCheck gives a structured indication only and does not replace GOV.UK guidance, legal advice or sponsor compliance checks.",
        report_id=report_id
    )
    
    # Save the data so a report can be generated
    get_report_store().save(report_id, response_data)
    
    return response_data
