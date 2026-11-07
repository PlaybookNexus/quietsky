# rank_tess.py

from pathlib import Path
import pandas as pd

# =====================================================
# CONFIG
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR /
    "tess_measurements.csv"
)

OUTPUT_FILE = (
    BASE_DIR /
    "tess_rankings.csv"
)

# =====================================================
# LOAD
# =====================================================

print()
print(
    f"Loading {INPUT_FILE.name}"
)

df = pd.read_csv(
    INPUT_FILE
)

print(
    f"Rows: {len(df):,}"
)

# =====================================================
# NORMALIZATION
# =====================================================

def normalize(series):

    maximum = series.max()

    if maximum == 0:

        return series * 0

    return series / maximum

# =====================================================
# COMPONENT SCORES
# =====================================================

df["rms_score"] = normalize(
    df["max_relative_rms"]
)

df["dimming_score"] = normalize(
    df["max_dimming"]
)

df["brightening_score"] = normalize(
    df["max_brightening"]
)

df["sector_score"] = normalize(
    df["sector_count"]
)

# =====================================================
# FINAL SCORE
# =====================================================

df["score"] = (

    df["rms_score"] * 0.40 +

    df["dimming_score"] * 0.30 +

    df["brightening_score"] * 0.20 +

    df["sector_score"] * 0.10

)

# =====================================================
# SORT
# =====================================================

df = df.sort_values(

    "score",

    ascending=False

)

# =====================================================
# RANK
# =====================================================

df.insert(

    0,

    "rank",

    range(
        1,
        len(df) + 1
    )

)

# =====================================================
# SAVE
# =====================================================

columns = [

    "rank",

    "target",

    "score",

    "sector_count",

    "total_points",

    "avg_relative_rms",

    "max_relative_rms",

    "max_dimming",

    "max_brightening"

]

df[columns].to_csv(

    OUTPUT_FILE,

    index=False

)

# =====================================================
# SUMMARY
# =====================================================

print()
print("=" * 60)
print("TESS RANKING COMPLETE")
print("=" * 60)
print()

print(
    f"Targets Ranked : {len(df):,}"
)

print()
print(
    f"Output : {OUTPUT_FILE.name}"
)

print()
print("TOP 20")
print("-" * 60)

print(

    df[
        [
            "rank",
            "target",
            "score",
            "sector_count"
        ]
    ]

    .head(20)

    .to_string(index=False)

)

print()