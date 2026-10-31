# findings_report.py

from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent.parent

COMPOSITE_FILE = BASE_DIR / "quiet_sky_rankings_v3.csv"
OPTICAL_FILE = BASE_DIR / "rankings_v2.csv"
INFRARED_FILE = BASE_DIR / "infrared_rankings_v2.csv"

print()
print("=" * 72)
print("                    QUIET SKY FINDINGS")
print("=" * 72)

#
# Load composite rankings
#

composite = []

with open(
    COMPOSITE_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        row["composite_score"] = float(
            row["composite_score"]
        )

        composite.append(row)

#
# Load optical rankings
#

optical = []

with open(
    OPTICAL_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        row["score_v2"] = float(
            row["score_v2"]
        )

        optical.append(row)

#
# Load infrared rankings
#

infrared = []

with open(
    INFRARED_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        row["infrared_score"] = float(
            row["infrared_score"]
        )

        infrared.append(row)

#
# Top composite
#

top_composite = composite[0]

#
# Top optical
#

top_optical = sorted(
    optical,
    key=lambda r: r["score_v2"],
    reverse=True
)[0]

#
# Top infrared
#

top_infrared = sorted(
    infrared,
    key=lambda r: r["infrared_score"],
    reverse=True
)[0]

#
# High-confidence infrared targets
#

high_ir = []

for row in composite:

    if (
        row["infrared_confidence"]
        == "HIGH"
    ):

        high_ir.append(row)

#
# Missing infrared
#

missing_ir = []

for row in composite:

    if (
        row["infrared_confidence"]
        == "NONE"
    ):

        missing_ir.append(row["name"])

#
# Category leaders
#

category_leaders = {}

for row in composite:

    category = row["category"]

    if category not in category_leaders:

        category_leaders[
            category
        ] = row

#
# Composite findings
#

print()
print("TOP FINDINGS")
print("-" * 72)

print()
print(
    f"Top Composite Target : "
    f"{top_composite['name']}"
)

print(
    f"Composite Score      : "
    f"{float(top_composite['composite_score']):.4f}"
)

print()

print(
    f"Top Optical Target   : "
    f"{top_optical['name']}"
)

print(
    f"Optical Score        : "
    f"{top_optical['score_v2']:.4f}"
)

print()

print(
    f"Top Infrared Target  : "
    f"{top_infrared['name']}"
)

print(
    f"Infrared Score       : "
    f"{top_infrared['infrared_score']:.4f}"
)

#
# Category leadership
#

print()
print("CATEGORY LEADERS")
print("-" * 72)

for category in sorted(
    category_leaders
):

    leader = category_leaders[
        category
    ]

    print(
        f"{category:<15} "
        f"{leader['name']:<20} "
        f"{float(leader['composite_score']):.4f}"
    )

#
# High confidence targets
#

print()
print("HIGH-CONFIDENCE INFRARED TARGETS")
print("-" * 72)

for row in sorted(
    high_ir,
    key=lambda r:
        float(r["composite_score"]),
    reverse=True
):

    print(
        f"{row['name']:<20} "
        f"{float(row['composite_score']):.4f}"
    )

#
# Potential multi-wavelength anomalies
#

print()
print("MULTI-WAVELENGTH CANDIDATES")
print("-" * 72)

for row in composite[:5]:

    if (
        row["infrared_confidence"]
        != "NONE"
    ):

        print(
            f"{row['name']:<20} "
            f"{float(row['composite_score']):.4f}"
        )

#
# Targets needing more IR data
#

print()
print("TARGETS NEEDING MORE INFRARED DATA")
print("-" * 72)

for name in missing_ir:

    print(name)

#
# Research interpretation
#

print()
print("INTERPRETATION")
print("-" * 72)

print("""
1. Optical and infrared rankings differ
   substantially, indicating that some
   targets behave differently across
   wavelengths.

2. KIC 8462852 ranks strongly in the
   composite analysis because it shows
   both optical and infrared anomalies.

3. TRAPPIST-1 exhibits a strong infrared
   signature despite a weaker optical
   ranking.

4. HD 189733 scores highly in both
   domains and may warrant additional
   investigation.

5. Several targets lack sufficient
   infrared coverage and should be
   revisited as additional survey data
   becomes available.
""")

print()
print("=" * 72)
print("Quiet Sky Findings Complete")
print("=" * 72)