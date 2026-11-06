# test_skyview.py

from astroquery.skyview import SkyView

print("URL:")
print(SkyView.URL)

print()
print("Testing surveys...")

try:

    surveys = SkyView.get_surveys()

    print(
        f"Found {len(surveys)} surveys"
    )

except Exception as e:

    print(e)