# candidate_comparison.py

from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent.parent

COMPOSITE_FILE = BASE_DIR / "quiet_sky_rankings_v3.csv"

TOP_N = 5

print()
print("=" * 72)
print("                QUIET SKY CANDIDATE COMPARISON")
print("=" * 72)

#
# Load composite rankings
#

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
# Compare consecutive candidates
#

for i in range(min(len(targets) - 1, TOP_N - 1)):

    a = targets[i]
    b = targets[i + 1]

    print()
    print("=" * 72)
    print(
        f"#{a['rank']} {a['name']}"
        f"  vs  "
        f"#{b['rank']} {b['name']}"
    )
    print("=" * 72)

    print()
    print("SCORES")
    print("-" * 72)

    print(
        f"{a['name']:<20}"
        f"Composite: {a['composite_score']:.4f}"
    )

    print(
        f"{b['name']:<20}"
        f"Composite: {b['composite_score']:.4f}"
    )

    difference = (
        a["composite_score"]
        -
        b["composite_score"]
    )

    print()

    print(
        f"Score Difference: "
        f"{difference:.4f}"
    )

    print()
    print("OPTICAL")
    print("-" * 72)

    print(
        f"{a['name']:<20}"
        f"{a['optical_score']:.4f}"
    )

    print(
        f"{b['name']:<20}"
        f"{b['optical_score']:.4f}"
    )

    if (
        a["optical_score"]
        >
        b["optical_score"]
    ):

        optical_winner = a["name"]

    else:

        optical_winner = b["name"]

    print()
    print(
        f"Optical Winner: "
        f"{optical_winner}"
    )

    print()
    print("INFRARED")
    print("-" * 72)

    print(
        f"{a['name']:<20}"
        f"{a['infrared_score']:.4f}"
    )

    print(
        f"{b['name']:<20}"
        f"{b['infrared_score']:.4f}"
    )

    if (
        a["infrared_score"]
        >
        b["infrared_score"]
    ):

        infrared_winner = a["name"]

    else:

        infrared_winner = b["name"]

    print()

    print(
        f"Infrared Winner: "
        f"{infrared_winner}"
    )

    print()
    print("COVERAGE")
    print("-" * 72)

    print(
        f"{a['name']:<20}"
        f"{a['infrared_confidence']}"
    )

    print(
        f"{b['name']:<20}"
        f"{b['infrared_confidence']}"
    )

    print()
    print("INTERPRETATION")
    print("-" * 72)

    explanations = []

    if (
        a["infrared_score"]
        >
        b["infrared_score"] * 1.25
    ):

        explanations.append(
            f"{a['name']} gains a significant "
            f"advantage from infrared analysis."
        )

    if (
        a["optical_score"]
        >
        b["optical_score"] * 1.25
    ):

        explanations.append(
            f"{a['name']} also leads in optical scoring."
        )

    if (
        b["optical_score"]
        >
        a["optical_score"] * 1.25
    ):

        explanations.append(
            f"{b['name']} performs better optically "
            f"but does not fully overcome the "
            f"infrared difference."
        )

    if (
        difference
        < 0.05
    ):

        explanations.append(
            "These candidates are effectively tied."
        )

    if (
        a["infrared_confidence"]
        == "HIGH"
    ):

        explanations.append(
            f"{a['name']} benefits from "
            f"high-confidence infrared coverage."
        )

    if not explanations:

        explanations.append(
            "Ranking difference appears to result "
            "from a combination of factors."
        )

    for explanation in explanations:

        print(
            f"- {explanation}"
        )

print()
print("=" * 72)
print("TOP 5 SUMMARY")
print("=" * 72)

for target in targets[:TOP_N]:

    print(
        f"#{target['rank']:<2} "
        f"{target['name']:<20}"
        f"{target['composite_score']:.4f}"
    )

print()
print("=" * 72)
print("Candidate comparison complete.")
print("=" * 72)