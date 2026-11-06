from pathlib import Path
import csv
import json

# =====================================================
# CONFIG
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR /
    "category_rankings.csv"
)

OUTPUT_FILE = (
    BASE_DIR /
    "ai_candidate_review_board.txt"
)

TOP_CANDIDATES = 10

# =====================================================
# LOAD CANDIDATES
# =====================================================

candidates = []

with open(
    INPUT_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        candidates.append({

            "name":
                row["name"],

            "category":
                row["category"],

            "rank":
                int(row["rank"]),

            "score":
                float(row["score"]),

            "z_score":
                float(row["z_score"])

        })

# =====================================================
# SORT BY Z SCORE
# =====================================================

candidates = sorted(

    candidates,

    key=lambda c: (
        c["z_score"],
        c["score"]
    ),

    reverse=True

)

# =====================================================
# RULE-BASED REVIEW
# =====================================================

def review_candidate(candidate):

    z = candidate["z_score"]

    if z >= 3:

        relevance = "HIGH"
        recommendation = (
            "HIGH PRIORITY REVIEW"
        )

    elif z >= 2:

        relevance = "MEDIUM"
        recommendation = (
            "REVIEW"
        )

    elif z >= 1:

        relevance = "LOW"
        recommendation = (
            "MONITOR"
        )

    else:

        relevance = "VERY LOW"
        recommendation = (
            "IGNORE"
        )

    return {

        "relevance": relevance,
        "recommendation":
            recommendation

    }

# =====================================================
# REPORT
# =====================================================

lines = []

lines.append(
    "=" * 72
)

lines.append(
    "QUIET SKY AI CANDIDATE REVIEW BOARD"
)

lines.append(
    "=" * 72
)

lines.append("")

lines.append(
    "Purpose:"
)

lines.append(
    "Evaluate category-level outliers"
)

lines.append(
    "using statistical evidence rather"
)

lines.append(
    "than raw ranking position alone."
)

# =====================================================
# REVIEWS
# =====================================================

for candidate in candidates[:TOP_CANDIDATES]:

    review = review_candidate(
        candidate
    )

    lines.append("")
    lines.append("=" * 72)

    lines.append(
        f"CANDIDATE: "
        f"{candidate['name']}"
    )

    lines.append("=" * 72)

    lines.append("")

    lines.append(
        f"Category: "
        f"{candidate['category']}"
    )

    lines.append(
        f"Category Rank: "
        f"{candidate['rank']}"
    )

    lines.append(
        f"Score: "
        f"{candidate['score']:.4f}"
    )

    lines.append(
        f"Z Score: "
        f"{candidate['z_score']:+.2f}"
    )

    lines.append("")

    lines.append(
        "Evidence Supporting Interest:"
    )

    if candidate["rank"] == 1:

        lines.append(
            "- Category Champion"
        )

    if candidate["z_score"] > 2:

        lines.append(
            "- Significant category outlier"
        )

    if candidate["z_score"] > 1:

        lines.append(
            "- Above category average"
        )

    lines.append("")

    lines.append(
        "Evidence Against Interest:"
    )

    lines.append(
        "- Statistical evidence only"
    )

    lines.append(
        "- No confirmed physical anomaly"
    )

    lines.append(
        "- Additional observations required"
    )

    lines.append("")

    lines.append(
        f"Technosignature Relevance: "
        f"{review['relevance']}"
    )

    lines.append(
        f"Recommendation: "
        f"{review['recommendation']}"
    )

# =====================================================
# BOARD SUMMARY
# =====================================================

lines.append("")
lines.append("=" * 72)
lines.append("BOARD SUMMARY")
lines.append("=" * 72)

for rank, candidate in enumerate(
    candidates[:10],
    start=1
):

    lines.append(

        f"{rank:>2}. "
        f"{candidate['name']:<25}"
        f"{candidate['category']:<15}"
        f"Z={candidate['z_score']:+.2f}"

    )

# =====================================================
# WRITE FILE
# =====================================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "\n".join(lines)
    )

print()
print("=" * 72)
print(
    "AI CANDIDATE REVIEW BOARD COMPLETE"
)
print("=" * 72)

print()

print(
    f"Candidates Reviewed : "
    f"{TOP_CANDIDATES}"
)

print(
    f"Report : "
    f"{OUTPUT_FILE.name}"
)

print()