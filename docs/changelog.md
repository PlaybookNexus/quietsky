CHANGELOG
Quiet Sky
[Beta 0.5] - November 2026
Category-Aware Discovery
Overview

Beta 0.5 introduces the first population-aware anomaly detection framework in Quiet Sky.

Previous releases focused on data acquisition, measurements, rankings, and report generation.

This release shifts the project toward candidate discovery by ranking targets relative to their peer populations rather than treating all astronomical objects as a single group.

Added
Category-Aware Rankings

Added support for category-level ranking and statistical analysis.

New populations:

Anomalous
Control
DebrisDisk
Exoplanet
Flare
Nearby
SolarAnalog
TransitAnomaly
Variable
WhiteDwarf
YoungStar


New outputs:

category_rankings.csv
category_outliers.csv

Population Statistics

Added statistical summaries for each category.

Metrics include:

Population Count
Mean Score
Standard Deviation
Minimum Score
Maximum Score


This provides scientific context for ranking interpretation.

Category Champions

Implemented automatic category leader detection.

Examples:

WhiteDwarf      Ross 640
Exoplanet       Ross 128
Variable        Delta Cephei
Flare           AU Microscopii


Category champions represent the strongest candidate within their peer group.

Z-Score Analysis

Implemented population-relative anomaly scoring.

Formula:

(Target Score - Category Mean)
/ Category Standard Deviation


Benefits:

Detects category outliers
Reduces population bias
Improves interpretability

Discovery Candidates Report

New script:

discovery_candidates_report.py


New menu item:

25. Discovery Candidates Report


Purpose:

Convert anomaly rankings into
actionable review candidates.


New output:

discovery_candidates_report.txt

AI Candidate Review Board

New script:

ai_candidate_review_board.py


New menu item:

26. AI Candidate Review Board


Purpose:

Evaluate promising candidates using
statistical evidence and review criteria.

Candidate Review System

New script:

candidate_review.py


Usage:

python candidate_review.py "Ross 640"


Capabilities:

Candidate Assessment
Ranking Review
Category Analysis
Technosignature Relevance
Evidence Review
Survey Inventory

Timestamped Candidate Reviews

Individual candidate investigations are now archived.

Examples:

reviews/

Ross_640_review_20261101_034522.txt

Ross_128_review_20261101_034701.txt

HD_5980_review_20261101_035021.txt


This creates permanent review history for future comparison.

Changed
Discovery Philosophy

Previous versions emphasized:

Highest Score Wins


Beta 0.5 emphasizes:

Most Unusual Relative To Peers Wins


This reduces bias between vastly different object types.

Ranking Interpretation

Raw scores are now supplemented with:

Category Ranking
Category Champion Status
Population Statistics
Z Scores


Result:

Improved scientific interpretability.

Discovery Workflow

Previous workflow:

Measurements
→ Rankings
→ Reports


New workflow:

Measurements
→ Rankings
→ Category Rankings
→ Discovery Candidates
→ Candidate Reviews
→ AI Review Board

Scientific Findings
Finding #016

Category-aware rankings identified the first significant population-level outlier in the expanded catalog.

Result:

Ross 640

Category:
WhiteDwarf

Z Score:
+2.26


Ross 640 became the first candidate promoted through category-relative analysis rather than raw score alone.

Finding #017

Population-based anomaly detection can reveal candidates that may not dominate global rankings.

This validates category-aware ranking as a useful scientific discovery tool.

Catalog Status
Catalog Size             133 Targets
Categories               11
Coordinate Resolution    133 / 133


Operational systems:

Optical Acquisition
Infrared Acquisition
Photometry
Anomaly Rankings
Composite Rankings
Category Rankings
Discovery Candidate Reports
AI Review Board
Candidate Reviews
Project Memory
Change Analysis

First Discovery Candidate List

Top candidates identified during Beta 0.5 validation:

Ross 640
Ross 128
EPIC 204376071
AU Microscopii
Delta Cephei
HD 5980


These objects form the initial candidate watchlist for future investigation.

Fixed
Menu Numbering Issues

Corrected pipeline menu numbering.

Current:

22. Run Optical Pipeline
23. Run Infrared Pipeline
24. Run Full Analysis
25. Discovery Candidates Report
26. AI Candidate Review Board

Candidate Review Exporting

Candidate reviews now automatically export to timestamped files.

This prevents reviews from being overwritten and supports longitudinal analysis.

Upgrade Notes

Beta 0.5 introduces new generated artifacts:

category_rankings.csv

category_outliers.csv

discovery_candidates_report.txt

reviews/


Existing users should regenerate rankings after upgrading.

Recommended sequence:

Generate Optical Rankings
Generate Infrared Rankings
Generate Composite Rankings
Generate Category Rankings
Generate Discovery Candidates
Generate Candidate Reviews

Looking Ahead
Planned for Beta 0.6
AI Candidate Intelligence

Goals:

Local LLM Review Generation
Candidate Trend Analysis
Historical Candidate Tracking
Multi-Epoch Comparisons
AI Scientific Narratives
Confidence Scoring

Long-Term Goal

Quiet Sky continues to investigate whether anomaly detection can identify astronomical systems worthy of additional scrutiny.

The objective remains:

Build a scientifically defensible,
AI-assisted discovery framework.


Success is not proving the existence of extraterrestrial intelligence.

Success is creating a repeatable process for identifying phenomena that remain unusual after conventional explanations are considered.

Release: Beta 0.5 ✅
 Project Phase: Category-Aware Discovery ✅
 Next Milestone: AI Candidate Intelligence