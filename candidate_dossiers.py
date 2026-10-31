# candidate_dossiers.py

from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent.parent

COMPOSITE_FILE = BASE_DIR / "quiet_sky_rankings_v3.csv"
OPTICAL_FILE = BASE_DIR / "rankings_v2.csv"
INFRARED_FILE = BASE_DIR / "infrared_rankings_v2.csv"

TOP_N = 5

print()
print("=" * 72)
print("                  QUIET SKY CANDIDATE DOSSIERS")
print("=" * 72)

#
# Load optical scores
#

optical = {}

with open(
    OPTICAL_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        optical[row["name"]] = {

            "rank":
                int(row["rank"]),

            "score":
                float(row["score_v2"])
        }

#
# Load infrared scores
#

infrared = {}

with open(
    INFRARED_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        infrared[row["name"]] = {

            "rank":
                int(row["rank"]),

            "score":
                float(
                    row["infrared_score"]
                ),

            "coverage":
                float(
                    row["coverage"]
                ),

            "confidence":
                row["confidence"]
        }

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

        row["rank"] = int(
            row["rank"]
        )

        row["composite_score"] = float(
            row["composite_score"]
        )

        composite.append(row)

#
# Generate dossiers
#

for target in composite[:TOP_N]:

    name = target["name"]

    category = target["category"]

    composite_rank = target["rank"]

    composite_score = (
        target["composite_score"]
    )

    optical_rank = "N/A"
    optical_score = 0.0

    if name in optical:

        optical_rank = (
            optical[name]["rank"]
        )

        optical_score = (
            optical[name]["score"]
        )

    infrared_rank = "N/A"
    infrared_score = 0.0
    confidence = "NONE"
    coverage = 0.0

    if name in infrared:

        infrared_rank = (
            infrared[name]["rank"]
        )

        infrared_score = (
            infrared[name]["score"]
        )

        confidence = (
            infrared[name]["confidence"]
        )

        coverage = (
            infrared[name]["coverage"]
        )

    #
    # Explanation
    #

    findings = []

    if optical_rank != "N/A" and optical_rank <= 5:

        findings.append(
            "Strong optical candidate"
        )

    if infrared_rank != "N/A" and infrared_rank <= 5:

        findings.append(
            "Strong infrared candidate"
        )

    if (
        optical_rank != "N/A"
        and infrared_rank != "N/A"
    ):

        findings.append(
            "Multi-wavelength candidate"
        )

    if confidence == "HIGH":

        findings.append(
            "High-confidence infrared coverage"
        )

    if category == "Variable":

        findings.append(
            "Known variable star"
        )

    elif category == "Nearby":

        findings.append(
            "Nearby stellar system"
        )

    elif category == "Exoplanet":

        findings.append(
            "Exoplanet host system"
        )

    elif category == "Anomalous":

        findings.append(
            "Anomalous candidate target"
        )

    #
    # Assessment
    #

    if composite_rank <= 3:

        assessment = (
            "Priority 1 Investigation"
        )

    elif composite_rank <= 5:

        assessment = (
            "Priority 2 Investigation"
        )

    else:

        assessment = (
            "Monitor"
        )

    #
    # Dossier
    #

    print()
    print("=" * 72)
    print(name)
    print("=" * 72)

    print(
        f"Category           : {category}"
    )

    print(
        f"Composite Rank     : #{composite_rank}"
    )

    print(
        f"Composite Score    : "
        f"{composite_score:.4f}"
    )

    print()

    print(
        f"Optical Rank       : "
        f"{optical_rank}"
    )

    print(
        f"Optical Score      : "
        f"{optical_score:.4f}"
    )

    print()

    print(
        f"Infrared Rank      : "
        f"{infrared_rank}"
    )

    print(
        f"Infrared Score     : "
        f"{infrared_score:.4f}"
    )

    print(
        f"IR Coverage        : "
        f"{coverage:.2f}"
    )

    print(
        f"IR Confidence      : "
        f"{confidence}"
    )

    print()
    print("Key Findings")
    print("-" * 72)

    for item in findings:

        print(
            f"- {item}"
        )

    print()
    print(
        f"Assessment: "
        f"{assessment}"
    )

print()
print("=" * 72)
print(
    f"Generated dossiers for "
    f"top {TOP_N} candidates."
)
print("=" * 72)