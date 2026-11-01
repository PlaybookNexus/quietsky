# project_memory.py

from pathlib import Path
from datetime import datetime
import csv
import json

# =====================================================
# CONFIG
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MEMORY_FILE = BASE_DIR / "project_memory.json"

HEALTH_FILE = BASE_DIR / "download_health_report.csv"

OPTICAL_FILE = BASE_DIR / "rankings_v2.csv"
INFRARED_FILE = BASE_DIR / "infrared_rankings_v2.csv"
COMPOSITE_FILE = BASE_DIR / "quiet_sky_rankings_v3.csv"

# =====================================================
# HELPERS
# =====================================================

def load_health():

    result = {

        "catalog_targets": 0,
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

            result["catalog_targets"] += 1

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


def load_top_candidate(
    csv_file
):

    if not csv_file.exists():

        return None

    try:

        with open(
            csv_file,
            newline="",
            encoding="utf-8"
        ) as f:

            reader = csv.DictReader(f)

            return next(reader)

    except Exception:

        return None


# =====================================================
# LOAD CURRENT STATUS
# =====================================================

print()
print("=" * 60)
print("QUIET SKY PROJECT MEMORY")
print("=" * 60)

health = load_health()

optical = load_top_candidate(
    OPTICAL_FILE
)

infrared = load_top_candidate(
    INFRARED_FILE
)

composite = load_top_candidate(
    COMPOSITE_FILE
)

snapshot = {

    "timestamp":
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

    "catalog_targets":
        health["catalog_targets"],

    "optical_ready":
        health["optical_ready"],

    "infrared_ready":
        health["infrared_ready"],

    "top_optical":
        (
            optical["name"]
            if optical
            else None
        ),

    "top_infrared":
        (
            infrared["name"]
            if infrared
            else None
        ),

    "top_composite":
        (
            composite["name"]
            if composite
            else None
        )

}

# =====================================================
# LOAD EXISTING MEMORY
# =====================================================

if MEMORY_FILE.exists():

    try:

        memory = json.loads(
            MEMORY_FILE.read_text(
                encoding="utf-8"
            )
        )

    except Exception:

        memory = {"runs": []}

else:

    memory = {"runs": []}

# =====================================================
# APPEND SNAPSHOT
# =====================================================

memory["runs"].append(
    snapshot
)

MEMORY_FILE.write_text(

    json.dumps(
        memory,
        indent=2
    ),

    encoding="utf-8"

)

# =====================================================
# DISPLAY
# =====================================================

print()

print(
    f"Timestamp       : "
    f"{snapshot['timestamp']}"
)

print(
    f"Catalog Targets : "
    f"{snapshot['catalog_targets']}"
)

print(
    f"Optical Ready   : "
    f"{snapshot['optical_ready']}"
)

print(
    f"Infrared Ready  : "
    f"{snapshot['infrared_ready']}"
)

print()

print(
    f"Top Optical     : "
    f"{snapshot['top_optical']}"
)

print(
    f"Top Infrared    : "
    f"{snapshot['top_infrared']}"
)

print(
    f"Top Composite   : "
    f"{snapshot['top_composite']}"
)

print()

print(
    f"Memory File     : "
    f"{MEMORY_FILE.name}"
)

print(
    f"Total Runs      : "
    f"{len(memory['runs'])}"
)

print()

print("=" * 60)
print("Memory Updated")
print("=" * 60)