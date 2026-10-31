from pathlib import Path
import csv
import time

from astroquery.skyview import SkyView

BASE_DIR = Path(__file__).resolve().parent.parent

TARGETS_FILE = BASE_DIR / "targets.csv"
DATA_DIR = BASE_DIR / "data"

SURVEYS = [
    "DSS",
    "DSS2 Red",
    "DSS2 Blue"
]


def safe_name(name):
    return (
        name.replace(" ", "_")
            .replace("/", "_")
            .replace("'", "")
    )


print()
print("Downloading Target Surveys")
print("=" * 60)

with open(
    TARGETS_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        name = row["name"].strip()

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

        position = f"{ra} {dec}"

        for survey in SURVEYS:

            filename = (
                survey
                .replace(" ", "_")
                .replace("/", "_")
                + ".fits"
            )

            filepath = (
                target_dir /
                filename
            )

            #
            # Skip existing files
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

                images[0][0].writeto(
                    filepath,
                    overwrite=True
                )

                print(
                    f"SAVED {filename}"
                )

                #
                # Be nice to SkyView
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