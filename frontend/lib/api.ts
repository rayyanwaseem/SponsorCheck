import { ClassificationResponse, ApplicantFacts } from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export async function classifyJobDescription(
  job_description: string,
  provider: string,
  llm_base_url: string,
  llm_api_key: string,
  llm_model: string,
  facts: ApplicantFacts = {}
): Promise<ClassificationResponse> {
  const res = await fetch(`${API_URL}/classify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      job_description,
      provider,
      llm_base_url,
      llm_api_key,
      llm_model,
      top_k: 15,
      facts
    }),
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Failed to classify job description');
  }

  return res.json();
}
