# expand_catalog.py

from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_FILE = BASE_DIR / "expanded_targets.csv"

targets = [

    #
    # Existing targets
    #

    ("KIC 8462852",      "Anomalous"),
    ("TRAPPIST-1",       "Exoplanet"),
    ("Vega",             "Control"),
    ("Altair",           "Control"),
    ("Deneb",            "Control"),
    ("Polaris",          "Control"),
    ("Arcturus",         "Control"),
    ("Capella",          "Control"),
    ("Rigel",            "Control"),
    ("Sirius",           "Control"),
    ("Barnards Star",    "Nearby"),
    ("Proxima Centauri", "Nearby"),
    ("Tau Ceti",         "Nearby"),
    ("Betelgeuse",       "Variable"),
    ("Mira",             "Variable"),
    ("Delta Cephei",     "Variable"),
    ("HD 189733",        "Exoplanet"),
    ("Kepler-186",       "Exoplanet"),

    #
    # Additional Variable Stars
    #

    ("RR Lyrae", "Variable"),
    ("Algol", "Variable"),
    ("Omicron Ceti", "Variable"),
    ("Gamma Cassiopeiae", "Variable"),
    ("R Coronae Borealis", "Variable"),
    ("Zeta Geminorum", "Variable"),
    ("T Cephei", "Variable"),
    ("R Aquarii", "Variable"),
    ("Chi Cygni", "Variable"),
    ("W Hydrae", "Variable"),
    ("RS Ophiuchi", "Variable"),
    ("U Monocerotis", "Variable"),
    ("R Leonis", "Variable"),
    ("SU Draconis", "Variable"),
    ("VY Canis Majoris", "Variable"),
    ("XZ Cygni", "Variable"),
    ("R Scuti", "Variable"),
    ("RW Cephei", "Variable"),
    ("T Ursae Minoris", "Variable"),
    ("R Pegasi", "Variable"),

    #
    # Nearby Stars
    #

    ("Wolf 359", "Nearby"),
    ("Lalande 21185", "Nearby"),
    ("Ross 154", "Nearby"),
    ("Ross 248", "Nearby"),
    ("Epsilon Eridani", "Nearby"),
    ("61 Cygni A", "Nearby"),
    ("61 Cygni B", "Nearby"),
    ("Groombridge 34", "Nearby"),
    ("YZ Ceti", "Nearby"),
    ("Teegardens Star", "Nearby"),
    ("Kapteyns Star", "Nearby"),
    ("Gliese 876", "Nearby"),
    ("Gliese 581", "Nearby"),
    ("Luytens Star", "Nearby"),
    ("Gliese 667C", "Nearby"),

    #
    # Exoplanet Hosts
    #

    ("Kepler-22", "Exoplanet"),
    ("Kepler-62", "Exoplanet"),
    ("Kepler-442", "Exoplanet"),
    ("Kepler-452", "Exoplanet"),
    ("WASP-12", "Exoplanet"),
    ("WASP-18", "Exoplanet"),
    ("WASP-121", "Exoplanet"),
    ("WASP-39", "Exoplanet"),
    ("55 Cancri", "Exoplanet"),
    ("HD 209458", "Exoplanet"),
    ("GJ 1214", "Exoplanet"),
    ("LHS 1140", "Exoplanet"),
    ("K2-18", "Exoplanet"),
    ("Kepler-10", "Exoplanet"),
    ("Kepler-90", "Exoplanet"),
    ("TOI-700", "Exoplanet"),
    ("HD 80606", "Exoplanet"),
    ("HD 149026", "Exoplanet"),
    ("CoRoT-7", "Exoplanet"),
    ("HAT-P-7", "Exoplanet"),

    #
    # Controls
    #

    ("Spica", "Control"),
    ("Aldebaran", "Control"),
    ("Antares", "Control"),
    ("Castor", "Control"),
    ("Pollux", "Control"),
    ("Fomalhaut", "Control"),
    ("Regulus", "Control"),
    ("Bellatrix", "Control"),
    ("Alnilam", "Control"),
    ("Alnitak", "Control"),
    ("Mintaka", "Control"),
    ("Dubhe", "Control"),
    ("Merak", "Control"),
    ("Mizar", "Control"),
    ("Alcor", "Control"),
    ("Shaula", "Control"),
    ("Kochab", "Control"),
    ("Hamal", "Control"),
    ("Rasalhague", "Control"),
    ("Denebola", "Control"),
    ("Mirfak", "Control"),
    ("Sadr", "Control"),
    ("Markab", "Control"),
    ("Enif", "Control"),
    ("Alphard", "Control"),
    ("Peacock", "Control"),
    ("Avior", "Control"),
    ("Wezen", "Control"),
    ("Adhara", "Control"),
    ("Menkent", "Control")
]

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow([
        "name",
        "category"
    ])

    for row in targets:
        writer.writerow(row)

print()
print("=" * 60)
print("Quiet Sky Expanded Catalog")
print("=" * 60)
print(
    f"Targets: {len(targets)}"
)
print(
    f"Saved: {OUTPUT_FILE}"
)
print("=" * 60)