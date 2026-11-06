# ai_research_journal.py

from pathlib import Path
from datetime import datetime
import csv
import json
import requests
import threading
import itertools
import time
import sys

# ============================================================
# CONFIG
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

OPTICAL_FILE = BASE_DIR / "rankings_v2.csv"
INFRARED_FILE = BASE_DIR / "infrared_rankings_v2.csv"
COMPOSITE_FILE = BASE_DIR / "quiet_sky_rankings_v3.csv"
HEALTH_FILE = BASE_DIR / "download_health_report.csv"

JOURNAL_FILE = BASE_DIR / "research_journal.md"

LLM_URL = "http://10.0.0.225:9931/v1/chat/completions"

MODEL_NAME = "default"

TOP_N = 5

# ============================================================
# UI HELPERS
# ============================================================

spinner_running = False
start_time = 0


def stage(message):

    print()
    print(f"[+] {message}")


def success(message):

    print(f"[OK] {message}")


def warning(message):

    print(f"[!] {message}")


def spinner(message):

    symbols = itertools.cycle("|/-\\")

    while spinner_running:

        elapsed = int(
            time.time() - start_time
        )

        sys.stdout.write(
            f"\r{message} "
            f"{next(symbols)} "
            f"[{elapsed}s]"
        )

        sys.stdout.flush()

        time.sleep(0.1)

    print("\r", end="")


# ============================================================
# DATA LOADERS
# ============================================================

def load_top_rows(
    filename,
    limit=TOP_N
):

    rows = []

    if not filename.exists():

        warning(
            f"Missing: {filename.name}"
        )

        return rows

    with open(
        filename,
        newline="",
        encoding="utf-8"
    ) as f:

        reader = csv.DictReader(f)

        for idx, row in enumerate(reader):

            if idx >= limit:
                break

            rows.append(row)

    return rows


def load_health():

    stats = {

        "total_targets": 0,
        "optical_ready": 0,
        "infrared_ready": 0

    }

    if not HEALTH_FILE.exists():

        warning(
            "No health report found."
        )

        return stats

    with open(
        HEALTH_FILE,
        newline="",
        encoding="utf-8"
    ) as f:

        reader = csv.DictReader(f)

        for row in reader:

            stats["total_targets"] += 1

            if (
                row.get(
                    "optical_complete",
                    ""
                )
                == "YES"
            ):

                stats["optical_ready"] += 1

            if (
                row.get(
                    "infrared_usable",
                    ""
                )
                == "YES"
            ):

                stats["infrared_ready"] += 1

    return stats


# ============================================================
# START
# ============================================================

print()
print("=" * 70)
print("           QUIET SKY AI RESEARCH JOURNAL")
print("=" * 70)

stage(
    "Loading rankings"
)

optical = load_top_rows(
    OPTICAL_FILE
)

infrared = load_top_rows(
    INFRARED_FILE
)

composite = load_top_rows(
    COMPOSITE_FILE
)

success(
    f"{len(optical)} optical candidates"
)

success(
    f"{len(infrared)} infrared candidates"
)

success(
    f"{len(composite)} composite candidates"
)

stage(
    "Loading health report"
)

health = load_health()

success(
    f"{health['total_targets']} targets"
)

success(
    f"{health['optical_ready']} optical-ready"
)

success(
    f"{health['infrared_ready']} infrared-ready"
)

# ============================================================
# BUILD PROMPT
# ============================================================

stage(
    "Building AI prompt"
)

prompt = f"""
You are the Quiet Sky astronomy research assistant.

Analyze the latest anomaly detection results.

Catalog Health:

{json.dumps(health, indent=2)}

Top Optical Candidates:

{json.dumps(optical, indent=2)}

Top Infrared Candidates:

{json.dumps(infrared, indent=2)}

Top Composite Candidates:

{json.dumps(composite, indent=2)}

Write:

1. Executive Summary

2. Most Interesting Candidate

3. Significant Ranking Changes

4. Data Quality Assessment

5. Recommended Next Actions

Rules:

- Conservative wording
- No alien speculation
- No extraordinary claims
- Focus on anomaly detection
- Professional astronomy tone
- Maximum 600 words
"""

success(
    f"Prompt size: {len(prompt):,} chars"
)

# ============================================================
# CALL QWEN
# ============================================================

stage(
    "Querying local model"
)

payload = {

    "model": MODEL_NAME,

    "messages": [

        {
            "role": "system",
            "content":
                (
                    "You are a professional "
                    "astronomy research assistant."
                )
        },

        {
            "role": "user",
            "content": prompt
        }

    ],

    "temperature": 0.3,

    "max_tokens": 800

}

try:

    start_time = time.time()

    spinner_running = True

    thread = threading.Thread(
        target=spinner,
        args=(
            "Qwen analyzing survey results",
        )
    )

    thread.start()

    response = requests.post(

        LLM_URL,

        json=payload,

        timeout=300

    )

    response.raise_for_status()

    spinner_running = False

    thread.join()

    elapsed = (
        time.time() -
        start_time
    )

    success(
        f"AI response completed in "
        f"{elapsed:.1f}s"
    )

    data = response.json()

    report = (
        data["choices"][0]
        ["message"]
        ["content"]
    )

except Exception as e:

    spinner_running = False

    print()

    print()
    print(
        "AI Journal generation failed."
    )

    print()
    print(e)

    raise SystemExit(1)

# ============================================================
# SAVE JOURNAL ENTRY
# ============================================================

stage(
    "Writing journal"
)

timestamp = datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
)

entry = f"""

# {timestamp}

## Catalog Snapshot

Targets: {health['total_targets']}

Optical Ready: {health['optical_ready']}

Infrared Ready: {health['infrared_ready']}

---

{report}

---

"""

mode = (
    "a"
    if JOURNAL_FILE.exists()
    else "w"
)

with open(
    JOURNAL_FILE,
    mode,
    encoding="utf-8"
) as f:

    f.write(entry)

success(
    f"Journal updated: "
    f"{JOURNAL_FILE.name}"
)

print()
print("=" * 70)
print("Research Journal Complete")
print("=" * 70)