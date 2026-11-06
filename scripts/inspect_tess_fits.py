# inspect_tess_fits.py

from astropy.io import fits

file = r"C:\Astromony\TabbysStar\data\11_Com\tess\mastDownload\TESS\tess2022057073128-s0049-0000000072437047-0221-s\tess2022057073128-s0049-0000000072437047-0221-s_lc.fits"

with fits.open(file) as hdul:

    hdul.info()

    print()

    for i, hdu in enumerate(hdul):

        print("=" * 60)
        print(f"HDU {i}")
        print("=" * 60)

        try:
            print(hdu.header)
        except Exception:
            pass