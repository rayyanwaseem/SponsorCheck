from sponsorcheck.domain.models import SocRecord
from sponsorcheck.domain.salary_models import ApplicantFacts, RouteResult
from sponsorcheck.domain.route_models import RouteStatus
from sponsorcheck.salary.base import RouteEvaluator
from sponsorcheck.data.salary_rule_store import get_salary_rule_store

class MediumSkilledGate(RouteEvaluator):
    route_id = "medium_skilled_gate"
    route_label = "Medium Skilled Verification"

    def evaluate(self, record: SocRecord, facts: ApplicantFacts) -> RouteResult:
        # Check if the code is medium skilled
        eligibility = record.eligibility
        if not eligibility:
            return RouteResult(
                route_id=self.route_id,
                route_label=self.route_label,
                status=RouteStatus.SOURCE_CHECK_REQUIRED,
                blocking_reasons=["Eligibility data missing for this code."]
            )
            
        if isinstance(eligibility, str):
            is_medium = "not eligible for normal skilled worker" in eligibility.lower() or "medium skilled" in eligibility.lower()
        else:
            is_medium = eligibility.get("is_medium_skilled", False)
            
        if not is_medium:
            return RouteResult(
                route_id=self.route_id,
                route_label=self.route_label,
                status=RouteStatus.NOT_APPLICABLE,
                calculation_steps=["Role is not classed as medium-skilled, gate check passed by default."]
            )
            
        missing_facts = []
        if facts.application_type is None: missing_facts.append("application_type")
        if facts.work_region is None: missing_facts.append("work_region")
        if facts.is_extension is None: missing_facts.append("is_extension")
        if facts.is_healthcare_or_education_role is None: missing_facts.append("is_healthcare_or_education_role")
        
        if missing_facts:
            return RouteResult(
                route_id=self.route_id,
                route_label=self.route_label,
                status=RouteStatus.NEEDS_MORE_INFORMATION,
                missing_facts=missing_facts,
                calculation_steps=["Code is medium-skilled. Checking for valid pathways (ISL, TSL, Health/Ed, Extension)..."],
                govuk_signposts=["Medium skilled roles are only eligible under specific conditions like Immigration Salary List, Temporary Shortage List, or specific transitional arrangements."]
            )
            
        # Simplified mock logic for the gate
        # If they are on a lower route list or it's an extension, they might pass
        passed_gate = facts.is_extension or facts.is_healthcare_or_education_role
        
        status = RouteStatus.APPLICABLE if passed_gate else RouteStatus.NOT_APPLICABLE
        
        rate_val = lower_rate.get("annual")
        if rate_val is None:
            rate_val = 0.0
            
        basis = lower_rate.get("basis_weekly_hours", 37.5)
        calculation_steps = ["Code is medium-skilled.", "Checked ISL/TSL/Extension pathways.", f"Lower going rate is £{rate_val:,.2f} based on {basis} hours/week."]

        return RouteResult(
            route_id=self.route_id,
            route_label=self.route_label,
            status=status,
            calculation_steps=calculation_steps,
            blocking_reasons=[] if passed_gate else ["Does not meet any allowed pathway for medium-skilled roles."]
        )
