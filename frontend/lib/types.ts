export interface RouteResult {
  route_id: string;
  route_label: string;
  status: string;
  required_salary?: number;
  offered_salary?: number;
  passed_salary_check?: boolean;
  missing_facts: string[];
  blocking_reasons: string[];
  calculation_steps: string[];
  govuk_signposts: string[];
  source_references: string[];
}

export interface SalaryEvaluation {
  selected_soc_code: string;
  standard_route?: RouteResult;
  possible_lower_routes: RouteResult[];
  blocked_routes: RouteResult[];
  routes_needing_more_information: RouteResult[];
  all_route_results: RouteResult[];
  missing_questions: string[];
  warnings: string[];
}

export interface SocCandidate {
  occupation_code: string;
  job_type: string;
  score: number;
  matched_terms: string[];
  eligibility: any;
  rates: any;
  special_salary_routes: string[];
}

export interface SocDecision {
  best_occupation_code: string;
  confidence: number;
  reasoning: string;
  evidence_from_jd: string[];
  alternative_codes: string[];
  warning_flags: string[];
  classification_method: string;
}

export interface ClassificationResponse {
  decision: SocDecision;
  selected_soc_record: any;
  candidates: SocCandidate[];
  salary_evaluation: SalaryEvaluation;
  disclaimer: string;
  report_id: string;
}

export interface ApplicantFacts {
  weekly_hours?: number;
  offered_salary?: number;
  work_region?: string;
  application_type?: string;
  visa_route?: string;
  first_certificate_of_sponsorship_date?: string;
  is_extension?: boolean;
  is_switching?: boolean;
  applicant_age?: number;
  has_student_or_graduate_visa_history?: boolean;
  is_new_entrant_claimed?: boolean;
  has_relevant_phd?: boolean;
  phd_is_stem?: boolean;
  phd_is_uk_or_ecctis_confirmed?: boolean;
  is_postdoctoral_role?: boolean;
  is_health_and_care_route?: boolean;
  is_healthcare_or_education_role?: boolean;
  uses_national_pay_scale?: boolean;
  national_pay_scale_details?: any;
  sponsor_notes?: string;
}
