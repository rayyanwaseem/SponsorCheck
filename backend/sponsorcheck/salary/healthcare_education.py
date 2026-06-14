from sponsorcheck.domain.models import SocRecord
from sponsorcheck.domain.salary_models import ApplicantFacts, RouteResult
from sponsorcheck.domain.route_models import RouteStatus
from sponsorcheck.salary.base import RouteEvaluator

class HealthcareEducation(RouteEvaluator):
    route_id = "healthcare_education"
    route_label = "Healthcare and Education National Pay Scales"

    def evaluate(self, record: SocRecord, facts: ApplicantFacts) -> RouteResult:
        if "national_pay_scales" not in record.special_salary_routes:
            return RouteResult(
                route_id=self.route_id,
                route_label=self.route_label,
                status=RouteStatus.NOT_APPLICABLE,
                calculation_steps=["This code is not subject to national pay scales."]
            )
            
        missing = []
        if facts.uses_national_pay_scale is None: missing.append("uses_national_pay_scale")
        
        if missing:
             return RouteResult(
                route_id=self.route_id,
                route_label=self.route_label,
                status=RouteStatus.NEEDS_MORE_INFORMATION,
                missing_facts=missing
            )
            
        if not facts.uses_national_pay_scale:
            return RouteResult(
                route_id=self.route_id,
                route_label=self.route_label,
                status=RouteStatus.NOT_APPLICABLE,
                calculation_steps=["Not using national pay scales."]
            )
            
        if facts.national_pay_scale_details is None:
             return RouteResult(
                route_id=self.route_id,
                route_label=self.route_label,
                status=RouteStatus.SOURCE_CHECK_REQUIRED,
                missing_facts=["national_pay_scale_details"],
                govuk_signposts=["Please verify the exact pay band and nation."]
            )
            
        return RouteResult(
            route_id=self.route_id,
            route_label=self.route_label,
            status=RouteStatus.APPLICABLE,
            calculation_steps=["Checked national pay scale details."]
        )
