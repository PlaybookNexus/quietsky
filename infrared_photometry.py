from pathlib import Path

from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

FILES = [
    "2MASS_J.fits",
    "2MASS_K.fits",
    "WISE_3_4.fits",
    "WISE_4_6.fits"
]

TARGET = SkyCoord(
    ra=301.564331,
    dec=44.457608,
    unit="deg"
)

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

APERTURE_RADIUS = 2


def measure_flux(img, x, y):

    x = int(np.rint(float(np.asarray(x).squeeze())))
    y = int(np.rint(float(np.asarray(y).squeeze())))

    #
    # Avoid edges
    #

    if (
        x < 12 or
        y < 12 or
        x > img.shape[1] - 12 or
        y > img.shape[0] - 12
    ):
        return np.nan

    #
    # Star aperture
    #

    star_box = img[
        y - APERTURE_RADIUS:y + APERTURE_RADIUS + 1,
        x - APERTURE_RADIUS:x + APERTURE_RADIUS + 1
    ]

    star_flux = np.sum(star_box)

    #
    # Background region
    #

    sky_box = img[
        y - 10:y + 11,
        x - 10:x + 11
    ]

    mask = np.ones(
        sky_box.shape,
        dtype=bool
    )

    #
    # Remove center area
    #

    mask[7:14, 7:14] = False

    background_pixels = sky_box[mask]

    background_level = np.median(
        background_pixels
    )

    background_flux = (
        background_level *
        star_box.size
    )

    corrected_flux = (
        star_flux -
        background_flux
    )

    return corrected_flux


print()
print("Infrared Photometry")
print("=" * 60)
print()

results = []

for filename in FILES:

    print(f"Band: {filename}")
    print("-" * 60)

    hdul = fits.open(
        DATA_DIR / filename
    )

    img = hdul[0].data
    wcs = WCS(
        hdul[0].header
    )

    #
    # Target
    #

    x_target, y_target = \
        wcs.world_to_pixel(
            TARGET
        )

    target_flux = measure_flux(
        img,
        x_target,
        y_target
    )

    print(
        f"Target Flux: "
        f"{target_flux:.2f}"
    )

    #
    # References
    #

    ref_fluxes = []

    for idx, star in enumerate(
        REFERENCE_STARS,
        start=1
    ):

        x_ref, y_ref = (
            wcs.world_to_pixel(
                star
            )
        )

        flux = measure_flux(
            img,
            x_ref,
            y_ref
        )

        ref_fluxes.append(flux)

        print(
            f"Ref{idx} Flux: "
            f"{flux:.2f}"
        )

    average_ref = np.nanmean(
        ref_fluxes
    )

    relative = (
        target_flux /
        average_ref
    )

    results.append(
        (
            filename,
            relative
        )
    )

    print(
        f"Average Ref: "
        f"{average_ref:.2f}"
    )

    print(
        f"Relative: "
        f"{relative:.4f}"
    )

    print()

print()
print("=" * 60)
print("SUMMARY")
print("=" * 60)

for band, value in results:

    print(
        f"{band:<20} {value:.4f}"
    )