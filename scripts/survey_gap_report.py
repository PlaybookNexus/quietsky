# survey_gap_report.py

from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "infrared_results.csv"

BANDS = [

    ("j_ratio",      "2MASS J"),
    ("k_ratio",      "2MASS K"),
    ("wise34_ratio", "WISE 3.4"),
    ("wise46_ratio", "WISE 4.6")

]

print()
print("=" * 72)
print("                  QUIET SKY SURVEY GAP REPORT")
print("=" * 72)

targets = []

with open(
    INPUT_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        missing = []

        available = 0

        for field, label in BANDS:

            value = row.get(field)

            if value is None:

                missing.append(label)
                continue

            value = str(value).strip()

            if value == "":
                missing.append(label)

            else:
                available += 1

        targets.append({

            "name":
                row["name"],

            "category":
                row["category"],

            "available":
                available,

            "missing":
                missing
        })

#
# Sort worst coverage first
#

targets.sort(
    key=lambda t:
        len(t["missing"]),
    reverse=True
)

print()

print(
    f"{'Target':<22}"
    f"{'Category':<12}"
    f"{'Coverage':<10}"
    f"{'Missing'}"
)

print("-" * 72)

for target in targets:

    coverage = (
        f"{target['available']}/4"
    )

    missing_text = (
        ", ".join(target["missing"])
        if target["missing"]
        else "None"
    )

    print(
        f"{target['name']:<22}"
        f"{target['category']:<12}"
        f"{coverage:<10}"
        f"{missing_text}"
    )

#
# Summary
#

total_targets = len(targets)

fully_covered = sum(
    1
    for t in targets
    if t["available"] == 4
)

partial_covered = sum(
    1
    for t in targets
    if 0 < t["available"] < 4
)

zero_covered = sum(
    1
    for t in targets
    if t["available"] == 0
)

print()
print("SUMMARY")
print("-" * 72)

print(
    f"Targets                : {total_targets}"
)

print(
    f"Full IR Coverage       : {fully_covered}"
)

print(
    f"Partial IR Coverage    : {partial_covered}"
)

print(
    f"No IR Coverage         : {zero_covered}"
)

#
# Priority list
#

print()
print("HIGH PRIORITY IR GAPS")
print("-" * 72)

for target in targets:

    if target["available"] == 0:

        print(
            f"{target['name']} "
            f"({target['category']})"
        )

print()
print("=" * 72)
print("Survey gap analysis complete.")
print("=" * 72)