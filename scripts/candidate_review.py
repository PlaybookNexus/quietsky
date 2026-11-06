# candidate_review.py

from pathlib import Path
from datetime import datetime
import csv
import sys

# =====================================================
# CONFIG
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RANKINGS_FILE = BASE_DIR / "rankings_v2.csv"
CATEGORY_RANKINGS_FILE = BASE_DIR / "category_rankings.csv"

DATA_DIR = BASE_DIR / "data"
REVIEWS_DIR = BASE_DIR / "reviews"

# =====================================================
# TARGET ARGUMENT
# =====================================================

if len(sys.argv) < 2:

    print()
    print("Usage:")
    print()
    print(
        'python candidate_review.py "Ross 640"'
    )
    print()

    raise SystemExit(1)

TARGET_NAME = (
    " ".join(sys.argv[1:])
).strip()

# =====================================================
# TIMESTAMP
# =====================================================

NOW = datetime.now()

TIMESTAMP = NOW.strftime(
    "%Y%m%d_%H%M%S"
)

DISPLAY_TIME = NOW.strftime(
    "%Y-%m-%d %H:%M:%S"
)

# =====================================================
# REPORT HELPER
# =====================================================

lines = []

def add(text=""):

    print(text)
    lines.append(text)

# =====================================================
# LOAD GLOBAL RANKINGS
# =====================================================

global_data = {}

with open(
    RANKINGS_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    rows = sorted(
        reader,
        key=lambda r: float(
            r["score_v2"]
        ),
        reverse=True
    )

    for rank, row in enumerate(
        rows,
        start=1
    ):

        global_data[
            row["name"]
        ] = {

            "rank": rank,

            "score":
                float(
                    row["score_v2"]
                ),

            "category":
                row["category"]

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

            "category":
                row["category"],

            "category_rank":
                int(
                    row["rank"]
                ),

            "z_score":
                float(
                    row["z_score"]
                )

        }

# =====================================================
# VALIDATE TARGET
# =====================================================

if TARGET_NAME not in global_data:

    print()
    print(
        f"Target not found: "
        f"{TARGET_NAME}"
    )

    raise SystemExit(1)

if TARGET_NAME not in category_data:

    print()
    print(
        f"Target missing from "
        f"category rankings: "
        f"{TARGET_NAME}"
    )

    raise SystemExit(1)

# =====================================================
# TARGET VALUES
# =====================================================

global_rank = (
    global_data[TARGET_NAME]["rank"]
)

score = (
    global_data[TARGET_NAME]["score"]
)

category = (
    category_data[TARGET_NAME]
    ["category"]
)

category_rank = (
    category_data[TARGET_NAME]
    ["category_rank"]
)

z_score = (
    category_data[TARGET_NAME]
    ["z_score"]
)

# =====================================================
# FIND DATA FILES
# =====================================================

safe_name = (
    TARGET_NAME
    .replace(" ", "_")
    .replace("/", "_")
    .replace("'", "")
)

target_dir = (
    DATA_DIR / safe_name
)

fits_files = []

if target_dir.exists():

    fits_files = sorted(

        p.name

        for p in target_dir.glob(
            "*.fits"
        )

    )

# =====================================================
# REVIEW CLASSIFICATION
# =====================================================

if z_score >= 3:

    relevance = "HIGH"

    recommendation = (
        "HIGH PRIORITY REVIEW"
    )

elif z_score >= 2:

    relevance = "MEDIUM"

    recommendation = (
        "REVIEW"
    )

elif z_score >= 1:

    relevance = "LOW"

    recommendation = (
        "MONITOR"
    )

else:

    relevance = "VERY LOW"

    recommendation = (
        "IGNORE"
    )

# =====================================================
# REVIEW
# =====================================================

add()
add("=" * 72)
add("QUIET SKY CANDIDATE REVIEW")
add("=" * 72)

add()

add(
    f"Review Generated : "
    f"{DISPLAY_TIME}"
)

add()

add(
    f"Target           : "
    f"{TARGET_NAME}"
)

add(
    f"Category         : "
    f"{category}"
)

add()

add(
    f"Global Rank      : "
    f"#{global_rank}"
)

add(
    f"Category Rank    : "
    f"#{category_rank}"
)

add(
    f"Raw Score        : "
    f"{score:.4f}"
)

add(
    f"Category Z Score : "
    f"{z_score:+.2f}"
)

add()

add("=" * 72)
add("WHY IT WAS PROMOTED")
add("=" * 72)

add()

if category_rank == 1:

    add(
        "- Category Champion"
    )

if global_rank <= 10:

    add(
        "- Top 10 Overall Candidate"
    )

if z_score >= 2:

    add(
        "- Significant Population Outlier"
    )

elif z_score >= 1:

    add(
        "- Above Category Average"
    )

add()

add("=" * 72)
add("SCIENTIFIC INTERPRETATION")
add("=" * 72)

add()

add(
    f"{TARGET_NAME} ranks "
    f"#{global_rank} overall and "
    f"#{category_rank} within the "
    f"{category} population."
)

add()

if z_score >= 2:

    add(
        "This object represents a statistically "
        "significant population-level outlier."
    )

elif z_score >= 1:

    add(
        "This object appears above average "
        "within its peer population."
    )

else:

    add(
        "This object does not currently appear "
        "highly unusual relative to its peers."
    )

add()

add("=" * 72)
add("EVIDENCE IN FAVOR")
add("=" * 72)

add(
    "- Survived automated ranking process"
)

add(
    "- Compared against peer population"
)

add(
    "- Measurable statistical deviation detected"
)

if category_rank == 1:

    add(
        "- Highest ranked object in category"
    )

add()

add("=" * 72)
add("EVIDENCE AGAINST")
add("=" * 72)

add(
    "- Statistical evidence only"
)

add(
    "- No confirmed physical anomaly"
)

add(
    "- Additional observations required"
)

add(
    "- Sample size effects remain possible"
)

add()

add("=" * 72)
add("DATA AVAILABILITY")
add("=" * 72)

add()

add(
    f"Directory : "
    f"{target_dir}"
)

add()

if fits_files:

    add(
        f"FITS Files ({len(fits_files)})"
    )

    add()

    for filename in fits_files:

        add(
            f"  {filename}"
        )

else:

    add(
        "No FITS files found."
    )

add()

add("=" * 72)
add("TECHNOSIGNATURE REVIEW")
add("=" * 72)

add()

add(
    f"Relevance      : "
    f"{relevance}"
)

add(
    f"Recommendation : "
    f"{recommendation}"
)

add()

if relevance == "HIGH":

    add(
        "Strong statistical outlier. "
        "Deserves immediate follow-up."
    )

elif relevance == "MEDIUM":

    add(
        "Interesting population-level anomaly."
    )

elif relevance == "LOW":

    add(
        "Worth monitoring but not currently exceptional."
    )

else:

    add(
        "Current evidence does not justify elevated attention."
    )

add()

add("=" * 72)

# =====================================================
# EXPORT
# =====================================================

review_file = (

    REVIEWS_DIR /

    f"{safe_name}_review_{TIMESTAMP}.txt"

)

with open(
    review_file,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "\n".join(lines)
    )

print()
print("=" * 72)
print("REVIEW EXPORTED")
print("=" * 72)
print()
print(review_file)
print()