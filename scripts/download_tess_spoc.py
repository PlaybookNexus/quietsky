# download_tess_spoc.py

from pathlib import Path
import csv
import time
import warnings

from lightkurve import search_lightcurve

# =====================================================
# CONFIG
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR /
    "targets_tess.csv"
)

DATA_DIR = (
    BASE_DIR /
    "data"
)

LOG_FILE = (
    BASE_DIR /
    "tess_download_log.csv"
)

CHECKPOINT = 25

# =====================================================
# RUN CONTROL
# =====================================================

START_INDEX = 3855

MAX_TARGETS = None

AUTHOR = "SPOC"

# =====================================================
# QUIET LIGHTKURVE WARNING
# =====================================================

warnings.filterwarnings(
    "ignore",
    message=".*tpfmodel submodule.*"
)

# =====================================================
# HELPERS
# =====================================================

def safe_name(name):

    return (
        name
        .replace("/", "_")
        .replace("\\", "_")
        .replace(":", "_")
        .replace("*", "_")
        .replace("?", "_")
        .replace('"', "_")
        .replace("<", "_")
        .replace(">", "_")
        .replace("|", "_")
        .replace(" ", "_")
    )


def progress_bar(
    current,
    total,
    width=40
):

    pct = current / total

    filled = int(
        width * pct
    )

    return (
        "█" * filled +
        "░" * (
            width - filled
        )
    )


def count_fits(folder):

    return len(
        list(
            folder.glob(
                "**/*.fits"
            )
        )
    )


def folder_size_gb(folder):

    total = 0

    for f in folder.glob("**/*"):

        if f.is_file():

            total += f.stat().st_size

    return total / (1024 ** 3)


