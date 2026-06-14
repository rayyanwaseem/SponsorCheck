from typing import List, Dict, Any
from sponsorcheck.domain.models import SocCandidate

def validate_soc_decision(decision_dict: Dict[str, Any], candidates: List[SocCandidate]) -> bool:
    best_code = decision_dict.get("best_occupation_code")
    if not best_code:
        return False
        
    candidate_codes = [c.occupation_code for c in candidates]
    if best_code not in candidate_codes:
        return False
        
    return True
