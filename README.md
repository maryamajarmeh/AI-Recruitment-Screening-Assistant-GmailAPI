# HireAI — AI Recruitment Screening Assistant

An AI-powered recruitment screening assistant that helps HR teams review job applications, evaluate CVs against job requirements, and identify candidates who best match a position. The system automates repetitive screening tasks while keeping final hiring decisions under human control.

## Overview

Reviewing large numbers of CVs manually can be time-consuming and inconsistent. HireAI streamlines the initial screening process by connecting to Gmail, collecting CV attachments, extracting candidate information, and evaluating applications against a job description.

HR users can define job requirements, identify non-negotiable qualifications, review matching results, and compare candidates based on their qualifications and supporting evidence.

**HireAI supports HR decision-making; it does not make final hiring decisions.**

## Key Features

- **Gmail Integration:** Retrieve application emails and CV attachments from the inbox.
- **CV Processing:** Download and extract text from supported PDF and DOCX files.
- **AI-Powered Matching:** Evaluate CVs against a job description using the OpenAI API.
- **Requirements Extraction:** Identify job requirements from a job description.
- **Must-Have Requirements:** Define and review essential qualifications separately from preferred qualifications.
- **Evidence-Based Evaluation:** Present matching strengths, skill gaps, missing essential requirements, and supporting explanations.
- **Candidate Ranking:** Compare candidates according to their relevance to the role.
- **Screening Dashboard:** Review candidates and their matching results through a Streamlit interface.
- **Human-in-the-Loop:** Keep shortlisting and rejection decisions under HR control.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| AI and Language Model | OpenAI API |
| Backend API | FastAPI |
| Frontend | Streamlit |
| Email Integration | Gmail API |
| PDF Processing | pypdf |
| Word Document Processing | python-docx |
| Data Validation | Pydantic |
| HTTP Requests | Requests |
| Environment Configuration | python-dotenv |
| Data Handling | Pandas |

## System Workflow

1. **Job Setup:** HR enters the job title, job description, and screening settings.
2. **Requirements Extraction:** The AI identifies relevant skills, qualifications, and experience requirements.
3. **Requirements Review:** HR reviews and edits the extracted requirements, distinguishing Must-Haves from preferred qualifications.
4. **CV Collection:** The system searches Gmail for relevant application emails and retrieves supported CV attachments.
5. **Text Extraction:** The system extracts readable text from CV files.
6. **AI Screening:** Each CV is evaluated against the job description and approved requirements.
7. **Results Review:** HR reviews candidate scores, matching evidence, strengths, gaps, and missing Must-Haves.
8. **Human Decision:** HR decides which candidates to shortlist, review further, or reject.

## Project Structure

The project is organized into separate modules for the API, screening logic, email integration, and user interface.

```text
AI Recruitment Screening Assistant/
│
├── app.py
├── api.py
├── style.py
├── job_matcher.py
├── screening_service.py
├── results_manager.py
│
├── pages/
│   ├── Job_Setup.py
│   ├── Important_Skills.py
│   └── Screening_Results.py
│
├── gmail_service.py
├── attachment_downloader.py
├── cv_extractor.py
│
├── requirements.txt
├── .env
├── .gitignore
│
├── credentials.json
├── token.json
│
└── temp_cvs/
```

*Note: The structure above is illustrative. Keep only the files and directories that exist in your actual project.*

## Getting Started

### Prerequisites

- Python 3.11 or a compatible version.
- A Google account with Gmail.
- A Google Cloud project with the Gmail API enabled.
- Gmail OAuth credentials configured for the application.
- An OpenAI API key with access to the configured model.

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd "AI Recruitment Screening Assistant"
```

Replace the repository URL with your actual GitHub repository URL.

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
```

Use the environment variable name expected by your application. Never commit API keys or other secrets to GitHub.

### 5. Configure Gmail API

1. Open the [Google Cloud Console](https://console.cloud.google.com/).
2. Create or select a Google Cloud project.
3. Enable the Gmail API.
4. Configure the OAuth consent screen and test users if required.
5. Create OAuth client credentials for a desktop application, following your implementation's requirements.
6. Download the credentials file and place it in the project root using the filename expected by your code.
7. Run the application and complete Google's authorization flow.

The application may generate a `token.json` file to store OAuth tokens. Keep credentials and tokens private, and use the minimum required Gmail permissions.

### 6. Run the Backend

Start the FastAPI server from the project root:

```bash
uvicorn api:app --reload
```

Open the interactive API documentation:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 7. Run the Frontend

Open a second terminal, activate the virtual environment, and run:

```bash
streamlit run app.py
```

The interface will usually be available at:

[http://localhost:8501](http://localhost:8501)

Ensure the frontend's configured API URL matches the running FastAPI server.

## Security and Privacy

CVs and email attachments may contain personally identifiable information. This project should be operated with appropriate safeguards.

- Keep `.env`, `credentials.json`, and `token.json` out of version control.
- Do not commit real candidate CVs or confidential recruitment data.
- Restrict access to downloaded CVs and extracted candidate information.
- Use Gmail read-only access when the application only needs to retrieve emails.
- Apply appropriate retention and deletion policies to downloaded files.
- Review AI-generated evaluations for errors, unsupported claims, and potential bias.
- Do not use AI-generated scores as the sole basis for employment decisions.

## Responsible AI

HireAI is designed as a decision-support tool for recruitment. Candidate evaluations should be based on job-related qualifications and verifiable evidence. HR professionals remain responsible for reviewing results and making employment decisions.


---

**Developed as an AI-assisted recruitment screening project using Python, FastAPI, Streamlit, Gmail API, and OpenAI.**
