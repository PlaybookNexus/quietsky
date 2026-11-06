from pathlib import Path
import csv
import statistics

BASE_DIR = Path(__file__).resolve().parent.parent

INFRARED_FILE = BASE_DIR / "infrared_results.csv"
OUTPUT_FILE = BASE_DIR / "infrared_rankings.csv"

print()
print("Quiet Sky Infrared Score")
print("=" * 60)

rankings = []

with open(
    INFRARED_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        values = []

        for field in [

            "j_ratio",
            "k_ratio",
            "wise34_ratio",
            "wise46_ratio"

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

                continue

        if len(values) < 2:
            continue

        spread = (
            max(values)
            -
            min(values)
        )

        variance = statistics.pvariance(
            values
        )

        average = (
            sum(values)
            /
            len(values)
        )

        infrared_excess = abs(
            average - values[0]
        )

        score = (
            spread * 0.5
            +
            variance * 0.3
            +
            infrared_excess * 0.2
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

            "infrared_excess":
                infrared_excess,

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
        "infrared_score",
        "spread",
        "variance",
        "infrared_excess"
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

            f"{target['infrared_excess']:.6f}"
        ])

print()
print("=" * 60)
print(
    f"Saved: {OUTPUT_FILE}"
)