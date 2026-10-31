# download_all_infrared.py

from pathlib import Path
import csv
import time

from astroquery.skyview import SkyView

BASE_DIR = Path(__file__).resolve().parent.parent

TARGETS_FILE = BASE_DIR / "targets_beta.csv"
DATA_DIR = BASE_DIR / "data"

SURVEYS = [
    ("2MASS-J", "2MASS_J.fits"),
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

        print()
        print("=" * 60)
        print(name)
        print("=" * 60)

        position = (
            f"{ra} {dec}"
        )

        for survey, filename in SURVEYS:

            filepath = (
                target_dir /
                filename
            )

            #
            # Skip existing downloads
            #

            if filepath.exists():

                print(
                    f"SKIP {filename}"
                )

                continue

            try:

                print(
                    f"Downloading {survey}..."
                )

                images = SkyView.get_images(
                    position=position,
                    survey=[survey]
                )

                if not images:

                    print(
                        f"FAILED {survey}"
                    )

                    continue

                images[0][0].writeto(
                    filepath,
                    overwrite=True
                )

                print(
                    f"SAVED {filename}"
                )

                #
                # Be polite to SkyView
                #

                time.sleep(1)

            except Exception as e:

                print(
                    f"FAILED {survey}"
                )

                print(
                    f"Reason: {e}"
                )

print()
print("=" * 60)
print("Finished.")