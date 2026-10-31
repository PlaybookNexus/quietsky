from pathlib import Path
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

files = [
    "DSS.fits",
    "DSS2_Red.fits",
    "DSS2_Blue.fits"
]

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for ax, name in zip(axes, files):

    img = fits.getdata(DATA_DIR / name)

    vmin = np.percentile(img, 5)
    vmax = np.percentile(img, 99)

    ax.imshow(
        img,
        cmap="gray",
        origin="lower",
        vmin=vmin,
        vmax=vmax
    )

    ax.set_title(name)

plt.tight_layout()
plt.show()
