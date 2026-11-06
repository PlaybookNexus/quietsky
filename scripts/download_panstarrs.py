from pathlib import Path
from astroquery.skyview import SkyView

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

TARGET = "KIC 8462852"

SURVEYS = [
    "PanSTARRS g",
    "PanSTARRS r",
    "PanSTARRS i"
]

DATA_DIR.mkdir(exist_ok=True)

for survey in SURVEYS:

    print(f"Downloading {survey}...")

    images = SkyView.get_images(
        position=TARGET,
        survey=[survey]
    )

    filename = (
        survey
        .replace(" ", "_")
        .replace("/", "_")
        + ".fits"
    )

    filepath = DATA_DIR / filename

    images[0][0].writeto(
        filepath,
        overwrite=True
    )

    print(f"Saved: {filepath}")

print()
print("Done.")