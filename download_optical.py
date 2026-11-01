# download_optical.py

from pathlib import Path
import csv

from astroquery.skyview import SkyView
from astropy.coordinates import SkyCoord
import astropy.units as u

BASE_DIR = Path(__file__).resolve().parent.parent

TARGETS_FILE = BASE_DIR / "targets_beta.csv"
DATA_DIR = BASE_DIR / "data"

SURVEYS = [

    ("DSS", "DSS.fits"),

    ("DSS2 Red", "DSS2_Red.fits"),

    ("DSS2 Blue", "DSS2_Blue.fits")

]


def safe_name(name):

    return (
        name.replace(" ", "_")
            .replace("/", "_")
            .replace("'", "")
    )


print()
print("=" * 60)
print("Quiet Sky Optical Downloads")
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

        print()
        print("=" * 60)
        print(name)
        print("=" * 60)

        coord = SkyCoord(
            ra=ra * u.deg,
            dec=dec * u.deg,
            frame="icrs"
        )

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