from sponsorcheck.domain.models import SocRecord
from sponsorcheck.domain.salary_models import ApplicantFacts, RouteResult
from sponsorcheck.domain.route_models import RouteStatus
from sponsorcheck.salary.base import RouteEvaluator

class Pre2024Cos(RouteEvaluator):
    route_id = "pre_2024_cos"
    route_label = "Pre-April 2024 CoS Rules"

    def evaluate(self, record: SocRecord, facts: ApplicantFacts) -> RouteResult:
        if facts.first_certificate_of_sponsorship_date is None:
             return RouteResult(
                route_id=self.route_id,
                route_label=self.route_label,
                status=RouteStatus.NEEDS_MORE_INFORMATION,
                missing_facts=["first_certificate_of_sponsorship_date"],
                govuk_signposts=["Transitional rules depend on the first CoS date."]
            )
            
        # Simplified: Check if date is before April 4 2024
        if "2024-04-04" <= facts.first_certificate_of_sponsorship_date:
            return RouteResult(
                route_id=self.route_id,
                route_label=self.route_label,
                status=RouteStatus.NOT_APPLICABLE,
                calculation_steps=["CoS date is after April 4 2024, transitional rules do not apply."]
            )
            
        return RouteResult(
            route_id=self.route_id,
            route_label=self.route_label,
            status=RouteStatus.APPLICABLE,
            calculation_steps=["Applying pre-April 2024 transitional rules..."]
        )
