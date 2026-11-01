# download_infrared.py

from pathlib import Path
import csv

from astroquery.skyview import SkyView
from astropy.coordinates import SkyCoord
import astropy.units as u

BASE_DIR = Path(__file__).resolve().parent.parent

TARGETS_FILE = BASE_DIR / "targets_beta.csv"
DATA_DIR = BASE_DIR / "data"

SURVEYS = [

    ("2MASS-J", "2MASS_J.fits"),

    # H-band intentionally excluded
    # ("2MASS-H", "2MASS_H.fits"),

    ("2MASS-K", "2MASS_K.fits"),

    ("WISE 3.4", "WISE_3_4.fits"),

    ("WISE 4.6", "WISE_4_6.fits")

]


def safe_name(name):

    return (
        name.replace(" ", "_")
            .replace("/", "_")
            .replace("'", "")
    )


print()
print("=" * 60)
print("Quiet Sky Infrared Downloads")
print("=" * 60)

with open(
    TARGETS_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        name = row["name"]

        ra = float(row["ra"])
        dec = float(row["dec"])

        target_dir = (
            DATA_DIR /
            safe_name(name)
        )

        target_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        coord = SkyCoord(
            ra=ra * u.deg,
            dec=dec * u.deg,
            frame="icrs"
        )

        print()
        print("=" * 60)
        print(name)
        print("=" * 60)

        for survey_name, filename in SURVEYS:

            output_file = (
                target_dir /
                filename
            )

            if output_file.exists():

                print(
                    f"SKIP {filename}"
                )

                continue

            print(
                f"Downloading {survey_name}..."
            )

            try:

                images = SkyView.get_images(

                    position=coord,

                    survey=[survey_name],

                    pixels=600

                )

                if not images:

                    print(
                        f"FAILED {survey_name}"
                    )

                    continue

                images[0].writeto(
                    output_file,
                    overwrite=True
                )

                print(
                    f"Saved: {filename}"
                )

            except Exception as e:

                print(
                    f"FAILED {survey_name}"
                )

                print(
                    f"Reason: {e}"
                )

print()
print("=" * 60)
print("Finished.")
print("=" * 60)