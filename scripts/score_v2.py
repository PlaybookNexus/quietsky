from pathlib import Path
import csv
import statistics

BASE_DIR = Path(__file__).resolve().parent.parent

RESULTS_FILE = BASE_DIR / "results.csv"
OUTPUT_FILE = BASE_DIR / "rankings_v2.csv"

print()
print("Quiet Sky Score V2")
print("=" * 60)

rankings = []

with open(
    RESULTS_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        values = []

        for field in [

            "dss_ratio",
            "dss2red_ratio",
            "dss2blue_ratio"

        ]:

            value = row.get(field)

            if value is None:
                continue

            value = str(value).strip()

            if not value:
                continue

            try:
                values.append(
                    float(value)
                )

            except ValueError:
                pass

        if len(values) < 3:
            continue

        spread = (
            max(values)
            -
            min(values)
        )

        variance = statistics.pvariance(
            values
        )

        unity_deviation = (
            sum(
                abs(v - 1.0)
                for v in values
            )
            /
            len(values)
        )

        score = (
            spread * 0.4
            +
            variance * 0.4
            +
            unity_deviation * 0.2
        )

        rankings.append({

            "name":
                row["name"],

            "category":
                row["category"],

            "spread":
                spread,

            "variance":
                variance,

            "unity":
                unity_deviation,

            "score":
                score
        })

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
        f"{target['score']:.4f}"
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
        "score_v2",
        "spread",
        "variance",
        "unity_deviation"
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

            f"{target['unity']:.6f}"
        ])

print()
print("=" * 60)
print(
    f"Saved: {OUTPUT_FILE}"
)