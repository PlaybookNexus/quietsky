from pathlib import Path
import csv
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent.parent

RANKINGS_FILE = BASE_DIR / "rankings_v2.csv"

print()
print("=" * 72)
print("                    QUIET SKY CATEGORY REPORT")
print("=" * 72)

category_scores = defaultdict(list)
category_targets = defaultdict(list)

with open(
    RANKINGS_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        category = row["category"]
        score = float(row["score_v2"])
        name = row["name"]

        category_scores[category].append(score)

        category_targets[category].append(
            (name, score)
        )

print()
print(
    f"{'Category':<15}"
    f"{'Count':>8}"
    f"{'Avg':>12}"
    f"{'Min':>12}"
    f"{'Max':>12}"
)

print("-" * 72)

for category in sorted(category_scores):

    scores = category_scores[category]

    avg_score = sum(scores) / len(scores)

    min_score = min(scores)
    max_score = max(scores)

    print(
        f"{category:<15}"
        f"{len(scores):>8}"
        f"{avg_score:>12.4f}"
        f"{min_score:>12.4f}"
        f"{max_score:>12.4f}"
    )

print()
print("=" * 72)
print("CATEGORY LEADERS")
print("=" * 72)

for category in sorted(category_targets):

    targets = sorted(
        category_targets[category],
        key=lambda t: t[1],
        reverse=True
    )

    leader = targets[0]

    print()
    print(f"{category}")

    print(
        f"  Leader : {leader[0]}"
    )

    print(
        f"  Score  : {leader[1]:.4f}"
    )

print()
print("=" * 72)
print("TOP 3 PER CATEGORY")
print("=" * 72)

for category in sorted(category_targets):

    print()
    print(f"[{category}]")

    targets = sorted(
        category_targets[category],
        key=lambda t: t[1],
        reverse=True
    )

    for rank, (name, score) in enumerate(
        targets[:3],
        start=1
    ):

        print(
            f"  {rank}. "
            f"{name:<20} "
            f"{score:.4f}"
        )

print()
print("=" * 72)

overall_scores = []

for scores in category_scores.values():

    overall_scores.extend(scores)

if overall_scores:

    overall_avg = (
        sum(overall_scores)
        /
        len(overall_scores)
    )

    print(
        f"Overall Average Score: "
        f"{overall_avg:.4f}"
    )

print("=" * 72)
