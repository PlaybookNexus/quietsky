# quiet_sky.py

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

MENU = {

    #
    # Data Acquisition
    #

    "1": (
        "Download Optical Surveys",
        "download_optical.py"
    ),

    "2": (
        "Download Infrared Surveys",
        "download_infrared.py"
    ),

    #
    # Measurements
    #

    "3": (
        "Measure Optical Targets",
        "measure_all_targets.py"
    ),

    "4": (
        "Measure Infrared Targets",
        "measure_all_infrared.py"
    ),

    #
    # Ranking
    #

    "5": (
        "Generate Optical Rankings",
        "score_v2.py"
    ),

    "6": (
        "Generate Infrared Rankings",
        "infrared_score_v2.py"
    ),

    "7": (
        "Generate Composite Rankings",
        "score_v3.py"
    ),

    #
    # Reports
    #

    "8": (
        "Findings Report",
        "findings_report.py"
    ),

    "9": (
        "Discovery Report",
        "discovery_report.py"
    ),

    "10": (
        "Candidate Dossiers",
        "candidate_dossiers.py"
    ),

    "11": (
        "Hypothesis Report",
        "hypothesis_report.py"
    ),

    "12": (
        "Candidate Comparison",
        "candidate_comparison.py"
    ),

    #
    # Health
    #

    "13": (
        "Data Health Report",
        "download_success_report.py"
    ),

    #
    # Catalogs
    #

    "14": (
        "Build Beta Catalog",
        "build_beta_catalog.py"
    ),

    "15": (
        "Resolve Coordinates",
        "resolve_catalog_coordinates_v2.py"
    ),

    "16": (
    "Project Status Dashboard",
    "project_status.py"
    ),

    "17": (
    "AI Discovery Assistant",
    "ai_discovery_assistant.py"
    ),

    "18": (
    "AI Research Journal",
    "ai_research_journal.py"
    ),

    "19": (
    "Ask Quiet Sky",
    "ask_quiet_sky.py"
    ),

    "20": (
    "Update Project Memory",
    "project_memory.py"
    ),

    "21": (
    "Change Analysis",
    "change_analysis.py"
    ),

    "22": (
    "AI Change Analysis",
    "what_changed_ai.py"
    ),
}


def clear():

    print("\n" * 3)


def pause():

    input(
        "\nPress Enter to continue..."
    )


def run_script(script_name):

    script_path = (
        BASE_DIR /
        script_name
    )

    if not script_path.exists():

        print()
        print(
            f"ERROR: {script_name} not found."
        )

        pause()
        return

    print()
    print("=" * 60)
    print(f"Running: {script_name}")
    print("=" * 60)
    print()

    try:

        subprocess.run(
            [
                sys.executable,
                str(script_path)
            ],
            check=False
        )

    except Exception as e:

        print()
        print(f"ERROR: {e}")

    pause()


def run_optical_pipeline():

    pipeline = [

        "measure_all_targets.py",
        "score_v2.py",
        "optical_beta_report.py"

    ]

    print()
    print("=" * 60)
    print("Quiet Sky Optical Pipeline")
    print("=" * 60)

    for script in pipeline:

        run_script(script)


def run_infrared_pipeline():

    pipeline = [

        "measure_all_infrared.py",
        "infrared_score_v2.py"

    ]

    print()
    print("=" * 60)
    print("Quiet Sky Infrared Pipeline")
    print("=" * 60)

    for script in pipeline:

        run_script(script)


def run_full_analysis():

    pipeline = [

        "measure_all_targets.py",

        "measure_all_infrared.py",

        "score_v2.py",

        "infrared_score_v2.py",

        "score_v3.py",

        "findings_report.py",

        "discovery_report.py",

        "download_success_report.py"

    ]

    print()
    print("=" * 60)
    print("Quiet Sky Full Analysis")
    print("=" * 60)

    for script in pipeline:

        run_script(script)


while True:

    clear()

    print("=" * 60)
    print("Quiet Sky Beta")
    print("AI-Assisted Astronomical Anomaly Detection")
    print("=" * 60)

    print()
    print("DATA ACQUISITION")
    print("----------------")

    print(" 1. Download Optical Surveys")
    print(" 2. Download Infrared Surveys")

    print()
    print("MEASUREMENTS")
    print("------------")

    print(" 3. Measure Optical Targets")
    print(" 4. Measure Infrared Targets")

    print()
    print("RANKINGS")
    print("--------")

    print(" 5. Generate Optical Rankings")
    print(" 6. Generate Infrared Rankings")
    print(" 7. Generate Composite Rankings")

    print()
    print("REPORTS")
    print("-------")

    print(" 8. Findings Report")
    print(" 9. Discovery Report")
    print("10. Candidate Dossiers")
    print("11. Hypothesis Report")
    print("12. Candidate Comparison")

    print()
    print("HEALTH")
    print("------")

    print("13. Data Health Report")

    print()
    print("CATALOG")
    print("-------")

    print("14. Build Beta Catalog")
    print("15. Resolve Coordinates")
    print("16. Project Status Dashboard")
    print("17. AI Discovery Assistant")
    print("18. AI Research Journal")
    print("19. Ask Quiet Sky")
    print("20. Update Project Memory")
    print("21. Change Analysis")
    print("22. AI Change Analysis")

    print()
    print("PIPELINES")
    print("---------")

    print("22. Run Optical Pipeline")
    print("23. Run Infrared Pipeline")
    print("24. Run Full Analysis")

    print()
    print("0. Exit")

    print()

    choice = input(
        "Selection: "
    ).strip()

    if choice == "0":

        print()
        print("Goodbye.")
        break

    if choice == "23":

        run_optical_pipeline()
        continue

    if choice == "24":

        run_infrared_pipeline()
        continue

    if choice == "25":

        run_full_analysis()
        continue

    if choice in MENU:

        _, script = MENU[choice]

        run_script(script)

    else:

        print()
        print("Invalid selection.")
        pause()