from sponsorcheck.domain.models import SocRecord
from sponsorcheck.domain.salary_models import ApplicantFacts, RouteResult
from sponsorcheck.domain.route_models import RouteStatus
from sponsorcheck.salary.base import RouteEvaluator
from sponsorcheck.data.salary_rule_store import get_salary_rule_store

class NewEntrant(RouteEvaluator):
    route_id = "new_entrant"
    route_label = "New Entrant"

    def evaluate(self, record: SocRecord, facts: ApplicantFacts) -> RouteResult:
        is_eligible = False
        if facts.applicant_age is not None and facts.applicant_age < 26:
            is_eligible = True
        if facts.has_student_or_graduate_visa_history:
            is_eligible = True
            
        if not is_eligible:
            missing = []
            if facts.applicant_age is None: missing.append("applicant_age")
            if facts.has_student_or_graduate_visa_history is None: missing.append("has_student_or_graduate_visa_history")
            
            if missing:
                return RouteResult(
                    route_id=self.route_id,
                    route_label=self.route_label,
                    status=RouteStatus.NEEDS_MORE_INFORMATION,
                    missing_facts=missing,
                    govuk_signposts=["New Entrant route requires checking age and visa history."]
                )
            
            return RouteResult(
                route_id=self.route_id,
                route_label=self.route_label,
                status=RouteStatus.NOT_APPLICABLE,
                calculation_steps=["Applicant does not meet new entrant criteria (age/visa history)."]
            )
            
        rules = get_salary_rule_store().get_rules().get("salary_rules", {})
        new_entrant_threshold = rules.get("discount_options", {}).get("new_entrant_standard_route", {}).get("minimum_annual_salary", 33400.0)
        
        rates = record.rates or {}
        std_rate = rates.get("standard", {}).get("annual")
        if std_rate is None:
            std_rate = 0.0
            
        basis = rates.get("standard", {}).get("basis_weekly_hours", 37.5)
        
        # New entrants get a 30% discount on going rate
        discounted_rate = std_rate * 0.7
        pro_rated = (discounted_rate / basis) * (facts.weekly_hours or 37.5)
        req_salary = max(new_entrant_threshold, pro_rated)
        
        if facts.offered_salary is None:
            return RouteResult(
                route_id=self.route_id,
                route_label=self.route_label,
                status=RouteStatus.NEEDS_MORE_INFORMATION,
                required_salary=req_salary,
                missing_facts=["offered_salary", "weekly_hours"] if facts.weekly_hours is None else ["offered_salary"]
            )
            
        passed = facts.offered_salary >= req_salary
        return RouteResult(
            route_id=self.route_id,
            route_label=self.route_label,
            status=RouteStatus.APPLICABLE if passed else RouteStatus.SALARY_TOO_LOW,
            required_salary=req_salary,
            offered_salary=facts.offered_salary,
            passed_salary_check=passed,
            calculation_steps=[
                "Applicant meets New Entrant criteria.",
                f"General threshold is £{new_entrant_threshold:,.2f}.",
                f"70% of going rate pro-rated is £{pro_rated:,.2f}.",
                f"Required salary is £{req_salary:,.2f}."
            ]
        )
