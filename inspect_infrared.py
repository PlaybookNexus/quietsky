# inspect_infrared.py

from pathlib import Path
from astropy.io import fits
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

FILES = [
    "2MASS_J.fits",
    "2MASS_H.fits",
    "2MASS_K.fits",
    "WISE_3_4.fits",
    "WISE_4_6.fits"
]

for filename in FILES:

    img = fits.getdata(DATA_DIR / filename)

    print()
    print(filename)

    print(
        f"Shape: {img.shape}"
    )

    print(
        f"Min: {np.min(img):.3f}"
    )

    print(
        f"Max: {np.max(img):.3f}"
    )

    print(
        f"Mean: {np.mean(img):.3f}"
    )