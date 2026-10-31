from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent.parent

ORIGINAL_FILE = BASE_DIR / "targets.csv"
RESOLVED_FILE = BASE_DIR / "targets_resolved.csv"

OUTPUT_FILE = BASE_DIR / "targets_beta.csv"

targets = {}
total_original = 0
total_added = 0

#
# Load original targets
#

with open(
    ORIGINAL_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        targets[row["name"]] = row
        total_original += 1

#
# Add newly resolved targets
#

with open(
    RESOLVED_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        name = row["name"]

        if name not in targets:

            targets[name] = row
            total_added += 1

#
# Sort alphabetically
#

sorted_targets = sorted(
    targets.values(),
    key=lambda r: r["name"]
)

#
# Save beta catalog
#

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow([
        "name",
        "category",
        "ra",
        "dec"
    ])

    for target in sorted_targets:

        writer.writerow([

            target["name"],
            target["category"],
            target["ra"],
            target["dec"]

        ])

print()
print("=" * 60)
print("Quiet Sky Beta Catalog")
print("=" * 60)

print(
    f"Original targets : {total_original}"
)

print(
    f"Added targets    : {total_added}"
)

print(
    f"Total targets    : {len(sorted_targets)}"
)

print()
print(
    f"Saved: {OUTPUT_FILE}"
)

print("=" * 60)