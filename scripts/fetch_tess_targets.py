# fetch_tess_targets.py

from pathlib import Path
from concurrent.futures import (
    ThreadPoolExecutor,
    TimeoutError
)

import csv
import time
import warnings

import astropy.units as u

from astropy.coordinates import SkyCoord
from lightkurve import search_lightcurve

# =====================================================
# CONFIG
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR /
    "targets_resolved_master.csv"
)

OUTPUT_FILE = (
    BASE_DIR /
    "targets_tess.csv"
)

MISSING_FILE = (
    BASE_DIR /
    "targets_no_tess.csv"
)

TIMEOUT_FILE = (
    BASE_DIR /
    "targets_timeout.csv"
)

CHECKPOINT = 100

SEARCH_RADIUS = 60 * u.arcsec

QUERY_TIMEOUT = 90
MAX_RETRIES = 1

DEBUG_MODE = False
DEBUG_TARGET = "AB Pic"

# =====================================================
# QUIET LIGHTKURVE WARNING
# =====================================================

warnings.filterwarnings(
    "ignore",
    message=".*tpfmodel submodule.*"
)

# =====================================================
# VISUALS
# =====================================================

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
        "░" * (width - filled)
    )


def dataset_bar(
    products,
    max_products=250
):

    width = 12

    products = min(
        products,
        max_products
    )

    filled = int(
        width *
        products /
        max_products
    )

    return (
        "█" * filled +
        "░" * (
            width - filled
        )
    )


def dataset_rating(products):

    if products >= 200:
        return "🌌 LEGENDARY"

    if products >= 100:
        return "🚀 EXCELLENT"

    if products >= 50:
        return "⭐ RICH"

    if products >= 20:
        return "✅ GOOD"

    return "• STANDARD"

# =====================================================
# SAVE
# =====================================================

def save_csv(
    filename,
    rows
):

    if not rows:
        return

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=rows[0].keys()
        )

        writer.writeheader()
        writer.writerows(rows)


def save_all():

    save_csv(
        OUTPUT_FILE,
        found
    )

    save_csv(
        MISSING_FILE,
        missing
    )

    save_csv(
        TIMEOUT_FILE,
        timeout_targets
    )

# =====================================================
# TIMEOUT QUERY
# =====================================================

def query_with_timeout(
    func,
    timeout=QUERY_TIMEOUT
):

    with ThreadPoolExecutor(
        max_workers=1
    ) as executor:

        future = executor.submit(func)

        return future.result(
            timeout=timeout
        )


# =====================================================
# SEARCH WRAPPER
# =====================================================

SLOW_QUERY_SECONDS = 30


def search_tess(
    callable_query,
    label,
    target_name
):

    for attempt in range(
        1,
        MAX_RETRIES + 1
    ):

        try:

            start = time.time()

            result = query_with_timeout(
                callable_query
            )

            elapsed = (
                time.time() -
                start
            )

            if elapsed > SLOW_QUERY_SECONDS:

                print(
                    f"⚠ Slow Query "
                    f"{elapsed:.1f}s"
                )

                slow_queries.append({

                    "target": target_name,

                    "method": label,

                    "seconds":
                        round(
                            elapsed,
                            1
                        )

                })

            return {

                "success": True,

                "result": result,

                "elapsed": elapsed

            }

        except TimeoutError:

            print(

                f"⚠ Timeout "
                f"{label} "
                f"{attempt}/{MAX_RETRIES}"

            )

        except Exception as e:

            print(

                f"⚠ Error "
                f"{label} "
                f"{attempt}/{MAX_RETRIES}"

            )

            print(f"   {e}")

        if attempt < MAX_RETRIES:

            time.sleep(
                attempt * 2
            )

    timeout_targets.append({

        "name":
            target_name,

        "method":
            label

    })

    return {

        "success": False,

        "result": None

    }

# =====================================================
# DEBUG MODE
# =====================================================

