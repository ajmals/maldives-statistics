# Maldives National Statistics Data Processing Pipeline

A comprehensive technical guide to the ingestion, extraction, linguistic normalization, and longitudinal harmonization of 19 editions of the **Statistical Yearbook of Maldives (2008–2026)**.

---

## 🏗️ Architecture Overview

The pipeline transforms heterogeneous, human-formatted government publications into unified, machine-readable datasets through a 4-stage pipeline:

```
┌────────────────────────────────┐
│   National Bureau of Statistics │ (PDFs, Excel .xls/.xlsx, HTML tables)
└────────────────┬───────────────┘
                 │ 1. Scrape & Ingest (download_yearbooks.py)
                 ▼
┌────────────────────────────────┐
│   data/raw/ (7,147 files)      │ 19 Editions (2008–2026), manifest.json
└────────────────┬───────────────┘
                 │ 2. Clean & Standardize (process_all_yearbooks.py)
                 ▼
┌────────────────────────────────┐
│   data/processed/ (3,937 CSVs) │ Standardized UTF-8 CSVs + JSON Schemas
└────────────────┬───────────────┘
                 │ 3. Category Consolidation (build_master_categories.py)
                 ▼
┌────────────────────────────────┐
│   data/master_categories/      │ 22 Categories: Wide CSVs & master_panel.csv
└────────────────┬───────────────┘
                 │ 4. Dashboard Synthesis (prepare_unified_dashboard_data.py)
                 ▼
┌────────────────────────────────┐
│   assets/                      │ dashboard_data_unified.json & .js
└────────────────────────────────┘
```

---

## 🛠️ Stage-by-Stage Breakdown

### Stage 1: Discovery & Scraper (`scripts/download_yearbooks.py`)
* **Source**: Scrapes the official National Bureau of Statistics (NBS) portal (`https://statisticsmaldives.gov.mv/yearbook/`).
* **Multi-Year Coverage**: Automatically crawls and indexes 19 editions (2008 to 2026).
* **Pre-2008 Archive Availability & Gap Handling**:
  * The NBS online portal exclusively hosts digital web directories from **2008 through 2026**.
  * Yearbooks published prior to 2008 are **missing from the online digital portal** (older editions were physical print volumes).
  * The 2008 online archive itself only published an introductory index table, with full multi-chapter downloadable spreadsheets commencing with the 2009 edition.
  * To bridge continuous longitudinal metrics for 2000–2007 (such as the 2004 Tsunami baseline, historical GDP, and Census 1995/2000/2006 records), the pipeline ingests official **retrospective historical tables** published in subsequent yearbooks (e.g. 2008–2014 editions) alongside multilateral post-disaster reports (*Joint World Bank / ADB / UN Tsunami Assessment 2005*).
* **Resilient Ingestion**:
  * Resolves broken ministry URLs, unescapes HTML entities, and safely encodes URI components.
  * Implements dynamic extension fallback (`.xlsx` ↔ `.xls`) for mislabeled server links.
  * Utilizes multi-threaded concurrent downloading with exponential backoff and resume capabilities (skipping existing verified files).
  * Generates per-year `manifest.json` files and a root `data/raw/manifest.json`.

---

### Stage 2: Table Cleaning & Standardization (`scripts/process_all_yearbooks.py`)

Government statistical spreadsheets are designed for human visual inspection and printing rather than automated computational ingestion. This script handles:

#### 1. The Thaana Linguistic Challenge
* **Unicode vs. Legacy Font Encodings**: Early yearbook editions (2008–2015) typed Dhivehi (Thaana) using Latin ASCII keystrokes styled with proprietary fonts (e.g., *Faruma*, *Faseyha*, *Randhoo*, *Waheed*, *Kuredhi*, *VoguePSMT*). When opened without those fonts, text displays as meaningless strings (e.g., `clwvwt`, `cnunemihob`).
* **Detection & Filtering**: The pipeline detects legacy font metadata and character distribution patterns to strip non-data Dhivehi headers and bilingual repetitions while preserving numerical integrity and English column labels.

