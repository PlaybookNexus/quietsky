from pathlib import Path
import csv
import json
import requests
import threading
import itertools
import time
import sys

# =====================================================
# CONFIG
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

OPTICAL_FILE = BASE_DIR / "rankings_v2.csv"
INFRARED_FILE = BASE_DIR / "infrared_rankings_v2.csv"
COMPOSITE_FILE = BASE_DIR / "quiet_sky_rankings_v3.csv"
HEALTH_FILE = BASE_DIR / "download_health_report.csv"

OUTPUT_FILE = BASE_DIR / "ai_findings_report.md"

LLM_URL = "http://10.0.0.225:9931/v1/chat/completions"

MODEL = "default"

TOP_N = 10

# =====================================================
# SPINNER
# =====================================================

spinner_running = False


def spinner():

    chars = itertools.cycle("|/-\\")

    while spinner_running:

        sys.stdout.write(
            f"\rQwen analyzing "
            f"{next(chars)}"
        )

        sys.stdout.flush()

        time.sleep(0.1)

    print("\r", end="")


# =====================================================
# CSV LOADERS
# =====================================================

def load_top_rows(path, limit=TOP_N):

    rows = []

    if not path.exists():
        return rows

    with open(
        path,
        newline="",
        encoding="utf-8"
    ) as f:

        reader = csv.DictReader(f)

        for i, row in enumerate(reader):

            if i >= limit:
                break

            rows.append(row)

    return rows


def load_health():

    result = {

        "targets": 0,
        "optical_ready": 0,
        "infrared_ready": 0

    }

    if not HEALTH_FILE.exists():
        return result

    with open(
        HEALTH_FILE,
        newline="",
        encoding="utf-8"
    ) as f:

        reader = csv.DictReader(f)

        for row in reader:

            result["targets"] += 1

            if (
                row.get(
                    "optical_complete",
                    ""
                ) == "YES"
            ):
                result["optical_ready"] += 1

            if (
                row.get(
                    "infrared_usable",
                    ""
                ) == "YES"
            ):
                result["infrared_ready"] += 1

    return result


# =====================================================
# START
# =====================================================

print()
print("=" * 60)
print("QUIET SKY AI DISCOVERY ASSISTANT")
print("=" * 60)

print()
print("[1/5] Loading rankings")

optical = load_top_rows(
    OPTICAL_FILE
)

infrared = load_top_rows(
    INFRARED_FILE
)

composite = load_top_rows(
    COMPOSITE_FILE
)

print(
    f"       Optical:   {len(optical)}"
)

print(
    f"       Infrared:  {len(infrared)}"
)

print(
    f"       Composite: {len(composite)}"
)

print()
print("[2/5] Loading health report")

health = load_health()

print(
    f"       Targets:         {health['targets']}"
)

print(
    f"       Optical Ready:   {health['optical_ready']}"
)

print(
    f"       Infrared Ready:  {health['infrared_ready']}"
)

print()
print("[3/5] Building AI prompt")

prompt = f"""
You are the Quiet Sky AI astronomy analyst.

Analyze the survey results below.

CATALOG HEALTH:

{json.dumps(health, indent=2)}

TOP OPTICAL TARGETS:

{json.dumps(optical, indent=2)}

TOP INFRARED TARGETS:

{json.dumps(infrared, indent=2)}

TOP COMPOSITE TARGETS:

{json.dumps(composite, indent=2)}

Generate:

1. Executive Summary

2. Most Interesting Candidate

3. Notable Ranking Patterns

4. Data Quality Assessment

5. Recommended Next Steps

Requirements:

- Professional research style
- No speculation about extraterrestrials
- Conservative scientific language
- Mention specific targets
- Maximum 800 words
"""

print(
    f"       Prompt Size: {len(prompt):,} chars"
)

print()
print("[4/5] Querying local Qwen")

payload = {

    "model": MODEL,

    "messages": [

        {
            "role": "system",
            "content":
            (
                "You are an astronomy "
                "research assistant."
            )
        },

        {
            "role": "user",
            "content": prompt
        }

    ],

    "temperature": 0.3,
    "max_tokens": 1200

}

spinner_running = True

thread = threading.Thread(
    target=spinner
)

thread.start()

start = time.time()

try:

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
        start
    )

    print(
        f"       Complete ({elapsed:.1f}s)"
    )

    data = response.json()

    report = (
        data["choices"][0]
        ["message"]
        ["content"]
    )

except Exception as e:

    spinner_running = False

    thread.join()

    print()
    print("AI request failed")
    print(e)

    raise SystemExit(1)

print()
print("[5/5] Saving report")

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "# Quiet Sky AI Findings\n\n"
    )

    f.write(report)

print(
    f"       Saved: {OUTPUT_FILE.name}"
)

print()
print("=" * 60)
print("AI DISCOVERY ANALYSIS")
print("=" * 60)
print()

print(report)

print()
print("=" * 60)
print("Analysis Complete")
print("=" * 60)