from pathlib import Path
from datetime import datetime
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
JOURNAL_FILE = BASE_DIR / "research_journal.md"

LLM_URL = "http://127.0.0.1:9931/v1/chat/completions"

MODEL = "default"

TOP_N = 10

# =====================================================
# LOGGING
# =====================================================

LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(
    exist_ok=True
)

SESSION_ID = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)

LOG_FILE = (
    LOG_DIR /
    f"quiet_sky_chat_{SESSION_ID}.md"
)

with open(
    LOG_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "# Quiet Sky Chat Session\n\n"
    )

    f.write(
        f"Session ID: {SESSION_ID}\n\n"
    )

    f.write(
        f"Started: {datetime.now()}\n\n"
    )

    f.write("---\n\n")

# =====================================================
# SPINNER
# =====================================================

spinner_running = False


def spinner():

    chars = itertools.cycle("|/-\\")

    while spinner_running:

        sys.stdout.write(
            f"\rThinking {next(chars)}"
        )

        sys.stdout.flush()

        time.sleep(0.1)

    print("\r", end="")


# =====================================================
# HELPERS
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

    stats = {

        "targets": 0,
        "optical_ready": 0,
        "infrared_ready": 0

    }

    if not HEALTH_FILE.exists():
        return stats

    with open(
        HEALTH_FILE,
        newline="",
        encoding="utf-8"
    ) as f:

        reader = csv.DictReader(f)

        for row in reader:

            stats["targets"] += 1

            if (
                row.get(
                    "optical_complete",
                    ""
                ) == "YES"
            ):
                stats["optical_ready"] += 1

            if (
                row.get(
                    "infrared_usable",
                    ""
                ) == "YES"
            ):
                stats["infrared_ready"] += 1

    return stats


def load_journal_tail():

    if not JOURNAL_FILE.exists():
        return ""

    try:

        text = JOURNAL_FILE.read_text(
            encoding="utf-8"
        )

        return text[-5000:]

    except Exception:

        return ""


# =====================================================
# LOAD DATA
# =====================================================

print()
print("=" * 60)
print("ASK QUIET SKY")
print("=" * 60)

print()
print(f"Session ID : {SESSION_ID}")
print(f"Chat Log   : {LOG_FILE}")
print(f"Journal    : {JOURNAL_FILE.name}")
print(f"Log Exists : {LOG_FILE.exists()}")

optical = load_top_rows(
    OPTICAL_FILE
)

infrared = load_top_rows(
    INFRARED_FILE
)

composite = load_top_rows(
    COMPOSITE_FILE
)

health = load_health()

journal = load_journal_tail()

print()

print(
    f"Targets         : {health['targets']}"
)

print(
    f"Optical Ready   : {health['optical_ready']}"
)

print(
    f"Infrared Ready  : {health['infrared_ready']}"
)

print()
print("Type 'exit' to quit.")

# =====================================================
# CHAT LOOP
# =====================================================

while True:

    print()

    question = input(
        "Quiet Sky > "
    ).strip()

    if not question:
        continue

    if question.lower() in (
        "exit",
        "quit",
        "q"
    ):
        break

    #
    # LOG QUESTION
    #

    question_time = datetime.now()

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            "## User\n\n"
        )

        f.write(
            f"Time: {question_time}\n\n"
        )

        f.write(
            question
        )

        f.write("\n\n")

    #
    # BUILD PROMPT
    #

    system_prompt = f"""
You are Quiet Sky's AI astronomy analyst.

You answer questions using:

- optical anomaly rankings
- infrared rankings
- composite rankings
- health metrics
- previous research journal entries

Use conservative scientific language.

Do not speculate about extraterrestrials.

If evidence is insufficient,
say so clearly.

Catalog Health:

{json.dumps(health, indent=2)}

Top Optical:

{json.dumps(optical, indent=2)}

Top Infrared:

{json.dumps(infrared, indent=2)}

Top Composite:

{json.dumps(composite, indent=2)}

Recent Journal:

{journal}
"""

    payload = {

        "model": MODEL,

        "messages": [

            {
                "role": "system",
                "content": system_prompt
            },

            {
                "role": "user",
                "content": question
            }

        ],

        "temperature": 0.3,

        "max_tokens": 1000

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

        data = response.json()

        answer = (
            data["choices"][0]
            ["message"]
            ["content"]
        )

        #
        # LOG ANSWER
        #

        with open(
            LOG_FILE,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                "## Quiet Sky AI\n\n"
            )

            f.write(
                f"Response Time: {elapsed:.1f}s\n\n"
            )

            f.write(answer)

            f.write(
                "\n\n---\n\n"
            )

        print()
        print(
            f"[{elapsed:.1f}s]"
        )

        print()
        print(answer)

    except Exception as e:

        spinner_running = False

        thread.join()

        print()
        print("Request failed")
        print(e)

        with open(
            LOG_FILE,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                "## Error\n\n"
            )

            f.write(
                str(e)
            )

            f.write(
                "\n\n---\n\n"
            )

print()
print("Goodbye.")
print(
    f"Session saved: {LOG_FILE}"
)