if DEBUG_MODE:

    print()
    print("=" * 72)
    print("DEBUG MODE")
    print("=" * 72)

    result = search_lightcurve(

        DEBUG_TARGET,

        mission="TESS"

    )

    print(result)

    print()
    print("COLUMNS")
    print("-" * 40)

    try:

        for col in result.table.colnames:

            print(col)

    except Exception as e:

        print(e)

    raise SystemExit()

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

TOTAL = len(targets)

# =====================================================
# STARTUP
# =====================================================

print()
print("═" * 72)
print("QUIET SKY TESS SURVEY")
print("═" * 72)
print()

print(
    f"Catalog Size : {TOTAL:,}"
)

print(
    f"Search Radius: {SEARCH_RADIUS}"
)

print(
    f"Timeout      : {QUERY_TIMEOUT}s"
)

print(
    f"Retries      : {MAX_RETRIES}"
)

print()

# =====================================================
# STATE
# =====================================================

found = []
missing = []
timeout_targets = []

slow_queries = []

coord_hits = 0
name_hits = 0

best_target = ""
best_products = 0

leaderboard = []

since_save = 0

start_time = time.time()

# =====================================================
# MAIN LOOP
# =====================================================

for i, row in enumerate(
    targets,
    start=1
):

    name = row["name"]

    try:

        query_start = time.time()

        coord = SkyCoord(

            ra=float(
                row["ra_deg"]
            ) * u.deg,

            dec=float(
                row["dec_deg"]
            ) * u.deg

        )

        coord_search = search_tess(

            lambda:
            search_lightcurve(

                coord,

                mission="TESS",

                radius=SEARCH_RADIUS

            ),

            "coordinate",

            name

        )

        result = None
        method = None

        if (
           coord_search["success"]
           and
           len(coord_search["result"]) > 0
        ):

           result = coord_search["result"]
           method = "coordinate"

        else:


            name_search = search_tess(

                lambda:
                search_lightcurve(

                    name,

                    mission="TESS"

                ),

                "name",

                name

            )

            if (
                name_search["success"]
                and
                name_search["result"] is not None
                and
                len(name_search["result"]) > 0
            ):

               result = (
                   name_search["result"]
               )

               method = "name"

        # -----------------------------------------

        if result is None:

            print()
            print(
                f"⏱ SKIPPED "
                f"{name}"
            )

            continue

        products = len(result)

        if products == 0:

            missing.append({

                "name":
                    name

            })

            continue

        # -----------------------------------------

        if method == "coordinate":

            coord_hits += 1

        else:

            name_hits += 1

        # -----------------------------------------

        authors = set()

        for item in result:

            author = getattr(
                item,
                "author",
                None
            )

            if author:

                authors.add(
                    str(author)
                )

        # -----------------------------------------

        found.append({

            "name":
                name,

            "search_method":
                method,

            "n_products":
                products,

            "n_authors":
                len(authors)

        })

        # -----------------------------------------

        leaderboard.append(

            (
                products,
                name
            )

        )

        leaderboard.sort(
            reverse=True
        )

        leaderboard = (
            leaderboard[:20]
        )

        # -----------------------------------------

        new_leader = False

        if products > best_products:

            best_products = products

            best_target = name

            new_leader = True

        # -----------------------------------------

        hit_rate = (
            len(found)
            /
            max(i, 1)
            * 100
        )

        elapsed = (
            time.time()
            - start_time
        )

        query_time = (
            time.time()
            - query_start
        )

        top3 = (
            leaderboard[:3]
        )

        # -----------------------------------------

        print()

        print(
            f"[{progress_bar(i,TOTAL)}] "
            f"{100*i/TOTAL:5.2f}%"
        )

        print(
            f"#{i:,}  {name}"
        )

        print()

        print(
            f"Method   : "
            f"{method}"
        )

        print(
            f"Products : "
            f"{products}"
        )

        print(
            f"Authors  : "
            f"{len(authors)}"
        )

        print(
            f"Query    : "
            f"{query_time:.1f}s"
        )

        print()

        print(
            f"Dataset  : "
            f"[{dataset_bar(products)}] "
            f"{products}"
        )

        print(
            f"Rating   : "
            f"{dataset_rating(products)}"
        )

        if new_leader:

            print()
            print(
                "🏆 NEW LEADER"
            )

            print(
                f"   {best_target}"
            )

            print(
                f"   {best_products} products"
            )

        print()

        print(
            f"Hits     : {len(found):,}"
        )

        print(
            f"Misses   : {len(missing):,}"
        )

        print(
            f"Timeouts : "
            f"{len(timeout_targets):,}"
        )

        print(
            f"Hit Rate : "
            f"{hit_rate:.1f}%"
        )

        print()

        print(
            f"Coord    : {coord_hits}"
        )

        print(
            f"Name     : {name_hits}"
        )

        print()

        print(
            "Top Datasets"
        )

        for rank, (
            prod,
            target
        ) in enumerate(
            top3,
            start=1
        ):

            print(
                f"  #{rank} "
                f"{target[:24]:<24} "
                f"{prod}"
            )

        if i >= 25:

            speed = (
                i / elapsed * 60
            )

            print()

            print(
                f"Speed    : "
                f"{speed:.1f}/min"
            )

            remaining = TOTAL - i

            eta_hours = (
                remaining /
                max(speed, 0.1)
            ) / 60

            print(
                f"ETA      : "
                f"{eta_hours:.1f} hr"
            )


        print()

        print(
            "─" * 60
        )

        # -----------------------------------------

        since_save += 1

        if since_save >= CHECKPOINT:

            save_all()

            print()
            print(
                "💾 CHECKPOINT SAVED"
            )

            print()

            print()

            print("TOP 10 DATASETS")
            print("-" * 50)

            for rank, (
                prod,
                target
            ) in enumerate(
                leaderboard[:10],
                start=1
            ):

                print(
                    f"{rank:2d}. "
                    f"{target:<30} "
                    f"{prod}"
                )

            print()

            print(
                "-" * 50
            )

            for item in sorted(

                slow_queries,

                key=lambda x: x["seconds"],

                reverse=True

            )[:5]:

                print(

                    f"{item['seconds']:6.1f}s  "

                    f"{item['target']}"

                )
            
            print(
                "-" * 50
            )

            for rank, (
                prod,
                target
            ) in enumerate(
                leaderboard[:10],
                start=1
            ):

                print(
                    f"{rank:2d}. "
                    f"{target:<30} "
                    f"{prod}"
                )

            print()

            since_save = 0

    except KeyboardInterrupt:

        print()
        print(
            "Interrupted. Saving..."
        )

        save_all()

        raise

    except Exception as e:

        print()
        print(
            f"⚠ UNEXPECTED ERROR"
        )

        print(name)

        print(e)

# =====================================================
# FINAL SAVE
# =====================================================

save_all()

# =====================================================
# SUMMARY
# =====================================================

elapsed = (
    time.time()
    - start_time
)

print()
print("═" * 72)
print("QUIET SKY COMPLETE")
print("═" * 72)
print()

print(
    f"TESS Hits  : "
    f"{len(found):,}"
)

print(
    f"Misses     : "
    f"{len(missing):,}"
)

print(
    f"Timeouts   : "
    f"{len(timeout_targets):,}"
)

print()

print(
    f"Top Target : "
    f"{best_target}"
)

print(
    f"Products   : "
    f"{best_products}"
)

print()

print(
    f"Elapsed    : "
    f"{elapsed/3600:.2f} hr"
)

print()

print(
    "HALL OF FAME"
)

print("-" * 50)

for rank, (
    prod,
    target
) in enumerate(
    leaderboard,
    start=1
):

    print(
        f"{rank:2d}. "
        f"{target:<30} "
        f"{prod}"
    )

print()
print("═" * 72)