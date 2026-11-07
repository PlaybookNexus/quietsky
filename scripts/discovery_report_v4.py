# discovery_report_v4.py

from pathlib import Path
import pandas as pd

# =====================================================
# CONFIG
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR /
    "quiet_sky_rankings_v4.csv"
)

OUTPUT_FILE = (
    BASE_DIR /
    "discovery_candidates_report_v4.txt"
)

TOP_N = 25

# =====================================================
# LOAD
# =====================================================

print()
print("=" * 60)
print("QUIET SKY DISCOVERY REPORT V4")
print("=" * 60)

df = pd.read_csv(
    INPUT_FILE
)

print()
print(
    f"Targets Loaded : {len(df):,}"
)

# =====================================================
# TOP CANDIDATES
# =====================================================

top = df.head(TOP_N)

# =====================================================
# REPORT
# =====================================================

lines = []

lines.append(
    "QUIET SKY DISCOVERY REPORT V4"
)

lines.append(
    "=" * 60
)

lines.append("")
lines.append(
    f"Targets Ranked : {len(df):,}"
)

lines.append(
    f"Top Candidates Reviewed : {TOP_N}"
)

lines.append("")
lines.append(
    "Composite rankings combine:"
)

lines.append(
    "- Optical anomaly score"
)

lines.append(
    "- Infrared anomaly score"
)

lines.append(
    "- TESS variability score"
)

lines.append("")
lines.append(
    "=" * 60
)

lines.append(
    "TOP CANDIDATES"
)

lines.append(
    "=" * 60
)

lines.append("")

for _, row in top.iterrows():

    lines.append(
        f"Rank #{int(row['rank'])}"
    )

    lines.append(
        f"Target : {row['name']}"
    )

    lines.append(
        f"Composite Score : "
        f"{row['composite_score']:.6f}"
    )

    lines.append(
        f"Optical Score   : "
        f"{row['optical_score']:.6f}"
    )

    lines.append(
        f"Infrared Score  : "
        f"{row['infrared_score']:.6f}"
    )

    lines.append(
        f"TESS Score      : "
        f"{row['tess_score']:.6f}"
    )

    lines.append(
        f"TESS Percentile : "
        f"{row['tess_percentile']:.2f}"
    )

    lines.append("")

# =====================================================
# SPECIAL TARGETS
# =====================================================

special_targets = [

    "KIC 8462852",
    "TRAPPIST-1",
    "Proxima Cen",
    "16 Cygni A",
    "16 Cygni B"

]

lines.append(
    "=" * 60
)

lines.append(
    "REFERENCE TARGETS"
)

lines.append(
    "=" * 60
)

lines.append("")

for target in special_targets:

    match = df[
        df["name"]
        .astype(str)
        .str.lower()
        ==
        target.lower()
    ]

    if len(match) == 0:
        continue

    row = match.iloc[0]

    lines.append(
        f"{row['name']}"
    )

    lines.append(
        f"Rank : {int(row['rank'])}"
    )

    lines.append(
        f"Composite Score : "
        f"{row['composite_score']:.6f}"
    )

    lines.append(
        f"TESS Percentile : "
        f"{row['tess_percentile']:.2f}"
    )

    lines.append("")

# =====================================================
# INTERPRETATION
# =====================================================

lines.append(
    "=" * 60
)

lines.append(
    "OBSERVATIONS"
)

lines.append(
    "=" * 60
)

lines.append("")

lines.append(
    "The highest-ranked targets exhibit "
    "strong evidence across one or more "
    "observation domains."
)

lines.append("")

lines.append(
    "Composite ranking rewards targets "
    "that remain unusual when multiple "
    "independent measurements are combined."
)

lines.append("")

lines.append(
    "A high TESS rank alone does not "
    "guarantee a high Quiet Sky rank."
)

lines.append("")

lines.append(
    "Likewise, targets that are only "
    "interesting in optical or infrared "
    "surveys may move downward unless "
    "supported by additional evidence."
)

lines.append("")

lines.append(
    "The purpose of this report is to "
    "identify targets deserving further "
    "human investigation."
)

# =====================================================
# SAVE
# =====================================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "\n".join(lines)
    )

# =====================================================
# SUMMARY
# =====================================================

print()
print("=" * 60)
print("REPORT COMPLETE")
print("=" * 60)

print()

print(
    f"Candidates Reviewed : "
    f"{TOP_N}"
)

print(
    f"Output File : "
    f"{OUTPUT_FILE.name}"
)

print()

print("TOP 10")
print("-" * 60)

print(

    top[
        [
            "rank",
            "name",
            "composite_score"
        ]
    ]

    .head(10)

    .to_string(index=False)

)

print()