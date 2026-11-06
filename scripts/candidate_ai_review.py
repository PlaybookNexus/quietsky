from pathlib import Path
from datetime import datetime
import csv
import json
import requests
import sys

# =====================================================
# CONFIG
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RANKINGS_FILE = BASE_DIR / "rankings_v2.csv"
CATEGORY_FILE = BASE_DIR / "category_rankings.csv"

REVIEWS_DIR = BASE_DIR / "reviews"

AI_ENDPOINT = (
    "http://10.0.0.225:9931/v1/chat/completions"
)

AI_MODEL = "gpt-oss"

TIMEOUT = 300

# =====================================================
# TARGET
# =====================================================

if len(sys.argv) < 2:

    print()
    print(
        'Usage: python candidate_ai_review.py "Ross 640"'
    )
    print()

    raise SystemExit(1)

TARGET_NAME = " ".join(
    sys.argv[1:]
).strip()

# =====================================================
# TIMESTAMP
# =====================================================

now = datetime.now()

timestamp = now.strftime(
    "%Y%m%d_%H%M%S"
)

display_time = now.strftime(
    "%Y-%m-%d %H:%M:%S"
)

# =====================================================
# LOAD GLOBAL RANKINGS
# =====================================================

global_data = {}

with open(
    RANKINGS_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    rows = sorted(
        reader,
        key=lambda r: float(
            r["score_v2"]
        ),
        reverse=True
    )

    for rank, row in enumerate(
        rows,
        start=1
    ):
        global_data[row["name"]] = {

            "rank":
                rank,

            "score":
                float(
                    row["score_v2"]
                ),

            "category":
                row["category"]

        }

# =====================================================
# LOAD CATEGORY DATA
# =====================================================

category_data = {}

with open(
    CATEGORY_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        category_data[
            row["name"]
        ] = {

            "category":
                row["category"],

            "category_rank":
                int(
                    row["rank"]
                ),

            "z_score":
                float(
                    row["z_score"]
                )

        }

# =====================================================
# VALIDATE
# =====================================================

if TARGET_NAME not in global_data:

    print()
    print(
        f"Target not found: "
        f"{TARGET_NAME}"
    )

    raise SystemExit(1)

if TARGET_NAME not in category_data:

    print()
    print(
        f"Target missing from "
        f"category ranking file."
    )

    raise SystemExit(1)

# =====================================================
# BUILD EVIDENCE PACKAGE
# =====================================================

global_rank = (
    global_data[TARGET_NAME]
    ["rank"]
)

raw_score = (
    global_data[TARGET_NAME]
    ["score"]
)

category = (
    category_data[TARGET_NAME]
    ["category"]
)

category_rank = (
    category_data[TARGET_NAME]
    ["category_rank"]
)

z_score = (
    category_data[TARGET_NAME]
    ["z_score"]
)

evidence = {

    "target":
        TARGET_NAME,

    "category":
        category,

    "global_rank":
        global_rank,

    "category_rank":
        category_rank,

    "raw_score":
        raw_score,

    "z_score":
        z_score

}

# =====================================================
# PROMPT
# =====================================================

prompt = f"""
You are the Quiet Sky AI Review Board.

Your role is to critically evaluate astronomical candidates.

You must be skeptical.

Do not claim evidence for extraterrestrial intelligence.

Prefer natural explanations whenever possible.

Candidate Data:

{json.dumps(evidence, indent=2)}

Provide the following sections:

1. Executive Summary

2. Why This Candidate Ranked Highly

3. Plausible Natural Explanations

4. Possible Measurement Artifacts

5. Follow-Up Observations Recommended

6. Technosignature Relevance

Choose one:
LOW
MEDIUM
HIGH

Explain why.

7. Final Recommendation

Choose one:

IGNORE
MONITOR
REVIEW
HIGH PRIORITY REVIEW

Be concise but scientific.
"""

# =====================================================
# CALL AI
# =====================================================

print()
print("=" * 72)
print("QUIET SKY AI REVIEW BOARD")
print("=" * 72)

print()
print(
    f"Generating review for "
    f"{TARGET_NAME}..."
)
print()

try:

    response = requests.post(

        AI_ENDPOINT,

        json={

            "model":
                AI_MODEL,

            "messages": [

                {
                    "role": "system",

                    "content":
                    (
                        "You are an astronomy "
                        "review board."
                    )
                },

                {
                    "role": "user",

                    "content":
                    prompt
                }

            ],

            "temperature": 0.2,
            "max_tokens": 1200

        },

        timeout=TIMEOUT

    )

    response.raise_for_status()

    result = response.json()

    ai_review = (
        result["choices"][0]
        ["message"]["content"]
    )

except Exception as e:

    ai_review = (
        "AI REVIEW FAILED\n\n"
        f"{e}"
    )

# =====================================================
# EXPORT
# =====================================================

safe_name = (
    TARGET_NAME
    .replace(" ", "_")
    .replace("/", "_")
    .replace("'", "")
)

outfile = (

    REVIEWS_DIR /

    f"{safe_name}_ai_review_{timestamp}.txt"

)

with open(
    outfile,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "=" * 72 +
        "\n"
    )

    f.write(
        "QUIET SKY AI CANDIDATE REVIEW\n"
    )

    f.write(
        "=" * 72 +
        "\n\n"
    )

    f.write(
        f"Generated: "
        f"{display_time}\n\n"
    )

    f.write(
        "Evidence Package\n"
    )

    f.write(
        "-" * 72 +
        "\n"
    )

    f.write(
        json.dumps(
            evidence,
            indent=2
        )
    )

    f.write(
        "\n\n"
    )

    f.write(
        "AI Assessment\n"
    )

    f.write(
        "-" * 72 +
        "\n"
    )

    f.write(
        ai_review
    )

print()
print(
    f"Review Complete"
)

print()

print(
    f"Target : {TARGET_NAME}"
)

print(
    f"Output : {outfile}"
)

print()