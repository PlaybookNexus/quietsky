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

TARGET = SkyCoord(
    ra=301.564331,
    dec=44.457608,
    unit="deg"
)

# Ref3 removed
REFERENCE_STARS = [
    SkyCoord(
        ra=301.599397,
        dec=44.461381,
        unit="deg"
    ),
    SkyCoord(
        ra=301.532587,
        dec=44.434465,
        unit="deg"
    )
]

BOX = 2


def measure_flux(img, x, y):

    x = int(np.rint(float(np.asarray(x).squeeze())))
    y = int(np.rint(float(np.asarray(y).squeeze())))

    box = img[
        y - BOX:y + BOX + 1,
        x - BOX:x + BOX + 1
    ]

    return np.sum(box)


print()
print("Differential Photometry v3")
print("=" * 60)

for filename in FILES:

    print()
    print(f"Survey: {filename}")
    print("-" * 60)

    hdul = fits.open(DATA_DIR / filename)

    img = hdul[0].data
    wcs = WCS(hdul[0].header)

    x_target, y_target = wcs.world_to_pixel(TARGET)

    target_flux = measure_flux(
        img,
        x_target,
        y_target
    )

    print(
        f"Target Pixel: "
        f"({float(x_target):.2f}, "
        f"{float(y_target):.2f})"
    )

    ref_fluxes = []

    for idx, star in enumerate(
        REFERENCE_STARS,
        start=1
    ):

        x_ref, y_ref = wcs.world_to_pixel(star)

        flux = measure_flux(
            img,
            x_ref,
            y_ref
        )

        ref_fluxes.append(flux)

        print(
            f"Ref {idx}: "
            f"Pixel=({float(x_ref):.2f}, "
            f"{float(y_ref):.2f}) "
            f"Flux={flux:.0f}"
        )

    average_ref = np.mean(ref_fluxes)

    relative = target_flux / average_ref

    print()
    print(f"Target Flux : {target_flux:.0f}")
    print(f"Average Ref : {average_ref:.0f}")
    print(f"Relative    : {relative:.4f}")

    print()
    print("Target / Ref Ratios")

    for idx, flux in enumerate(
        ref_fluxes,
        start=1
    ):

        ratio = target_flux / flux

        print(
            f"Ref{idx}: {ratio:.4f}"
        )

print()
print("Done.")