# merge_tess_into_master.py

from pathlib import Path
import csv

# =====================================================
# CONFIG
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MASTER_FILE = (
    BASE_DIR /
    "targets_resolved_master.csv"
)

TESS_FILE = (
    BASE_DIR /
    "tess_target_rankings.csv"
)

OUTPUT_FILE = (
    BASE_DIR /
    "targets_master_tess.csv"
)

# =====================================================
# LOAD TESS RANKINGS
# =====================================================

tess = {}

with open(
    TESS_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        name = row["target"].strip()

        tess[name] = row

# =====================================================
# MERGE
# =====================================================

rows = []

matched = 0

with open(
    MASTER_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        name = row["name"].strip()

        tess_row = tess.get(name)

        if tess_row:

            matched += 1

            row["tess_available"] = "YES"

            row["tess_sector_count"] = tess_row.get(
                "sector_count",
                ""
            )

            row["tess_total_points"] = tess_row.get(
                "total_points",
                ""
            )

            row["tess_max_score"] = tess_row.get(
                "max_score",
                ""
            )

            row["tess_avg_score"] = tess_row.get(
                "avg_score",
                ""
            )

            row["tess_relative_rms"] = tess_row.get(
                "max_relative_rms",
                ""
            )

            row["tess_max_dimming"] = tess_row.get(
                "max_dimming",
                ""
            )

            row["tess_max_brightening"] = tess_row.get(
                "max_brightening",
                ""
            )

        else:

            row["tess_available"] = "NO"

            row["tess_sector_count"] = ""
            row["tess_total_points"] = ""
            row["tess_max_score"] = ""
            row["tess_avg_score"] = ""
            row["tess_relative_rms"] = ""
            row["tess_max_dimming"] = ""
            row["tess_max_brightening"] = ""

        rows.append(row)

# =====================================================
# OUTPUT COLUMNS
# =====================================================

fieldnames = [

    "name",
    "category",
    "ra_deg",
    "dec_deg",

    "tess_available",
    "tess_sector_count",
    "tess_total_points",

    "tess_max_score",
    "tess_avg_score",

    "tess_relative_rms",
    "tess_max_dimming",
    "tess_max_brightening"

]

# =====================================================
# SAVE
# =====================================================

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

    writer.writerows(rows)

# =====================================================
# SUMMARY
# =====================================================

print()
print("=" * 60)
print("MERGE COMPLETE")
print("=" * 60)
print()

print(
    f"Master Targets : "
    f"{len(rows):,}"
)

print(
    f"TESS Matches   : "
    f"{matched:,}"
)

print(
    f"TESS Missing   : "
    f"{len(rows)-matched:,}"
)

print()

print(
    f"Output File : "
    f"{OUTPUT_FILE}"
)

print()