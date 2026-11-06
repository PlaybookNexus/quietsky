# resolve_targets_pass2.py

from pathlib import Path
import csv
import re
import time

from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
import astropy.units as u

# =====================================================
# CONFIG
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "targets_unresolved.csv"

OUTPUT_FILE = BASE_DIR / "targets_resolved_pass2.csv"

FAILED_FILE = BASE_DIR / "targets_unresolved_pass2.csv"

# =====================================================
# SIMBAD
# =====================================================

simbad = Simbad()
simbad.server = "simbad.harvard.edu"

# =====================================================
# DETERMINE COORD COLUMNS
# =====================================================

print()
print("=" * 60)
print("PASS 2 RESOLUTION")
print("=" * 60)
print()

print("Testing SIMBAD...")

test = simbad.query_object("TRAPPIST-1")

if test is None:
    raise RuntimeError(
        "Cannot reach SIMBAD"
    )

ra_col = None
dec_col = None

for col in test.colnames:

    if col.lower() == "ra":
        ra_col = col

    if col.lower() == "dec":
        dec_col = col

print(f"RA column  : {ra_col}")
print(f"DEC column : {dec_col}")

# =====================================================
# HELPERS
# =====================================================

def candidate_names(name):

    candidates = [name]

    suffixes = [

        r"\s+A$",
        r"\s+B$",
        r"\s+AB$",
        r"\s+Aa$",
        r"\s+Ab$",
        r"\s+Ba$",
        r"\s+Bb$",

    ]

    for pattern in suffixes:

        stripped = re.sub(
            pattern,
            "",
            name
        )

        if stripped != name:
            candidates.append(
                stripped
            )

    return list(
        dict.fromkeys(
            candidates
        )
    )


def skip_object(name):

    prefixes = (

        "KMT-",
        "MOA-",
        "OGLE-"

    )

    return name.startswith(
        prefixes
    )

# =====================================================
# LOAD TARGETS
# =====================================================

targets = []

with open(
    INPUT_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    targets = list(reader)

# =====================================================
# RESOLVE
# =====================================================

resolved = []
failed = []

for row in targets:

    name = row["name"]
    category = row["category"]

    print()
    print(name)

    if skip_object(name):

        print(
            "  SKIP (Microlensing Event)"
        )

        failed.append(row)

        continue

    success = False

    for try_name in candidate_names(name):

        print(
            f"  TRY: {try_name}"
        )

        try:

            result = simbad.query_object(
                try_name
            )

            if result is None:

                continue

            if len(result) == 0:

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

            print(
                "  RESOLVED"
            )

            print(
                f"    RA={coord.ra.deg:.8f}"
            )

            print(
                f"    DEC={coord.dec.deg:.8f}"
            )

            resolved.append({

                "original_name":
                    name,

                "resolved_name":
                    try_name,

                "category":
                    category,

                "ra_deg":
                    f"{coord.ra.deg:.8f}",

                "dec_deg":
                    f"{coord.dec.deg:.8f}"

            })

            success = True

            break

        except Exception as e:

            print(
                f"    ERROR: {e}"
            )

    if not success:

        failed.append({

            "name": name,
            "category": category

        })

    time.sleep(0.2)

# =====================================================
# SAVE RESOLVED
# =====================================================

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.DictWriter(

        f,

        fieldnames=[

            "original_name",
            "resolved_name",
            "category",
            "ra_deg",
            "dec_deg"

        ]

    )

    writer.writeheader()

    writer.writerows(
        resolved
    )

# =====================================================
# SAVE FAILED
# =====================================================

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

    writer.writerows(
        failed
    )

# =====================================================
# SUMMARY
# =====================================================

print()
print("=" * 60)

print(
    f"Resolved : {len(resolved)}"
)

print(
    f"Failed   : {len(failed)}"
)

print("=" * 60)