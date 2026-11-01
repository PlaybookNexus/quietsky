# download_infrared.py

from pathlib import Path
import csv
import time

from astroquery.skyview import SkyView
from astropy.coordinates import SkyCoord
import astropy.units as u

# =====================================================
# CONFIG
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

TARGETS_FILE = BASE_DIR / "targets_beta.csv"

DATA_DIR = BASE_DIR / "data"

PIXELS = 300
RETRIES = 3
DELAY_SECONDS = 2

SURVEYS = [

    ("2MASS-J", "2MASS_J.fits"),

    ("2MASS-K", "2MASS_K.fits"),

    ("WISE 3.4", "WISE_3_4.fits"),

    ("WISE 4.6", "WISE_4_6.fits")

]

# =====================================================
# HELPERS
# =====================================================

def safe_name(name):

    return (

        name.replace(" ", "_")
            .replace("/", "_")
            .replace("'", "")

    )


def download_survey(
    coord,
    survey_name
):

    last_error = None

    for attempt in range(1, RETRIES + 1):

        try:

            print(
                f"Attempt {attempt}/{RETRIES}"
            )

            images = SkyView.get_images(

                position=coord,

                survey=[survey_name],

                pixels=PIXELS

            )

            if images:

                return images

        except Exception as e:

            last_error = e

            print(
                f"Retrying in "
                f"{DELAY_SECONDS}s..."
            )

            time.sleep(
                DELAY_SECONDS
            )

    if last_error:
        if last_error:
    raise last_error

raise RuntimeError(
    f"No images returned for {survey_name}"
)

    raise RuntimeError(
        f"No images returned for {survey_name}"
    )


# =====================================================
# STARTUP
# =====================================================

print()
print("=" * 60)
print("QUIET SKY INFRARED DOWNLOADS")
print("=" * 60)

print()
print("SkyView URL")
print("-" * 60)
print(SkyView.URL)

print()

if not TARGETS_FILE.exists():

    print(
        f"Missing: {TARGETS_FILE}"
    )

    raise SystemExit(1)

success_count = 0
failure_count = 0

# =====================================================
# PROCESS TARGETS
# =====================================================

with open(
    TARGETS_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        name = row["name"]

        ra = float(
            row["ra"]
        )

        dec = float(
            row["dec"]
        )

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

        print(
            f"RA  : {ra:.6f}"
        )

        print(
            f"DEC : {dec:.6f}"
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

            print()
            print(
                f"Downloading "
                f"{survey_name}..."
            )

            try:

                images = download_survey(

                    coord,

                    survey_name

                )

                if not images:

                    print(
                        "No images returned"
                    )

                    failure_count += 1

                    continue

                images[0].writeto(

                    output_file,

                    overwrite=True

                )

                print(
                    f"Saved: {filename}"
                )

                success_count += 1

                time.sleep(
                    DELAY_SECONDS
                )

            except Exception as e:

                print(
                    f"FAILED "
                    f"{survey_name}"
                )

                print(
                    f"Reason: {e}"
                )

                failure_count += 1

# =====================================================
# SUMMARY
# =====================================================

print()
print("=" * 60)
print("DOWNLOADS COMPLETE")
print("=" * 60)

print()

print(
    f"Successful : {success_count}"
)

print(
    f"Failed     : {failure_count}"
)

print(
    f"Targets    : {TARGETS_FILE}"
)

print()