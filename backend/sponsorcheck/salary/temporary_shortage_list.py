from sponsorcheck.domain.models import SocRecord
from sponsorcheck.domain.salary_models import ApplicantFacts, RouteResult
from sponsorcheck.domain.route_models import RouteStatus
from sponsorcheck.salary.base import RouteEvaluator

class TemporaryShortageList(RouteEvaluator):
    route_id = "temporary_shortage_list"
    route_label = "Temporary Shortage List"

    def evaluate(self, record: SocRecord, facts: ApplicantFacts) -> RouteResult:
        if "temporary_shortage_list" not in record.special_salary_routes:
            return RouteResult(
                route_id=self.route_id,
                route_label=self.route_label,
                status=RouteStatus.NOT_APPLICABLE,
                calculation_steps=["Code is not on the Temporary Shortage List."]
            )
            
        missing = []
        if facts.application_type is None: missing.append("application_type")
        if facts.work_region is None: missing.append("work_region")
        
        if missing:
            return RouteResult(
                route_id=self.route_id,
                route_label=self.route_label,
                status=RouteStatus.NEEDS_MORE_INFORMATION,
                missing_facts=missing,
                govuk_signposts=["Temporary Shortage List applies under certain conditions."]
            )
            
        return RouteResult(
            route_id=self.route_id,
            route_label=self.route_label,
            status=RouteStatus.APPLICABLE,
            calculation_steps=["Role meets TSL criteria."]
        )
