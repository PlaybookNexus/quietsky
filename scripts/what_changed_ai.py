from pathlib import Path
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

MEMORY_FILE = BASE_DIR / "project_memory.json"

OUTPUT_FILE = BASE_DIR / "what_changed_report.md"

LLM_URL = "http://10.0.0.225:9931/v1/chat/completions"

MODEL = "default"

# =====================================================
# SPINNER
# =====================================================

spinner_running = False


def spinner():

    chars = itertools.cycle("|/-\\")

    while spinner_running:

        sys.stdout.write(
            f"\rAnalyzing changes {next(chars)}"
        )

        sys.stdout.flush()

        time.sleep(0.1)

    print("\r", end="")


# =====================================================
# LOAD MEMORY
# =====================================================

print()
print("=" * 60)
print("QUIET SKY AI CHANGE ANALYSIS")
print("=" * 60)

if not MEMORY_FILE.exists():

    print()
    print(
        "No project memory found."
    )

    raise SystemExit(1)

memory = json.loads(

    MEMORY_FILE.read_text(
        encoding="utf-8"
    )

)

runs = memory.get(
    "runs",
    []
)

if len(runs) < 2:

    print()
    print(
        "Need at least two snapshots."
    )

    raise SystemExit(1)

previous = runs[-2]
current = runs[-1]

# =====================================================
# BUILD CHANGE DATA
# =====================================================

change_data = {

    "previous": previous,
    "current": current

}

print()
print(
    f"Comparing:"
)

print(
    previous["timestamp"]
)

print(
    current["timestamp"]
)

# =====================================================
# BUILD PROMPT
# =====================================================

prompt = f"""
You are the Quiet Sky AI research analyst.

Compare these two project snapshots.

Data:

{json.dumps(change_data, indent=2)}

Generate:

1. Executive Summary

2. Important Changes

3. Candidate Changes

4. Data Quality Changes

5. Scientific Significance

6. Recommended Next Steps

Requirements:

- Use conservative language
- No speculation about extraterrestrials
- Explain why changes matter
- Maximum 600 words
"""

payload = {

    "model": MODEL,

    "messages": [

        {
            "role": "system",
            "content":
            (
                "You are a professional "
                "astronomy research analyst."
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

# =====================================================
# QUERY QWEN
# =====================================================

print()
print(
    "Querying local model..."
)

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
        f"Complete "
        f"({elapsed:.1f}s)"
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
    print(
        "AI request failed."
    )

    print(e)

    raise SystemExit(1)

# =====================================================
# SAVE REPORT
# =====================================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "# Quiet Sky Change Report\n\n"
    )

    f.write(report)

print()
print(
    f"Saved: {OUTPUT_FILE.name}"
)

print()
print("=" * 60)
print("WHAT CHANGED?")
print("=" * 60)
print()

print(report)

print()
print("=" * 60)
print("Analysis Complete")
print("=" * 60)