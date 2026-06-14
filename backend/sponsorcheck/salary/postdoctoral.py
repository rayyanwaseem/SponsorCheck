from sponsorcheck.domain.models import SocRecord
from sponsorcheck.domain.salary_models import ApplicantFacts, RouteResult
from sponsorcheck.domain.route_models import RouteStatus
from sponsorcheck.salary.base import RouteEvaluator
from sponsorcheck.data.salary_rule_store import get_salary_rule_store

class Postdoctoral(RouteEvaluator):
    route_id = "postdoctoral"
    route_label = "Postdoctoral"

    def evaluate(self, record: SocRecord, facts: ApplicantFacts) -> RouteResult:
        rules = get_salary_rule_store().get_rules()
        postdoc_codes = rules.get("special_sets", {}).get("postdoctoral_codes", [])
        
        if record.occupation_code not in postdoc_codes:
            return RouteResult(
                route_id=self.route_id,
                route_label=self.route_label,
                status=RouteStatus.NOT_APPLICABLE,
                calculation_steps=["Role is not in the allowed postdoctoral SOC codes list."]
            )
            
        if facts.is_postdoctoral_role is None:
            return RouteResult(
                route_id=self.route_id,
                route_label=self.route_label,
                status=RouteStatus.NEEDS_MORE_INFORMATION,
                missing_facts=["is_postdoctoral_role"],
                govuk_signposts=["Need to confirm if the role is genuinely postdoctoral."]
            )
            
        if not facts.is_postdoctoral_role:
             return RouteResult(
                route_id=self.route_id,
                route_label=self.route_label,
                status=RouteStatus.NOT_APPLICABLE,
                calculation_steps=["User confirmed role is not postdoctoral."]
            )
            
        # Simplified calculation for postdoctoral
        return RouteResult(
            route_id=self.route_id,
            route_label=self.route_label,
            status=RouteStatus.APPLICABLE,
            calculation_steps=["Role is postdoctoral and in permitted SOC codes."]
        )
