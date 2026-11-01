# run_full_analysis.py

import subprocess
import sys

PIPELINE = [

    "measure_all_targets.py",
    "measure_all_infrared.py",

    "score_v2.py",
    "infrared_score_v2.py",
    "score_v3.py",

    "findings_report.py",
    "discovery_report.py",
    "download_success_report.py"

]

for index, script in enumerate(
    PIPELINE,
    start=1
):

    print()
    print(
        f"Step {index}/{len(PIPELINE)}"
    )

    print(
        f"Running {script}"
    )

    subprocess.run(
        [sys.executable, script]
    )

print()
print("Analysis Complete")