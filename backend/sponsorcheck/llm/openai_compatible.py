import httpx
from typing import Dict, Any, List
from sponsorcheck.classification.prompts import SYSTEM_PROMPT
from sponsorcheck.data.salary_rule_store import get_salary_rule_store

def get_dynamic_system_prompt() -> str:
    rules = get_salary_rule_store().get_rules().get("salary_rules", {})
    route_opts = rules.get("route_options", {})
    
    std_thresh = route_opts.get("standard_skilled_worker", {}).get("general_threshold_annual", 41700)
    health_thresh = route_opts.get("health_and_care_worker", {}).get("general_threshold_annual", 31300)
    
    facts = (
        f"\n\nBACKGROUND FACTS (For reasoning accuracy only):\n"
        f"If you discuss salary in your reasoning, use the current dataset facts:\n"
        f"- Standard Skilled Worker general threshold is £{std_thresh}.\n"
        f"- Health and Care general threshold is £{health_thresh}.\n"
        f"- Discount routes (New Entrant, PhD) minimum threshold is £33,400.\n"
        f"Do not hallucinate older thresholds like £38,700.\n\n"
        f"CRITICAL INSTRUCTION: You must base your SOC code classification SOLELY on the job duties, skills, and responsibilities. "
        f"Do NOT let the salary facts above influence which SOC code you select."
    )
    
    return SYSTEM_PROMPT + facts

async def call_openai_compatible_api(
    base_url: str,
    api_key: str,
    model: str,
    job_description: str,
    candidates: List[Dict[str, Any]]
) -> str:
    
    candidates_text = "\n".join([f"{c['occupation_code']} - {c['job_type']}" for c in candidates])
    
    user_prompt = f"""Job Description:
{job_description}

Candidates:
{candidates_text}

Please classify the job description into the best matching SOC code from the candidates above."""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": get_dynamic_system_prompt()},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.1,
        "response_format": { "type": "json_object" }
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url.rstrip('/')}/chat/completions",
            headers=headers,
            json=payload,
            timeout=60.0
        )
        if response.status_code != 200:
            error_msg = response.text
            try:
                error_msg = response.json().get("error", response.text)
                if isinstance(error_msg, dict) and "message" in error_msg:
                    error_msg = error_msg["message"]
            except Exception:
                pass
            raise Exception(f"API Error ({response.status_code}): {error_msg}")
            
        data = response.json()
        return data["choices"][0]["message"]["content"]
