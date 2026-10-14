import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from screening_service import run_screening
from results_manager import get_ranked_candidates


load_dotenv()

API_KEY = os.getenv("openai_key")
MODEL_NAME = "gpt-6-luna"

if not API_KEY:
    raise ValueError(
        "OpenAI API key is missing. Check your .env file."
    )

client = OpenAI(api_key=API_KEY)

app = FastAPI(title="AI Recruitment Screening API")

CONFIG_FILE = Path("job_config.json")


class JobInput(BaseModel):
    job_title: str
    job_description: str
    max_cvs: int
    email_subject: str = ""


class RequirementsInput(BaseModel):
    requirements: list[dict]


def read_config():
    if not CONFIG_FILE.exists():
        return None

    return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))


def write_config(data):
    CONFIG_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def extract_job_requirements(job_description: str) -> list:
    """Extract job requirements using OpenAI."""

    prompt = f"""
Analyze the following job description and extract its requirements.

JOB DESCRIPTION:
{job_description}

Return JSON using this structure:
{{
  "requirements": [
    {{
      "requirement": "Specific skill or qualification",
      "category": "must_have",
      "reason": "Reason based on the job description"
    }}
  ]
}}

Rules:
- Use only requirements supported by the job description.
- Use must_have only for explicitly mandatory requirements.
- Use preferred for desirable qualifications.
- Use unclear when the category cannot be determined.
- Do not invent requirements.
- Avoid duplicate requirements.
- Return valid JSON only.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an evidence-based recruitment assistant. "
                    "Return valid JSON only."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
    )

    result = json.loads(response.choices[0].message.content)
    requirements = result.get("requirements", [])

    if not isinstance(requirements, list):
        raise ValueError("Invalid requirements returned by the model.")

    valid_categories = {"must_have", "preferred", "unclear"}
    cleaned_requirements = []

    for item in requirements:
        if not isinstance(item, dict):
            continue

        requirement = str(item.get("requirement", "")).strip()
        category = item.get("category", "unclear")

        if not requirement:
            continue

        if category not in valid_categories:
            category = "unclear"

        cleaned_requirements.append({
            "requirement": requirement,
            "category": category,
            "reason": str(item.get("reason", "")).strip(),
        })

    return cleaned_requirements


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/jobs/current")
def get_current_job():
    return read_config() or {}


@app.post("/jobs")
def save_job(job: JobInput):
    if not job.job_title.strip():
        raise HTTPException(400, "Job title is required.")

    if not job.job_description.strip():
        raise HTTPException(400, "Job description is required.")

    if not 1 <= job.max_cvs <= 500:
        raise HTTPException(
            400, "Number of CVs must be between 1 and 500."
        )

    data = job.model_dump()
    data["requirements"] = []
    write_config(data)

    return {"message": "Job details saved."}


@app.post("/requirements/extract")
def extract_requirements():
    job = read_config()

    if not job:
        raise HTTPException(400, "Save the job details first.")

    try:
        requirements = extract_job_requirements(
            job["job_description"]
        )
        return {"requirements": requirements}

    except Exception as error:
        raise HTTPException(
            500, f"Could not extract requirements: {error}"
        )


@app.put("/requirements")
def save_requirements(data: RequirementsInput):
    job = read_config()

    if not job:
        raise HTTPException(400, "Save the job details first.")

    valid_categories = {"must_have", "preferred", "unclear"}

    for item in data.requirements:
        if not item.get("requirement", "").strip():
            raise HTTPException(
                400, "Every requirement needs a description."
            )

        if item.get("category") not in valid_categories:
            raise HTTPException(400, "Invalid requirement category.")

    job["requirements"] = data.requirements
    write_config(job)

    return {"message": "Requirements saved."}


@app.post("/screen")
def screen_candidates():
    job = read_config()

    if not job:
        raise HTTPException(400, "Save the job details first.")

    requirements = job.get("requirements", [])

    if not requirements:
        raise HTTPException(400, "Save the requirements first.")

    try:
        return run_screening(job, requirements)

    except Exception as error:
        raise HTTPException(500, f"Screening failed: {error}")


@app.get("/candidates")
def list_candidates():
    job = read_config()

    if not job:
        return []

    return get_ranked_candidates(job_title=job["job_title"])