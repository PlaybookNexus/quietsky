from pathlib import Path
import csv

import numpy as np

from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
TARGETS_FILE = BASE_DIR / "targets.csv"

SURVEYS = [
    "DSS.fits",
    "DSS2_Red.fits",
    "DSS2_Blue.fits"
]


def safe_name(name):

    return (
        name.replace(" ", "_")
            .replace("/", "_")
            .replace("'", "")
    )


def scalar(value):

    return float(
        np.asarray(value).squeeze()
    )


print()
print("QUIET SKY AUDIT")
print("=" * 90)
print()

print(
    f"{'Target':<20}"
    f"{'Data':<10}"
    f"{'WCS':<10}"
    f"{'Pixel':<10}"
    f"{'Status':<20}"
)

print("-" * 90)

with open(
    TARGETS_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        name = row["name"]

        target = SkyCoord(
            ra=float(row["ra"]),
            dec=float(row["dec"]),
            unit="deg"
        )

        folder = (
            DATA_DIR /
            safe_name(name)
        )

        #
        # Folder exists?
        #

        if not folder.exists():

            print(
                f"{name:<20}"
                f"{'NO':<10}"
                f"{'-':<10}"
                f"{'-':<10}"
                f"{'Missing folder'}"
            )

            continue

        #
        # Try DSS first
        #

        dss_file = (
            folder /
            "DSS.fits"
        )

        if not dss_file.exists():

            print(
                f"{name:<20}"
                f"{'NO':<10}"
                f"{'-':<10}"
                f"{'-':<10}"
                f"{'Missing DSS'}"
            )

            continue

        try:

            hdul = fits.open(
                dss_file
            )

            img = hdul[0].data

            wcs = WCS(
                hdul[0].header
            )

            x, y = (
                wcs.world_to_pixel(
                    target
                )
            )

            x = scalar(x)
            y = scalar(y)

            #
            # Inside image?
            #

            inside = (
                0 <= x < img.shape[1]
                and
                0 <= y < img.shape[0]
            )

            if inside:

                status = "READY"

            else:

                status = "OFF IMAGE"

            print(
                f"{name:<20}"
                f"{'YES':<10}"
                f"{'YES':<10}"
                f"{'YES':<10}"
                f"{status}"
            )

        except Exception as e:

            print(
                f"{name:<20}"
                f"{'YES':<10}"
                f"{'FAIL':<10}"
                f"{'-':<10}"
                f"{str(e)[:20]}"
            )

print()
print("=" * 90)
print("Audit complete.")