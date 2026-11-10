# QGI 1.0 — Pairwise Country Correlation Engine & First Streamlit Prototype (2023)

**Generation 1.0 of 7.0** · Originally developed under **`AminAlAit/trojan`** (core engine) and **`AminAlAit/trojan-streamlit`** (experimental UI) · **Current Production Platform:** [**`AminAlAit/qgi` (QGI 7.0)**](https://github.com/AminAlAit/qgi) ([qgintelligence.com](https://qgintelligence.com))

---

## Overview

In early 2023, Quantitative Geopolitical Intelligence started under the working codename **Trojan** (`AminAlAit/trojan` and `AminAlAit/trojan-streamlit`). The core question was simple: *if Country A's macroeconomic trajectory over a 10-year window closely mirrors a historical window from Country B, does Country B's subsequent trajectory tell us what Country A is heading toward?*

This repository preserves **Generation 1.0 of 7.0** — the initial Python correlation engine and the first interactive Streamlit prototype built to test that hypothesis across 237 countries and territories. Both original 2023 repositories (`trojan` and `trojan-streamlit`, including `trojan-streamlit`'s full 32-commit history) are unified here.

---

## How It Worked

1. **Time-Series Preparation (`data engine/dataPrep.py`, `initial_index_pipeline.py`):**
   - Ingested raw country-level indicator panels (`countries.csv`) and normalized annual country series into comparable sliding windows.
2. **Pairwise Pattern Discovery (`data engine/patternEngine.py`, `patternFinder.py`):**
   - `findPattern2Countries()` and `findAllPatterns()` iterated across country pairs (`Country A`, `Country B`), slicing variable-length historical windows and ranking bilateral indicator matches.
   - `patternValidator.py` filtered out low-overlap or degenerate time windows and exported per-country pattern dictionaries (`countries patterns/*_PATTERNS_DF.csv` and `*_REFINED_DICT.pkl`).
3. **Composite Index Stocker (`data engine/countriesIndex.py`, `nbs/stockers/`):**
   - Aggregated pairwise alignment counts and directional diffs into early country risk/alignment tables (`stockers/index_stocker.csv`, `showcase/allSortedPatternsShowcase.csv`).
4. **First Interactive Dashboard (`trojan-streamlit/`):**
   - Originally maintained in `AminAlAit/trojan-streamlit` (preserved on branch `trojan-streamlit/main` and merged under `trojan-streamlit/`).
   - Built an interactive Streamlit explorer (`trojan-streamlit/main.py`, `trojan.py`, `ST_testing_ground.ipynb`) to inspect matched country pairs and indicator overlays visually.

---

## Repository Structure

```text
qgi-1.0/
├── data engine/                         # Core 2023 pairwise correlation & pattern scripts (from AminAlAit/trojan)
│   ├── countriesIndex.py                # Country index aggregation logic
│   ├── dataPrep.py                      # Time-series cleaning & window slicing
│   ├── patternEngine.py                 # engine(), findAllPatterns(), findPattern2Countries()
│   ├── patternFinder.py                 # Sliding-window correlation search
│   ├── patternValidator.py              # Threshold & overlap validation
│   └── viz.py                           # Matplotlib/Plotly diagnostic plots
├── nbs/                                 # Research & prototyping notebooks
│   ├── country profiler/                # Per-country profile generation (countryProfileMaker.ipynb)
│   ├── explorers/                       # Exploratory data analysis (EDA_oneCeller.ipynb, eda.ipynb)
│   └── stockers/                        # Composite index construction (index_stocker_maker.ipynb)
├── countries patterns/                  # Pre-computed per-country pattern CSVs & pickled dictionaries
├── showcase/                            # Aggregated pattern showcases (allSortedPatternsShowcase.csv)
├── trojan-streamlit/                    # Merged history & source of AminAlAit/trojan-streamlit
│   ├── main.py                          # Early Streamlit interactive dashboard
│   ├── trojan.py                        # Streamlit helper & state logic
│   └── ST_testing_ground.ipynb          # UI & charting sandbox notebook
├── initial_index_pipeline.ipynb         # End-to-end 2023 index pipeline notebook
└── main.py                              # CLI entry point
```

---

## Why We Outgrew QGI 1.0

- **Flat-File Bottleneck:** Storing intermediate bilateral outputs as hundreds of `.csv` and `.pkl` files (`countries patterns/`) worked for a single composite index, but did not scale once we wanted to test dozens of distinct macro-indicators simultaneously.
- **Ad-Hoc Packaging:** Scripts relied on relative path imports (`data engine/`) and flat `requirements.txt` files, motivating the move to structured Python classes and Poetry dependency management in **QGI 2.0**.

---

## QGI Generational Roadmap (`v1.0` → `v7.0`)

| Generation | Year | Repository | Original Name(s) | Architectural Milestone |
| :--- | :--- | :--- | :--- | :--- |
| **QGI 1.0** *(Here)* | 2023 | **`AminAlAit/qgi-1.0`** | `trojan`, `trojan-streamlit` | Initial pairwise country correlation engine & first Streamlit UI |
| **QGI 2.0** | 2023 | [`AminAlAit/qgi-2.0`](https://github.com/AminAlAit/qgi-2.0) | `trojan-2.0` | Poetry-packaged ETLP pipeline, `Index` OOP hierarchy & STUMPY matrix profiles |
| **QGI 3.0** | 2024 | [`AminAlAit/qgi-3.0`](https://github.com/AminAlAit/qgi-3.0) | `qgi` (2024), `qgi-streamlit`, `qgi-local` | Multi-page Streamlit analytical terminal backed by relational SQLite/MySQL queries |
| **QGI 4.0** | 2025 | [`AminAlAit/qgi-4.0`](https://github.com/AminAlAit/qgi-4.0) | `qgi-4.0` | Formalization of the SCDI metric (Spearman + Cross-Correlation + DTW), Pipelines A–E & X Bot v1 |
| **QGI 5.0** | 2025–2026 | [`AminAlAit/qgi-5.0`](https://github.com/AminAlAit/qgi-5.0) | `qgi-pipeline-a/b/c` | First AWS cloud migration: Serverless Lambda ETL, Dockerized AWS Batch FFT worker & Athena CTAS |
| **QGI 6.0** | 2026 | `AminAlAit/qgi-6.0` | `qgi-aws-tf`, `qgi-infra`, `qgi-pipeline`, `qgi-data`, `qgi-ml`, `qgi-frontend`, `qgi-docs` | 4-account AWS Organization (14.3B FFT correlations), 42-model Trajectory Engine & Next.js 16 terminal |
| **QGI 7.0** *(Active)* | 2026–Present | [**`AminAlAit/qgi`**](https://github.com/AminAlAit/qgi) | `qgi`, `qgi-docs` | Unified production monorepo & live analytical terminal at [qgintelligence.com](https://qgintelligence.com) |
