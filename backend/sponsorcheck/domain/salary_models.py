from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict

class ApplicantFacts(BaseModel):
    weekly_hours: Optional[float] = None
    offered_salary: Optional[float] = None
    work_region: Optional[str] = None
    application_type: Optional[str] = None
    visa_route: Optional[str] = None
    first_certificate_of_sponsorship_date: Optional[str] = None
    is_extension: Optional[bool] = None
    is_switching: Optional[bool] = None
    applicant_age: Optional[int] = None
    has_student_or_graduate_visa_history: Optional[bool] = None
    is_new_entrant_claimed: Optional[bool] = None
    has_relevant_phd: Optional[bool] = None
    phd_is_stem: Optional[bool] = None
    phd_is_uk_or_ecctis_confirmed: Optional[bool] = None
    is_postdoctoral_role: Optional[bool] = None
    is_health_and_care_route: Optional[bool] = None
    is_healthcare_or_education_role: Optional[bool] = None
    uses_national_pay_scale: Optional[bool] = None
    national_pay_scale_details: Optional[Dict[str, Any]] = None
    sponsor_notes: Optional[str] = None

class RouteResult(BaseModel):
    route_id: str
    route_label: str
    status: str
    required_salary: Optional[float] = None
    offered_salary: Optional[float] = None
    passed_salary_check: Optional[bool] = None
    missing_facts: List[str] = Field(default_factory=list)
    blocking_reasons: List[str] = Field(default_factory=list)
    calculation_steps: List[str] = Field(default_factory=list)
    govuk_signposts: List[str] = Field(default_factory=list)
    source_references: List[str] = Field(default_factory=list)

class SalaryEvaluation(BaseModel):
    selected_soc_code: str
    standard_route: Optional[RouteResult] = None
    possible_lower_routes: List[RouteResult] = Field(default_factory=list)
    blocked_routes: List[RouteResult] = Field(default_factory=list)
    routes_needing_more_information: List[RouteResult] = Field(default_factory=list)
    all_route_results: List[RouteResult] = Field(default_factory=list)
    missing_questions: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
