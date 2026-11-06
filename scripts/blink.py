from pathlib import Path

from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

FILES = [
    "DSS.fits",
    "DSS2_Red.fits",
    "DSS2_Blue.fits"
]

TARGET_X = 149
TARGET_Y = 151

images = []

for filename in FILES:

    img = fits.getdata(DATA_DIR / filename)

    vmin = np.percentile(img, 5)
    vmax = np.percentile(img, 99)

    img = np.clip(img, vmin, vmax)
    img = (img - vmin) / (vmax - vmin)

    images.append((filename, img))

index = 0
blinking = True
delay = 0.8

fig, ax = plt.subplots(figsize=(8, 8))


def draw_current():

    ax.clear()

    name, img = images[index]

    ax.imshow(
        img,
        cmap="gray",
        origin="lower"
    )

    ax.scatter(
        [TARGET_X],
        [TARGET_Y],
        s=250,
        edgecolors="red",
        facecolors="none",
        linewidths=2
    )

    ax.set_title(
        f"{name}   |   B=blink  Space=next  +/- speed  Q=quit"
    )

    fig.canvas.draw_idle()


def on_key(event):
    global index
    global blinking
    global delay

    key = event.key.lower() if event.key else ""

    if key == " ":
        blinking = False
        index = (index + 1) % len(images)
        draw_current()

    elif key == "b":
        blinking = not blinking
        print(
            f"Blinking {'ON' if blinking else 'OFF'}"
        )

    elif key in ["+", "="]:
        delay = max(0.1, delay - 0.1)
        print(f"Delay = {delay:.1f}s")

    elif key == "-":
        delay += 0.1
        print(f"Delay = {delay:.1f}s")

    elif key == "q":
        plt.close(fig)


fig.canvas.mpl_connect(
    "key_press_event",
    on_key
)

draw_current()

plt.ion()

while plt.fignum_exists(fig.number):

    if blinking:

        index = (index + 1) % len(images)

        draw_current()

        plt.pause(delay)

    else:

        plt.pause(0.1)

print("Blink viewer closed.")