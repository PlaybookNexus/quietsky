from pathlib import Path
import csv
import time

from astropy.coordinates import SkyCoord

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "expanded_targets.csv"
OUTPUT_FILE = BASE_DIR / "targets_resolved.csv"
FAILED_FILE = BASE_DIR / "targets_unresolved.csv"

print()
print("=" * 60)
print("Quiet Sky Coordinate Resolver V2")
print("=" * 60)

resolved = []
failed = []

with open(
    INPUT_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        name = row["name"]
        category = row["category"]

        print()
        print(f"Resolving: {name}")

        try:

            coord = SkyCoord.from_name(
                name
            )

            resolved.append({

                "name": name,
                "category": category,
                "ra": coord.ra.deg,
                "dec": coord.dec.deg

            })

            print(
                f"  RA  = {coord.ra.deg:.6f}"
            )

            print(
                f"  DEC = {coord.dec.deg:.6f}"
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

#
# Save resolved
#

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

#
# Save unresolved
#

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

print()
print("=" * 60)
print("Resolution Complete")
print("=" * 60)

print(
    f"Resolved: {len(resolved)}"
)

print(
    f"Failed:   {len(failed)}"
)

print()
print(
    f"Resolved catalog:"
)

print(
    OUTPUT_FILE
)

print()

print(
    f"Unresolved catalog:"
)

print(
    FAILED_FILE
)