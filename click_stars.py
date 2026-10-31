from pathlib import Path
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

img = fits.getdata(DATA_DIR / "DSS.fits")

vmin = np.percentile(img, 5)
vmax = np.percentile(img, 99)

fig, ax = plt.subplots(figsize=(10,10))

ax.imshow(
    img,
    cmap="gray",
    origin="lower",
    vmin=vmin,
    vmax=vmax
)

def onclick(event):
    if event.xdata is not None:
        print(
            f"X={event.xdata:.1f}  Y={event.ydata:.1f}"
        )

fig.canvas.mpl_connect(
    "button_press_event",
    onclick
)

plt.title("Click Stars")
plt.show()