from pathlib import Path

from astropy.io import fits
from astropy.wcs import WCS

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

hdul = fits.open(DATA_DIR / "DSS.fits")
wcs = WCS(hdul[0].header)

stars = {
    "Target": (149, 151),
    "RefA": (96, 159),
    "RefB": (197, 102),
    "RefC": (238, 224),
}

print()

for name, (x, y) in stars.items():

    ra, dec = wcs.pixel_to_world_values(x, y)

    print(
        f"{name:8}"
        f" RA={ra:.6f}"
        f" DEC={dec:.6f}"
    )