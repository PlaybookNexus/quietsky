# merge_resolved_catalogs.py

from pathlib import Path
import csv

# =====================================================
# CONFIG
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PASS1_FILE = (
    BASE_DIR /
    "targets_resolved.csv"
)

PASS2_FILE = (
    BASE_DIR /
    "targets_resolved_pass2.csv"
)

OUTPUT_FILE = (
    BASE_DIR /
    "targets_resolved_master.csv"
)

# =====================================================
# LOAD PASS 1
# =====================================================

master = {}
count_pass1 = 0

with open(
    PASS1_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        name = row["name"].strip()

        master[name] = {

            "name": name,
            "category": row["category"],

            "ra_deg": row["ra_deg"],
            "dec_deg": row["dec_deg"]

        }

        count_pass1 += 1

# =====================================================
# LOAD PASS 2
# =====================================================

count_pass2 = 0
added_pass2 = 0

with open(
    PASS2_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        count_pass2 += 1

        original_name = row[
            "original_name"
        ].strip()

        if original_name in master:
            continue

        master[original_name] = {

            "name":
                original_name,

            "category":
                row["category"],

            "ra_deg":
                row["ra_deg"],

            "dec_deg":
                row["dec_deg"]

        }

        added_pass2 += 1

# =====================================================
# SORT OUTPUT
# =====================================================

rows = sorted(
    master.values(),
    key=lambda x:
        x["name"].lower()
)

# =====================================================
# WRITE MASTER FILE
# =====================================================

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[

            "name",
            "category",

            "ra_deg",
            "dec_deg"

        ]
    )

    writer.writeheader()

    writer.writerows(
        rows
    )

# =====================================================
# SUMMARY
# =====================================================

print()
print("=" * 60)
print("MERGE COMPLETE")
print("=" * 60)
print()

print(
    f"Pass 1 Resolved : {count_pass1}"
)

print(
    f"Pass 2 Resolved : {count_pass2}"
)

print(
    f"Added From Pass 2 : {added_pass2}"
)

print()

print(
    f"Master Catalog : {len(rows)}"
)

print()

print(
    f"Output File : {OUTPUT_FILE}"
)

print()