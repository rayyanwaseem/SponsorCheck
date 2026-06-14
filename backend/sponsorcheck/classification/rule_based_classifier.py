from typing import List
from sponsorcheck.domain.models import SocCandidate, SocDecision

def classify_rule_based(job_description: str, candidates: List[SocCandidate]) -> SocDecision:
    if not candidates:
        raise ValueError("No candidates provided for rule-based classification")
    
    top_candidate = candidates[0]
    
    # Extract naive evidence based on matched terms if any, or just state lexical matching
    evidence = []
    if hasattr(top_candidate, 'matched_terms') and top_candidate.matched_terms:
        evidence = [f"Found term '{term}' in job description." for term in top_candidate.matched_terms]
    else:
        evidence = ["Lexical TF-IDF match with job title and duties."]
        
    reasoning = (
        f"Rule-based classification selected {top_candidate.occupation_code} "
        f"({top_candidate.job_type}) based on highest lexical similarity score "
        f"({top_candidate.score:.2f}) from local retrieval."
    )
    
    return SocDecision(
        best_occupation_code=top_candidate.occupation_code,
        confidence=top_candidate.score if top_candidate.score <= 1.0 else 0.8,
        reasoning=reasoning,
        evidence_from_jd=evidence,
        alternative_codes=[c.occupation_code for c in candidates[1:4]],
        warning_flags=["Used rule-based lexical matching method instead of an AI model. Results may be less context-aware."],
        classification_method="rule_based"
    )
