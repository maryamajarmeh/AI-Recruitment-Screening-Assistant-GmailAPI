
from pathlib import Path
import json

from attachment_downloader import get_cv_attachments, save_attachment
from gmail_reader import get_header, get_message, search_emails
from cv_text_extractor import extract_cv_text
from job_matcher import load_job_description, check_cv_match
from results_manager import save_candidate_result

GMAIL_QUERY ='in:inbox has:attachment subject:"AI Engineer"'
TEMP_DIR = "temp_cvs"
PROCESSED_EMAILS_FILE = Path("processed_emails.json")


def load_processed_emails():
    if not PROCESSED_EMAILS_FILE.exists():
        return set()

    data = json.loads(
        PROCESSED_EMAILS_FILE.read_text(encoding="utf-8")
    )
    return set(data)


def save_processed_emails(processed_ids):
    PROCESSED_EMAILS_FILE.write_text(
        json.dumps(sorted(processed_ids), indent=2),
        encoding="utf-8",
    )


def main():
    print("Connecting to Gmail...")

    # 1. Load job description
    job_description = load_job_description()
    print("Job description loaded.")

    # 2. Load previously processed emails
    processed_ids = load_processed_emails()

    # 3. Search Gmail
    messages = search_emails(
        query=GMAIL_QUERY,
        max_results=5,
    )

    if not messages:
        print("No matching emails found.")
        return

    print(f"Found {len(messages)} email(s).")

    # 4. Process emails
    for message_item in messages:
        message_id = message_item["id"]

        if message_id in processed_ids:
            print("Email already processed. Skipping.")
            continue

        message = get_message(message_id)

        headers = message.get("payload", {}).get("headers", [])
        subject = get_header(headers, "Subject")
        sender = get_header(headers, "From")

        print("\n" + "=" * 50)
        print(f"Subject: {subject}")
        print(f"From: {sender}")

        # 5. Find CV attachments
        attachments = get_cv_attachments(message)

        if not attachments:
            print("No supported CV attachment found.")
            processed_ids.add(message_id)
            save_processed_emails(processed_ids)
            continue

        email_success = True

        # 6. Process each attachment
        for attachment in attachments:
            print(f"\nAttachment: {attachment['filename']}")

            try:
                # Download CV
                saved_path = save_attachment(
                    message_id=message_id,
                    attachment=attachment,
                    output_dir=TEMP_DIR,
                )

                # Extract CV text
                cv_text = extract_cv_text(str(saved_path))

                if not cv_text.strip():
                    print("No text could be extracted.")
                    email_success = False
                    continue

                print(f"Extracted {len(cv_text)} characters.")

                # Match CV with job description
                print("Checking CV against job requirements...")

                result = check_cv_match(
                    cv_text=cv_text,
                    job_description=job_description,
                )

                # Display results
                print("\nMatching Results:")
                print(json.dumps(result, indent=2, ensure_ascii=False))

                score = result["score"]
                
                save_candidate_result({
                    "message_id": message_id,
                    "candidate_email": sender,
                    "subject": subject,
                    "cv_filename": Path(saved_path).name,
                    "score": score,
                    "missing_must_haves": result["missing_must_haves"],
                    "requirement_results": result["requirement_results"],
                    "cv_path": str(saved_path) if score >= 50 else None,
                })

                print("Candidate result saved.")
                print(f"\nOverall Score: {score}%")

                for item in result["requirement_results"]:
                    print(f"\nRequirement: {item['requirement']}")
                    print(f"Category: {item['category']}")
                    print(f"Status: {item['status']}")
                    print(f"Explanation: {item['explanation']}")
                    print(
                        f"Semantic Similarity: "
                        f"{item['semantic_similarity']}%"
                    )

                    if item["evidence"]:
                        print("Evidence:")
                        for quote in item["evidence"]:
                            print(f"- {quote}")
                    else:
                        print("Evidence: No supporting quote found.")

                if result["missing_must_haves"]:
                    print("\nMissing or unconfirmed Must-Haves:")
                    for requirement in result["missing_must_haves"]:
                        print(f"- {requirement}")

                # Delete CV if score is below 50%
                if score < 50:
                    print("Score below 50%. Deleting CV.")
                    Path(saved_path).unlink(missing_ok=True)
                else:
                    print("Score is 50% or higher. Keeping CV.")

            except Exception as error:
                print(f"Could not process attachment: {error}")
                email_success = False

        # 7. Save email status
        if email_success:
            processed_ids.add(message_id)
            save_processed_emails(processed_ids)
            print("\nEmail processing completed.")
        else:
            print("\nEmail processing was incomplete. It can be retried.")


if __name__ == "__main__":
    main()