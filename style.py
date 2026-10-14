import streamlit as st


def apply_styles():
    st.markdown("""
    <style>
    :root {
        --primary: #6558E8;
        --primary-dark: #5143D5;
        --background: #F5F6FC;
        --text: #20233A;
        --muted: #777D95;
        --border: #E7E9F4;
    }

    .stApp {
        background: var(--background);
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: var(--text);
        letter-spacing: -0.5px;
    }

    h1 {
        font-size: 2.1rem !important;
        font-weight: 750 !important;
    }

    p, label, .stMarkdown {
        color: var(--text);
    }

    [data-testid="stSidebar"] {
        background: #191B35;
        border-right: 1px solid #292B49;
    }

    [data-testid="stSidebar"] * {
        color: #F5F5FF;
    }

    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #A8ACCC;
    }

    [data-testid="stSidebar"] [data-testid="stButton"] button,
    [data-testid="stSidebar"] [data-testid="stPageLink"] a {
        border-radius: 10px;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        background: var(--primary);
        color: white;
        border: 1px solid var(--primary);
        border-radius: 10px;
        min-height: 43px;
        font-weight: 600;
        transition: 0.2s ease;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        background: var(--primary-dark);
        color: white;
        border-color: var(--primary-dark);
    }

    .stButton > button:focus,
    .stFormSubmitButton > button:focus {
        box-shadow: 0 0 0 0.2rem #6558E844;
    }

    [data-testid="stForm"],
    [data-testid="stDataFrame"],
    [data-testid="stTable"] {
        border-radius: 14px;
    }

    [data-testid="stForm"] {
        background: white;
        padding: 25px;
        border: 1px solid var(--border);
    }

    [data-testid="stMetric"] {
        background: white;
        padding: 20px;
        border: 1px solid var(--border);
        border-radius: 14px;
        box-shadow: 0 3px 12px #20233A08;
    }

    [data-testid="stMetricLabel"] {
        color: var(--muted);
    }

    [data-testid="stMetricValue"] {
        color: var(--primary);
        font-weight: 750;
    }

    input, textarea {
        border-radius: 9px !important;
    }

    [data-testid="stProgressBar"] > div > div {
        background-color: var(--primary);
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    .hero {
        background: linear-gradient(120deg, #6558E8 0%, #8276F4 60%, #9B91FA 100%);
        border-radius: 20px;
        padding: 32px;
        color: white;
        margin: 10px 0 25px 0;
        box-shadow: 0 12px 30px #6558E822;
    }

    .hero h1, .hero p, .hero span {
        color: white !important;
    }

    .hero h1 {
        margin-bottom: 10px;
    }

    .hero p {
        opacity: 0.93;
        font-size: 1rem;
        line-height: 1.7;
    }

    .section-card {
        background: white;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 22px;
        margin: 12px 0;
        box-shadow: 0 3px 14px #20233A06;
    }

    .section-card h3 {
        margin-top: 0;
    }

    .eyebrow {
        text-transform: uppercase;
        font-size: 12px;
        font-weight: 750;
        letter-spacing: 1.4px;
        color: #DCD8FF !important;
    }

    .step-number {
        display: inline-flex;
        width: 38px;
        height: 38px;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        background: #EEECFF;
        color: var(--primary);
        font-weight: 800;
        margin-bottom: 10px;
    }

    .small-muted {
        color: var(--muted) !important;
        font-size: 13px;
        line-height: 1.6;
    }

    hr {
        border-color: var(--border);
    }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="padding: 12px 0 18px 0;">
            <div style="font-size: 27px; font-weight: 800;">
                ◈ Hire<span style="color:#A69CFF;">AI</span>
            </div>
            <div style="color:#A8ACCC; font-size:12px; margin-top:5px;">
                RECRUITMENT INTELLIGENCE
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()
        st.markdown("### WORKSPACE")

        st.page_link("app.py", label="⌂  Dashboard")
        st.page_link("pages/Job_Setup.py", label="▤  Job Setup")
        st.page_link(
            "pages/Important_Skills.py",
            label="◇  Skills & Requirements"
        )
        st.page_link(
            "pages/Screening_Results.py",
            label="♙  Screening Results"
        )

        st.divider()
        st.markdown("""
        <div style="background:#252747; padding:14px; border-radius:12px;">
            <div style="font-weight:650;">AI-assisted screening</div>
            <div style="font-size:12px; color:#B8BCDA; margin-top:6px;">
                Evidence-based matching.<br>
                Final decisions remain with HR.
            </div>
        </div>
        """, unsafe_allow_html=True)
