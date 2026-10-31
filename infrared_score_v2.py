from pathlib import Path
import csv
import statistics
import math

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "infrared_results.csv"
OUTPUT_FILE = BASE_DIR / "infrared_rankings_v2.csv"

BANDS = [
    "j_ratio",
    "k_ratio",
    "wise34_ratio",
    "wise46_ratio"
]

print()
print("Quiet Sky Infrared Score V2")
print("=" * 60)

rankings = []

with open(
    INPUT_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        values = []

        available_bands = 0

        for band in BANDS:

            value = row.get(band)

            if value is None:
                continue

            value = str(value).strip()

            if not value:
                continue

            try:

                value = float(value)

                #
                # Ignore NaN
                #

                if math.isnan(value):
                    continue

                values.append(value)

                available_bands += 1

            except ValueError:

                continue

        #
        # Need at least 2 bands for
        # meaningful comparisons
        #

        if available_bands < 2:
            continue

        spread = (
            max(values)
            -
            min(values)
        )

        variance = statistics.pvariance(
            values
        )

        mean_value = (
            sum(values)
            /
            len(values)
        )

        #
        # Average distance
        # from normalized value
        #

        infrared_excess = (
            sum(
                abs(v - 1.0)
                for v in values
            )
            /
            len(values)
        )

        coverage = (
            available_bands
            /
            len(BANDS)
        )

        #
        # Core score
        #

        score = (
            spread * 0.50
            +
            variance * 0.30
            +
            infrared_excess * 0.20
        )

        #
        # Confidence
        #

        if coverage >= 0.75:

            confidence = "HIGH"

        elif coverage >= 0.50:

            confidence = "MEDIUM"

        else:

            confidence = "LOW"

        rankings.append({

            "name":
                row["name"],

            "category":
                row["category"],

            "score":
                score,

            "spread":
                spread,

            "variance":
                variance,

            "infrared_excess":
                infrared_excess,

            "coverage":
                coverage,

            "bands":
                available_bands,

            "confidence":
                confidence
        })

#
# Highest score first
#

rankings.sort(
    key=lambda r: r["score"],
    reverse=True
)

print()

for rank, target in enumerate(
    rankings,
    start=1
):

    print(
        f"{rank:2d}. "
        f"{target['name']:<20} "
        f"{target['score']:.4f} "
        f"[{target['confidence']}] "
        f"({target['bands']}/4 bands)"
    )

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

        "infrared_score",

        "spread",

        "variance",

        "infrared_excess",

        "coverage",

        "bands",

        "confidence"
    ])

    for rank, target in enumerate(
        rankings,
        start=1
    ):

        writer.writerow([

            rank,

            target["name"],

            target["category"],

            f"{target['score']:.6f}",

            f"{target['spread']:.6f}",

            f"{target['variance']:.6f}",

            f"{target['infrared_excess']:.6f}",

            f"{target['coverage']:.2f}",

            target["bands"],

            target["confidence"]
        ])

print()
print("=" * 60)
print(
    f"Processed {len(rankings)} targets."
)

print(
    f"Saved: {OUTPUT_FILE}"
)