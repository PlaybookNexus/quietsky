# test_skyview_download.py

from astroquery.skyview import SkyView

try:

    images = SkyView.get_images(
        position="TRAPPIST-1",
        survey=["2MASS-J"],
        pixels=300
    )

    print("SUCCESS")
    print(len(images))

except Exception as e:

    print("FAILED")
    print(e)