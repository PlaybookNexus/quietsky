import urllib.request

url = (
    "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    "?query=select+top+10+hostname+from+pscomppars"
    "&format=csv"
)

print(
    urllib.request
    .urlopen(url)
    .read()
    .decode("utf-8")
)