#### 2. Merged & Hierarchical Header Resolution
* Government tables frequently feature 2 to 4 levels of merged cells (e.g., `Year` spanning multiple sub-columns such as `Male`, `Female`, `Both Sexes`).
* The extraction engine dynamically traverses merged cell ranges, forwards top-level categories, and synthesizes flat, unambiguous column names (e.g., `2019 - Female`, `2020 - Both Sexes`).

#### 3. Table Boundary & Noise Elimination
* Detects and removes decorative title banners, ministry logos, Dhivehi table captions, explanatory footnotes located inside the data grid, blank spacer rows, and embedded summary charts.

#### 4. Type Coercion & Numerical Precision
* Cleans currency signs, commas, and percentage markers while retaining native floating-point precision.
* Standardizes statistical missingness codes (`-`, `...`, `na`, `np`, `*`) into structured null representations.
* Generates paired `.csv` files alongside `.json` metadata companions containing original titles, units, notes, and sources.

---

### Stage 3: Master Category Consolidation (`scripts/build_master_categories.py`)

Statistical Yearbooks publish discrete annual slices. To enable multi-decade time-series analysis:

1. **Harmonized 22 Thematic Categories**: Standardizes variations in chapter names across editions (e.g., mapping `3.0 population`, `Population and Housing`, and `Demographics` to `3.0 Population`).
2. **Wide Time-Series CSVs (`tables/<table_id>.csv`)**: Merges identical statistical indicators across yearbooks into wide tables with chronological year columns spanning from the 1980s through 2026+.
3. **Revision Resolution**: Where published numbers differ between editions (due to revised preliminary figures), the pipeline establishes precedence for the latest official publication.
4. **Tidy Long-Format Panel (`master_panel.csv`)**: Converts wide tables into long-format tidy datasets (`category`, `table_id`, `item_name`, `metric_name`, `year`, `value`, `unit`) ready for Pandas, R, or database bulk loading.
5. **Local SQLite Generation**: Builds `maldives_statistics_master.db` and `<category>.db` locally for analysts who prefer SQL querying over CSVs.

---

### Stage 4: Dashboard Payload Synthesis (`scripts/prepare_unified_dashboard_data.py`)

* Synthesizes longitudinal time-series (2000–2026) across 10 national macroeconomic pillars.
* Merges census demographic cohorts (1995–2014) and population projections (2014–2030) from [`data/demographics_pyramid.json`](data/demographics_pyramid.json).
* Builds the **2004 Indian Ocean Tsunami** and **COVID-19 Pandemic Shock** crisis analytics payloads:
  * **2004 Tsunami**: 6-phase timeline scrubber, displaced populations by atoll, post-tsunami reconstruction capital expenditure (NBS Cat 13.9 & 13.11), and comparative shock contraction benchmarks.
  * **COVID-19 Pandemic**: 48-month continuous visitor arrival trajectory (2019–2022), April–June 2020 aviation closure anatomy, source market rotation (Russia & India surge), and global SIDS comparative benchmarks.
* Exports lightweight, pre-indexed JSON and JS payloads to [`assets/`](assets/) to power the zero-backend client-side web dashboard.

---

## 💻 Running the Pipeline Locally

### Prerequisites
```bash
git clone https://github.com/ajmals/maldives-statistics.git
cd maldives-statistics

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Full Pipeline Execution
```bash
# 1. Download all available yearbook editions (2008–2026)
python scripts/download_yearbooks.py --years all

# 2. Extract, clean, and standardize tables into CSVs + JSON metadata
python scripts/process_all_yearbooks.py

# 3. Consolidate into 22 longitudinal categories and build panel archives
python scripts/build_master_categories.py

# 4. Generate the optimized dashboard data bundle
python scripts/prepare_unified_dashboard_data.py
```
