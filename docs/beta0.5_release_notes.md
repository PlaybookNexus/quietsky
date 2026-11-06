Quiet Sky Beta 0.5
Category-Aware Discovery & Candidate Intelligence

Release Date: November 2026

Executive Summary

Quiet Sky Beta 0.5 marks the transition from anomaly ranking to candidate discovery.

Previous releases focused on collecting data, measuring targets, and generating scores. Beta 0.5 introduces population-aware analysis capable of identifying objects that stand out relative to their peers rather than simply producing high raw scores.

This release represents the first implementation of comparative anomaly detection across multiple stellar populations and establishes the framework required for AI-assisted candidate evaluation.

The project continues to pursue its central research question:

Which astronomical systems remain unusual when compared against similar objects across multiple wavelengths and surveys?

Add this section immediately after Installation and before Major New Capabilities.

Installation
Requirements

Quiet Sky Beta 0.5 requires:

Python 3.11+
Astropy
Astroquery
NumPy
Matplotlib


Install dependencies:

pip install -r requirements.txt


or

pip install astropy
pip install astroquery
pip install numpy
pip install matplotlib

Fresh Installation

Clone the repository:

git clone https://github.com/<your-account>/TabbysStar.git

cd TabbysStar


Create a virtual environment:

python -m venv .venv

.\.venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt


Build the catalog:

python quiet_sky.py


Select:

14. Build Beta Catalog
15. Resolve Coordinates


Download survey data:

1. Download Optical Surveys
2. Download Infrared Surveys


Measure targets:

3. Measure Optical Targets
4. Measure Infrared Targets


Generate rankings:

5. Generate Optical Rankings
6. Generate Infrared Rankings
7. Generate Composite Rankings


The system is now ready for analysis.

Upgrading to Beta 0.5

Existing Beta 0.4 users should perform the following upgrade steps.

Step 1: Pull Latest Changes
git pull


or

git pull origin main

Step 2: Update Dependencies
pip install -r requirements.txt --upgrade

Step 3: Create New Review Directory

Beta 0.5 introduces candidate review case files.

Create:

reviews/


Project structure:

TabbysStar/

├─ data/
├─ reports/
├─ reviews/
├─ scripts/
└─ ...

Step 4: Generate Category Rankings

Run:

Generate Composite Rankings


followed by:

python category_report_v2.py


This creates:

category_rankings.csv
category_outliers.csv


Required by the new discovery framework.

Step 5: Generate Discovery Candidates

Run:

python discovery_candidates_report.py


Output:

discovery_candidates_report.txt


This identifies category champions and population-level outliers.

Step 6: Generate Candidate Reviews

Example:

python candidate_review.py "Ross 640"


Exports:

reviews/

Ross_640_review_20261030_194501.txt


Additional examples:

python candidate_review.py "Ross 128"

python candidate_review.py "HD 5980"

python candidate_review.py "KIC 8462852"

python candidate_review.py "EPIC 204376071"

New Files Introduced in Beta 0.5
Rankings
category_rankings.csv
category_outliers.csv


Purpose:

Category-aware anomaly detection

Reports
discovery_candidates_report.txt


Purpose:

Candidate prioritization

Reviews
candidate_review.py


Purpose:

Investigate individual targets


Exports:

