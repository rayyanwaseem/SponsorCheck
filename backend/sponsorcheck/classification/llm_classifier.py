from typing import List
from sponsorcheck.domain.models import SocCandidate, SocDecision
from sponsorcheck.llm.openai_compatible import call_openai_compatible_api
from sponsorcheck.classification.json_utils import extract_json_from_text
from sponsorcheck.classification.validation import validate_soc_decision
from sponsorcheck.classification.rule_based_classifier import classify_rule_based

async def classify_with_llm(
    base_url: str,
    api_key: str,
    model: str,
    job_description: str,
    candidates: List[SocCandidate]
) -> SocDecision:
    
    if not candidates:
        raise ValueError("No candidates provided for classification")

    candidates_dict_list = [{"occupation_code": c.occupation_code, "job_type": c.job_type} for c in candidates]
    
    last_error = "Validation failed or unknown error"
    
    for attempt in range(2):
        try:
            response_text = await call_openai_compatible_api(
                base_url=base_url,
                api_key=api_key,
                model=model,
                job_description=job_description,
                candidates=candidates_dict_list
            )
            
            decision_dict = extract_json_from_text(response_text)
            
            if validate_soc_decision(decision_dict, candidates):
                decision_dict["classification_method"] = "openai_compatible"
                return SocDecision(**decision_dict)
            else:
                last_error = "AI returned invalid JSON or a made-up SOC code."
                
        except Exception as e:
            last_error = f"{type(e).__name__}: {str(e)}"
            if attempt == 1:
                # Log exception properly in real app, then fallback
                pass
                
    # Fallback if both attempts fail or validation fails
    decision = classify_rule_based(job_description, candidates)
    decision.warning_flags.append(f"AI Classification failed, fell back to rule-based. Error: {last_error}")
    return decision
