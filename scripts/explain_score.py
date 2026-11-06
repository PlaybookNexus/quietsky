from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent.parent

RANKINGS_FILE = BASE_DIR / "rankings_v2.csv"

print()
print("=" * 72)
print("                    QUIET SKY EXPLAINER")
print("=" * 72)

with open(
    RANKINGS_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        name = row["name"]
        category = row["category"]

        score = float(row["score_v2"])
        spread = float(row["spread"])
        variance = float(row["variance"])
        unity = float(row["unity_deviation"])

        print()
        print("=" * 72)
        print(name)
        print("=" * 72)

        print(
            f"Category          : {category}"
        )

        print(
            f"Quiet Sky Score   : {score:.4f}"
        )

        print(
            f"Spread Score      : {spread:.4f}"
        )

        print(
            f"Variance Score    : {variance:.4f}"
        )

        print(
            f"Unity Deviation   : {unity:.4f}"
        )

        print()

        reasons = []

        if spread > 1.0:
            reasons.append(
                "Very large disagreement between surveys"
            )
        elif spread > 0.5:
            reasons.append(
                "Moderate disagreement between surveys"
            )
        else:
            reasons.append(
                "Good agreement between surveys"
            )

        if variance > 0.10:
            reasons.append(
                "High measurement variance"
            )
        elif variance > 0.03:
            reasons.append(
                "Moderate measurement variance"
            )
        else:
            reasons.append(
                "Low measurement variance"
            )

        if unity > 0.40:
            reasons.append(
                "Strong deviation from normalized expectation"
            )
        elif unity > 0.20:
            reasons.append(
                "Moderate deviation from normalized expectation"
            )
        else:
            reasons.append(
                "Measurements remain near expected values"
            )

        #
        # Category-specific commentary
        #

        if category == "Variable":
            reasons.append(
                "Known variable-star category"
            )

        elif category == "Control":
            reasons.append(
                "Expected to be comparatively stable"
            )

        elif category == "Exoplanet":
            reasons.append(
                "Member of exoplanet-host population"
            )

        elif category == "Nearby":
            reasons.append(
                "Nearby stars may exhibit proper-motion effects"
            )

        elif category == "Anomalous":
            reasons.append(
                "Selected as an anomalous-candidate target"
            )

        print("Interpretation")
        print("-" * 72)

        for reason in reasons:

            print(
                f"- {reason}"
            )

        #
        # Risk classification
        #

        print()

        if score > 0.80:

            level = "HIGH"

        elif score > 0.40:

            level = "MEDIUM"

        else:

            level = "LOW"

        print(
            f"Investigation Priority : {level}"
        )

print()
print("=" * 72)
print("Explanation report complete.")
print("=" * 72)