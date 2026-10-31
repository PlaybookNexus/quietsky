from pathlib import Path

from astropy.io import fits
import matplotlib.pyplot as plt
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

fig, axes = plt.subplots(
    1,
    len(FILES),
    figsize=(20, 5)
)

for ax, filename in zip(axes, FILES):

    img = fits.getdata(DATA_DIR / filename)

    vmin = np.percentile(img, 5)
    vmax = np.percentile(img, 99)

    ax.imshow(
        img,
        cmap="inferno",
        origin="lower",
        vmin=vmin,
        vmax=vmax
    )

    ax.set_title(filename)
    ax.axis("off")

plt.tight_layout()
plt.show()