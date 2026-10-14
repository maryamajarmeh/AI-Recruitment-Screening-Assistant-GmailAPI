
import requests
import streamlit as st
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="HireAI | Match Details",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #f7f8fc;
    color: #20233a;
}
[data-testid="stSidebar"] {
    background: #15182e;
}
[data-testid="stSidebar"] * {
    color: #f5f6ff;
}
[data-testid="stSidebar"] [data-testid="stButton"] button {
    text-align: left;
}
.block-container {
    padding-top: 1.5rem;
    max-width: 1500px;
}
.panel {
    background: white;
    border: 1px solid #e8eaf3;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 14px;
}
.muted {
    color: #777d91;
    font-size: 13px;
}
.score {
    color: #5639e8;
    font-size: 48px;
    font-weight: 750;
    line-height: 1.2;
}
.pill {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 20px;
    background: #e8f8ef;
    color: #188451;
    font-size: 12px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


# Sidebar
with st.sidebar:
    st.markdown("## ◈ HireAI")
    st.divider()
    st.markdown("### Navigation")
    st.page_link("app.py", label="⌂  Dashboard")
    st.page_link("pages/1_Job_Setup.py", label="▤  Jobs")
    st.page_link("pages/2_Important_Skills.py", label="♧  Skills & Requirements")
    st.page_link("pages/3_Screening_Results.py", label="♙  Candidates")
    st.markdown("---")
    st.caption("AI Recruitment Screening Assistant")


# Load data
try:
    job_response = requests.get(
        f"{API_URL}/jobs/current", timeout=10
    )
    job_response.raise_for_status()
    job = job_response.json()

    results_response = requests.get(
        f"{API_URL}/candidates", timeout=30
    )
    results_response.raise_for_status()
    candidates = results_response.json()

except requests.RequestException as error:
    st.error(f"Cannot connect to FastAPI: {error}")
    st.stop()


st.markdown(
    "<div class='muted'>Candidates　›　Match Details</div>",
    unsafe_allow_html=True
)
st.title("Semantic JD Matching")

st.caption(
    f"Job: {job.get('job_title', 'Not set')}　"
    "|　AI-assisted candidate evaluation"
)

if not candidates:
    st.info("No candidate results are available yet.")
    st.page_link(
        "pages/1_Job_Setup.py",
        label="Set up a job"
    )
    st.stop()


# Candidate selection
candidate_names = [
    f"{c['cv_filename']} — {c['score']}%"
    for c in candidates
]

selected_label = st.selectbox(
    "Select candidate",
    candidate_names
)

selected_index = candidate_names.index(selected_label)
candidate = candidates[selected_index]

score = int(candidate.get("score", 0))
breakdown = candidate.get("breakdown", {})
strengths = candidate.get("strengths", [])
gaps = candidate.get("gaps", [])
reasons = candidate.get("why_matches", [])
missing = candidate.get("missing_must_haves", [])


# Header
st.markdown(f"## {candidate['cv_filename']}")
st.caption(candidate.get("candidate_email", "Email not available"))


# Main three-column layout
left, middle, right = st.columns([1.0, 1.8, 1.0], gap="medium")


with left:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("### Candidate Profile")
    st.markdown("#### " + candidate["cv_filename"])
    st.write(candidate.get("candidate_email", "Unknown email"))
    st.caption("CV-based profile")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("### Job Description")
    st.markdown(f"**{job.get('job_title', 'Position')}**")
    description = job.get("job_description", "")
    st.write(
        description[:700] + ("..." if len(description) > 700 else "")
    )
    st.markdown("</div>", unsafe_allow_html=True)


with middle:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("### Overall Match Score")

    st.markdown(
        f"<div class='score'>{score}%</div>",
        unsafe_allow_html=True
    )

    if score >= 80:
        st.markdown(
            "<span class='pill'>Strong Match</span>",
            unsafe_allow_html=True
        )
    elif score >= 60:
        st.markdown(
            "<span class='pill'>Moderate Match</span>",
            unsafe_allow_html=True
        )
    else:
        st.caption("Lower match — review the evidence before deciding.")

    st.progress(score / 100)
    st.write(candidate.get("summary", "No summary available."))
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("### Match Score Breakdown")

    for category in ["Skills", "Experience", "Domain", "Education"]:
        value = int(breakdown.get(category, 0))
        col_label, col_bar = st.columns([1, 2])

        with col_label:
            st.write(category)

        with col_bar:
            st.progress(max(0, min(100, value)) / 100)
            st.caption(f"{value}%")

    st.markdown("</div>", unsafe_allow_html=True)


with right:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("### Why This Candidate Matches")

    if reasons:
        for reason in reasons:
            st.markdown(f"- {reason}")
    else:
        st.caption("No match reasons were returned.")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("### Must-Have Requirements")

    if missing:
        for item in missing:
            st.markdown(f"- ⚠️ {item}")
    else:
        st.success("No missing Must-Haves reported.")

    st.markdown("</div>", unsafe_allow_html=True)


# Lower sections
strength_col, gaps_col = st.columns(2, gap="medium")

with strength_col:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("### Candidate Strengths")

    if strengths:
        for item in strengths:
            st.markdown(f"- ✓ {item}")
    else:
        st.caption("No strengths were returned.")

    st.markdown("</div>", unsafe_allow_html=True)

with gaps_col:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("### Gaps to Review")

    if gaps:
        for item in gaps:
            st.markdown(f"- {item}")
    else:
        st.caption("No gaps were returned.")

    st.markdown("</div>", unsafe_allow_html=True)


# Ranked candidates
st.markdown("## Other Candidates")

other_candidates = [
    c for i, c in enumerate(candidates)
    if i != selected_index
][:5]

if other_candidates:
    other_table = pd.DataFrame([
        {
            "Candidate": c["cv_filename"],
            "Email": c.get("candidate_email", ""),
            "Overall Match": f"{c['score']}%",
        }
        for c in other_candidates
    ])

    st.dataframe(
        other_table,
        use_container_width=True,
        hide_index=True
    )
else:
    st.caption("No other candidates available.")