reviews/*_review_TIMESTAMP.txt

AI Systems
ai_candidate_review_board.py


Purpose:

AI-assisted candidate evaluation

Beta 0.5 Migration Checklist
[ ] Pull latest code
[ ] Update dependencies
[ ] Create reviews folder
[ ] Regenerate composite rankings
[ ] Generate category rankings
[ ] Generate discovery candidates
[ ] Generate first candidate reviews


Recommended first reviews:

Ross 640
Ross 128
HD 5980
EPIC 204376071
KIC 8462852


These targets currently represent the strongest discovery candidates identified by the Beta 0.5 category-aware ranking framework.

Upgrade Verification

Successful Beta 0.5 installation should produce:

rankings_v2.csv

category_rankings.csv
category_outliers.csv

discovery_candidates_report.txt

reviews/


and the Quiet Sky menu should include:

25. Discovery Candidates Report
26. AI Candidate Review Board


Major New Capabilities
Category-Aware Rankings

Previous ranking systems treated all targets as a single population.

Beta 0.5 introduces category-aware analysis.

Examples:

Exoplanets
White Dwarfs
Variable Stars
Nearby Stars
Transit Anomalies
Solar Analogs
Young Stellar Objects
Debris Disk Systems
Control Stars
Anomalous Objects
Flare Stars


Each target is now evaluated relative to comparable systems.

This prevents fundamentally different object types from competing directly against one another.

Population Statistics

Quiet Sky now calculates:

Category Population Size
Category Mean Score
Category Standard Deviation
Category Minimum Score
Category Maximum Score


Example output:

WhiteDwarf

Count   : 8
Average : 0.2469
StdDev  : 0.2229


This provides statistical context for every anomaly score.

Z-Score Analysis

Quiet Sky now computes category-relative Z-scores.

Z Score =
(Target Score - Category Mean)
/
Category Standard Deviation


This allows detection of objects that appear unusual relative to their own populations.

The system now identifies:

Population Outliers


rather than only:

High Scores

Category Champions

Each population now produces a category leader.

Example:

WhiteDwarf      Ross 640
Exoplanet       Ross 128
TransitAnomaly  EPIC 204376071
Variable        Delta Cephei


These objects represent the strongest candidates within each population.

Discovery Candidate System
Discovery Candidates Report

New report:

discovery_candidates_report.py


Purpose:

Convert rankings into candidate lists.


Inputs:

Composite Rankings
Category Rankings
Z Scores
Outlier Detection


Outputs:

Prioritized candidate list
Category champions
Population outliers


This report answers:

Which targets deserve immediate attention?

rather than:

Which targets scored highest?

Discovery Scoring

Quiet Sky now assigns Discovery Scores based on:

Global Ranking
Category Ranking
Category Champion Status
Population Outlier Status
Z Score


This promotes objects that remain unusual when viewed through multiple perspectives.

AI Candidate Intelligence
AI Candidate Review Board

New capability:

ai_candidate_review_board.py


Purpose:

Evaluate candidates using evidence-based review.


The review board classifies targets according to:

Population Status
Category Champion Status
Statistical Significance
Review Priority


The objective is not to identify extraterrestrial intelligence.

The objective is to identify targets that warrant further scientific investigation.

Candidate Review System

New capability:

candidate_review.py


Example:

python candidate_review.py "Ross 640"


Generated output:

Target Review
Category
Global Rank
Category Rank
Z Score
Technosignature Relevance
Scientific Assessment
Available Survey Data

Timestamped Case Files

Candidate reviews are now archived automatically.

Examples:

reviews/

Ross_640_review_20261101_034522.txt
Ross_128_review_20261101_034701.txt
HD_5980_review_20261101_035021.txt


This creates a permanent candidate history.

Scientific Findings
Finding #016

Category-aware rankings identified the first population-level outlier in the expanded catalog.

Result:

Ross 640
WhiteDwarf
Z = +2.26


Ross 640 became the first target promoted primarily through category-relative analysis rather than raw score alone.

This validates the category-aware ranking architecture.

Finding #017

Population-based anomaly detection can reveal candidates that would otherwise be overlooked.

Objects may rank highly because they are unusual relative to their peers even when they do not possess the highest raw scores in the entire catalog.

This finding supports the use of category-aware statistics as a discovery tool.

Current Leading Candidates

At the time of release:

Ross 640
Ross 128
EPIC 204376071
AU Microscopii
Delta Cephei
HD 5980


represent the highest-priority discovery candidates produced by the Beta 0.5 framework.

These rankings are expected to evolve as additional survey coverage and measurements become available.

Research Significance

Beta 0.5 changes the project's behavior from:

Anomaly Ranking


to:

Candidate Discovery


The system no longer asks:

Which stars have high scores?


The system now asks:

Which stars appear unusual relative to their peers?


This distinction substantially improves scientific interpretability.

Current Catalog Status
Targets: 133

Categories: 11

Coordinate Resolution: 133 / 133

Optical Pipeline: Operational

Infrared Pipeline: Operational

Category Rankings: Operational

Discovery Candidates: Operational

AI Candidate Review Board: Operational

Case File Generation: Operational

Looking Forward
Beta 0.6

Planned focus:

AI Candidate Intelligence


Candidate enhancements:

Local LLM Scientific Reviews
Population Trend Tracking
Discovery Candidate Watchlists
Historical Candidate Evolution
Multi-Review Comparison
Confidence Scoring


The long-term objective remains unchanged.

Success is not finding extraterrestrial intelligence.

Success is building a repeatable, evidence-based anomaly detection framework capable of identifying astronomical systems worthy of closer scientific investigation.

Status: Beta 0.5 Released ✅

Project Phase: Category-Aware Discovery ✅

Next Milestone: AI-Assisted Candidate Intelligence 🚀🌌🤖