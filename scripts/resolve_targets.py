# resolve_targets.py

from pathlib import Path
import csv
import time

from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
import astropy.units as u

# =====================================================
# CONFIG
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "targets_master.csv"

OUTPUT_FILE = BASE_DIR / "targets_resolved.csv"

FAILED_FILE = BASE_DIR / "targets_unresolved.csv"

CHECKPOINT = 100

# =====================================================
# SIMBAD
# =====================================================

simbad = Simbad()

# Harvard mirror (worked previously)
simbad.server = "simbad.harvard.edu"

# =====================================================
# SAVE FUNCTION
# =====================================================

def save_results(resolved, failed):

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "name",
                "category",
                "ra_deg",
                "dec_deg"
            ]
        )

        writer.writeheader()
        writer.writerows(resolved)

    with open(
        FAILED_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "name",
                "category"
            ]
        )

        writer.writeheader()
        writer.writerows(failed)

# =====================================================
# START
# =====================================================

print()
print("=" * 60)
print("QUIET SKY TARGET RESOLVER")
print("=" * 60)

print()
print(f"Server : {simbad.server}")

# =====================================================
# TEST CONNECTION
# =====================================================

print()
print("Testing SIMBAD...")

try:

    result = simbad.query_object(
        "TRAPPIST-1"
    )

except Exception as e:

    print()
    print("SIMBAD FAILED")
    print(e)

    raise SystemExit(1)

if result is None:

    print("TRAPPIST-1 not found")

    raise SystemExit(1)

print("SIMBAD OK")

print()
print("Columns returned:")

for c in result.colnames:
    print(" ", c)

# =====================================================
# DETERMINE COORD COLUMNS
# =====================================================

ra_col = None
dec_col = None

for c in result.colnames:

    if c.lower() == "ra":
        ra_col = c

    if c.lower() == "dec":
        dec_col = c

if ra_col is None or dec_col is None:

    print()
    print("RA/DEC columns not found.")
    print(result.colnames)

    raise SystemExit(1)

print()
print(f"RA column  : {ra_col}")
print(f"DEC column : {dec_col}")

# =====================================================
# LOAD TARGETS
# =====================================================

targets = []

seen = set()

with open(
    INPUT_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        name = row["name"].strip()
        category = row["category"].strip()

        if not name:
            continue

        if name in seen:
            continue

        seen.add(name)

        targets.append({

            "name": name,
            "category": category

        })

print()
print(
    f"Unique targets : {len(targets)}"
)

# -----------------------------------------------------
# TEST MODE
# -----------------------------------------------------
#
# Uncomment for testing:
#
# targets = targets[:10]
#
# -----------------------------------------------------

# =====================================================
# RESOLVE
# =====================================================

resolved = []
failed = []

processed_since_save = 0

for i, target in enumerate(
    targets,
    start=1
):

    name = target["name"]
    category = target["category"]

    print()
    print(
        f"[{i}/{len(targets)}] {name}"
    )

    try:

        result = simbad.query_object(
            name
        )

        if result is None:

            print(
                "  NOT FOUND"
            )

            failed.append({

                "name": name,
                "category": category

            })

            continue

        ra_text = str(
            result[ra_col][0]
        )

        dec_text = str(
            result[dec_col][0]
        )

        coord = SkyCoord(

            ra_text,
            dec_text,

            unit=(
                u.hourangle,
                u.deg
            )

        )

        ra_deg = coord.ra.deg
        dec_deg = coord.dec.deg

        resolved.append({

            "name": name,
            "category": category,

            "ra_deg":
                f"{ra_deg:.8f}",

            "dec_deg":
                f"{dec_deg:.8f}"

        })

        print(
            f"  RA  = {ra_deg:.8f}"
        )

        print(
            f"  DEC = {dec_deg:.8f}"
        )

        processed_since_save += 1

        if processed_since_save >= CHECKPOINT:

            print()
            print(
                "*** CHECKPOINT SAVE ***"
            )

            save_results(
                resolved,
                failed
            )

            processed_since_save = 0

        time.sleep(0.25)

    except Exception as e:

        print(
            f"  ERROR: {e}"
        )

        failed.append({

            "name": name,
            "category": category

        })

# =====================================================
# FINAL SAVE
# =====================================================

print()
print("Saving results...")

save_results(
    resolved,
    failed
)

# =====================================================
# SUMMARY
# =====================================================

print()
print("=" * 60)
print("COMPLETE")
print("=" * 60)

print()

print(
    f"Resolved : {len(resolved)}"
)

print(
    f"Failed   : {len(failed)}"
)

print()

print(
    f"Resolved Catalog : {OUTPUT_FILE}"
)

print(
    f"Failed Catalog   : {FAILED_FILE}"
)

print()