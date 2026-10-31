from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent.parent

RESULTS_FILE = BASE_DIR / "results.csv"
RANKINGS_FILE = BASE_DIR / "rankings.csv"

print()
print("Quiet Sky Anomaly Scoring")
print("=" * 60)

rankings = []

with open(
    RESULTS_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        name = row.get("name", "Unknown")
        category = row.get("category", "Unknown")

        values = []

        metric_fields = [
            "dss_ratio",
            "dss2red_ratio",
            "dss2blue_ratio"
        ]

        for field in metric_fields:

            value = row.get(field)

            #
            # Skip missing columns
            #

            if value is None:
                continue

            value = str(value).strip()

            #
            # Skip empty placeholders
            #

            if value == "":
                continue

            if value == "...":
                continue

            try:

                values.append(
                    float(value)
                )

            except ValueError:

                continue

        #
        # Need at least two measurements
        #

        if len(values) < 2:

            print(
                f"SKIP {name} "
                f"(insufficient data)"
            )

            continue

        anomaly_score = (
            max(values) -
            min(values)
        )

        average_value = (
            sum(values) /
            len(values)
        )

        rankings.append(
            {
                "name": name,
                "category": category,
                "score": anomaly_score,
                "average": average_value,
                "measurements": len(values)
            }
        )

#
# Highest anomaly first
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
        f"Score={target['score']:.4f} "
        f"Avg={target['average']:.4f}"
    )

#
# Save rankings
#

with open(
    RANKINGS_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow(
        [
            "rank",
            "name",
            "category",
            "anomaly_score",
            "average_ratio",
            "measurements"
        ]
    )

    for rank, target in enumerate(
        rankings,
        start=1
    ):

        writer.writerow(
            [
                rank,
                target["name"],
                target["category"],
                f"{target['score']:.4f}",
                f"{target['average']:.4f}",
                target["measurements"]
            ]
        )

print()
print("=" * 60)
print(f"Processed {len(rankings)} targets.")
print(f"Saved: {RANKINGS_FILE}")