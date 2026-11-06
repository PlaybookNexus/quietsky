from pathlib import Path
from datetime import datetime
import csv

# =====================================================
# CONFIG
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CATALOG_DIR = (
    BASE_DIR / "catalogs"
)

OUTPUT_FILE = (
    BASE_DIR / "targets_master.csv"
)

# =====================================================
# CATEGORY FILES
# =====================================================

CATEGORY_FILES = [

    "exoplanets.csv",
    "white_dwarfs.csv",
    "flare_stars.csv",
    "variable_stars.csv",
    "nearby_stars.csv",
    "solar_analogs.csv",
    "young_stars.csv",
    "debris_disks.csv",
    "brown_dwarfs.csv",
    "wolf_rayet.csv",
    "transit_anomalies.csv",
    "eclipsing_binaries.csv"

]

# =====================================================
# LOAD SOURCES
# =====================================================

targets = []
seen = set()

stats = {}

for filename in CATEGORY_FILES:

    filepath = (
        CATALOG_DIR / filename
    )

    if not filepath.exists():

        print(
            f"WARNING: Missing {filename}"
        )

        continue

    count = 0

    with open(
        filepath,
        newline="",
        encoding="utf-8"
    ) as f:

        reader = csv.DictReader(f)

        for row in reader:

            name = (
                row["name"]
                .strip()
            )

            if not name:

                continue

            key = name.lower()

            if key in seen:

                continue

            seen.add(key)

            target = {

                "name":
                    name,

                "category":
                    row.get(
                        "category",
                        ""
                    ).strip(),

                "ra":
                    row.get(
                        "ra",
                        ""
                    ).strip(),

                "dec":
                    row.get(
                        "dec",
                        ""
                    ).strip(),

                "distance_pc":
                    row.get(
                        "distance_pc",
                        ""
                    ).strip(),

                "spectral_type":
                    row.get(
                        "spectral_type",
                        ""
                    ).strip(),

                "source_catalog":
                    row.get(
                        "source_catalog",
                        filename
                    ).strip()

            }

            targets.append(
                target
            )

            count += 1

    stats[filename] = count

# =====================================================
# SORT
# =====================================================

targets = sorted(

    targets,

    key=lambda x: (
        x["category"],
        x["name"]
    )

)

# =====================================================
# EXPORT
# =====================================================

fieldnames = [

    "name",
    "category",
    "ra",
    "dec",
    "distance_pc",
    "spectral_type",
    "source_catalog"

]

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames
    )

    writer.writeheader()

    writer.writerows(
        targets
    )

# =====================================================
# SUMMARY
# =====================================================

print()
print("=" * 72)
print("QUIET SKY EXTENDED CATALOG")
print("=" * 72)

print()

for category_file, count in stats.items():

    print(
        f"{category_file:<30}"
        f"{count:>5}"
    )

print()

print(
    f"Total Targets : "
    f"{len(targets)}"
)

print(
    f"Generated     : "
    f"{datetime.now()}"
)

print()

print(
    f"Output        : "
    f"{OUTPUT_FILE}"
)

print()
print("=" * 72)