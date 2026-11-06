from pathlib import Path
import csv
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent.parent

RANKINGS_FILE = BASE_DIR / "rankings.csv"

print()
print("=" * 72)
print("                QUIET SKY DASHBOARD")
print("=" * 72)

targets = []

with open(
    RANKINGS_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        try:

            row["rank"] = int(
                row["rank"]
            )

            row["score"] = float(
                row["anomaly_score"]
            )

            targets.append(row)

        except Exception:

            continue

#
# Top 10
#

print()
print("TOP TARGETS")
print("-" * 72)

for target in targets[:10]:

    score = target["score"]

    if score > 1.0:
        flag = "🔴"
    elif score > 0.3:
        flag = "🟡"
    else:
        flag = "🟢"

    print(
        f"{target['rank']:>2}. "
        f"{target['name']:<20} "
        f"{target['category']:<12} "
        f"{score:>8.4f} "
        f"{flag}"
    )

#
# Category stats
#

category_scores = defaultdict(list)

for target in targets:

    category_scores[
        target["category"]
    ].append(
        target["score"]
    )

print()
print("CATEGORY AVERAGES")
print("-" * 72)

for category, scores in sorted(
    category_scores.items()
):

    avg_score = (
        sum(scores) /
        len(scores)
    )

    print(
        f"{category:<15} "
        f"{avg_score:.4f}"
    )

#
# Highest score
#

if targets:

    top = targets[0]

    print()
    print("HIGHEST ANOMALY")
    print("-" * 72)

    print(
        f"Target   : {top['name']}"
    )

    print(
        f"Category : {top['category']}"
    )

    print(
        f"Score    : "
        f"{top['score']:.4f}"
    )

#
# Histogram
#

print()
print("ANOMALY DISTRIBUTION")
print("-" * 72)

for target in targets:

    bars = int(
        target["score"] * 20
    )

    bars = max(
        bars,
        1
    )

    print(
        f"{target['name'][:18]:<18} "
        f"{'#' * bars}"
    )

print()
print("=" * 72)
print(
    f"Targets analyzed: "
    f"{len(targets)}"
)
print("=" * 72)