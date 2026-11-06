# optical_beta_report.py

from pathlib import Path
import csv
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent.parent

RANKINGS_FILE = BASE_DIR / "rankings_v2.csv"

print()
print("=" * 80)
print("                QUIET SKY BETA OPTICAL REPORT")
print("=" * 80)

targets = []

with open(
    RANKINGS_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        row["rank"] = int(row["rank"])
        row["score"] = float(row["score_v2"])

        targets.append(row)

targets.sort(
    key=lambda r: r["score"],
    reverse=True
)

#
# Top candidates
#

print()
print("TOP OPTICAL CANDIDATES")
print("-" * 80)

for row in targets[:10]:

    print(
        f"#{row['rank']:<2} "
        f"{row['name']:<25} "
        f"{row['score']:.4f}"
    )

#
# Category leaders
#

print()
print("CATEGORY LEADERS")
print("-" * 80)

leaders = {}

for row in targets:

    category = row["category"]

    if category not in leaders:

        leaders[category] = row

for category in sorted(leaders):

    leader = leaders[category]

    print(
        f"{category:<15} "
        f"{leader['name']:<25} "
        f"{leader['score']:.4f}"
    )

#
# Category averages
#

print()
print("CATEGORY AVERAGES")
print("-" * 80)

scores = defaultdict(list)

for row in targets:

    scores[row["category"]].append(
        row["score"]
    )

for category in sorted(scores):

    avg = sum(
        scores[category]
    ) / len(scores[category])

    print(
        f"{category:<15} "
        f"{avg:.4f}"
    )

#
# Discovery section
#

print()
print("OPTICAL DISCOVERIES")
print("-" * 80)

for row in targets[:10]:

    if row["name"] not in [

        "KIC 8462852",
        "TRAPPIST-1",
        "HD 189733",
        "Kepler-186",
        "Delta Cephei",
        "Barnards Star"

    ]:

        print(
            f"NEW HIGH RANKING TARGET: "
            f"{row['name']} "
            f"({row['category']}) "
            f"Score={row['score']:.4f}"
        )

#
# Interesting shifts
#

print()
print("KNOWN TARGET CHECK")
print("-" * 80)

watchlist = [

    "KIC 8462852",
    "TRAPPIST-1",
    "HD 189733",
    "Kepler-186",
    "Delta Cephei",
    "Barnards Star"

]

for name in watchlist:

    match = next(

        (
            t
            for t in targets
            if t["name"] == name
        ),

        None

    )

    if match:

        print(

            f"{match['name']:<20}"

            f"Rank: #{match['rank']:<3}"

            f"Score: {match['score']:.4f}"

        )

#
# Conclusions
#

print()
print("CONCLUSIONS")
print("-" * 80)

top = targets[0]

print()

print(
    f"Strongest Optical Target: "
    f"{top['name']}"
)

print(
    f"Optical Score: "
    f"{top['score']:.4f}"
)

print()

print(
    "Primary Beta objective:"
)

print(
    "Determine whether newly-added catalog "
    "targets begin displacing original "
    "seed candidates from the Top 10."
)

print()

print(
    "A new target entering the Top 10 "
    "would indicate Quiet Sky is "
    "transitioning from validation "
    "to discovery."
)

print()
print("=" * 80)
print("Optical report complete.")
print("=" * 80)