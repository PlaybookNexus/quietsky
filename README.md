<div align="center">

# 🔭 Quiet Sky

### AI-Assisted Astronomical Anomaly Detection

*Large-scale multi-wavelength analysis of stellar systems using optical, infrared, and time-domain observations.*

https://img.shields.io/badge/Python-3.11+-blue
https://img.shields.io/badge/Status-Active-success
https://img.shields.io/badge/Version-v4.0-orange
https://img.shields.io/badge/Catalog-4,547%20Targets-purple
https://img.shields.io/badge/TESS-4,466%20Detections-blueviolet
https://img.shields.io/badge/TESS%20Measured-4,166-green
https://img.shields.io/badge/TESS%20Archive-98.85GB-red
https://img.shields.io/badge/License-MIT-brightgreen

</div>

---

# Mission

Quiet Sky is an experimental astronomy platform designed to identify statistically unusual stellar systems through automated anomaly detection.

The project began as an investigation of **KIC 8462852 (Tabby's Star)** and evolved into a generalized framework capable of analyzing thousands of astronomical objects across:

- Optical surveys
- Infrared surveys
- Time-domain observations
- Multiple stellar populations
- Multi-decade archives

The project does **not** attempt to prove extraterrestrial intelligence.

Instead, it seeks to answer a simpler and more scientifically defensible question:

> Which astronomical objects appear statistically unusual when compared against similar stars?

---

# Project Highlights

| Metric | Value |
|----------|----------:|
| Curated Research Catalog | 103 Targets |
| TESS Survey Catalog | 4,547 Targets |
| TESS Detections | 4,466 Targets |
| Coverage Rate | 98.2% |
| TESS Targets Measured | 4,166 |
| TESS Products Downloaded | 4,561 |
| Archive Size | 98.85 GB |
| Composite Ranking Engine | v4 |
| Candidate Dossiers Generated | 25 |

---

# Key Results

## TESS Survey

```text
Targets Searched : 4,547
TESS Detections  : 4,466
Coverage Rate    : 98.2%

Variability Analysis
Targets Measured : 4,166
Targets Ranked   : 4,166

Notable Composite Result
KIC 8462852 (Tabby's Star)

TESS Rank      : #800
Composite Rank : #18


This result demonstrates the value of combining multiple independent observation domains rather than relying on a single survey.

Table of Contents
#current-capabilities
#scientific-dataset
#data-sources
#tess-pipeline
#project-architecture
#installation
#project-milestones
#key-findings
#current-assessment
#research-philosophy
#long-term-vision
Current Capabilities
Acquisition

✅ DSS survey retrieval

✅ 2MASS survey retrieval

✅ WISE survey retrieval

✅ TESS archive retrieval

✅ Automated coordinate resolution

Measurements

✅ Astrometric localization

✅ Differential photometry

✅ Background subtraction

✅ Difference imaging

✅ Time-domain variability extraction

Analysis

✅ Optical ranking engine

✅ Infrared ranking engine

✅ TESS ranking engine

✅ Composite anomaly scoring

✅ Discovery reports

✅ Candidate dossiers

✅ AI-assisted analysis

Scientific Dataset
Curated Catalog
Resolved Targets : 103
Coordinate Failures : 0


Categories:

Exoplanet Hosts
Variable Stars
Nearby Stars
Solar Analogs
Flare Stars
Control Targets
Anomalous Targets
Large-Scale TESS Catalog
Targets Searched : 4,547
TESS Detections  : 4,466
Coverage Rate    : 98.2%

Data Sources
Optical
DSS
DSS
DSS2 Red
DSS2 Blue

Purpose:

Historical imaging
Long-term comparison
Visual inspection
Near Infrared
2MASS
J
K

Purpose:

Near-infrared characterization
Color comparison
Infrared
WISE
W1 (3.4 μm)
W2 (4.6 μm)

Purpose:

Infrared excess analysis
Dust signatures
Time Domain
TESS

Purpose:

Variability detection
Transit detection
Dimming event analysis
Anomaly ranking
TESS Pipeline
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
TESS FITS Archive
        │
        ▼
measure_all_tess.py
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

Sector coverage
Observation density
Relative RMS variability
Maximum dimming
Maximum brightening
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
Measurement Engines
      │
      ├── Optical
      ├── Infrared
      └── Time Domain
      │
      ▼
Ranking Engines
      │
      ▼
Composite Scoring
      │
      ▼
Discovery Reports
      │
      ▼
Candidate Dossiers
      │
      ▼
AI-Assisted Analysis

Installation
Requirements
Python 3.11+
Internet connection
5 GB minimum storage
100+ GB recommended for full TESS archive acquisition
Clone Repository
git clone https://github.com/PlaybookNexus/quietsky.git

cd TabbysStar

Virtual Environment
python -m venv .venv

.\.venv\Scripts\activate

Install Dependencies
pip install -r requirements.txt

Project Milestones
2026

✅ Multi-target catalog framework

✅ 103-target research catalog

✅ 4,547-target TESS catalog

✅ 98.2% TESS coverage discovery

✅ Automated coordinate resolution

✅ Automated TESS archive ingestion

✅ 98.85 GB TESS archive

✅ 4,166 TESS targets measured

✅ 4,166 TESS targets ranked

✅ Automated aggregation engine

✅ Composite scoring engine

✅ Discovery report generation

✅ Candidate dossier generation

Key Findings
Finding #001

Measurements must be tied to sky coordinates.

Finding #002

WCS localization significantly improves multi-survey agreement.

Finding #003

Reference-star selection materially impacts photometric measurements.

Finding #004

Infrared and optical evidence can be successfully combined.

Finding #005

Visual inspection alone does not reveal compelling anomalies.

Finding #006

98.2% of catalog targets possess useful TESS coverage.

Finding #007

Quiet Sky now supports large-scale automated time-domain anomaly detection.

Finding #008

KIC 8462852 ranks far higher in composite scoring than in TESS scoring alone.

Current Assessment

At present:

No compelling artificial signatures have been observed.
No extraordinary infrared excess has been identified.
No target currently dominates every analysis domain.
Several targets remain worthy of follow-up investigation.

This is considered a successful outcome.

The principal achievement of the project is the development of a repeatable and scientifically defensible methodology for identifying unusual stellar systems.

Research Philosophy

Traditional SETI efforts focus on communication:

Radio signals
Optical beacons
Directed transmissions

Quiet Sky explores a different possibility.

If advanced technological civilizations become:

AI-assisted
Computationally focused
Resource optimized
Highly automated
Post-biological

then unusual systems may be easier to detect through statistical anomalies than through deliberate communication.

Quiet Sky therefore focuses on anomaly detection rather than communication detection.

Long-Term Vision

Develop a scalable anomaly-detection platform capable of:

Processing tens of thousands of targets
Integrating Gaia observations
Incorporating spectroscopy
Tracking historical changes
Performing machine-learning classification
Generating automated scientific assessments

Success is not finding aliens.

Success is building a scientifically defensible system capable of identifying astronomical objects worthy of deeper investigation.