from pathlib import Path

from astropy.io import fits

import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

#
# Load images
#

dss = fits.getdata(DATA_DIR / "DSS.fits")
red = fits.getdata(DATA_DIR / "DSS2_Red.fits")
blue = fits.getdata(DATA_DIR / "DSS2_Blue.fits")

#
# Normalize
#

def normalize(img):

    vmin = np.percentile(img, 5)
    vmax = np.percentile(img, 99)

    img = np.clip(img, vmin, vmax)

    return (
        img - vmin
    ) / (
        vmax - vmin
    )


dss = normalize(dss)
red = normalize(red)
blue = normalize(blue)

#
# Differences
#

diff_red = red - dss
diff_blue = blue - dss

fig, axes = plt.subplots(
    1,
    2,
    figsize=(12, 6)
)

axes[0].imshow(
    diff_red,
    cmap="seismic",
    origin="lower",
    vmin=-1,
    vmax=1
)

axes[0].set_title(
    "DSS2 Red - DSS"
)

axes[1].imshow(
    diff_blue,
    cmap="seismic",
    origin="lower",
    vmin=-1,
    vmax=1
)

axes[1].set_title(
    "DSS2 Blue - DSS"
)

plt.tight_layout()
plt.show()