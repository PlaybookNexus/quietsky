# import_exoplanets.py

import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "catalogs" / "raw_exoplanets.csv"
OUT_FILE = BASE_DIR / "catalogs" / "exoplanets.csv"

seen = set()
rows = []

with open(
    RAW_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        name = row["hostname"].strip('"').strip()

        if not name:
            continue

        if name in seen:
            continue

        seen.add(name)

        rows.append([
            name,
            "Exoplanet"
        ])

with open(
    OUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow([
        "name",
        "category"
    ])

    writer.writerows(rows)

print(
    f"Imported {len(rows)} unique host stars"
)