from pathlib import Path
import csv

# =====================================================
# CONFIG
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RESOLVED_FILE = BASE_DIR / "targets_resolved.csv"
MASTER_FILE = BASE_DIR / "targets_master.csv"

# =====================================================
# LOAD EXISTING MASTER
# =====================================================

master = {}

if MASTER_FILE.exists():

    with open(
        MASTER_FILE,
        newline="",
        encoding="utf-8"
    ) as f:

        reader = csv.DictReader(f)

        for row in reader:

            master[
                row["name"].strip().lower()
            ] = row

# =====================================================
# LOAD NEWLY RESOLVED TARGETS
# =====================================================

new_targets = 0
duplicates = 0

if not RESOLVED_FILE.exists():

    print(
        "targets_resolved.csv not found."
    )

    raise SystemExit(1)

with open(
    RESOLVED_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        key = row["name"].strip().lower()

        if key in master:

            duplicates += 1
            continue

        master[key] = row
        new_targets += 1

# =====================================================
# SAVE MASTER CATALOG
# =====================================================

sorted_rows = sorted(
    master.values(),
    key=lambda x: x["name"]
)

with open(
    MASTER_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.DictWriter(

        f,

        fieldnames=[
            "name",
            "category",
            "ra",
            "dec"
        ]

    )

    writer.writeheader()

    writer.writerows(
        sorted_rows
    )

# =====================================================
# REPORT
# =====================================================

print()
print("=" * 60)
print("QUIET SKY MASTER CATALOG")
print("=" * 60)

print()

print(
    f"New Targets      : {new_targets}"
)

print(
    f"Duplicates Skipped: {duplicates}"
)

print(
    f"Total Targets    : {len(master)}"
)

print()

print(
    f"Saved: {MASTER_FILE}"
)

print()
print("=" * 60)
print("Catalog Updated")
print("=" * 60)