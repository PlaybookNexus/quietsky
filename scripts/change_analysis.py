# change_analysis.py

from pathlib import Path
import json

# =====================================================
# CONFIG
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MEMORY_FILE = BASE_DIR / "project_memory.json"

# =====================================================
# LOAD MEMORY
# =====================================================

print()
print("=" * 60)
print("QUIET SKY CHANGE ANALYSIS")
print("=" * 60)

if not MEMORY_FILE.exists():

    print()
    print("No project memory found.")
    print("Run project_memory.py first.")
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
        "At least two snapshots are required."
    )

    print(
        "Run project_memory.py again after "
        "another analysis cycle."
    )

    raise SystemExit(1)

# =====================================================
# SELECT SNAPSHOTS
# =====================================================

previous = runs[-2]
current = runs[-1]

# =====================================================
# HELPERS
# =====================================================

def delta(old, new):

    change = new - old

    if change > 0:
        return f"+{change}"

    return str(change)


print()
print(
    f"Previous Run : "
    f"{previous['timestamp']}"
)

print(
    f"Current Run  : "
    f"{current['timestamp']}"
)

print()

print("=" * 60)
print("DATASET CHANGES")
print("=" * 60)

print()

catalog_change = delta(
    previous["catalog_targets"],
    current["catalog_targets"]
)

print(
    f"Catalog Targets : "
    f"{previous['catalog_targets']} -> "
    f"{current['catalog_targets']} "
    f"({catalog_change})"
)

optical_change = delta(
    previous["optical_ready"],
    current["optical_ready"]
)

print(
    f"Optical Ready   : "
    f"{previous['optical_ready']} -> "
    f"{current['optical_ready']} "
    f"({optical_change})"
)

infrared_change = delta(
    previous["infrared_ready"],
    current["infrared_ready"]
)

print(
    f"Infrared Ready  : "
    f"{previous['infrared_ready']} -> "
    f"{current['infrared_ready']} "
    f"({infrared_change})"
)

print()

print("=" * 60)
print("LEADER CHANGES")
print("=" * 60)

print()

#
# Optical
#

if (
    previous["top_optical"]
    ==
    current["top_optical"]
):

    print(
        f"Optical Leader : "
        f"UNCHANGED "
        f"({current['top_optical']})"
    )

else:

    print(
        f"Optical Leader : "
        f"{previous['top_optical']} -> "
        f"{current['top_optical']}"
    )

#
# Infrared
#

if (
    previous["top_infrared"]
    ==
    current["top_infrared"]
):

    print(
        f"Infrared Leader : "
        f"UNCHANGED "
        f"({current['top_infrared']})"
    )

else:

    print(
        f"Infrared Leader : "
        f"{previous['top_infrared']} -> "
        f"{current['top_infrared']}"
    )

#
# Composite
#

if (
    previous["top_composite"]
    ==
    current["top_composite"]
):

    print(
        f"Composite Leader : "
        f"UNCHANGED "
        f"({current['top_composite']})"
    )

else:

    print(
        f"Composite Leader : "
        f"{previous['top_composite']} -> "
        f"{current['top_composite']}"
    )

print()

print("=" * 60)
print("ASSESSMENT")
print("=" * 60)

print()

if (

    previous["catalog_targets"]
    ==
    current["catalog_targets"]

    and

    previous["optical_ready"]
    ==
    current["optical_ready"]

    and

    previous["infrared_ready"]
    ==
    current["infrared_ready"]

):

    print(
        "No dataset growth detected."
    )

else:

    print(
        "Dataset changes detected."
    )

if (
    current["infrared_ready"]
    >
    previous["infrared_ready"]
):

    print(
        "Infrared coverage improved."
    )

if (
    current["optical_ready"]
    >
    previous["optical_ready"]
):

    print(
        "Optical coverage improved."
    )

if (
    current["top_composite"]
    !=
    previous["top_composite"]
):

    print(
        "Composite leadership changed."
    )

print()

print("=" * 60)
print("Analysis Complete")
print("=" * 60)