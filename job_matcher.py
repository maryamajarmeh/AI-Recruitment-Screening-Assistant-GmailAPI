
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("openai_key") or os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-6-luna"

if not API_KEY:
    raise ValueError(
        "OpenAI API key is missing. Add openai_key to your .env file."
    )

client = OpenAI(api_key=API_KEY)


def check_cv_match(
    cv_text: str,
    job_description: str,
    requirements: list = None
) -> dict:
    requirements = requirements or []

    prompt = f"""
You are an evidence-based recruitment screening assistant.

Evaluate the candidate against the job description and HR-approved
requirements. Use only evidence found in the CV. Do not invent
experience, skills, education, or qualifications.

JOB DESCRIPTION:
{job_description}

HR-APPROVED REQUIREMENTS:
{json.dumps(requirements, ensure_ascii=False)}

CANDIDATE CV:
{cv_text}

Return JSON with exactly this structure:
{{
  "score": 0,
  "summary": "Short overall assessment",
  "strengths": ["Evidence-supported strength"],
  "gaps": ["Missing or weakly supported qualification"],
  "missing_must_haves": ["Unmet mandatory requirement"],
  "why_matches": ["Evidence-supported reason"],
  "breakdown": {{
    "Skills": 0,
    "Experience": 0,
    "Education": 0,
    "Domain": 0
  }}
}}

Rules:
- score must be one overall match percentage from 0 to 100.
- Each breakdown value must be from 0 to 100.
- Assess relevance to the actual job, not just keyword overlap.
- Do not give credit for experience that the CV does not demonstrate.
- A missing item is not proof the candidate lacks that ability;
  describe it as "not evidenced" when appropriate.
- Include only mandatory requirements that are not sufficiently
  supported in missing_must_haves.
- Strengths and reasons must be grounded in the CV.
- Return valid JSON only.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "Return only valid JSON. Evaluate CVs fairly and use evidence."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={"type": "json_object"}
    )

    result = json.loads(response.choices[0].message.content)

    score = max(0, min(100, int(result.get("score", 0))))
    breakdown = result.get("breakdown", {})

    return {
        "score": score,
        "summary": result.get("summary", ""),
        "strengths": result.get("strengths", []),
        "gaps": result.get("gaps", []),
        "missing_must_haves": result.get("missing_must_haves", []),
        "why_matches": result.get("why_matches", []),
        "breakdown": {
            category: max(0, min(100, int(breakdown.get(category, 0))))
            for category in ["Skills", "Experience", "Education", "Domain"]
        }
    }
