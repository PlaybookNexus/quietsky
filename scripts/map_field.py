# map_field.py

from pathlib import Path

from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

hdul = fits.open(DATA_DIR / "DSS.fits")

img = hdul[0].data
wcs = WCS(hdul[0].header)

target = SkyCoord.from_name("KIC 8462852")

x, y = wcs.world_to_pixel(target)

x = float(np.asarray(x).squeeze())
y = float(np.asarray(y).squeeze())

vmin = np.percentile(img, 5)
vmax = np.percentile(img, 99)

plt.figure(figsize=(12,12))

plt.imshow(
    img,
    cmap="gray",
    origin="lower",
    vmin=vmin,
    vmax=vmax
)

plt.scatter(
    [x],
    [y],
    s=500,
    edgecolors="red",
    facecolors="none",
    linewidths=2
)

plt.grid(True)

plt.title("Tabby's Star Field")
plt.show()