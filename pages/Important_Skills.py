
import requests
import streamlit as st
from style import apply_styles, render_sidebar

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Important Skills", layout="wide")
apply_styles()
render_sidebar()

st.markdown("""
<div class="hero">
    <div class="eyebrow">STEP 02 · REQUIREMENT ANALYSIS</div>
    <h1>Define what matters.</h1>
    <p>
        Review AI-extracted requirements, confirm mandatory
        qualifications, and keep HR in control of the screening criteria.
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

if not job.get("job_description"):
    st.warning("Set up a job first.")
    if st.button("Go to Job Setup"):
        st.switch_page("pages/1_Job_Setup.py")
    st.stop()

st.write(f"**Position:** {job['job_title']}")
st.write("Review the extracted requirements and choose their importance.")

if "requirements_data" not in st.session_state:
    st.session_state["requirements_data"] = job.get("requirements", [])

if st.button("Extract Requirements from Job Description"):
    try:
        with st.spinner("Ollama is extracting requirements..."):
            response = requests.post(
                f"{API_URL}/requirements/extract",
                timeout=600
            )
            response.raise_for_status()

        st.session_state["requirements_data"] = response.json()["requirements"]
        st.success("Requirements extracted. Review them below.")

    except requests.RequestException as error:
        st.error(f"Could not extract requirements: {error}")

requirements = st.session_state["requirements_data"]

if requirements:
    edited = st.data_editor(
        requirements,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "requirement": st.column_config.TextColumn(
                "Skill or Requirement",
                required=True
            ),
            "category": st.column_config.SelectboxColumn(
                "Importance",
                options=["must_have", "preferred", "unclear"],
                required=True
            )
        },
        key="requirements_editor"
    )

    st.caption(
        "must_have = mandatory; preferred = nice-to-have; "
        "unclear = review or classify later."
    )

    if st.button("Save Skills and Start Screening", type="primary"):
        requirement_list = edited.to_dict(orient="records")

        requirement_list = [
            {
                "requirement": str(item.get("requirement", "")).strip(),
                "category": item.get("category", "unclear")
            }
            for item in requirement_list
            if str(item.get("requirement", "")).strip()
        ]

        if not requirement_list:
            st.error("Add at least one requirement.")
        else:
            try:
                save_response = requests.put(
                    f"{API_URL}/requirements",
                    json={"requirements": requirement_list},
                    timeout=30
                )
                save_response.raise_for_status()

                with st.spinner(
                    "Screening CVs. This may take several minutes..."
                ):
                    screen_response = requests.post(
                        f"{API_URL}/screen",
                        timeout=3600
                    )
                    screen_response.raise_for_status()

                summary = screen_response.json()
                st.success(
                    f"Screening finished. "
                    f"CVs attempted: {summary['processed_cvs']}"
                )

                if summary.get("errors"):
                    st.warning(
                        f"{len(summary['errors'])} processing error(s) occurred. "
                        "Check the API terminal for details."
                    )

                st.switch_page("pages/3_Screening_Results.py")

            except requests.RequestException as error:
                st.error(f"Could not complete screening: {error}")
else:
    st.info(
        "Click 'Extract Requirements from Job Description' "
        "to create the initial requirements list."
    )