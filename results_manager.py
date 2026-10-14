
import json
from pathlib import Path

RESULTS_FILE = Path("screening_results.json")


def save_candidate_result(candidate):
    if RESULTS_FILE.exists():
        candidates = json.loads(
            RESULTS_FILE.read_text(encoding="utf-8")
        )
    else:
        candidates = []

    for i, old in enumerate(candidates):
        if (
            old.get("job_title") == candidate["job_title"]
            and old["message_id"] == candidate["message_id"]
            and old["cv_filename"] == candidate["cv_filename"]
        ):
            candidates[i] = candidate
            break
    else:
        candidates.append(candidate)

    candidates.sort(
        key=lambda c: (
            bool(c["missing_must_haves"]),
            -c["score"]
        )
    )

    RESULTS_FILE.write_text(
        json.dumps(candidates, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def get_ranked_candidates(job_title=None):
    if not RESULTS_FILE.exists():
        return []

    candidates = json.loads(
        RESULTS_FILE.read_text(encoding="utf-8")
    )

    if job_title:
        candidates = [
            c for c in candidates
            if c.get("job_title") == job_title
        ]

    return sorted(
        candidates,
        key=lambda c: (
            bool(c["missing_must_haves"]),
            -c["score"]
        )
    )