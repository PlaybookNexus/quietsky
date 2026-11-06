# discovery_report.py

from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent.parent

COMPOSITE_FILE = BASE_DIR / "quiet_sky_rankings_v3.csv"

print()
print("=" * 72)
print("                  QUIET SKY DISCOVERY REPORT")
print("=" * 72)

targets = []

with open(
    COMPOSITE_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        row["rank"] = int(row["rank"])

        row["composite_score"] = float(
            row["composite_score"]
        )

        row["optical_score"] = float(
            row["optical_score"]
        )

        row["infrared_score"] = float(
            row["infrared_score"]
        )

        row["infrared_coverage"] = float(
            row["infrared_coverage"]
        )

        targets.append(row)

#
# Discovery categories
#

infrared_outliers = []
optical_outliers = []
data_limited = []
high_confidence = []

for target in targets:

    optical = target["optical_score"]
    infrared = target["infrared_score"]

    #
    # Infrared much stronger
    #

    if (
        infrared > 0
        and
        infrared > optical * 2
    ):

        infrared_outliers.append(
            target
        )

    #
    # Optical much stronger
    #

    elif (
        optical > 0
        and
        optical > max(infrared, 0.01) * 2
    ):

        optical_outliers.append(
            target
        )

    #
    # Missing weak data
    #

    if (
        target["infrared_confidence"]
        == "NONE"
        and
        optical > 0.3
    ):

        data_limited.append(
            target
        )

    #
    # Strong confidence
    #

    if (
        target["infrared_confidence"]
        == "HIGH"
        and
        target["composite_score"]
        > 0.4
    ):

        high_confidence.append(
            target
        )

#
# Unexpected infrared detections
#

print()
print("UNEXPECTED INFRARED CANDIDATES")
print("-" * 72)

if infrared_outliers:

    for target in infrared_outliers:

        print()
        print(
            f"{target['name']}"
        )

        print(
            f"  Composite Rank : "
            f"#{target['rank']}"
        )

        print(
            f"  Optical Score  : "
            f"{target['optical_score']:.4f}"
        )

        print(
            f"  Infrared Score : "
            f"{target['infrared_score']:.4f}"
        )

        print()

        print(
            "  Discovery:"
        )

        print(
            "    Infrared signal greatly "
            "exceeds optical signal."
        )

else:

    print(
        "No significant infrared outliers detected."
    )

#
# Unexpected optical detections
#

print()
print("OPTICAL-DOMINANT CANDIDATES")
print("-" * 72)

if optical_outliers:

    for target in optical_outliers:

        print()
        print(
            f"{target['name']}"
        )

        print(
            f"  Composite Rank : "
            f"#{target['rank']}"
        )

        print(
            f"  Optical Score  : "
            f"{target['optical_score']:.4f}"
        )

        print(
            f"  Infrared Score : "
            f"{target['infrared_score']:.4f}"
        )

        print()

        print(
            "  Discovery:"
        )

        print(
            "    Optical signal exceeds "
            "infrared behavior."
        )

else:

    print(
        "No significant optical-dominant targets."
    )

#
# High confidence discoveries
#

print()
print("HIGH-CONFIDENCE DISCOVERIES")
print("-" * 72)

for target in sorted(
    high_confidence,
    key=lambda t:
        t["composite_score"],
    reverse=True
):

    print(
        f"#{target['rank']:<2} "
        f"{target['name']:<20} "
        f"{target['composite_score']:.4f}"
    )

#
# Data limited discoveries
#

print()
print("DATA-LIMITED ANOMALIES")
print("-" * 72)

for target in sorted(
    data_limited,
    key=lambda t:
        t["composite_score"],
    reverse=True
):

    print(
        f"#{target['rank']:<2} "
        f"{target['name']:<20} "
        f"{target['composite_score']:.4f}"
    )

#
# Most interesting objects
#

print()
print("MOST INTERESTING CURRENT TARGETS")
print("-" * 72)

for target in targets[:5]:

    print(
        f"#{target['rank']:<2} "
        f"{target['name']:<20} "
        f"{target['composite_score']:.4f}"
    )

#
# Executive interpretation
#

print()
print("DISCOVERY SUMMARY")
print("-" * 72)

print()

print(
    "Quiet Sky identified several targets "
    "that behave differently in optical and "
    "infrared analysis."
)

print()

print(
    "Particularly notable are targets that "
    "remain highly ranked across multiple "
    "independent scoring systems."
)

print()

print(
    "Current leading multi-wavelength "
    "candidates include:"
)

for target in targets[:3]:

    print(
        f"  - {target['name']}"
    )

print()

print(
    "The highest-value future work is "
    "improving infrared completeness for "
    "strong optical candidates."
)

print()
print("=" * 72)
print("Discovery analysis complete.")
print("=" * 72)