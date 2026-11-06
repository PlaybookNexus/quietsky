# test_url.py

import urllib.parse

query = """
select hostname
from pscomppars
"""

url = (
    "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?"
    + urllib.parse.urlencode({
        "query": query,
        "format": "csv"
    })
)

print(url)