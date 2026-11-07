# aggregate_tess.py

from pathlib import Path
import pandas as pd

# =====================================================
# CONFIG
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR /
    "tess_rankings.csv"
)

OUTPUT_FILE = (
    BASE_DIR /
    "tess_target_rankings.csv"
)

# =====================================================
# LOAD
# =====================================================

print()
print("=" * 60)
print("TESS AGGREGATION")
print("=" * 60)

df = pd.read_csv(
    INPUT_FILE
)

total = len(df)

print()
print(
    f"Targets Loaded : {total:,}"
)

# =====================================================
# PERCENTILE
# =====================================================

df["tess_percentile"] = (
    (
        total -
        df["rank"] +
        1
    )
    /
    total
) * 100

# =====================================================
# ANOMALY CLASS
# =====================================================

def classify(percentile):

    if percentile >= 99.9:
        return "Extreme"

    if percentile >= 99:
        return "Very High"

    if percentile >= 95:
        return "High"

    if percentile >= 90:
        return "Elevated"

    if percentile >= 50:
        return "Moderate"

    return "Typical"

df["anomaly_class"] = (
    df["tess_percentile"]
    .apply(classify)
)

# =====================================================
# TOP FLAGS
# =====================================================

df["top_1_percent"] = (
    df["tess_percentile"] >= 99
)

df["top_5_percent"] = (
    df["tess_percentile"] >= 95
)

df["top_10_percent"] = (
    df["tess_percentile"] >= 90
)

# =====================================================
# ROUND VALUES
# =====================================================

numeric_columns = [

    "score",

    "tess_percentile",

    "avg_relative_rms",

    "max_relative_rms",

    "max_dimming",

    "max_brightening"

]

for column in numeric_columns:

    if column in df.columns:

        df[column] = (
            df[column]
            .round(6)
        )

# =====================================================
# OUTPUT COLUMNS
# =====================================================

columns = [

    "rank",

    "target",

    "score",

    "tess_percentile",

    "anomaly_class",

    "top_1_percent",

    "top_5_percent",

    "top_10_percent",

    "sector_count",

    "total_points",

    "avg_relative_rms",

    "max_relative_rms",

    "max_dimming",

    "max_brightening"

]

output = df[columns]

# =====================================================
# SAVE
# =====================================================

output.to_csv(
    OUTPUT_FILE,
    index=False
)

# =====================================================
# SUMMARY
# =====================================================

print()
print("=" * 60)
print("AGGREGATION COMPLETE")
print("=" * 60)

print()

print(
    f"Targets Aggregated : "
    f"{len(output):,}"
)

print(
    f"Top 1 Percent      : "
    f"{len(output[output['top_1_percent']]):,}"
)

print(
    f"Top 5 Percent      : "
    f"{len(output[output['top_5_percent']]):,}"
)

print(
    f"Top 10 Percent     : "
    f"{len(output[output['top_10_percent']]):,}"
)

print()

print(
    f"Output File : "
    f"{OUTPUT_FILE.name}"
)

print()

print("TOP 20")
print("-" * 60)

print(

    output[
        [
            "rank",
            "target",
            "score",
            "tess_percentile",
            "anomaly_class"
        ]
    ]

    .head(20)

    .to_string(index=False)

)

print()