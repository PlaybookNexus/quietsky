# measure_all_tess.py

from pathlib import Path
import csv
import numpy as np
from astropy.io import fits
import warnings
import time

# =====================================================
# CONFIG
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = (
    BASE_DIR /
    "data"
)

OUTPUT_FILE = (
    BASE_DIR /
    "tess_measurements.csv"
)

CHECKPOINT = 25

START_INDEX = 0

MIN_FITS_SIZE = 500_000

# =====================================================
# WARNINGS
# =====================================================

warnings.filterwarnings("ignore")

# =====================================================
# FITS MEASUREMENT
# =====================================================

def measure_fits(path):

    try:

        if path.stat().st_size < MIN_FITS_SIZE:

            print(
                f"      SKIP SMALL : "
                f"{path.name}"
            )

            return None

        with fits.open(
            path,
            memmap=False,
            lazy_load_hdus=False
        ) as hdul:

            if len(hdul) < 2:
                return None

            data = hdul[1].data

            if data is None:
                return None

            if "PDCSAP_FLUX" not in data.names:
                return None

            flux = data["PDCSAP_FLUX"]

            flux = flux[
                np.isfinite(flux)
            ]

            if len(flux) == 0:
                return None

            median_flux = np.median(
                flux
            )

            if median_flux == 0:
                return None

            rms = np.std(flux)

            relative_rms = (
                rms /
                median_flux
            )

            max_dimming = (

                median_flux -
                np.min(flux)

            ) / median_flux

            max_brightening = (

                np.max(flux) -
                median_flux

            ) / median_flux

            return {

                "points":
                    len(flux),

                "median_flux":
                    median_flux,

                "relative_rms":
                    relative_rms,

                "max_dimming":
                    max_dimming,

                "max_brightening":
                    max_brightening

            }

    except Exception:

        print(
            f"      BAD FITS : "
            f"{path.name}"
        )

        return None

# =====================================================
# SAVE CHECKPOINT
# =====================================================

def save_rows(rows):

    if not rows:
        return

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(

            f,

            fieldnames=[

                "target",

                "sector_count",
                "total_points",

                "avg_relative_rms",
                "max_relative_rms",

                "max_dimming",
                "max_brightening"

            ]

        )

        writer.writeheader()

        writer.writerows(rows)

# =====================================================
# TARGETS
# =====================================================

targets = [

    x

    for x in sorted(
        DATA_DIR.iterdir()
    )

    if x.is_dir()

]

targets = targets[
    START_INDEX:
]

TOTAL = len(targets)

# =====================================================
# MAIN
# =====================================================

rows = []

start_time = time.time()

print()
print("=" * 70)
print("QUIET SKY TESS MEASUREMENT")
print("=" * 70)
print()

print(
    f"Targets : {TOTAL:,}"
)

print()

for index, target in enumerate(

    targets,

    start=1

):

    tess_dir = (
        target /
        "tess"
    )

    if not tess_dir.exists():
        continue

    fits_files = list(

        tess_dir.glob(
            "**/*.fits"
        )

    )

    if not fits_files:
        continue

    print()
    print(
        f"[{index:,}/{TOTAL:,}] "
        f"{target.name}"
    )

    print(
        f"   FITS : "
        f"{len(fits_files)}"
    )

    sector_count = 0

    total_points = 0

    rms_values = []

    dim_values = []

    bright_values = []

    for file_index, fits_file in enumerate(

        fits_files,

        start=1

    ):

        print(

            f"      "

            f"[{file_index}/"

            f"{len(fits_files)}] "

            f"{fits_file.name}"

        )

        result = measure_fits(
            fits_file
        )

        if result is None:
            continue

        sector_count += 1

        total_points += result[
            "points"
        ]

        rms_values.append(

            result[
                "relative_rms"
            ]

        )

        dim_values.append(

            result[
                "max_dimming"
            ]

        )

        bright_values.append(

            result[
                "max_brightening"
            ]

        )

    if sector_count == 0:

        print(
            "   No usable sectors"
        )

        continue

    rows.append({

        "target":
            target.name,

        "sector_count":
            sector_count,

        "total_points":
            total_points,

        "avg_relative_rms":
            np.mean(rms_values),

        "max_relative_rms":
            np.max(rms_values),

        "max_dimming":
            np.max(dim_values),

        "max_brightening":
            np.max(bright_values)

    })

    # -----------------------------------------
    # CHECKPOINT
    # -----------------------------------------

    if index % CHECKPOINT == 0:

        save_rows(rows)

        elapsed = (
            time.time()
            - start_time
        )

        speed = (

            index /

            elapsed *

            60

        )

        print()
        print(
            "=" * 70
        )

        print(
            f"CHECKPOINT "
            f"{index:,}"
        )

        print()

        print(
            f"Targets Measured : "
            f"{len(rows):,}"
        )

        print(
            f"Speed            : "
            f"{speed:.2f}/min"
        )

        print(
            "=" * 70
        )

# =====================================================
# FINAL SAVE
# =====================================================

save_rows(rows)

elapsed = (
    time.time()
    - start_time
)

print()
print("=" * 70)
print("MEASUREMENT COMPLETE")
print("=" * 70)
print()

print(
    f"Targets Measured : "
    f"{len(rows):,}"
)

print(
    f"Output File      : "
    f"{OUTPUT_FILE.name}"
)

print(
    f"Elapsed Hours    : "
    f"{elapsed/3600:.2f}"
)

print()