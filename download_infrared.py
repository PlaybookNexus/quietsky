from pathlib import Path
from astroquery.skyview import SkyView

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

TARGET = "KIC 8462852"

SURVEYS = [
    "2MASS-J",
    "2MASS-H",
    "2MASS-K",
    "WISE 3.4",
    "WISE 4.6"
]

for survey in SURVEYS:

    print(f"Downloading {survey}...")

    try:

        images = SkyView.get_images(
            position=TARGET,
            survey=[survey]
        )

        filename = (
            survey
            .replace(" ", "_")
            .replace(".", "_")
            .replace("-", "_")
            + ".fits"
        )

        images[0][0].writeto(
            DATA_DIR / filename,
            overwrite=True
        )

        print("Success")

    except Exception as e:

        print(f"Failed: {e}")

print("Done")