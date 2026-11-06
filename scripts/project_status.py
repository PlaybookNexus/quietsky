# project_status.py

from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent.parent

TARGETS_FILE = BASE_DIR / "expanded_targets_v2.csv"

OPTICAL_RANKINGS = (
    BASE_DIR / "rankings_v2.csv"
)

IR_RANKINGS = (
    BASE_DIR / "infrared_rankings_v2.csv"
)

COMPOSITE_RANKINGS = (
    BASE_DIR / "quiet_sky_rankings_v3.csv"
)

HEALTH_REPORT = (
    BASE_DIR / "download_health_report.csv"
)


def file_exists(path):

    return "YES" if path.exists() else "NO"


#
# Target count
#

target_count = 0

if TARGETS_FILE.exists():

    with open(
        TARGETS_FILE,
        newline="",
        encoding="utf-8"
    ) as f:

        target_count = max(
            0,
            sum(1 for _ in f) - 1
        )

#
# Health metrics
#

optical_ready = 0
infrared_ready = 0

if HEALTH_REPORT.exists():

    with open(
        HEALTH_REPORT,
        newline="",
        encoding="utf-8"
    ) as f:

        reader = csv.DictReader(f)

        for row in reader:

            if (
                row["optical_complete"]
                == "YES"
            ):

                optical_ready += 1

            if (
                row["infrared_usable"]
                == "YES"
            ):

                infrared_ready += 1

#
# Optical leader
#

optical_leader = "Unknown"
optical_score = "N/A"

if OPTICAL_RANKINGS.exists():

    with open(
        OPTICAL_RANKINGS,
        newline="",
        encoding="utf-8"
    ) as f:

        reader = csv.DictReader(f)

        try:

            first = next(reader)

            optical_leader = first["name"]

            optical_score = (
                first["score_v2"]
            )

        except StopIteration:

            pass

#
# Infrared leader
#

infrared_leader = "Unknown"
infrared_score = "N/A"

if IR_RANKINGS.exists():

    with open(
        IR_RANKINGS,
        newline="",
        encoding="utf-8"
    ) as f:

        reader = csv.DictReader(f)

        try:

            first = next(reader)

            infrared_leader = first["name"]

            infrared_score = (
                first["infrared_score"]
            )

        except StopIteration:

            pass

#
# Composite leader
#

composite_leader = "Unknown"
composite_score = "N/A"

if COMPOSITE_RANKINGS.exists():

    with open(
        COMPOSITE_RANKINGS,
        newline="",
        encoding="utf-8"
    ) as f:

        reader = csv.DictReader(f)

        try:

            first = next(reader)

            composite_leader = first["name"]

            composite_score = (
                first["composite_score"]
            )

        except StopIteration:

            pass

#
# Display
#

print()
print("=" * 72)
print("                    QUIET SKY STATUS")
print("=" * 72)

print()
print("PROJECT")
print("-" * 72)

print(
    f"Catalog Targets         : "
    f"{target_count}"
)

print(
    f"Optical Ready Targets   : "
    f"{optical_ready}"
)

print(
    f"Infrared Ready Targets  : "
    f"{infrared_ready}"
)

print()

print("FILES")
print("-" * 72)

print(
    f"Optical Rankings        : "
    f"{file_exists(OPTICAL_RANKINGS)}"
)

print(
    f"Infrared Rankings       : "
    f"{file_exists(IR_RANKINGS)}"
)

print(
    f"Composite Rankings      : "
    f"{file_exists(COMPOSITE_RANKINGS)}"
)

print(
    f"Health Report           : "
    f"{file_exists(HEALTH_REPORT)}"
)

print()

print("CURRENT LEADERS")
print("-" * 72)

print(
    f"Optical Leader          : "
    f"{optical_leader}"
)

print(
    f"Optical Score           : "
    f"{optical_score}"
)

print()

print(
    f"Infrared Leader         : "
    f"{infrared_leader}"
)

print(
    f"Infrared Score          : "
    f"{infrared_score}"
)

print()

print(
    f"Composite Leader        : "
    f"{composite_leader}"
)

print(
    f"Composite Score         : "
    f"{composite_score}"
)

print()

print("PIPELINE STATUS")
print("-" * 72)

if optical_ready >= 15:

    print(
        "Optical Pipeline        : READY"
    )

else:

    print(
        "Optical Pipeline        : NEEDS DATA"
    )

if infrared_ready >= 5:

    print(
        "Infrared Pipeline       : READY"
    )

else:

    print(
        "Infrared Pipeline       : EXPERIMENTAL"
    )

if (
    file_exists(COMPOSITE_RANKINGS)
    == "YES"
):

    print(
        "Discovery Engine        : READY"
    )

else:

    print(
        "Discovery Engine        : NOT RUN"
    )

print()
print("=" * 72)
print("Quiet Sky Beta")
print("=" * 72)