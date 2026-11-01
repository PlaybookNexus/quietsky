from pathlib import Path
import csv

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

OUTPUT_FILE = (
    BASE_DIR / "discovery_candidates_report.txt"
)

# =====================================================
# LOAD COMPOSITE RANKINGS
# =====================================================

composite_ranks = {}

with open(
    RANKINGS_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for rank, row in enumerate(
        sorted(
            reader,
            key=lambda r: float(
                r["score_v2"]
            ),
            reverse=True
        ),
        start=1
    ):

        name = row["name"]

        composite_ranks[name] = {

            "rank": rank,
            "score": float(
                row["score_v2"]
            ),
            "category": row["category"]

        }

# =====================================================
# LOAD CATEGORY RANKINGS
# =====================================================

category_data = {}

with open(
    CATEGORY_RANKINGS_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        category_data[
            row["name"]
        ] = {

            "category_rank":
                int(row["rank"]),

            "z_score":
                float(row["z_score"]),

            "category":
                row["category"]

        }

# =====================================================
# BUILD DISCOVERY SCORES
# =====================================================

candidates = []

for target in composite_ranks:

    score = 0

    composite_rank = (
        composite_ranks[target]["rank"]
    )

    category_rank = (
        category_data[target]
        ["category_rank"]
    )

    z_score = (
        category_data[target]
        ["z_score"]
    )

    category = (
        category_data[target]
        ["category"]
    )

    # ------------------------
    # Global rank bonus
    # ------------------------

    if composite_rank <= 5:
        score += 10

    elif composite_rank <= 10:
        score += 8

    elif composite_rank <= 20:
        score += 5

    # ------------------------
    # Category champion
    # ------------------------

    if category_rank == 1:
        score += 5

    elif category_rank <= 3:
        score += 3

    # ------------------------
    # Z-score bonus
    # ------------------------

    if z_score >= 3:
        score += 10

    elif z_score >= 2:
        score += 5

    elif z_score >= 1:
        score += 2

    # ------------------------
    # Anomalous population
    # ------------------------

    if category == "Anomalous":
        score += 2

    candidates.append({

        "name": target,
        "category": category,
        "discovery_score": score,
        "rank": composite_rank,
        "category_rank": category_rank,
        "z_score": z_score,
        "score_v2": (
            composite_ranks[target]
            ["score"]
        )

    })

# =====================================================
# SORT DISCOVERY CANDIDATES
# =====================================================

candidates = sorted(

    candidates,

    key=lambda c: (
        c["discovery_score"],
        c["z_score"],
        c["score_v2"]
    ),

    reverse=True

)

# =====================================================
# GENERATE REPORT
# =====================================================

lines = []

lines.append(
    "=" * 72
)

lines.append(
    "QUIET SKY DISCOVERY CANDIDATES REPORT"
)

lines.append(
    "=" * 72
)

lines.append("")

lines.append(
    f"Targets Evaluated : "
    f"{len(candidates)}"
)

lines.append("")

lines.append(
    "The following targets were "
    "prioritized using:"
)

lines.append("")

lines.append(
    "- Composite Score"
)

lines.append(
    "- Category Rank"
)

lines.append(
    "- Category Z-Score"
)

lines.append(
    "- Discovery Heuristics"
)

lines.append("")

lines.append(
    "=" * 72
)

lines.append(
    "TOP DISCOVERY CANDIDATES"
)

lines.append(
    "=" * 72
)

for rank, target in enumerate(
    candidates[:15],
    start=1
):

    lines.append("")

    lines.append(
        f"{rank}. {target['name']}"
    )

    lines.append(
        f"   Category       : "
        f"{target['category']}"
    )

    lines.append(
        f"   Discovery Score: "
        f"{target['discovery_score']}"
    )

    lines.append(
        f"   Composite Rank : "
        f"{target['rank']}"
    )

    lines.append(
        f"   Category Rank  : "
        f"{target['category_rank']}"
    )

    lines.append(
        f"   Z Score        : "
        f"{target['z_score']:+.2f}"
    )

    lines.append(
        f"   Raw Score      : "
        f"{target['score_v2']:.4f}"
    )

# =====================================================
# CATEGORY CHAMPIONS
# =====================================================

lines.append("")
lines.append("=" * 72)
lines.append("CATEGORY CHAMPIONS")
lines.append("=" * 72)

shown = set()

for target in candidates:

    category = target["category"]

    if category in shown:
        continue

    if target["category_rank"] != 1:
        continue

    shown.add(category)

    lines.append("")

    lines.append(
        f"{category}"
    )

    lines.append(
        f"  Champion : "
        f"{target['name']}"
    )

    lines.append(
        f"  Z Score  : "
        f"{target['z_score']:+.2f}"
    )

# =====================================================
# OUTLIERS
# =====================================================

lines.append("")
lines.append("=" * 72)
lines.append("CATEGORY OUTLIERS")
lines.append("=" * 72)

outliers_found = False

for target in candidates:

    if target["z_score"] >= 2:

        outliers_found = True

        lines.append(
            f"{target['name']:<25}"
            f"{target['category']:<18}"
            f"Z={target['z_score']:+.2f}"
        )

if not outliers_found:

    lines.append(
        "No significant "
        "category outliers detected."
    )

# =====================================================
# FINDING 016
# =====================================================

lines.append("")
lines.append("=" * 72)
lines.append("FINDING #016")
lines.append("=" * 72)

lines.append("")

lines.append(
    "Category-aware rankings identify "
    "objects that are unusual relative "
    "to their own populations."
)

lines.append("")

lines.append(
    "This reduces population bias and "
    "improves scientific interpretability."
)

lines.append("")

lines.append(
    "Objects promoted by category "
    "ranking may not be global ranking "
    "leaders, but they may represent "
    "important population-specific "
    "outliers."
)

# =====================================================
# WRITE REPORT
# =====================================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "\n".join(lines)
    )

# =====================================================
# SUMMARY
# =====================================================

print()
print("=" * 72)
print(
    "DISCOVERY CANDIDATES REPORT GENERATED"
)
print("=" * 72)

print()

print(
    f"Candidates Reviewed : "
    f"{len(candidates)}"
)

print(
    f"Report : "
    f"{OUTPUT_FILE.name}"
)

print()

print(
    f"Top Candidate : "
    f"{candidates[0]['name']}"
)

print(
    f"Category      : "
    f"{candidates[0]['category']}"
)

print(
    f"Discovery Score : "
    f"{candidates[0]['discovery_score']}"
)

print()
print("=" * 72)