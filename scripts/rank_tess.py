# rank_tess.py

from pathlib import Path
import pandas as pd
import numpy as np

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

print()

# =====================================================
# FILTER
# =====================================================

# Exclude normalized TARS products
# They use FLUX around 1.0 and are
# not directly comparable to SPOC.

df = df[
    df["flux_column"] != "FLUX"
].copy()

print(
    f"SPOC Rows: {len(df):,}"
)

# =====================================================
# DERIVED METRICS
# =====================================================

df["relative_rms"] = (

    df["rms"]

    /

    df["median_flux"].replace(
        0,
        np.nan
    )

)

df["relative_rms"] = (

    df["relative_rms"]

    .fillna(0)

)

# =====================================================
# SCORE
# =====================================================

df["score"] = (

    df["relative_rms"] * 1000

    +

    df["max_dimming"] * 100

    +

    df["max_brightening"] * 50

)

# =====================================================
# SORT
# =====================================================

df = df.sort_values(

    "score",

    ascending=False

)

# =====================================================
# SAVE
# =====================================================

df.to_csv(

    OUTPUT_FILE,

    index=False

)

# =====================================================
# DISPLAY
# =====================================================

print()

print("═" * 72)
print("QUIET SKY TESS RANKINGS")
print("═" * 72)

print()

top = df.head(25)

for rank, (_, row) in enumerate(

    top.iterrows(),

    start=1

):

    print(

        f"{rank:2d}. "

        f"{row['target']:<20} "

        f"S{int(row['sector']):>3} "

        f"{row['score']:8.4f}"

    )

print()

print("═" * 72)

print(
    f"Saved: {OUTPUT_FILE}"
)

print(
    f"Ranked Rows: {len(df):,}"
)

print("═" * 72)