def save_log():

    if not download_log:
        return

    with open(
        LOG_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(

            f,

            fieldnames=[
                "name",
                "products",
                "fits_files",
                "status"
            ]

        )

        writer.writeheader()

        writer.writerows(
            download_log
        )

# =====================================================
# LOAD TARGETS
# =====================================================

with open(
    INPUT_FILE,
    newline="",
    encoding="utf-8"
) as f:

    targets = list(
        csv.DictReader(f)
    )

targets = targets[START_INDEX:]

if MAX_TARGETS is not None:

    targets = (
        targets[:MAX_TARGETS]
    )

TOTAL = len(targets)

# =====================================================
# STARTUP
# =====================================================

print()
print("═" * 72)
print("QUIET SKY TESS SPOC ARCHIVE INGEST")
print("═" * 72)
print()

print(
    f"Targets : {TOTAL:,}"
)

print(
    f"Start   : {START_INDEX:,}"
)

print(
    f"Source  : {AUTHOR}"
)

print()

# =====================================================
# STATE
# =====================================================

success = 0
failed = 0
skipped = 0

downloaded_products = 0

download_log = []

start_time = time.time()

# =====================================================
# MAIN LOOP
# =====================================================

for i, row in enumerate(
    targets,
    start=1
):

    name = row["name"]

    print()

    print(
        f"[{progress_bar(i,TOTAL)}] "
        f"{100*i/TOTAL:5.2f}%"
    )

    print(
        f"#{START_INDEX + i:,} "
        f"{name}"
    )

    target_dir = (

        DATA_DIR /

        safe_name(name) /

        "tess"

    )

    target_dir.mkdir(

        parents=True,

        exist_ok=True

    )

    try:

        # ------------------------------------------------
        # SKIP EXISTING
        # ------------------------------------------------

        existing_fits = count_fits(
            target_dir
        )

        if existing_fits > 0:

            skipped += 1

            print(
                f"✅ Already downloaded "
                f"({existing_fits} FITS)"
            )

            download_log.append({

                "name":
                    name,

                "products":
                    "",

                "fits_files":
                    existing_fits,

                "status":
                    "skipped"

            })

            continue

        # ------------------------------------------------
        # SEARCH
        # ------------------------------------------------

        search = search_lightcurve(

            name,

            mission="TESS",

            author=AUTHOR

        )

        products = len(search)

        print(
            f"{AUTHOR} Products : "
            f"{products}"
        )

        if products == 0:

            failed += 1

            print(
                "No products"
            )

            download_log.append({

                "name":
                    name,

                "products":
                    0,

                "fits_files":
                    0,

                "status":
                    "no_products"

            })

            continue

        # ------------------------------------------------
        # DOWNLOAD
        # ------------------------------------------------

        try:

            search.download_all(

                download_dir=str(
                    target_dir
                )

            )

        except Exception as e:

            message = str(e)

            if (

                "This file may be corrupt"

                in

                message

            ):

                print()

                print(
                    "⚠ Lightkurve parse warning"
                )

                print(
                    "Checking downloaded FITS..."
                )

            else:

                raise

        # ------------------------------------------------
        # VERIFY
        # ------------------------------------------------

        fits_count = count_fits(
            target_dir
        )

        if fits_count > 0:

            success += 1

            downloaded_products += products

            print(

                f"✅ Archive stored "
                f"({fits_count} FITS)"

            )

            download_log.append({

                "name":
                    name,

                "products":
                    products,

                "fits_files":
                    fits_count,

                "status":
                    "success"

            })

        else:

            failed += 1

            print(
                "❌ No FITS found"
            )

            download_log.append({

                "name":
                    name,

                "products":
                    products,

                "fits_files":
                    0,

                "status":
                    "failed"

            })

        # ------------------------------------------------
        # CHECKPOINT
        # ------------------------------------------------

        if i % CHECKPOINT == 0:

            save_log()

            elapsed = (
                time.time()
                - start_time
            )

            speed = (
                i / elapsed * 60
            )

            remaining = (
                TOTAL - i
            )

            eta_hours = (

                remaining

                /

                max(speed, 0.1)

            ) / 60

            storage_gb = (
                folder_size_gb(
                    DATA_DIR
                )
            )

            processed = (

                success +

                skipped +

                failed

            )

            projected_gb = (

                storage_gb

                /

                max(processed, 1)

            ) * TOTAL

            print()
            print("═" * 72)
            print(
                f"CHECKPOINT {START_INDEX + i:,}"
            )
            print("═" * 72)
            print()

            print(
                f"Downloaded Targets : "
                f"{success:,}"
            )

            print(
                f"Skipped Targets    : "
                f"{skipped:,}"
            )

            print(
                f"Failed Targets     : "
                f"{failed:,}"
            )

            print(
                f"Products Seen      : "
                f"{downloaded_products:,}"
            )

            print()

            print(
                f"Storage Used       : "
                f"{storage_gb:.2f} GB"
            )

            print(
                f"Projected Final    : "
                f"{projected_gb:.1f} GB"
            )

            print()

            print(
                f"Speed              : "
                f"{speed:.1f}/min"
            )

            print(
                f"ETA                : "
                f"{eta_hours:.2f} hr"
            )

            print()

    except KeyboardInterrupt:

        print()
        print(
            "Interrupted. Saving log..."
        )

        save_log()

        raise

    except Exception as e:

        failed += 1

        print()
        print(
            f"❌ ERROR {name}"
        )

        print(e)

        download_log.append({

            "name":
                name,

            "products":
                0,

            "fits_files":
                0,

            "status":
                "error"

        })

# =====================================================
# FINAL SAVE
# =====================================================

save_log()

# =====================================================
# SUMMARY
# =====================================================

elapsed = (
    time.time()
    - start_time
)

storage_gb = (
    folder_size_gb(
        DATA_DIR
    )
)

print()
print("═" * 72)
print("ARCHIVE INGEST COMPLETE")
print("═" * 72)
print()

print(
    f"Downloaded Targets : "
    f"{success:,}"
)

print(
    f"Skipped Targets    : "
    f"{skipped:,}"
)

print(
    f"Failed Targets     : "
    f"{failed:,}"
)

print(
    f"Products Seen      : "
    f"{downloaded_products:,}"
)

print()

print(
    f"Storage Used       : "
    f"{storage_gb:.2f} GB"
)

print()

print(
    f"Elapsed Hours      : "
    f"{elapsed/3600:.2f}"
)

print()

print(
    f"Log File           : "
    f"{LOG_FILE.name}"
)

print()

print("═" * 72)