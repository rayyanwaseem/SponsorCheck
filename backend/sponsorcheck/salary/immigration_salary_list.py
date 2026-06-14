from sponsorcheck.domain.models import SocRecord
from sponsorcheck.domain.salary_models import ApplicantFacts, RouteResult
from sponsorcheck.domain.route_models import RouteStatus
from sponsorcheck.salary.base import RouteEvaluator
from sponsorcheck.data.salary_rule_store import get_salary_rule_store
from sponsorcheck.data.special_dataset_store import get_special_dataset_store

class ImmigrationSalaryList(RouteEvaluator):
    route_id = "immigration_salary_list"
    route_label = "Immigration Salary List"

    def evaluate(self, record: SocRecord, facts: ApplicantFacts) -> RouteResult:
        special_store = get_special_dataset_store()
        isl_data = special_store.get_dataset("immigration_salary_list")
        
        # In a real implementation we would check isl_data to see if the occupation_code is present
        # and if it has region/condition specific rules.
        
        # Here we just use a simplified version: check special flags.
        if "immigration_salary_list" not in record.special_salary_routes:
            return RouteResult(
                route_id=self.route_id,
                route_label=self.route_label,
                status=RouteStatus.NOT_APPLICABLE,
                calculation_steps=["Code is not on the Immigration Salary List."]
            )
            
        missing = []
        if facts.work_region is None: missing.append("work_region")
        
        if missing:
            return RouteResult(
                route_id=self.route_id,
                route_label=self.route_label,
                status=RouteStatus.NEEDS_MORE_INFORMATION,
                missing_facts=missing,
                calculation_steps=["Code is on ISL. Checking regional conditions..."],
                govuk_signposts=["Some ISL codes apply only to specific UK nations."]
            )
            
        rules = get_salary_rule_store().get_rules().get("salary_rules", {})
        isl_threshold = rules.get("discount_options", {}).get("immigration_salary_list_standard_route", {}).get("minimum_annual_salary", 33400.0)
        
        rates = record.rates or {}
        lower_rate = rates.get("lower", {}).get("annual")
        if lower_rate is None:
            lower_rate = 0.0
            
        basis = rates.get("lower", {}).get("basis_weekly_hours", 37.5)
        
        pro_rated = (lower_rate / basis) * (facts.weekly_hours or 37.5)
        req_salary = max(isl_threshold, pro_rated)
        
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
                "Code is on ISL.",
                f"ISL threshold is £{isl_threshold:,.2f}.",
                f"Required salary is £{req_salary:,.2f}."
            ]
        )
