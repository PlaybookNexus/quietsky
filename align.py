from pathlib import Path

from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord

import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

FILES = [
    "DSS.fits",
    "DSS2_Red.fits",
    "DSS2_Blue.fits"
]

TARGET = SkyCoord(
    ra=301.564331,
    dec=44.457608,
    unit="deg"
)

fig, axes = plt.subplots(
    1,
    len(FILES),
    figsize=(15, 5)
)

for ax, filename in zip(axes, FILES):

    hdul = fits.open(DATA_DIR / filename)

    img = hdul[0].data
    wcs = WCS(hdul[0].header)

    x, y = wcs.world_to_pixel(TARGET)

    vmin = np.percentile(img, 5)
    vmax = np.percentile(img, 99)

    ax.imshow(
        img,
        cmap="gray",
        origin="lower",
        vmin=vmin,
        vmax=vmax
    )

    ax.scatter(
        [x],
        [y],
        s=250,
        edgecolors="red",
        facecolors="none",
        linewidths=2
    )

    ax.set_title(filename)

plt.tight_layout()
plt.show()