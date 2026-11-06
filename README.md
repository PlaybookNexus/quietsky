Quiet Sky
AI-Assisted Astronomical Anomaly Detection
Overview

Quiet Sky is an experimental astronomy project exploring whether publicly available astronomical survey data can be used to identify unusual stellar systems through anomaly detection.

The project began with a single target, KIC 8462852 (Tabby's Star), and evolved into a generalized framework capable of comparing thousands of stars across:

multiple decades
multiple surveys
multiple wavelengths
multiple target populations
multiple time-domain observations

The goal is not to prove extraterrestrial intelligence.

The goal is to create a repeatable and scientifically defensible system capable of answering a simpler question:

Which astronomical objects appear statistically unusual when compared against similar stars?

Current Capabilities

Implemented:

✅ Optical survey acquisition

✅ Infrared survey acquisition

✅ TESS light-curve acquisition

✅ Coordinate resolution

✅ Astrometric localization

✅ Differential photometry

✅ Background subtraction

✅ Difference imaging

✅ Multi-wavelength analysis

✅ Time-domain photometry

✅ Automated variability measurements

✅ TESS ranking engine

✅ Multi-target comparison framework

✅ AI-assisted analysis

Installation
Prerequisites
Python 3.11+
Internet connection
5 GB minimum free disk space
100+ GB recommended for full TESS archive acquisition
Clone Repository
git clone https://github.com/PlaybookNexus/quietsky.git

cd TabbysStar

Create Virtual Environment
python -m venv .venv

.\.venv\Scripts\activate

Install Dependencies
pip install astropy
pip install astroquery
pip install matplotlib
pip install numpy
pip install pandas
pip install lightkurve


Or:

pip install -r requirements.txt

Scientific Dataset
Research Catalog

Current curated catalog:

Targets Resolved      : 103
Coordinate Failures   : 0


Target categories:

Anomalous
Exoplanet Hosts
Variable Stars
Nearby Stars
Control Stars
Large-Scale TESS Catalog

Survey results:

Targets Searched      : 4,547
TESS Detections       : 4,466
Coverage Rate         : 98.2%
Timeouts              : 28


This discovery established that most Quiet Sky targets possess useful TESS coverage suitable for large-scale time-domain analysis.

Data Sources
Optical
Digitized Sky Survey
DSS
DSS2 Red
DSS2 Blue

Purpose:

historical imaging
long-term comparison
visual anomaly inspection
Near Infrared
2MASS
J Band
K Band

Notes:

H Band retrieval produced invalid data
and is excluded from analysis.


Purpose:

near infrared comparison
Infrared
WISE
3.4 μm
4.6 μm

Purpose:

infrared characterization
infrared excess analysis
Time Domain
TESS

Purpose:

long-term photometric monitoring
variability detection
transit detection
dimming-event identification
anomaly ranking

Current archive acquisition:

4,466 TESS-enabled targets

TESS Pipeline

Implemented in 2026.

Pipeline:

targets_resolved_master.csv
        │
        ▼
fetch_tess_targets.py
        │
        ▼
targets_tess.csv
        │
        ▼
download_tess_spoc.py
        │
        ▼
TESS FITS archive
        │
        ▼
measure_tess.py
        │
        ▼
tess_measurements.csv
        │
        ▼
rank_tess.py
        │
        ▼
tess_rankings.csv
        │
        ▼
aggregate_tess.py
        │
        ▼
tess_target_rankings.csv


Measurements include:

sector coverage
observation count
RMS variability
relative RMS variability
maximum dimming
maximum brightening
Project Architecture
Target Catalog
      │
      ▼
Coordinate Resolution
      │
      ▼
Survey Acquisition
      │
      ├── DSS
      ├── 2MASS
      ├── WISE
      └── TESS
      │
      ▼
Measurements
      │
      ├── Optical
      ├── Infrared
      └── Time Domain
      │
      ▼
Ranking Engines
      │
      ▼
Composite Ranking
      │
      ▼
Reports
      │
      ▼
AI Analysis
      │
      ▼
Project Memory

Project Milestones
2026

✅ Multi-target catalog framework

✅ 103-target curated research catalog

✅ 4,547-target TESS catalog

✅ 98.2% TESS coverage discovery

✅ Automated coordinate resolution

✅ Automated TESS archive ingestion

✅ Multi-format FITS handling

✅ Automated variability measurements

✅ Automated ranking pipeline

✅ Target-level aggregation

Key Findings
Finding #001

Survey images cannot be reliably compared using fixed pixel coordinates.

Conclusion

Measurements must be tied to sky coordinates.

Finding #002

WCS-based localization significantly improved survey agreement.

Conclusion

Sky-coordinate alignment is essential.

Finding #003

Reference-star selection materially affects photometric results.

Conclusion

Reference stars require validation.

Finding #004

Infrared data from 2MASS and WISE were successfully integrated.

Conclusion

Quiet Sky supports multi-wavelength analysis.

Finding #005

No visually distinct anomaly was observed at the position of Tabby's Star.

Conclusion

Visual survey inspection alone is insufficient.

Finding #006

The TESS survey identified:

4,466 TESS-enabled targets


from:

4,547 targets searched

Conclusion

Most Quiet Sky targets possess useful time-domain coverage.

Finding #007

Automated TESS measurement extraction was successfully implemented.

Metrics include:

variability
dimming
brightening
sector coverage
observation density
Conclusion

Quiet Sky now supports automated time-domain anomaly detection.

Current Assessment

At present:

No strong anomaly has been identified.
No compelling infrared excess has been observed.
No visually obvious artificial structures have been detected.
No target currently stands out as extraordinary.

This is considered a successful outcome.

The primary achievement of the project has been building a reproducible methodology while eliminating sources of observational and analytical error.

Research Philosophy

Traditional SETI efforts primarily search for communication:

radio signals
optical beacons
deliberate transmissions

Quiet Sky explores a different possibility.

If advanced technological civilizations eventually become:

AI-assisted
computationally focused
resource optimized
post-biological

then the most detectable signatures may not be messages.

Instead, unusual systems may reveal themselves through statistically rare behavior:

long-term dimming
variability anomalies
unusual infrared characteristics
uncommon energy distributions
deviations from comparable populations

Quiet Sky therefore focuses on anomaly detection rather than communication detection.

Primary Research Question

Can a repeatable AI-assisted pipeline identify astronomical systems that differ significantly from comparable stars across time and wavelength?

Long-Term Vision

Develop an extensible anomaly-detection platform capable of:

processing thousands of stars
integrating additional survey archives
comparing multiple wavelengths
incorporating Gaia data
incorporating spectroscopic data
generating anomaly rankings
supporting machine-learning classification
detecting historical trends across project snapshots

Success is not finding aliens.

Success is building a scientifically defensible system capable of identifying astronomical objects that deserve closer investigation.