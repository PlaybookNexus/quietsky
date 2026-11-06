# measure_tess.py

from pathlib import Path
import csv

import numpy as np
from astropy.io import fits

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

UNKNOWN_FILE = (
    BASE_DIR /
    "tess_unknown_formats.csv"
)

# =====================================================
# STATE
# =====================================================

results = []

unknown_formats = []

fits_files = list(
    DATA_DIR.glob(
        "**/*_lc.fits"
    )
)

print()

print(
    f"Found {len(fits_files):,} FITS files"
)

print()

# =====================================================
# MAIN
# =====================================================

for n, file in enumerate(
    fits_files,
    start=1
):

    try:

        with fits.open(file) as hdul:

            # -----------------------------------------
            # FIND LIGHTCURVE TABLE
            # -----------------------------------------

            if "LIGHTCURVE" not in hdul:

                print(
                    f"⚠ No LIGHTCURVE HDU"
                )

                print(file)

                continue

            header = hdul[0].header

            data = hdul["LIGHTCURVE"].data

            columns = (
                data.columns.names
            )

            # -----------------------------------------
            # DETECT FLUX COLUMN
            # -----------------------------------------

            flux_column = None

            preferred_columns = [

                "PDCSAP_FLUX",
                "SAP_FLUX",
                "FLUX",
                "CORRECTED_FLUX",
                "RAW_FLUX"

            ]

            for c in preferred_columns:

                if c in columns:

                    flux_column = c

                    break

            # -----------------------------------------
            # UNKNOWN FORMAT
            # -----------------------------------------

            if flux_column is None:

                print()

                print(
                    "⚠ UNKNOWN FORMAT"
                )

                print(
                    file.name
                )

                print(
                    columns
                )

                unknown_formats.append({

                    "file":
                        str(file),

                    "columns":
                        ";".join(columns)

                })

                continue

            # -----------------------------------------
            # EXTRACT FLUX
            # -----------------------------------------

            flux = data[
                flux_column
            ]

            flux = np.asarray(
                flux,
                dtype=float
            )

            flux = flux[
                np.isfinite(flux)
            ]

            if len(flux) < 100:

                continue

            # -----------------------------------------
            # METRICS
            # -----------------------------------------

            median_flux = np.median(
                flux
            )

            rms = np.std(
                flux
            )

            normalized = (
                flux /
                median_flux
            )

            max_dimming = (
                1 -
                np.min(normalized)
            )

            max_brightening = (
                np.max(normalized)
                - 1
            )

            results.append({

                "target":
                    header.get(
                        "OBJECT",
                        "Unknown"
                    ),

                "tic":
                    header.get(
                        "TICID",
                        ""
                    ),

                "sector":
                    header.get(
                        "SECTOR",
                        ""
                    ),

                "points":
                    len(flux),

                "flux_column":
                    flux_column,

                "median_flux":
                    round(
                        float(
                            median_flux
                        ),
                        3
                    ),

                "rms":
                    round(
                        float(rms),
                        3
                    ),

                "max_dimming":
                    round(
                        float(
                            max_dimming
                        ),
                        6
                    ),

                "max_brightening":
                    round(
                        float(
                            max_brightening
                        ),
                        6
                    )

            })

            print(

                f"[{n}/{len(fits_files)}] "

                f"{header.get('OBJECT','?')} "

                f"{flux_column}"

            )

    except Exception as e:

        print()

        print(
            f"❌ ERROR"
        )

        print(file)

        print(e)

# =====================================================
# SAVE MEASUREMENTS
# =====================================================

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
            "tic",
            "sector",
            "points",
            "flux_column",
            "median_flux",
            "rms",
            "max_dimming",
            "max_brightening"

        ]

    )

    writer.writeheader()

    writer.writerows(
        results
    )

# =====================================================
# SAVE UNKNOWNS
# =====================================================

if unknown_formats:

    with open(
        UNKNOWN_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(

            f,

            fieldnames=[

                "file",
                "columns"

            ]

        )

        writer.writeheader()

        writer.writerows(
            unknown_formats
        )

# =====================================================
# SUMMARY
# =====================================================

print()
print("═" * 72)
print("TESS MEASUREMENT COMPLETE")
print("═" * 72)

print()

print(
    f"Measurements : "
    f"{len(results):,}"
)

print(
    f"Unknown      : "
    f"{len(unknown_formats):,}"
)

print()

print(
    f"Output       : "
    f"{OUTPUT_FILE.name}"
)

print(
    f"Unknown File : "
    f"{UNKNOWN_FILE.name}"
)

print()

print("═" * 72)