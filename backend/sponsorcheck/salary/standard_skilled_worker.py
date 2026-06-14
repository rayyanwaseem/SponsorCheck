from sponsorcheck.domain.models import SocRecord
from sponsorcheck.domain.salary_models import ApplicantFacts, RouteResult
from sponsorcheck.domain.route_models import RouteStatus
from sponsorcheck.salary.base import RouteEvaluator
from sponsorcheck.data.salary_rule_store import get_salary_rule_store

class StandardSkilledWorker(RouteEvaluator):
    route_id = "standard"
    route_label = "Standard Skilled Worker"

    def evaluate(self, record: SocRecord, facts: ApplicantFacts) -> RouteResult:
        rules = get_salary_rule_store().get_rules().get("salary_rules", {})
        general_threshold = rules.get("route_options", {}).get("standard_skilled_worker", {}).get("general_threshold_annual", 41700.0)
        
        calculation_steps = [f"General threshold is £{general_threshold:,.2f}."]
        
        # Try to find standard rate
        rates = record.rates or {}
        standard_rate = rates.get("standard")
        if not standard_rate:
            return RouteResult(
                route_id=self.route_id,
                route_label=self.route_label,
                status=RouteStatus.NOT_APPLICABLE,
                calculation_steps=calculation_steps,
                blocking_reasons=["No standard going rate found for this SOC code."]
            )
            
        rate_val = standard_rate.get("annual")
        if rate_val is None:
            rate_val = 0.0
            
        basis = standard_rate.get("basis_weekly_hours", 37.5)
        calculation_steps.append(f"Standard going rate is £{rate_val:,.2f} based on {basis} hours/week.")
        
        if facts.weekly_hours is None:
            return RouteResult(
                route_id=self.route_id,
                route_label=self.route_label,
                status=RouteStatus.NEEDS_MORE_INFORMATION,
                calculation_steps=calculation_steps,
                missing_facts=["weekly_hours"],
                govuk_signposts=["Please provide weekly hours to calculate the pro-rated going rate."]
            )
            
        pro_rated = (rate_val / basis) * facts.weekly_hours
        calculation_steps.append(f"Pro-rated going rate for {facts.weekly_hours} hours is £{pro_rated:,.2f}.")
        
        required_salary = max(general_threshold, pro_rated)
        calculation_steps.append(f"Required salary is the higher of the two: £{required_salary:,.2f}.")
        
        if facts.offered_salary is None:
            return RouteResult(
                route_id=self.route_id,
                route_label=self.route_label,
                status=RouteStatus.NEEDS_MORE_INFORMATION,
                required_salary=required_salary,
                calculation_steps=calculation_steps,
                missing_facts=["offered_salary"],
                govuk_signposts=["Please provide the offered salary to determine if it meets the requirement."]
            )
            
        passed = facts.offered_salary >= required_salary
        status = RouteStatus.APPLICABLE if passed else RouteStatus.SALARY_TOO_LOW
        
        return RouteResult(
            route_id=self.route_id,
            route_label=self.route_label,
            status=status,
            required_salary=required_salary,
            offered_salary=facts.offered_salary,
            passed_salary_check=passed,
            calculation_steps=calculation_steps,
            blocking_reasons=["Offered salary is below the required threshold."] if not passed else []
        )
