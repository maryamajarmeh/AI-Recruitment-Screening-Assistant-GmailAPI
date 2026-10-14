import requests
import streamlit as st

from style import apply_styles, render_sidebar

st.set_page_config(
    page_title="HireAI | Dashboard",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_styles()
render_sidebar()

API_URL = "http://127.0.0.1:8000"

# Load dashboard data
job = {}
candidates = []
api_available = True

try:
    job_response = requests.get(
        f"{API_URL}/jobs/current", timeout=5
    )
    job_response.raise_for_status()
    job = job_response.json()

    candidates_response = requests.get(
        f"{API_URL}/candidates", timeout=10
    )
    candidates_response.raise_for_status()
    candidates = candidates_response.json()

except requests.RequestException:
    api_available = False


# Header
st.markdown("""
<div class="hero">
    <div class="eyebrow">RECRUITMENT WORKSPACE</div>
    <h1>Find the right talent, faster.</h1>
    <p>
        Manage job requirements, screen CVs with AI, and review
        evidence-backed candidate matches in one workspace.
    </p>
</div>
""", unsafe_allow_html=True)

if not api_available:
    st.warning(
        "Cannot connect to FastAPI. Start the API to load your "
        "job information and screening results."
    )

# Overview
st.subheader("Overview")
st.caption("A snapshot of your current recruitment workflow.")

total_candidates = len(candidates)
high_matches = sum(
    1 for c in candidates if int(c.get("score", 0)) >= 80
)
review_candidates = sum(
    1 for c in candidates if 50 <= int(c.get("score", 0)) < 80
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Current Position",
        job.get("job_title") or "Not configured",
    )

with col2:
    st.metric(
        "Candidates Screened",
        total_candidates,
    )

with col3:
    st.metric(
        "Strong Matches",
        high_matches,
        help="Candidates with a match score of 80% or higher.",
    )

with col4:
    st.metric(
        "Needs Review",
        review_candidates,
        help="Candidates with scores between 50% and 79%.",
    )

st.divider()

# Workflow cards
st.subheader("Recruitment Workflow")
st.caption("Complete each step to screen candidates for a position.")

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("""
    <div class="section-card">
        <div class="step-number">01</div>
        <h3>Job Setup</h3>
        <p class="small-muted">
            Enter the position, job description, CV processing limit,
            and optional Gmail subject keyword.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Configure Job →", use_container_width=True):
        st.switch_page("pages/Job_Setup.py")

with col2:
    st.markdown("""
    <div class="section-card">
        <div class="step-number">02</div>
        <h3>Requirements</h3>
        <p class="small-muted">
            Extract job requirements with AI, review them, and classify
            mandatory skills versus preferred qualifications.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Review Requirements →", use_container_width=True):
        st.switch_page("pages/Important_Skills.py")

with col3:
    st.markdown("""
    <div class="section-card">
        <div class="step-number">03</div>
        <h3>Screening Results</h3>
        <p class="small-muted">
            Compare candidate scores, inspect evidence, and review
            missing Must-Haves before making HR decisions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("View Candidates →", use_container_width=True):
        st.switch_page("pages/Screening_Results.py")

# Current job
st.divider()
st.subheader("Current Job")

if job.get("job_title"):
    left, right = st.columns([3, 1])

    with left:
        st.markdown(
            f"""
            <div class="section-card">
                <div class="small-muted">ACTIVE POSITION</div>
                <h3>{job['job_title']}</h3>
                <p class="small-muted">
                    CV processing limit: {job.get('max_cvs', 'Not set')}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.write("")
        st.write("")
        if st.button("Edit Job", use_container_width=True):
            st.switch_page("pages/Job_Setup.py")
else:
    st.info(
        "No job has been configured yet. Start by adding a job "
        "description."
    )

    if st.button("Create Your First Job", type="primary"):
        st.switch_page("pages/Job_Setup.py")

# Recent candidates
st.divider()
st.subheader("Top Matching Candidates")

if candidates:
    ranked = sorted(
        candidates,
        key=lambda c: int(c.get("score", 0)),
        reverse=True,
    )[:5]

    for candidate in ranked:
        name = candidate.get("cv_filename", "Unknown CV")
        score = max(0, min(100, int(candidate.get("score", 0))))

        with st.container(border=True):
            left, middle, right = st.columns([3, 2, 1])

            with left:
                st.markdown(f"**{name}**")
                st.caption(
                    candidate.get("candidate_email", "Email unavailable")
                )

            with middle:
                st.progress(score / 100)
                st.caption(f"{score}% match")

            with right:
                if score >= 80:
                    st.success("Strong")
                elif score >= 50:
                    st.warning("Review")
                else:
                    st.error("Low")

    if st.button("View All Screening Results"):
        st.switch_page("pages/Screening_Results.py")
else:
    st.caption(
        "Your ranked candidates will appear here after screening."
    )

st.divider()
st.caption(
    "HireAI · AI-assisted recruitment screening · "
    "Final hiring decisions remain with HR."
)
