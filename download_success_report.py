# download_success_report.py

from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
TARGETS_FILE = BASE_DIR / "targets_beta.csv"

HEALTH_CSV = BASE_DIR / "download_health_report.csv"
OPTICAL_READY_CSV = BASE_DIR / "targets_optical_ready.csv"
IR_READY_CSV = BASE_DIR / "targets_infrared_ready.csv"

OPTICAL_FILES = [
    "DSS.fits",
    "DSS2_Red.fits",
    "DSS2_Blue.fits"
]

IR_FILES = [
    "2MASS_J.fits",
    "2MASS_K.fits",
    "WISE_3_4.fits",
    "WISE_4_6.fits"
]


def safe_name(name):

    return (
        name.replace(" ", "_")
            .replace("/", "_")
            .replace("'", "")
    )


print()
print("=" * 80)
print("                 QUIET SKY DATA HEALTH REPORT")
print("=" * 80)

results = []

#
# Scan catalog
#

with open(
    TARGETS_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        name = row["name"]
        category = row["category"]

        folder = DATA_DIR / safe_name(name)

        optical_count = 0
        infrared_count = 0

        for filename in OPTICAL_FILES:

            if (folder / filename).exists():

                optical_count += 1

        for filename in IR_FILES:

            if (folder / filename).exists():

                infrared_count += 1

        total_files = (
            optical_count +
            infrared_count
        )

        results.append({

            "name":
                name,

            "category":
                category,

            "optical":
                optical_count,

            "infrared":
                infrared_count,

            "total":
                total_files
        })

#
# Summary metrics
#

total_targets = len(results)

full_optical = sum(
    1
    for r in results
    if r["optical"] == 3
)

full_infrared = sum(
    1
    for r in results
    if r["infrared"] == 4
)

usable_optical = sum(
    1
    for r in results
    if r["optical"] >= 2
)

usable_infrared = sum(
    1
    for r in results
    if r["infrared"] >= 2
)

optical_pct = (
    100 * full_optical / total_targets
)

infrared_pct = (
    100 * full_infrared / total_targets
)

#
# Console report
#

print()

print(
    f"{'Target':<25}"
    f"{'Category':<12}"
    f"{'Optical':<10}"
    f"{'Infrared'}"
)

print("-" * 80)

for r in sorted(
    results,
    key=lambda x:
        (
            x["optical"],
            x["infrared"]
        )
):

    print(

        f"{r['name']:<25}"
        f"{r['category']:<12}"
        f"{r['optical']}/3".ljust(10)
        + f"{r['infrared']}/4"

    )

print()
print("=" * 80)
print("PIPELINE HEALTH")
print("=" * 80)

print()
print(f"Total Targets            : {total_targets}")
print(f"Full Optical Coverage    : {full_optical}")
print(f"Full Infrared Coverage   : {full_infrared}")
print(f"Usable Optical Targets   : {usable_optical}")
print(f"Usable Infrared Targets  : {usable_infrared}")

print()
print(
    f"Optical Success Rate     : "
    f"{optical_pct:.1f}%"
)

print(
    f"Infrared Success Rate    : "
    f"{infrared_pct:.1f}%"
)

#
# Save master health report
#

sorted_results = sorted(
    results,
    key=lambda r: (
        r["total"],
        r["optical"],
        r["infrared"]
    ),
    reverse=True
)

with open(
    HEALTH_CSV,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow([

        "name",
        "category",

        "optical_files",
        "infrared_files",
        "total_files",

        "optical_complete",
        "infrared_usable"

    ])

    for r in sorted_results:

        writer.writerow([

            r["name"],
            r["category"],

            r["optical"],
            r["infrared"],

            r["total"],

            "YES" if r["optical"] == 3 else "NO",

            "YES" if r["infrared"] >= 2 else "NO"

        ])

#
# Optical-ready catalog
#

with open(
    OPTICAL_READY_CSV,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow([
        "name",
        "category"
    ])

    for r in results:

        if r["optical"] == 3:

            writer.writerow([

                r["name"],
                r["category"]

            ])

#
# IR-ready catalog
#

with open(
    IR_READY_CSV,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow([
        "name",
        "category"
    ])

    for r in results:

        if r["infrared"] >= 2:

            writer.writerow([

                r["name"],
                r["category"]

            ])

print()
print("=" * 80)
print("EXPORTS")
print("=" * 80)

print(
    f"Health CSV            : "
    f"{HEALTH_CSV.name}"
)

print(
    f"Optical Ready Catalog : "
    f"{OPTICAL_READY_CSV.name}"
)

print(
    f"Infrared Ready Catalog: "
    f"{IR_READY_CSV.name}"
)

print()

print(
    f"Optical-ready targets : "
    f"{full_optical}"
)

print(
    f"Infrared-ready targets: "
    f"{usable_infrared}"
)

print()

if full_optical >= 15:

    print(
        "Status: Optical Beta Ready ✅"
    )

else:

    print(
        "Status: More optical data needed ⚠️"
    )

if usable_infrared >= 10:

    print(
        "Status: Infrared Beta Ready ✅"
    )

else:

    print(
        "Status: Infrared still experimental ⚠️"
    )

print()
print("=" * 80)
print("Health analysis complete.")
print("=" * 80)