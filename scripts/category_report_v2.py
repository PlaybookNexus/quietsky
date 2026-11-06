from pathlib import Path
import csv
import statistics
from collections import defaultdict

# =====================================================
# CONFIG
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RANKINGS_FILE = BASE_DIR / "rankings_v2.csv"

CATEGORY_RANKINGS_FILE = (
    BASE_DIR / "category_rankings.csv"
)

OUTLIERS_FILE = (
    BASE_DIR / "category_outliers.csv"
)

# =====================================================
# LOAD DATA
# =====================================================

print()
print("=" * 72)
print("           QUIET SKY CATEGORY REPORT V2")
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
        name = row["name"]
        score = float(row["score_v2"])

        category_scores[category].append(
            score
        )

        category_targets[category].append({

            "name": name,
            "score": score

        })

# =====================================================
# CATEGORY STATISTICS
# =====================================================

category_stats = {}

print()
print(
    f"{'Category':<20}"
    f"{'Count':>8}"
    f"{'Average':>12}"
    f"{'StdDev':>12}"
    f"{'Min':>12}"
    f"{'Max':>12}"
)

print("-" * 76)

for category in sorted(category_scores):

    scores = category_scores[category]

    count = len(scores)
    avg_score = statistics.mean(scores)

    if count > 1:
        stddev = statistics.stdev(scores)
    else:
        stddev = 0

    min_score = min(scores)
    max_score = max(scores)

    category_stats[category] = {

        "count": count,
        "avg": avg_score,
        "stddev": stddev,
        "min": min_score,
        "max": max_score

    }

    print(
        f"{category:<20}"
        f"{count:>8}"
        f"{avg_score:>12.4f}"
        f"{stddev:>12.4f}"
        f"{min_score:>12.4f}"
        f"{max_score:>12.4f}"
    )

# =====================================================
# CALCULATE Z-SCORES
# =====================================================

for category in category_targets:

    avg = category_stats[category]["avg"]
    stddev = category_stats[category]["stddev"]

    for target in category_targets[category]:

        if stddev == 0:

            z_score = 0

        else:

            z_score = (
                target["score"] - avg
            ) / stddev

        target["z_score"] = z_score

# =====================================================
# EXPORT CATEGORY RANKINGS
# =====================================================

category_rankings = []

for category in category_targets:

    ranked_targets = sorted(
        category_targets[category],
        key=lambda t: t["z_score"],
        reverse=True
    )

    for rank, target in enumerate(
        ranked_targets,
        start=1
    ):

        category_rankings.append({

            "category": category,
            "rank": rank,
            "name": target["name"],
            "score": target["score"],
            "z_score": target["z_score"]

        })

with open(
    CATEGORY_RANKINGS_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow([

        "category",
        "rank",
        "name",
        "score",
        "z_score"

    ])

    for row in sorted(
        category_rankings,
        key=lambda r: (
            r["category"],
            r["rank"]
        )
    ):

        writer.writerow([

            row["category"],
            row["rank"],
            row["name"],
            f"{row['score']:.6f}",
            f"{row['z_score']:.6f}"

        ])

# =====================================================
# EXPORT OUTLIERS
# =====================================================

with open(
    OUTLIERS_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow([

        "category",
        "name",
        "score",
        "z_score"

    ])

    for row in sorted(
        category_rankings,
        key=lambda r: r["z_score"],
        reverse=True
    ):

        if row["z_score"] >= 2.0:

            writer.writerow([

                row["category"],
                row["name"],
                f"{row['score']:.6f}",
                f"{row['z_score']:.6f}"

            ])

# =====================================================
# CATEGORY LEADERS
# =====================================================

print()
print("=" * 72)
print("CATEGORY CHAMPIONS")
print("=" * 72)

for category in sorted(category_targets):

    targets = sorted(
        category_targets[category],
        key=lambda t: t["z_score"],
        reverse=True
    )

    champion = targets[0]

    print()
    print(f"{category}")

    print(
        f"  Target : "
        f"{champion['name']}"
    )

    print(
        f"  Score  : "
        f"{champion['score']:.4f}"
    )

    print(
        f"  Z      : "
        f"{champion['z_score']:.4f}"
    )

# =====================================================
# TOP 5 PER CATEGORY
# =====================================================

print()
print("=" * 72)
print("TOP 5 PER CATEGORY")
print("=" * 72)

for category in sorted(category_targets):

    print()
    print(f"[{category}]")

    targets = sorted(
        category_targets[category],
        key=lambda t: t["z_score"],
        reverse=True
    )

    for rank, target in enumerate(
        targets[:5],
        start=1
    ):

        print(
            f"  {rank}. "
            f"{target['name']:<30}"
            f"Score={target['score']:.4f} "
            f"Z={target['z_score']:+.2f}"
        )

# =====================================================
# EXTREME OUTLIERS
# =====================================================

print()
print("=" * 72)
print("EXTREME CATEGORY OUTLIERS")
print("=" * 72)

outlier_count = 0

for row in sorted(
    category_rankings,
    key=lambda r: r["z_score"],
    reverse=True
):

    if row["z_score"] >= 2.0:

        outlier_count += 1

        print(
            f"{row['name']:<30}"
            f"{row['category']:<18}"
            f"Z={row['z_score']:+.2f}"
        )

if outlier_count == 0:

    print()
    print(
        "No category outliers "
        "(Z >= 2.0) detected."
    )

# =====================================================
# SUMMARY
# =====================================================

# =====================================================
# SUMMARY
# =====================================================

overall_scores = []

for scores in category_scores.values():

    overall_scores.extend(scores)

overall_avg = statistics.mean(
    overall_scores
)

print()
print("=" * 72)

print(
    f"Overall Average Score : "
    f"{overall_avg:.4f}"
)

print(
    f"Categories            : "
    f"{len(category_scores)}"
)

print(
    f"Targets               : "
    f"{len(overall_scores)}"
)

print()

print(
    f"Category Rankings CSV : "
    f"{CATEGORY_RANKINGS_FILE.name}"
)

print(
    f"Outliers CSV          : "
    f"{OUTLIERS_FILE.name}"
)

print()

print("Interpretation")
print("- Z > 2.0 : Outlier")
print("- Z > 3.0 : Strong Outlier")
print("- Z > 4.0 : Extreme Outlier")

print("=" * 72)