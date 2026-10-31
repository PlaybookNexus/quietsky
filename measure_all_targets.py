from pathlib import Path
import csv

import numpy as np

from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
TARGETS_FILE = BASE_DIR / "targets.csv"
RESULTS_FILE = BASE_DIR / "results.csv"

SURVEYS = [
    ("DSS.fits", "dss_ratio"),
    ("DSS2_Red.fits", "dss2red_ratio"),
    ("DSS2_Blue.fits", "dss2blue_ratio")
]

APERTURE_RADIUS = 2


def safe_name(name):

    return (
        name.replace(" ", "_")
            .replace("/", "_")
            .replace("'", "")
    )


def to_pixel(value):

    return int(
        np.rint(
            float(
                np.asarray(value).squeeze()
            )
        )
    )


def measure_flux(img, x, y):

    x = to_pixel(x)
    y = to_pixel(y)

    #
    # Edge protection
    #

    if (
        x < 10 or
        y < 10 or
        x > img.shape[1] - 10 or
        y > img.shape[0] - 10
    ):
        return None

    #
    # 5x5 aperture
    #

    star_box = img[
        y - APERTURE_RADIUS:y + APERTURE_RADIUS + 1,
        x - APERTURE_RADIUS:x + APERTURE_RADIUS + 1
    ]

    return float(
        np.sum(star_box)
    )


print()
print("Quiet Sky Target Measurements")
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

        print()
        print(name)

        target = SkyCoord(
            ra=float(row["ra"]),
            dec=float(row["dec"]),
            unit="deg"
        )

        target_folder = (
            DATA_DIR /
            safe_name(name)
        )

        fluxes = {}

        #
        # Measure each survey
        #

        for filename, field in SURVEYS:

            filepath = (
                target_folder /
                filename
            )

            if not filepath.exists():

                print(
                    f"  Missing {filename}"
                )

                fluxes[field] = None
                continue

            try:

                hdul = fits.open(filepath)

                img = hdul[0].data

                wcs = WCS(
                    hdul[0].header
                )

                x, y = (
                    wcs.world_to_pixel(
                        target
                    )
                )

                flux = measure_flux(
                    img,
                    x,
                    y
                )

                fluxes[field] = flux

                if flux is not None:

                    print(
                        f"  {filename}: "
                        f"{flux:.0f}"
                    )

                else:

                    print(
                        f"  {filename}: edge"
                    )

            except Exception as e:

                fluxes[field] = None

                print(
                    f"  ERROR {filename}"
                )

                print(
                    f"      {e}"
                )

        #
        # Normalization
        #

        valid_fluxes = [
            v
            for v in fluxes.values()
            if v is not None
        ]

        output_row = {
            "name": name,
            "category": category
        }

        if len(valid_fluxes) >= 2:

            mean_flux = np.mean(
                valid_fluxes
            )

            for _, field in SURVEYS:

                value = fluxes[field]

                if value is None:

                    output_row[field] = ""

                else:

                    output_row[field] = (
                        value / mean_flux
                    )

        else:

            for _, field in SURVEYS:

                output_row[field] = ""

        results.append(
            output_row
        )

#
# Save CSV
#

with open(
    RESULTS_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow([
        "name",
        "category",
        "dss_ratio",
        "dss2red_ratio",
        "dss2blue_ratio"
    ])

    for row in results:

        writer.writerow([
            row["name"],
            row["category"],
            row["dss_ratio"],
            row["dss2red_ratio"],
            row["dss2blue_ratio"]
        ])

print()
print("=" * 60)
print(f"Saved: {RESULTS_FILE}")