from pathlib import Path
from astroquery.skyview import SkyView

TARGET = "KIC 8462852"

SURVEYS = [
    "DSS",
    "DSS2 Red",
    "DSS2 Blue"
]

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(exist_ok=True)

print(f"Target: {TARGET}")
print(f"Saving to: {DATA_DIR}")
print()

for survey in SURVEYS:

    print(f"Downloading {survey}...")

    images = SkyView.get_images(
        position=TARGET,
        survey=[survey]
    )

    filename = survey.replace(" ", "_") + ".fits"
    filepath = DATA_DIR / filename

    images[0][0].writeto(
        str(filepath),
        overwrite=True
    )

    print(f"Saved: {filepath}")

print()
print("All downloads complete.")
