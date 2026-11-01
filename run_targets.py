import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TARGETS_FILE = BASE_DIR / "expanded_targets_v2.csv"

print()
print("Loading Targets")
print("=" * 60)

targets = []

with open(TARGETS_FILE,
          newline="",
          encoding="utf-8") as f:

    reader = csv.DictReader(f)

    for row in reader:

        targets.append(row)

        print(
            f"OK  {row['name']}"
        )

print()
print("=" * 60)
print("Loaded Targets")
print("=" * 60)

for t in targets:

    print(
        f"{t['name']:<20} "
        f"RA={float(t['ra']):.6f} "
        f"DEC={float(t['dec']):.6f} "
        f"{t['category']}"
    )

print()
print(f"Loaded {len(targets)} targets.")