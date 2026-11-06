from pathlib import Path
import csv
import time

from astroquery.simbad import Simbad

# =====================================================
# CONFIG
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "expanded_targets_v2.csv"
OUTPUT_FILE = BASE_DIR / "targets_resolved.csv"
FAILED_FILE = BASE_DIR / "targets_unresolved.csv"

# =====================================================
# SIMBAD CONFIG
# =====================================================

custom_simbad = Simbad()

# Harvard mirror
custom_simbad.server = "simbad.harvard.edu"

print()
print("=" * 60)
print("Quiet Sky Coordinate Resolver V5")
print("=" * 60)

print()
print("SIMBAD Configuration")
print("-" * 60)
print(f"Server : {custom_simbad.server}")

# =====================================================
# TEST CONNECTION
# =====================================================

try:

    print()
    print("Testing SIMBAD...")

    test = custom_simbad.query_object(
        "TRAPPIST-1"
    )

    if test is None:

        print(
            "[FAIL] Test returned no result"
        )

        raise SystemExit(1)

    print("[OK] SIMBAD reachable")

except Exception as e:

    print()
    print("[FAIL] SIMBAD connection failed")
    print(e)

    raise SystemExit(1)

# =====================================================
# PROCESS TARGETS
# =====================================================

resolved = []
failed = []

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

        if name.startswith("#"):
            continue

        print()
        print(f"Resolving: {name}")

        try:

            result = custom_simbad.query_object(
                name
            )

            if result is None:

                print(
                    "  FAILED: Not Found"
                )

                failed.append({

                    "name": name,
                    "category": category

                })

                continue

            if "ra" not in result.colnames:

                raise RuntimeError(
                    f"ra missing: {result.colnames}"
                )

            if "dec" not in result.colnames:

                raise RuntimeError(
                    f"dec missing: {result.colnames}"
                )

            ra_deg = float(
                result["ra"][0]
            )

            dec_deg = float(
                result["dec"][0]
            )

            resolved.append({

                "name": name,
                "category": category,
                "ra": ra_deg,
                "dec": dec_deg

            })

            print(
                f"  RA  = {ra_deg:.8f}"
            )

            print(
                f"  DEC = {dec_deg:.8f}"
            )

            time.sleep(0.25)

        except Exception as e:

            print(
                f"  FAILED"
            )

            print(
                f"  {e}"
            )

            failed.append({

                "name": name,
                "category": category

            })

# =====================================================
# SAVE RESOLVED
# =====================================================

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow([

        "name",
        "category",
        "ra",
        "dec"

    ])

    for target in resolved:

        writer.writerow([

            target["name"],
            target["category"],
            f"{target['ra']:.8f}",
            f"{target['dec']:.8f}"

        ])

# =====================================================
# SAVE UNRESOLVED
# =====================================================

with open(
    FAILED_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow([

        "name",
        "category"

    ])

    for target in failed:

        writer.writerow([

            target["name"],
            target["category"]

        ])

# =====================================================
# SUMMARY
# =====================================================

print()
print("=" * 60)
print("RESOLUTION COMPLETE")
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