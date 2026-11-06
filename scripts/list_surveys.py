# list_surveys.py

from astroquery.skyview import SkyView

surveys = SkyView.list_surveys()

for category in surveys:
    print("\n" + "=" * 60)
    print(category)

    try:
        for survey in surveys[category]:
            print("  ", survey)
    except Exception:
        print(surveys[category])