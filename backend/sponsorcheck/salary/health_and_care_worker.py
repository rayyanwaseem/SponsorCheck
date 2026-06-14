from sponsorcheck.domain.models import SocRecord
from sponsorcheck.domain.salary_models import ApplicantFacts, RouteResult
from sponsorcheck.domain.route_models import RouteStatus
from sponsorcheck.salary.base import RouteEvaluator

class HealthAndCareWorker(RouteEvaluator):
    route_id = "health_and_care_worker"
    route_label = "Health and Care Worker"

    def evaluate(self, record: SocRecord, facts: ApplicantFacts) -> RouteResult:
        if "health_and_care" not in record.special_salary_routes:
             return RouteResult(
                route_id=self.route_id,
                route_label=self.route_label,
                status=RouteStatus.NOT_APPLICABLE,
                calculation_steps=["SOC code is not eligible for Health and Care Worker visa."]
            )
            
        if facts.is_health_and_care_route is None:
            return RouteResult(
                route_id=self.route_id,
                route_label=self.route_label,
                status=RouteStatus.NEEDS_MORE_INFORMATION,
                missing_facts=["is_health_and_care_route"],
                govuk_signposts=["Need confirmation if this is a Health and Care Worker visa application."]
            )
            
        if not facts.is_health_and_care_route:
             return RouteResult(
                route_id=self.route_id,
                route_label=self.route_label,
                status=RouteStatus.NOT_APPLICABLE,
                calculation_steps=["Applicant is not applying for Health and Care Worker visa."]
            )
            
        return RouteResult(
            route_id=self.route_id,
            route_label=self.route_label,
            status=RouteStatus.APPLICABLE,
            calculation_steps=["Applicant is eligible for Health and Care Worker route checks."]
        )
