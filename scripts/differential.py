from pathlib import Path

from astropy.io import fits
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

FILES = [
    "DSS.fits",
    "DSS2_Red.fits",
    "DSS2_Blue.fits"
]

# x, y
TARGET = (149, 151)

REFS = [
    (96, 159),
    (197, 102),
    (238, 224)
]

BOX = 2


def flux(img, x, y):

    box = img[
        y - BOX:y + BOX + 1,
        x - BOX:x + BOX + 1
    ]

    return np.sum(box)


print()
print("Survey".ljust(15), "Relative Brightness")
print("-" * 40)

for filename in FILES:

    img = fits.getdata(DATA_DIR / filename)

    target_flux = flux(
        img,
        TARGET[0],
        TARGET[1]
    )

    ref_fluxes = []

    for x, y in REFS:

        ref_fluxes.append(
            flux(img, x, y)
        )

    average_ref = np.mean(ref_fluxes)

    relative = (
        target_flux /
        average_ref
    )

    print(
        f"{filename:<15} {relative:.4f}"
    )