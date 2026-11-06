from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent.parent

CATALOG_DIR = (
    BASE_DIR / "catalogs"
)

CATALOG_DIR.mkdir(
    exist_ok=True
)

# =====================================================
# SEED CATALOGS
# =====================================================

CATALOGS = {

    "exoplanets.csv": [

        ("Ross 128", "Exoplanet"),
        ("TRAPPIST-1", "Exoplanet"),
        ("TOI-270", "Exoplanet"),
        ("LHS 1140", "Exoplanet"),
        ("GJ 1214", "Exoplanet"),
        ("HD 219134", "Exoplanet"),
        ("K2-18", "Exoplanet"),
        ("Proxima Centauri", "Exoplanet"),
        ("55 Cancri", "Exoplanet"),
        ("Tau Ceti", "Exoplanet")

    ],

    "white_dwarfs.csv": [

        ("Ross 640", "WhiteDwarf"),
        ("Sirius B", "WhiteDwarf"),
        ("Stein 2051 B", "WhiteDwarf"),
        ("Wolf 489", "WhiteDwarf"),
        ("WD 1145+017", "WhiteDwarf"),
        ("Procyon B", "WhiteDwarf")

    ],

    "flare_stars.csv": [

        ("AU Microscopii", "Flare"),
        ("EQ Pegasi", "Flare"),
        ("DO Cephei", "Flare"),
        ("AD Leonis", "Flare"),
        ("YZ Canis Minoris", "Flare"),
        ("EV Lacertae", "Flare")

    ],

    "nearby_stars.csv": [

        ("Barnards Star", "Nearby"),
        ("Wolf 359", "Nearby"),
        ("Ross 154", "Nearby"),
        ("Ross 248", "Nearby"),
        ("Lalande 21185", "Nearby")

    ],

    "brown_dwarfs.csv": [

        ("Luhman 16 A", "BrownDwarf"),
        ("Luhman 16 B", "BrownDwarf"),
        ("WISE 0855-0714", "BrownDwarf")

    ],

    "wolf_rayet.csv": [

        ("WR 6", "WolfRayet"),
        ("WR 11", "WolfRayet"),
        ("WR 24", "WolfRayet"),
        ("WR 40", "WolfRayet"),
        ("WR 134", "WolfRayet")

    ],

    "transit_anomalies.csv": [

        ("KIC 8462852", "TransitAnomaly"),
        ("EPIC 204376071", "TransitAnomaly"),
        ("KIC 12557548", "TransitAnomaly")

    ],

    "variable_stars.csv": [

        ("Delta Cephei", "Variable"),
        ("Mira", "Variable"),
        ("RR Lyrae", "Variable"),
        ("Betelgeuse", "Variable")

    ],

    "solar_analogs.csv": [

        ("16 Cygni A", "SolarAnalog"),
        ("16 Cygni B", "SolarAnalog"),
        ("18 Scorpii", "SolarAnalog"),
        ("HD 146233", "SolarAnalog")

    ],

    "young_stars.csv": [

        ("LkCa 15", "YoungStar"),
        ("TW Hydrae", "YoungStar"),
        ("HD 100546", "YoungStar")

    ],

    "debris_disks.csv": [

        ("HD 32297", "DebrisDisk"),
        ("Beta Pictoris", "DebrisDisk"),
        ("Fomalhaut", "DebrisDisk"),
        ("49 Ceti", "DebrisDisk")

    ],

    "eclipsing_binaries.csv": [

        ("Algol", "EclipsingBinary"),
        ("Beta Lyrae", "EclipsingBinary"),
        ("VV Cephei", "EclipsingBinary")

    ]

}

# =====================================================
# WRITE FILES
# =====================================================

for filename, rows in CATALOGS.items():

    filepath = (
        CATALOG_DIR / filename
    )

    with open(
        filepath,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "name",
            "category"
        ])

        writer.writerows(rows)

    print(
        f"Created: {filename} "
        f"({len(rows)} targets)"
    )

print()
print("=" * 60)
print("CATALOG FILES GENERATED")
print("=" * 60)