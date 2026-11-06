from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR /
    "tess_rankings.csv"
)

OUTPUT_FILE = (
    BASE_DIR /
    "tess_target_rankings.csv"
)

df = pd.read_csv(
    INPUT_FILE
)

summary = (

    df

    .groupby("target")

    .agg({

        "sector": "nunique",

        "points": "sum",

        "score": ["max", "mean"],

        "relative_rms": "max",

        "max_dimming": "max",

        "max_brightening": "max"

    })

)

summary.columns = [

    "sector_count",

    "total_points",

    "max_score",

    "avg_score",

    "max_relative_rms",

    "max_dimming",

    "max_brightening"

]

summary = (

    summary

    .sort_values(

        "max_score",

        ascending=False

    )

    .reset_index()

)

summary.to_csv(

    OUTPUT_FILE,

    index=False

)

print()
print("TOP TARGETS")
print("-" * 72)

for i, row in enumerate(

    summary.head(20).itertuples(),

    start=1

):

    print(

        f"{i:2d}. "

        f"{row.target:<20} "

        f"Score={row.max_score:.3f}  "

        f"Sectors={row.sector_count}"

    )

print()

print(
    f"Saved: {OUTPUT_FILE}"
)