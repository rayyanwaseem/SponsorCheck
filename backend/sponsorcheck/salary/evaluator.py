from sponsorcheck.domain.models import SocRecord
from sponsorcheck.domain.salary_models import ApplicantFacts, RouteResult, SalaryEvaluation
from sponsorcheck.domain.route_models import RouteStatus

from .standard_skilled_worker import StandardSkilledWorker
from .medium_skilled_gate import MediumSkilledGate
from .immigration_salary_list import ImmigrationSalaryList
from .temporary_shortage_list import TemporaryShortageList
from .new_entrant import NewEntrant
from .phd_discount import PhdDiscount
from .postdoctoral import Postdoctoral
from .healthcare_education import HealthcareEducation
from .health_and_care_worker import HealthAndCareWorker
from .pre_2024_cos import Pre2024Cos

def evaluate_salary_routes(record: SocRecord, facts: ApplicantFacts) -> SalaryEvaluation:
    evaluators = [
        StandardSkilledWorker(),
        MediumSkilledGate(),
        ImmigrationSalaryList(),
        TemporaryShortageList(),
        NewEntrant(),
        PhdDiscount(),
        Postdoctoral(),
        HealthcareEducation(),
        HealthAndCareWorker(),
        Pre2024Cos()
    ]
    
    all_results = []
    standard_route = None
    possible_lower = []
    blocked = []
    needing_info = []
    
    for evaluator in evaluators:
        res = evaluator.evaluate(record, facts)
        all_results.append(res)
        
        if res.route_id == "standard":
            standard_route = res
            if res.status == RouteStatus.NOT_APPLICABLE or res.status == RouteStatus.SALARY_TOO_LOW:
                blocked.append(res)
            elif res.status == RouteStatus.NEEDS_MORE_INFORMATION:
                needing_info.append(res)
        else:
            if res.status == RouteStatus.APPLICABLE:
                possible_lower.append(res)
            elif res.status == RouteStatus.NOT_APPLICABLE or res.status == RouteStatus.SALARY_TOO_LOW:
                blocked.append(res)
            elif res.status == RouteStatus.NEEDS_MORE_INFORMATION or res.status == RouteStatus.SOURCE_CHECK_REQUIRED:
                needing_info.append(res)
                
    missing_questions = []
    for r in needing_info:
        missing_questions.extend(r.missing_facts)
        
    # Deduplicate missing facts
    missing_questions = list(set(missing_questions))
    
    return SalaryEvaluation(
        selected_soc_code=record.occupation_code,
        standard_route=standard_route,
        possible_lower_routes=possible_lower,
        blocked_routes=blocked,
        routes_needing_more_information=needing_info,
        all_route_results=all_results,
        missing_questions=missing_questions,
        warnings=["Salary threshold derived from current local rules JSON. Always verify on GOV.UK."]
    )
