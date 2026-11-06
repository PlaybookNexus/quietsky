from pathlib import Path
import csv
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent.parent

RANKINGS_FILE = BASE_DIR / "rankings_v2.csv"

OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

REPORT_FILE = OUTPUT_DIR / "quiet_sky_report.html"

targets = []

with open(
    RANKINGS_FILE,
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        row["rank"] = int(row["rank"])
        row["score"] = float(row["score_v2"])
        row["spread"] = float(row["spread"])
        row["variance"] = float(row["variance"])
        row["unity"] = float(row["unity_deviation"])

        targets.append(row)

targets.sort(
    key=lambda r: r["score"],
    reverse=True
)

max_score = max(
    t["score"]
    for t in targets
)

#
# Executive Summary
#

highest = targets[0]

kic_rank = next(
    (
        t["rank"]
        for t in targets
        if t["name"] == "KIC 8462852"
    ),
    "N/A"
)

#
# Category Analytics
#

category_stats = defaultdict(list)

for t in targets:

    category_stats[
        t["category"]
    ].append(t)

#
# Histogram bins
#

bins = {
    "0.0-0.2": 0,
    "0.2-0.4": 0,
    "0.4-0.6": 0,
    "0.6-0.8": 0,
    "0.8+": 0
}

for t in targets:

    score = t["score"]

    if score < 0.2:
        bins["0.0-0.2"] += 1
    elif score < 0.4:
        bins["0.2-0.4"] += 1
    elif score < 0.6:
        bins["0.4-0.6"] += 1
    elif score < 0.8:
        bins["0.6-0.8"] += 1
    else:
        bins["0.8+"] += 1

html = f"""
<!DOCTYPE html>
<html>

<head>

<meta charset="utf-8">

<title>Quiet Sky Beta Report</title>

<style>

body {{
    font-family: Arial, sans-serif;
    max-width: 1400px;
    margin: auto;
    padding: 30px;
    background: #f5f7fa;
}}

h1, h2, h3 {{
    color: #1d3557;
}}

.card {{
    background: white;
    margin-bottom: 25px;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,.12);
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

th {{
    background: #1d3557;
    color: white;
    padding: 10px;
    cursor: pointer;
}}

td {{
    padding: 10px;
    border-bottom: 1px solid #ddd;
}}

.high {{
    color: #c1121f;
    font-weight: bold;
}}

.medium {{
    color: #ff8800;
    font-weight: bold;
}}

.low {{
    color: #2a9d8f;
    font-weight: bold;
}}

.bar {{
    height: 18px;
    background: #4a90e2;
    border-radius: 4px;
    margin-bottom: 10px;
}}

.note {{
    background: #eef6ff;
    padding: 10px;
    border-radius: 6px;
    margin-bottom: 15px;
}}

summary {{
    cursor: pointer;
    font-weight: bold;
    font-size: 16px;
}}

</style>

</head>

<body>

<div class="card">

<h1>Quiet Sky Beta Report</h1>

<p>
AI-Assisted Astronomical Anomaly Detection
</p>

</div>

<div class="card">

<h2>Executive Summary</h2>

<p><b>Targets Analysed:</b> {len(targets)}</p>

<p><b>Highest Ranked:</b> {highest["name"]}</p>

<p><b>Highest Score:</b> {highest["score"]:.4f}</p>

<p><b>KIC 8462852 Rank:</b> {kic_rank} / {len(targets)}</p>

</div>

<div class="card">

<h2>Leaderboard</h2>

<table id="leaderboard">

<tr>
<th onclick="sortTable(0)">Rank ↕</th>
<th onclick="sortTable(1)">Target ↕</th>
<th onclick="sortTable(2)">Category ↕</th>
<th onclick="sortTable(3)">Score ↕</th>
<th>Explanation</th>
</tr>
"""

for row in targets:

    score = row["score"]

    if score > 0.8:
        css = "high"
    elif score > 0.4:
        css = "medium"
    else:
        css = "low"

    reasons = []

    if row["spread"] > 1.0:
        reasons.append(
            "Very high survey disagreement"
        )

    elif row["spread"] > 0.5:
        reasons.append(
            "Moderate survey disagreement"
        )

    if row["variance"] > 0.10:
        reasons.append(
            "High variance"
        )

    if row["unity"] > 0.30:
        reasons.append(
            "Large deviation from expected profile"
        )

    category = row["category"]

    if category == "Variable":
        reasons.append(
            "Known variable star"
        )

    elif category == "Nearby":
        reasons.append(
            "Possible proper-motion effects"
        )

    elif category == "Exoplanet":
        reasons.append(
            "Exoplanet host"
        )

    elif category == "Anomalous":
        reasons.append(
            "Candidate anomalous target"
        )

    explanation = "; ".join(reasons)

    html += f"""
<tr>
<td>{row['rank']}</td>
<td>{row['name']}</td>
<td>{category}</td>
<td class="{css}">{score:.4f}</td>
<td>{explanation}</td>
</tr>
"""

html += """
</table>
</div>
"""

#
# Category Analytics
#

html += """
<div class="card">

<h2>Category Analytics</h2>

<table>

<tr>
<th>Category</th>
<th>Count</th>
<th>Average Score</th>
<th>Top Target</th>
</tr>
"""

for category, rows in sorted(
    category_stats.items()
):

    avg_score = (
        sum(
            r["score"]
            for r in rows
        )
        /
        len(rows)
    )

    leader = max(
        rows,
        key=lambda r: r["score"]
    )

    html += f"""
    <tr>
    <td>{category}</td>
    <td>{len(rows)}</td>
    <td>{avg_score:.4f}</td>
    <td>{leader['name']}</td>
    </tr>
    """

html += """
</table>
</div>
"""

#
# Top 5
#

html += """
<div class="card">

<h2>Top 5 Candidates</h2>

<ol>
"""

for row in targets[:5]:

    html += (
        f"<li><b>{row['name']}</b> "
        f"({row['category']}) "
        f"- {row['score']:.4f}</li>"
    )

html += """
</ol>
</div>
"""

#
# Anomaly Bars
#

html += """
<div class="card">
<h2>Relative Anomaly Scores</h2>
"""

for row in targets:

    pct = (
        row["score"]
        /
        max_score
    ) * 100

    html += f"""
    <p>
    {row['name']}
    ({row['score']:.4f})
    </p>

    <div
        class="bar"
        style="width:{pct:.1f}%;">
    </div>
    """

html += """
</div>
"""

#
# Histogram
#

html += """
<div class="card">

<h2>Score Distribution</h2>

<table>
<tr>
<th>Range</th>
<th>Count</th>
</tr>
"""

for key, value in bins.items():

    html += f"""
    <tr>
        <td>{key}</td>
        <td>{value}</td>
    </tr>
    """

html += """
</table>
</div>
"""

#
# Target Details
#

html += """
<div class="card">

<h2>Target Details</h2>
"""

for row in targets:

    score = row["score"]

    if score > 0.8:
        assessment = (
            "Strong anomaly candidate."
        )
    elif score > 0.4:
        assessment = (
            "Moderate anomaly candidate."
        )
    else:
        assessment = (
            "Low anomaly score."
        )

    html += f"""
    <details>

    <summary>
    {row['name']}
    </summary>

    <div class="note">

    <p><b>Category:</b>
    {row['category']}</p>

    <p><b>Score:</b>
    {score:.4f}</p>

    <p><b>Spread:</b>
    {row['spread']:.4f}</p>

    <p><b>Variance:</b>
    {row['variance']:.4f}</p>

    <p><b>Unity Deviation:</b>
    {row['unity']:.4f}</p>

    <p>
    <b>Assessment:</b>
    {assessment}
    </p>

    </div>

    </details>
    """

html += """
</div>

<div class="card">

<h2>Research Notes</h2>

<ul>

<li>
Quiet Sky ranks targets using
cross-survey photometric comparisons.
</li>

<li>
Higher scores indicate stronger
inter-survey disagreement.
</li>

<li>
Known variable stars appearing near the
top of the rankings provide validation
for the methodology.
</li>

<li>
Anomaly scores do not imply artificiality.
They identify targets worth review.
</li>

<li>
Most anomalies are expected to have
natural explanations.
</li>

</ul>

</div>

<script>

function sortTable(col) {{

    const table =
        document.getElementById(
            "leaderboard"
        );

    let switching = true;

    let dir = "desc";

    while (switching) {{

        switching = false;

        let rows =
            table.rows;

        for (
            let i = 1;
            i < rows.length - 1;
            i++
        ) {{

            let shouldSwitch =
                false;

            let x =
                rows[i]
                .getElementsByTagName(
                    "TD"
                )[col];

            let y =
                rows[i+1]
                .getElementsByTagName(
                    "TD"
                )[col];

            let xv =
                x.innerText;

            let yv =
                y.innerText;

            let xn =
                parseFloat(xv);

            let yn =
                parseFloat(yv);

            if (
                !isNaN(xn)
                &&
                !isNaN(yn)
            ) {{
                xv = xn;
                yv = yn;
            }}

            if (
                dir == "desc"
                &&
                xv < yv
            ) {{
                shouldSwitch = true;
            }}

            if (
                dir == "asc"
                &&
                xv > yv
            ) {{
                shouldSwitch = true;
            }}

            if (shouldSwitch) {{

                rows[i]
                .parentNode
                .insertBefore(
                    rows[i+1],
                    rows[i]
                );

                switching = true;
                break;
            }}
        }}

        if (
            !switching
            &&
            dir == "desc"
        ) {{

            dir = "asc";
            switching = true;
        }}
    }}
}}

</script>

</body>
</html>
"""

REPORT_FILE.write_text(
    html,
    encoding="utf-8"
)

print()
print("Quiet Sky Beta Report Generated")
print("=" * 60)
print(REPORT_FILE)