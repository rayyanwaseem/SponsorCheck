from sponsorcheck.domain.models import SocRecord
from sponsorcheck.domain.salary_models import ApplicantFacts, RouteResult
from sponsorcheck.domain.route_models import RouteStatus
from sponsorcheck.salary.base import RouteEvaluator

class PhdDiscount(RouteEvaluator):
    route_id = "phd_discount"
    route_label = "PhD Discount"

    def evaluate(self, record: SocRecord, facts: ApplicantFacts) -> RouteResult:
        if "phd_discount" not in record.special_salary_routes:
            return RouteResult(
                route_id=self.route_id,
                route_label=self.route_label,
                status=RouteStatus.NOT_APPLICABLE,
                calculation_steps=["This SOC code is not eligible for PhD discounts."]
            )
            
        missing = []
        if facts.has_relevant_phd is None: missing.append("has_relevant_phd")
        
        if missing:
            return RouteResult(
                route_id=self.route_id,
                route_label=self.route_label,
                status=RouteStatus.NEEDS_MORE_INFORMATION,
                missing_facts=missing,
                govuk_signposts=["Needs confirmation of relevant PhD."]
            )
            
        if not facts.has_relevant_phd:
            return RouteResult(
                route_id=self.route_id,
                route_label=self.route_label,
                status=RouteStatus.NOT_APPLICABLE,
                calculation_steps=["Applicant does not have a relevant PhD."]
            )
            
        missing_phd_details = []
        if facts.phd_is_stem is None: missing_phd_details.append("phd_is_stem")
        if facts.phd_is_uk_or_ecctis_confirmed is None: missing_phd_details.append("phd_is_uk_or_ecctis_confirmed")
        
        if missing_phd_details:
             return RouteResult(
                route_id=self.route_id,
                route_label=self.route_label,
                status=RouteStatus.NEEDS_MORE_INFORMATION,
                missing_facts=missing_phd_details
            )
            
        # Would implement actual rate calculations here...
        return RouteResult(
            route_id=self.route_id,
            route_label=self.route_label,
            status=RouteStatus.APPLICABLE,
            calculation_steps=["Applicant has relevant confirmed PhD."]
        )
