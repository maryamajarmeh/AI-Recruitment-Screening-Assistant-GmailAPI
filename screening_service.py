
import json
from pathlib import Path

from attachment_downloader import get_cv_attachments, save_attachment
from gmail_reader import get_header, get_message, search_emails
from cv_text_extractor import extract_cv_text
from job_matcher import check_cv_match
from results_manager import save_candidate_result


PROCESSED_FILE = Path("processed_emails.json")
TEMP_DIR = "temp_cvs"


def load_processed_emails():
    if not PROCESSED_FILE.exists():
        return set()

    return set(json.loads(
        PROCESSED_FILE.read_text(encoding="utf-8")
    ))


def save_processed_emails(processed_ids):
    PROCESSED_FILE.write_text(
        json.dumps(sorted(processed_ids), indent=2),
        encoding="utf-8"
    )


def run_screening(job, requirements):
    processed_ids = load_processed_emails()

    query = "in:inbox has:attachment"
    subject_keyword = job.get("email_subject", "").strip()
    if subject_keyword:
        subject_keyword = subject_keyword.replace('"', "")
        query += f' subject:"{subject_keyword}"'

    max_cvs = int(job["max_cvs"])
    messages = search_emails(
        query=query,
        max_results=min(500, max(100, max_cvs * 3))
    )

    processed_count = 0
    errors = []

    for message_item in messages:
        if processed_count >= max_cvs:
            break

        message_id = message_item["id"]

        if message_id in processed_ids:
            continue

        try:
            message = get_message(message_id)
            headers = message.get("payload", {}).get("headers", [])
            subject = get_header(headers, "Subject")
            sender = get_header(headers, "From")

            attachments = get_cv_attachments(message)

            if not attachments:
                processed_ids.add(message_id)
                save_processed_emails(processed_ids)
                continue

            email_success = True

            for attachment in attachments:
                if processed_count >= max_cvs:
                    email_success = False
                    break

                processed_count += 1

                try:
                    saved_path = save_attachment(
                        message_id=message_id,
                        attachment=attachment,
                        output_dir=TEMP_DIR
                    )

                    cv_text = extract_cv_text(str(saved_path))

                    if not cv_text.strip():
                        raise ValueError("No text could be extracted from this CV.")

                    result = check_cv_match(
                        cv_text=cv_text,
                        job_description=job["job_description"],
                        requirements=requirements
                    )

                    score = result["score"]

                                        
                    save_candidate_result({
                        "job_title": job["job_title"],
                        "message_id": message_id,
                        "candidate_email": sender,
                        "subject": subject,
                        "cv_filename": Path(saved_path).name,
                        "score": result["score"],
                        "summary": result["summary"],
                        "strengths": result["strengths"],
                        "gaps": result["gaps"],
                        "why_matches": result["why_matches"],
                        "breakdown": result["breakdown"],
                        "missing_must_haves": result["missing_must_haves"],
                        "cv_path": (
                            str(saved_path)
                            if result["score"] >= 50
                            else None
                        )
                    })

                    if result["score"] < 50:
                        Path(saved_path).unlink(missing_ok=True)


                    # Keep the result, but remove CV files below 50%.
                    if score < 50:
                        Path(saved_path).unlink(missing_ok=True)

                except Exception as error:
                    email_success = False
                    errors.append(
                        f"{attachment.get('filename', 'Unknown file')}: {error}"
                    )

            if email_success:
                processed_ids.add(message_id)

            save_processed_emails(processed_ids)

        except Exception as error:
            errors.append(f"Email {message_id}: {error}")

    return {
        "processed_cvs": processed_count,
        "errors": errors,
        "message": "Screening finished."
    }