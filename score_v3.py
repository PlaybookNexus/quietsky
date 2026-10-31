from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent.parent

OPTICAL_FILE = BASE_DIR / "rankings_v2.csv"
INFRARED_FILE = BASE_DIR / "infrared_rankings_v2.csv"

OUTPUT_FILE = BASE_DIR / "quiet_sky_rankings_v3.csv"

print()
print("Quiet Sky Composite Score V3")
print("=" * 60)

#
# Load optical scores
#

optical = {}

with open(
    OPTICAL_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        optical[row["name"]] = {

            "category":
                row["category"],

            "optical_score":
                float(
                    row["score_v2"]
                )
        }

#
# Load infrared scores
#

infrared = {}

with open(
    INFRARED_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        infrared[row["name"]] = {

            "infrared_score":
                float(
                    row["infrared_score"]
                ),

            "coverage":
                float(
                    row["coverage"]
                ),

            "confidence":
                row["confidence"]
        }

#
# Merge
#

results = []

for name, optical_row in optical.items():

    optical_score = \
        optical_row["optical_score"]

    category = \
        optical_row["category"]

    infrared_score = 0.0
    coverage = 0.0
    confidence = "NONE"

    if name in infrared:

        infrared_score = \
            infrared[name][
                "infrared_score"
            ]

        coverage = \
            infrared[name][
                "coverage"
            ]

        confidence = \
            infrared[name][
                "confidence"
            ]

    #
    # Weight infrared
    # according to coverage
    #

    weighted_ir = (
        infrared_score *
        coverage
    )

    #
    # Composite
    #
    # Optical remains primary
    # Infrared contributes
    # only when data exists.
    #

    composite_score = (
        optical_score * 0.60
        +
        weighted_ir * 0.40
    )

    results.append({

        "name":
            name,

        "category":
            category,

        "optical_score":
            optical_score,

        "infrared_score":
            infrared_score,

        "coverage":
            coverage,

        "confidence":
            confidence,

        "composite_score":
            composite_score
    })

#
# Ranking
#

results.sort(
    key=lambda r:
        r["composite_score"],
    reverse=True
)

#
# Console output
#

print()

for rank, target in enumerate(
    results,
    start=1
):

    print(
        f"{rank:2d}. "
        f"{target['name']:<20} "
        f"{target['composite_score']:.4f} "
        f"[IR {target['confidence']}]"
    )

#
# Save CSV
#

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow([

        "rank",

        "name",

        "category",

        "composite_score",

        "optical_score",

        "infrared_score",

        "infrared_coverage",

        "infrared_confidence"
    ])

    for rank, target in enumerate(
        results,
        start=1
    ):

        writer.writerow([

            rank,

            target["name"],

            target["category"],

            f"{target['composite_score']:.6f}",

            f"{target['optical_score']:.6f}",

            f"{target['infrared_score']:.6f}",

            f"{target['coverage']:.2f}",

            target["confidence"]
        ])

print()
print("=" * 60)
print(
    f"Processed {len(results)} targets."
)
print(
    f"Saved: {OUTPUT_FILE}"
)