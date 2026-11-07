# score_v4.py

from pathlib import Path
import pandas as pd

# =====================================================
# CONFIG
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

OPTICAL_FILE = (
    BASE_DIR /
    "rankings_v2.csv"
)

INFRARED_FILE = (
    BASE_DIR /
    "infrared_rankings_v2.csv"
)

TESS_FILE = (
    BASE_DIR /
    "tess_target_rankings.csv"
)

OUTPUT_FILE = (
    BASE_DIR /
    "quiet_sky_rankings_v4.csv"
)

# =====================================================
# HELPERS
# =====================================================

def normalize(series):

    maximum = series.max()

    if maximum == 0:
        return series * 0

    return series / maximum


def normalize_name(name):

    return (
        str(name)
        .strip()
        .replace("_", " ")
        .lower()
    )

# =====================================================
# LOAD
# =====================================================

print()
print("=" * 60)
print("QUIET SKY V4")
print("=" * 60)

optical = pd.read_csv(
    OPTICAL_FILE
)

infrared = pd.read_csv(
    INFRARED_FILE
)

tess = pd.read_csv(
    TESS_FILE
)

print()
print(
    f"Optical Rows  : {len(optical):,}"
)

print(
    f"Infrared Rows : {len(infrared):,}"
)

print(
    f"TESS Rows     : {len(tess):,}"
)

# =====================================================
# NORMALIZE NAMES
# =====================================================

optical["join_name"] = (
    optical["name"]
    .apply(normalize_name)
)

infrared["join_name"] = (
    infrared["name"]
    .apply(normalize_name)
)

tess["join_name"] = (
    tess["target"]
    .apply(normalize_name)
)

# =====================================================
# KEEP FIELDS
# =====================================================

optical = optical[
    [
        "join_name",
        "name",
        "score_v2"
    ]
].rename(
    columns={
        "score_v2":
        "optical_score"
    }
)

infrared = infrared[
    [
        "join_name",
        "infrared_score"
    ]
]

tess = tess[
    [
        "join_name",
        "score",
        "tess_percentile"
    ]
].rename(
    columns={
        "score":
        "tess_score"
    }
)

# =====================================================
# MERGE
# =====================================================

df = optical.copy()

df = df.merge(

    infrared,

    on="join_name",

    how="left"

)

df = df.merge(

    tess,

    on="join_name",

    how="left"

)

# =====================================================
# FILL NULLS
# =====================================================

df["infrared_score"] = (
    df["infrared_score"]
    .fillna(0)
)

df["tess_score"] = (
    df["tess_score"]
    .fillna(0)
)

df["tess_percentile"] = (
    df["tess_percentile"]
    .fillna(0)
)

# =====================================================
# NORMALIZE COMPONENTS
# =====================================================

df["optical_norm"] = normalize(
    df["optical_score"]
)

df["infrared_norm"] = normalize(
    df["infrared_score"]
)

df["tess_norm"] = normalize(
    df["tess_score"]
)

# =====================================================
# COMPOSITE
# =====================================================

df["composite_score"] = (

    df["optical_norm"] * 0.35 +

    df["infrared_norm"] * 0.25 +

    df["tess_norm"] * 0.40

)

# =====================================================
# SORT
# =====================================================

df = df.sort_values(

    "composite_score",

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

output_columns = [

    "rank",

    "name",

    "composite_score",

    "optical_score",

    "infrared_score",

    "tess_score",

    "tess_percentile"

]

df[output_columns].to_csv(

    OUTPUT_FILE,

    index=False

)

# =====================================================
# SUMMARY
# =====================================================

print()
print("=" * 60)
print("COMPOSITE RANKING COMPLETE")
print("=" * 60)

print()

print(
    f"Targets Ranked : {len(df):,}"
)

print(
    f"Output File    : {OUTPUT_FILE.name}"
)

print()

print("TOP 20")
print("-" * 60)

print(

    df[
        [
            "rank",
            "name",
            "composite_score"
        ]
    ]

    .head(20)

    .to_string(index=False)

)

print()