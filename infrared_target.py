from pathlib import Path

from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

FILES = [
    "2MASS_J.fits",
    "2MASS_K.fits",
    "WISE_3_4.fits",
    "WISE_4_6.fits"
]

target = SkyCoord(
    ra=301.564331,
    dec=44.457608,
    unit="deg"
)

for filename in FILES:

    hdul = fits.open(DATA_DIR / filename)

    wcs = WCS(hdul[0].header)

    x, y = wcs.world_to_pixel(target)

    print()
    print(filename)
    print(f"X = {float(x):.2f}")
    print(f"Y = {float(y):.2f}")