# hypothesis_report.py

from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent.parent

COMPOSITE_FILE = BASE_DIR / "quiet_sky_rankings_v3.csv"

print()
print("=" * 72)
print("                 QUIET SKY HYPOTHESIS REPORT")
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
# Top candidates only
#

TOP_N = 10

for target in targets[:TOP_N]:

    print()
    print("=" * 72)
    print(target["name"])
    print("=" * 72)

    print(
        f"Category           : {target['category']}"
    )

    print(
        f"Composite Rank     : #{target['rank']}"
    )

    print(
        f"Composite Score    : "
        f"{target['composite_score']:.4f}"
    )

    print()

    print(
        f"Optical Score      : "
        f"{target['optical_score']:.4f}"
    )

    print(
        f"Infrared Score     : "
        f"{target['infrared_score']:.4f}"
    )

    print(
        f"IR Coverage        : "
        f"{target['infrared_coverage']:.2f}"
    )

    print(
        f"IR Confidence      : "
        f"{target['infrared_confidence']}"
    )

    print()
    print("OBSERVATIONS")
    print("-" * 72)

    observations = []

    optical = target["optical_score"]
    infrared = target["infrared_score"]

    if optical > infrared * 1.5:

        observations.append(
            "Optical anomaly stronger than infrared anomaly."
        )

    elif infrared > optical * 1.5:

        observations.append(
            "Infrared anomaly stronger than optical anomaly."
        )

    else:

        observations.append(
            "Optical and infrared signatures are broadly aligned."
        )

    if target["infrared_confidence"] == "HIGH":

        observations.append(
            "Infrared evidence has high confidence."
        )

    elif target["infrared_confidence"] == "MEDIUM":

        observations.append(
            "Infrared evidence has moderate confidence."
        )

    else:

        observations.append(
            "Limited infrared evidence available."
        )

    for item in observations:

        print(
            f"- {item}"
        )

    print()
    print("HYPOTHESES")
    print("-" * 72)

    hypotheses = []

    #
    # Optical dominant
    #

    if optical > 0.5 and infrared == 0:

        hypotheses.append(
            "Candidate may represent optical variability without supporting infrared data."
        )

    #
    # Infrared dominant
    #

    if (
        infrared > optical * 1.5
        and infrared > 0
    ):

        hypotheses.append(
            "Target may exhibit stronger infrared behavior than optical behavior."
        )

    #
    # Multi-wavelength
    #

    if (
        optical > 0.4
        and infrared > 0.4
    ):

        hypotheses.append(
            "Target appears unusual across multiple wavelength domains."
        )

    #
    # Known variable stars
    #

    if target["category"] == "Variable":

        hypotheses.append(
            "Observed anomaly may be explained by known stellar variability."
        )

    #
    # Exoplanets
    #

    if target["category"] == "Exoplanet":

        hypotheses.append(
            "Host-star or system properties may contribute to the observed signal."
        )

    #
    # Nearby stars
    #

    if target["category"] == "Nearby":

        hypotheses.append(
            "Proper-motion effects may influence multi-epoch measurements."
        )

    #
    # Anomalous candidates
    #

    if target["category"] == "Anomalous":

        hypotheses.append(
            "Target merits continued monitoring due to sustained anomaly ranking."
        )

    if not hypotheses:

        hypotheses.append(
            "No obvious explanatory pattern identified from current data."
        )

    for item in hypotheses:

        print(
            f"- {item}"
        )

    print()
    print("RECOMMENDED ACTION")
    print("-" * 72)

    if target["rank"] <= 3:

        print(
            "Priority 1: Detailed follow-up recommended."
        )

    elif target["rank"] <= 5:

        print(
            "Priority 2: Additional data collection recommended."
        )

    else:

        print(
            "Monitor and revisit after additional survey coverage."
        )

print()
print("=" * 72)
print(
    f"Hypotheses generated for top {TOP_N} candidates."
)
print("=" * 72)