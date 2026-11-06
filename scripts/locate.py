# locate.py

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

print(f"X={x}")
print(f"Y={y}")

vmin = np.percentile(img, 5)
vmax = np.percentile(img, 99)

plt.figure(figsize=(10,10))
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
    s=300,
    edgecolors="red",
    facecolors="none",
    linewidths=2
)

plt.title("Tabby's Star")
plt.show()