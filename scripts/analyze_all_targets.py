from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
TARGETS_FILE = BASE_DIR / "expanded_targets_v2.csv"

REQUIRED_FILES = [
    "DSS.fits",
    "DSS2_Red.fits",
    "DSS2_Blue.fits"
]

def safe_name(name):
    return (
        name.replace(" ", "_")
            .replace("/", "_")
            .replace("'", "")
    )

print()
print("Target Analysis")
print("=" * 60)

results = []

with open(
    TARGETS_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        name = row["name"]
        category = row["category"]

        folder = (
            DATA_DIR /
            safe_name(name)
        )

        found = 0

        for survey in REQUIRED_FILES:

            if (folder / survey).exists():
                found += 1

        completeness = (
            found /
            len(REQUIRED_FILES)
        )

        results.append({
            "name": name,
            "category": category,
            "surveys": found,
            "score": completeness
        })

results.sort(
    key=lambda r: r["score"],
    reverse=True
)

print()

for r in results:

    print(
        f"{r['name']:<20} "
        f"{r['category']:<12} "
        f"{r['surveys']}/3 "
        f"{r['score']:.2f}"
    )

print()
print("=" * 60)

complete = sum(
    1 for r in results
    if r["score"] == 1.0
)

print(
    f"{complete} targets fully downloaded."
)