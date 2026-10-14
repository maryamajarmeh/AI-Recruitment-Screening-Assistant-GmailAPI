
import requests
import streamlit as st
from style import apply_styles, render_sidebar

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Job Setup", layout="wide")
apply_styles()
render_sidebar()

st.markdown("""
<div class="hero">
    <div class="eyebrow">STEP 01 · JOB CONFIGURATION</div>
    <h1>Set up your next hire.</h1>
    <p>
        Define the position and provide the job description.
        AI will use these details to evaluate candidate CVs.
    </p>
</div>
""", unsafe_allow_html=True)

try:
    response = requests.get(f"{API_URL}/jobs/current", timeout=10)
    response.raise_for_status()
    job = response.json()
except requests.RequestException:
    st.error("FastAPI is not running. Start the API first.")
    st.stop()

with st.form("job_form"):
    job_title = st.text_input(
        "Job Title",
        value=job.get("job_title", ""),
        placeholder="e.g. AI Engineer"
    )

    job_description = st.text_area(
        "Job Description",
        value=job.get("job_description", ""),
        height=250,
        placeholder="Paste the complete job description here..."
    )

    max_cvs = st.number_input(
        "Maximum CVs to Process",
        min_value=1,
        max_value=500,
        value=int(job.get("max_cvs", 20))
    )

    email_subject = st.text_input(
        "Gmail Subject Keyword (optional)",
        value=job.get("email_subject", ""),
        placeholder="e.g. AI Engineer Application"
    )

    submitted = st.form_submit_button("Save and Continue")

if submitted:
    if not job_title.strip() or not job_description.strip():
        st.error("Job title and job description are required.")
    else:
        payload = {
            "job_title": job_title.strip(),
            "job_description": job_description.strip(),
            "max_cvs": int(max_cvs),
            "email_subject": email_subject.strip()
        }

        try:
            response = requests.post(
                f"{API_URL}/jobs",
                json=payload,
                timeout=15
            )

            if response.ok:
                st.session_state.pop("requirements_data", None)
                st.success("Job details saved.")
                st.switch_page("pages/2_Important_Skills.py")
            else:
                st.error(response.text)

        except requests.RequestException as error:
            st.error(f"Could not save job details: {error}")