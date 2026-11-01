from pathlib import Path
import csv
import time

from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
import astropy.units as u

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "expanded_targets.csv"
OUTPUT_FILE = BASE_DIR / "targets_resolved.csv"

print()
print("=" * 60)
print("Quiet Sky Coordinate Resolver")
print("=" * 60)

custom_simbad = Simbad()

print()
print("SIMBAD Configuration")
print("-" * 60)

try:

    print(
        f"Server : {custom_simbad.server}"
    )

except Exception as e:

    print(
        f"Could not determine server: {e}"
    )

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

            result = custom_simbad.query_object(
                name
            )

            if result is None:

                print(
                    "  FAILED: Not Found"
                )

                failed.append(name)
                continue

            ra_str = result["RA"][0]
            dec_str = result["DEC"][0]

            coord = SkyCoord(
                ra_str,
                dec_str,
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
                "ra": ra_deg,
                "dec": dec_deg

            })

            print(
                f"  RA  = {ra_deg:.6f}"
            )

            print(
                f"  DEC = {dec_deg:.6f}"
            )

            #
            # Be polite to SIMBAD
            #

            time.sleep(0.3)

        except Exception as e:

            print(
                f"  ERROR: {e}"
            )

            failed.append(name)

#
# Save resolved catalog
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

print()
print("=" * 60)
print("Coordinate Resolution Complete")
print("=" * 60)

print(
    f"Resolved: {len(resolved)}"
)

print(
    f"Failed:   {len(failed)}"
)

if failed:

    print()
    print("FAILED OBJECTS")

    print("-" * 60)

    for name in failed:

        print(name)

print()
print(
    f"Saved: {OUTPUT_FILE}"
)