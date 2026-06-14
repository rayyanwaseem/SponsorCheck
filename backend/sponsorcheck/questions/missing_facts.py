from typing import List
from sponsorcheck.domain.salary_models import SalaryEvaluation

def derive_missing_facts_questions(evaluation: SalaryEvaluation) -> List[str]:
    # This dynamic question engine maps internal fact keys to user-facing questions
    questions_map = {
        "weekly_hours": "What are the contracted weekly hours?",
        "offered_salary": "What is the total annual offered salary?",
        "work_region": "Which UK nation is the job located in? (England, Scotland, Wales, Northern Ireland)",
        "application_type": "Is this a new application or an extension?",
        "is_extension": "Is this an extension of a current Skilled Worker visa?",
        "applicant_age": "What is the applicant's age?",
        "has_student_or_graduate_visa_history": "Does the applicant have a Student or Graduate visa?",
        "has_relevant_phd": "Does the applicant have a PhD relevant to the job?",
        "phd_is_stem": "Is the PhD in a STEM subject?",
        "phd_is_uk_or_ecctis_confirmed": "Is the PhD from a UK institution or confirmed by Ecctis?",
        "is_postdoctoral_role": "Is this a genuinely postdoctoral role?",
        "is_health_and_care_route": "Is the applicant applying under the Health and Care Worker visa?",
        "is_healthcare_or_education_role": "Is this a frontline healthcare or education role?",
        "uses_national_pay_scale": "Is this role subject to a national pay scale?",
        "national_pay_scale_details": "Please provide the exact pay band and region for the national pay scale.",
        "first_certificate_of_sponsorship_date": "What was the date of the first Certificate of Sponsorship?"
    }
    
    questions = []
    for mq in evaluation.missing_questions:
        if mq in questions_map:
            questions.append(questions_map[mq])
        else:
            questions.append(f"Missing information: {mq}")
            
    return questions
