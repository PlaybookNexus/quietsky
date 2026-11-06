# fetch_exoplanets.py

from pathlib import Path
import csv
import urllib.request

BASE_DIR = Path(__file__).resolve().parent.parent

CATALOG_DIR = BASE_DIR / "catalogs"
CATALOG_DIR.mkdir(exist_ok=True)

OUTFILE = CATALOG_DIR / "exoplanets.csv"

URL = (
    "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    "?query="
    "select+hostname,sy_dist,rastr,decstr,st_spectype"
    "+from+pscomppars"
    "+where+default_flag=1"
    "+and+sy_dist+is+not+null"
    "+order+by+sy_dist"
    "&format=csv"
)

print()
print("Downloading NASA Exoplanet Archive...")
print()

response = urllib.request.urlopen(URL)

rows = list(
    csv.DictReader(
        response.read().decode("utf-8").splitlines()
    )
)

seen = set()
targets = []

for row in rows:

    name = row["hostname"].strip()

    if name in seen:
        continue

    seen.add(name)

    targets.append({

        "name": name,
        "category": "Exoplanet",
        "ra": row.get("rastr", ""),
        "dec": row.get("decstr", ""),
        "distance_pc": row.get("sy_dist", ""),
        "spectral_type": row.get("st_spectype", ""),
        "source_catalog": "NASA Exoplanet Archive"

    })

    if len(targets) >= 100:
        break

with open(
    OUTFILE,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.DictWriter(

        f,

        fieldnames=[

            "name",
            "category",
            "ra",
            "dec",
            "distance_pc",
            "spectral_type",
            "source_catalog"

        ]

    )

    writer.writeheader()
    writer.writerows(targets)

print(
    f"Saved {len(targets)} exoplanets"
)

print(
    f"Output: {OUTFILE}"
)

print()