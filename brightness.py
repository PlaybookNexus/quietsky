from pathlib import Path

from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

FILES = [
    "DSS.fits",
    "DSS2_Red.fits",
    "DSS2_Blue.fits"
]

target = SkyCoord.from_name("KIC 8462852")

for filename in FILES:

    hdul = fits.open(DATA_DIR / filename)

    img = hdul[0].data
    wcs = WCS(hdul[0].header)

    x, y = wcs.world_to_pixel(target)

    x = int(x.item())
    y = int(y.item())

    box = img[y-2:y+3, x-2:x+3]

    brightness = np.sum(box)

    print(
        f"{filename:15} brightness = {brightness:12.2f}"
    )