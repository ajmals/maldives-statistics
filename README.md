# Statistical Yearbook 2021 Maldives — Interactive Dashboard & Analysis

[![Live Dashboard](https://img.shields.io/badge/Live%20Dashboard-GitHub%20Pages-brightgreen?style=for-the-badge&logo=github)](https://ajmals.github.io/maldives-statistics-2021/)
[![Datasets](https://img.shields.io/badge/Datasets-309%20Tables-blue.svg)](datasets/)
[![Chapters](https://img.shields.io/badge/Chapters-20%20Thematic%20Areas-green.svg)](datasets/catalog.json)
[![Indicators](https://img.shields.io/badge/Indicators-18%20Series%20%28incl.%20Poverty%29-purple.svg)](datasets/indicators/)
[![Analysis](https://img.shields.io/badge/EDA-Comprehensive%20Report-orange.svg)](EXPLORATORY_DATA_ANALYSIS.md)
[![Python](https://img.shields.io/badge/Python-3.14%20%7C%20Pandas-yellow.svg)](requirements.txt)

> 🚀 **Live Interactive Web Application**: [https://ajmals.github.io/maldives-statistics-2021/](https://ajmals.github.io/maldives-statistics-2021/)

A complete, machine-readable, open-data repository and interactive dashboard of the **Statistical Yearbook of Maldives 2021**, originally published by the **National Bureau of Statistics (NBS)**, Maldives.

This repository transforms the official annual statistical compendium into **309 clean, tabular UTF-8 CSV datasets** with structured JSON metadata, accompanied by **18 Indicator datasets** (including Poverty), an **Interactive Web Dashboard hosted live on GitHub Pages**, extensive **Exploratory Data Analysis (EDA)**, interactive Jupyter Notebook, and visualization figures.

---

## 🌐 Live Interactive Dashboard

Explore the interactive web application directly in your browser:  
👉 **[https://ajmals.github.io/maldives-statistics-2021/](https://ajmals.github.io/maldives-statistics-2021/)**

The dashboard is built with HTML5, Vanilla CSS3, modern JavaScript, and Chart.js, requiring zero backend or complex build pipeline.

### 🌟 Key Features:
- **Zero-Build Deployment**: Hosted live via GitHub Pages directly from the repository.
- **Animated Population Pyramid (2014–2030 & Censuses 1995–2014)**: Interactive year-on-year demographic transitions across 17 age cohorts with playback controls, timeline scrubber, sub-population filters (Total, Maldivians, Foreign Expats), and geographic scopes (National, Malé City, Outer Atolls).
- **Global Benchmarking Suite**: Directly contrasts Maldives data against international indicators (Paris, Manhattan, Manila, Tokyo, Spain, Iceland, World averages).
- **Curated Trivia & Interesting Facts**: Interactive categorized flashcards revealing geographic, economic, and demographic extremes.
- **Dynamic Chart Suite**: Interactive radar, line, bar, and doughnut charts with dark/light mode toggle.
- **190-Island Interactive Directory**: Live search and sort across all 190 inhabited localities by population, land area, density, and distance to Malé.
- **309-Table Master Catalog Explorer**: Filter by chapter or search any table to immediately access and download clean CSVs.

---

## 📊 Key Highlights & Exploratory Data Analysis

A detailed empirical investigation is available in **[`EXPLORATORY_DATA_ANALYSIS.md`](EXPLORATORY_DATA_ANALYSIS.md)** and the **[`notebooks/exploratory_data_analysis.ipynb`](notebooks/exploratory_data_analysis.ipynb)** notebook.

### Core Empirical Findings:
- **Primate City Density**: Malé Island concentrates **153,904 residents (39.4% of national population)** onto **2.05 km²**, reaching a world-leading density of **74,879 people/km²** (vs a median of 1,009 residents on outer atoll islands).
- **The 2020 COVID-19 Macro Shock**: Real GDP contracted by **-33.5%** in 2020 (77.1B MVR down to 51.3B MVR)—more than **2.5× the impact of the 2004 Tsunami** (-13.1%) and **4.6× the 2008 Global Financial Crisis** (-7.2%).
- **Tourism Collapse & Geopolitical Rebound**: Annual tourist arrivals fell by **-67.4%** (from 1.70M in 2019 to 555k in 2020). Border closure in Q2 saw just 55 arrivals, followed by a rapid winter recovery led by **India (62,960)** and **Russia (61,387)**, displacing **China** (plunging from 284k to 34k).
- **The Blue Economy Stabilizer**: While service sectors halted, the **Fisheries sector expanded by +10.2%**, landing a record **148,583 metric tons** of fish (led by **103,871 MT of Skipjack Tuna**), with **70.8% exported**.
- **Freshwater Scarcity**: Between **70 and 91 inhabited islands** exhaust their freshwater reserves during the dry season, requiring emergency maritime water deliveries at an average cost of **2,750+ MVR per ton**.

---

## 📁 Repository Structure

```text
statistical-year-book-2021/
├── index.html                             # Interactive Web Dashboard UI
├── app.js                                 # Dashboard state, search, and Chart.js logic
├── styles.css                             # Dark/light theme & responsive styling
├── dashboard_data.js                      # Pre-bundled dashboard dataset & catalog
├── data/                                  # Multi-year statistical repository
│   ├── raw/                               # Official original files (PDFs, Excel, HTML)
│   │   ├── manifest.json                  # Multi-year collection metadata index
│   │   ├── 2026/ ... 2008/                # 18 Yearbook editions (7,147 files, 1.37 GB)
│   │   └── 2021/                          # 2021 raw PDFs & Excel files (20 chapters)
│   └── processed/                         # Extracted, standardized datasets
│       └── 2021/                          # 309 clean CSVs + JSON schema & metadata
├── datasets/ -> data/processed/2021/      # Symlink for backward-compatibility
├── raw_stats_data/ -> data/raw/2021/      # Symlink for backward-compatibility
├── figures/                               # Publication-grade visualization figures (PNG)
├── notebooks/
│   └── exploratory_data_analysis.ipynb   # Interactive analysis Jupyter Notebook
├── scripts/
│   ├── download_yearbooks.py             # Multi-year scraper & downloader (2008-2026)
│   ├── prepare_dashboard_data.py          # Dashboard bundling script
│   ├── generate_eda_visualizations.py    # Figure generation pipeline
│   └── build_eda_notebook.py             # Notebook generation pipeline
├── EXPLORATORY_DATA_ANALYSIS.md          # Full in-depth research report
├── requirements.txt                      # Python dependencies
└── README.md                             # Repository overview
```

### 📥 Downloading Additional Yearbooks
You can run the multi-year downloader anytime to update or download specific editions:
```bash
# Download all available editions (2008-2026)
python scripts/download_yearbooks.py --years all

# Download specific yearbooks (e.g. 2026 and 2025)
python scripts/download_yearbooks.py --years 2026,2025
```


---

## 🚀 Quickstart & Usage

### 1. Installation
Clone the repository and install dependencies in a virtual environment:
```bash
git clone https://github.com/ajmals/maldives-statistics-2021.git
cd maldives-statistics-2021

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Loading Datasets with Python & Pandas
Every table is stored in clean CSV format alongside a `.json` companion holding original units, Dhivehi titles, notes, and sources:

```python
import json
import pandas as pd

# Load master catalog
with open('datasets/catalog.json') as f:
    catalog = json.load(f)

# Find any table by keyword
tour_tables = [t for t in catalog if 'tourist' in t['title_en'].lower()]
print(f"Found {len(tour_tables)} tourism datasets.")

# Load Real GDP data
df_gdp = pd.read_csv('datasets/16.0 National Accounts/16.1.csv')
print(df_gdp.head())
```

### 3. Re-generating Analysis Visualizations
To re-run the analysis and re-generate all 7 figures in `figures/`:
```bash
python scripts/generate_eda_visualizations.py
```

---

## 📈 Visual Gallery

| Catalog Distribution | Island Population Density |
| :---: | :---: |
| ![Catalog](figures/fig1_catalog_breakdown.png) | ![Geography](figures/fig2_geographic_concentration.png) |

| Tourism COVID Shock & Rebound | Real GDP Trajectory (2003-2020) |
| :---: | :---: |
| ![Tourism](figures/fig3_tourism_shock_2020.png) | ![GDP](figures/fig4_gdp_structural_shock.png) |

| Fisheries Production & Exports | Emergency Island Freshwater Logistics |
| :---: | :---: |
| ![Fisheries](figures/fig6_fisheries_production_utilization.png) | ![Water](figures/fig7_emergency_water_vulnerability.png) |

---

## 📜 Citation & Attribution
- **Data Source**: National Bureau of Statistics (NBS), Ministry of National Planning, Housing and Infrastructure, Republic of Maldives.
- **Publication**: *Statistical Yearbook of Maldives 2021*.
- **Licensing**: Data is published under open statistical access terms by the NBS.
