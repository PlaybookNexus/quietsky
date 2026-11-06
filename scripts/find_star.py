from pathlib import Path

from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

file = DATA_DIR / "DSS.fits"

hdul = fits.open(file)

wcs = WCS(hdul[0].header)

target = SkyCoord.from_name("KIC 8462852")

x, y = wcs.world_to_pixel(target)

print()
print("Tabby's Star")
print(f"RA  = {target.ra.deg:.6f}")
print(f"DEC = {target.dec.deg:.6f}")
print()
print(f"Pixel X = {x:.2f}")
print(f"Pixel Y = {y:.2f}")