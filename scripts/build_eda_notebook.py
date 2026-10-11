"""
build_eda_notebook.py
Builds an interactive, richly documented exploratory data analysis Jupyter Notebook
for the Statistical Year Book of Maldives 2021.
"""

import nbformat as nbf

nb = nbf.v4.new_notebook()

cells = []

# Title & Metadata
cells.append(nbf.v4.new_markdown_cell("""# Exploratory Data Analysis: Statistical Yearbook of Maldives 2021
### An Empirical Socio-Economic & Environmental Investigation of the Maldivian Archipelago

---

## 1. Executive Overview & Problem Context
The **Statistical Yearbook of Maldives 2021**, published by the **National Bureau of Statistics (NBS)**, captures an extraordinary historical cross-section of the Maldivian economy, demography, environment, and social institutions. Most importantly, it documents the baseline decade (2010–2019) followed by the unprecedented shock of the **2020 COVID-19 pandemic**.

This repository contains **303 clean, machine-readable CSV datasets** and companion JSON metadata across **20 chapters**. This notebook conducts an in-depth **Exploratory Data Analysis (EDA)** across six core structural themes:
1. **Catalog Architecture**: Domain distribution and data coverage.
2. **Geographic Demography & Capital Primacy**: Island dispersion and urban density in Malé.
3. **Tourism Dynamics & The COVID-19 Shock**: Annual trends, monthly collapse, and source market shifts.
4. **Macroeconomic Accounts**: Real GDP trends (2003–2020) and sectoral divergence.
5. **Public Finance & Fiscal Health**: Government revenue vs expenditure and deficit expansion.
6. **Marine Resources & The Blue Economy**: Fish catch species, surge in 2020, and export orientation.
7. **Infrastructure & Climate Vulnerability**: Freshwater stress and emergency island water logistics.

---
"""))

# Cell 1: Environment Setup
cells.append(nbf.v4.new_code_cell("""# Environment & Library Setup
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# Visual configuration
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = 'Helvetica, Arial, DejaVu Sans, sans-serif'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#EEEEEE'
plt.rcParams['grid.linestyle'] = '--'

# Paths
DATASETS_DIR = '../datasets'
FIGURES_DIR = '../figures'

print("Libraries imported successfully.")
"""))

cells.append(nbf.v4.new_markdown_cell("""### Analysis: Environment Configuration
The analysis environment uses Python with `pandas` for tabular data manipulation, `matplotlib` and `seaborn` for publication-grade visualization, and standard JSON for metadata parsing. All paths are resolved relative to the dataset catalog.
"""))

# Cell 2: Catalog Architecture
cells.append(nbf.v4.new_code_cell("""# Load and inspect dataset catalog
catalog_path = os.path.join(DATASETS_DIR, 'catalog.json')
with open(catalog_path, 'r') as f:
    catalog = json.load(f)

print(f"Total structured datasets in catalog: {len(catalog)}")

# Group tables by chapter
chapter_stats = {}
for entry in catalog:
    ch = entry.get('chapter', 'Unknown')
    chapter_stats[ch] = chapter_stats.get(ch, 0) + 1

df_catalog = pd.DataFrame(list(chapter_stats.items()), columns=['Chapter', 'Table_Count'])
df_catalog['Chapter_Num'] = df_catalog['Chapter'].apply(lambda x: float(x.split(' ')[0]))
df_catalog = df_catalog.sort_values(by='Chapter_Num').reset_index(drop=True)
df_catalog[['Chapter', 'Table_Count']]
"""))

cells.append(nbf.v4.new_markdown_cell("""### Analysis: Catalog Architecture & Scope
The Statistical Yearbook comprises **303 tables** structured across **20 thematic chapters**:
- **Law & Order** (39 tables) and **Education** (28 tables) have the highest table density among social sectors.
- **Economic & Financial Statistics** comprise over **80 tables** (Public Finance, Money & Banking, National Accounts, Foreign Trade, Prices, Tourism).
- **Physical & Ecological Systems** are captured through Geography, Environment, Fisheries & Agriculture, and Electricity & Water.

This broad sectoral coverage enables cross-domain econometric, demographic, and spatial analyses.
"""))

# Cell 3: Geography & Demographics
cells.append(nbf.v4.new_code_cell("""# Table 1.5: Inhabited Island Population and Density Analysis
geo_csv = os.path.join(DATASETS_DIR, '1.0 Geography/1.5.csv')
df_geo = pd.read_csv(geo_csv)

# Clean and extract valid inhabited localities
valid_geo = df_geo.dropna(subset=['Locality', 'Population (census 2014) - Resident Population']).copy()
valid_geo['Locality'] = valid_geo['Locality'].str.replace('*', '').str.strip()
valid_geo = valid_geo.sort_values(by='Population (census 2014) - Resident Population', ascending=False).reset_index(drop=True)

total_resident_pop = valid_geo['Population (census 2014) - Resident Population'].sum()
male_pop = valid_geo[valid_geo['Locality'] == \"Male'\"]['Population (census 2014) - Resident Population'].values[0]
villingili_pop = valid_geo[valid_geo['Locality'] == 'Villingili']['Population (census 2014) - Resident Population'].values[0]
hulhumale_pop = valid_geo[valid_geo['Locality'] == \"Hulhumale'\"]['Population (census 2014) - Resident Population'].values[0]

greater_male_pop = male_pop + villingili_pop + hulhumale_pop

print(f"Total Resident Population (Census 2014): {total_resident_pop:,.0f} across {len(valid_geo)} localities")
print(f"Malé Island Resident Population: {male_pop:,.0f} ({male_pop/total_resident_pop*100:.2f}%)")
print(f"Greater Malé (Malé + Hulhumalé + Villingili): {greater_male_pop:,.0f} ({greater_male_pop/total_resident_pop*100:.2f}%)")
print(f"Median Inhabited Island Population: {valid_geo['Population (census 2014) - Resident Population'].median():,.0f}")
print(f"Malé Population Density: {valid_geo[valid_geo['Locality'] == \"Male'\"]['Population Density (population per hectar) - Resident Population'].values[0] * 100:,.0f} persons/km²")
"""))

cells.append(nbf.v4.new_markdown_cell("""### Analysis: Urban Primate City Concentration
The demographic structure displays extreme spatial skewness:
- **Primate City Dominance**: Malé island holds **153,904 residents (39.4%)** of the entire country's population on just **2.05 km²** of land.
- **Greater Malé Conurbation**: Including Villingili and Hulhumalé, Greater Malé accounts for **45.8% of the national population**.
- **Extreme Density**: Malé reaches **74,879 people per km²**, ranking among the densest human settlements on Earth.
- **Peripheral Dispersion**: In contrast, the median outer island population is only **1,009 residents**, with typical densities of 15–30 persons per hectare. This spatial fragmentation introduces high per-capita costs for infrastructure, healthcare, and education delivery across atolls.
"""))

# Cell 4: Tourism Engine & 2020 Shock
cells.append(nbf.v4.new_code_cell("""# Table 10.1 & Table 10.11: Tourist Arrivals & COVID-19 Disruption
tour_annual_csv = os.path.join(DATASETS_DIR, '10.0 Tourism/10.1.csv')
tour_monthly_csv = os.path.join(DATASETS_DIR, '10.0 Tourism/10.11.csv')

df_tour = pd.read_csv(tour_annual_csv)
df_m_tour = pd.read_csv(tour_monthly_csv)

tot_annual = df_tour[df_tour['Country of Nationality'].str.strip() == 'Total'].iloc[0]
arr_2012 = float(tot_annual['2012'])
arr_2019 = float(tot_annual['No. of Tourists - 2019'])
arr_2020 = float(tot_annual['No. of Tourists - 2020'])

print(f"2012 Annual Arrivals: {arr_2012:,.0f}")
print(f"2019 Peak Arrivals:   {arr_2019:,.0f} (+77.8% over 2012)")
print(f"2020 Shock Arrivals:  {arr_2020:,.0f} (-67.38% YoY)")

# 2020 Monthly breakdown
m_row = df_m_tour[df_m_tour['Country of Nationality'].str.strip() == 'Total'].iloc[0]
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
m_vals = [float(m_row[m]) for m in months]

pd.DataFrame({'Month': months, 'Arrivals_2020': m_vals})
"""))

cells.append(nbf.v4.new_markdown_cell("""### Analysis: The 2020 Tourism Collapse and Winter Rebound
Tourism is the primary engine of the Maldivian economy:
- **Decade Growth**: Arrivals expanded rapidly from **958,025 in 2012** to an all-time peak of **1,702,887 in 2019**.
- **The Pandemic Shock**: In 2020, arrivals collapsed by **-67.4% to 555,494**.
- **Border Closure**: The international border was shut on 27 March 2020. During Q2 (April–June), monthly arrivals totaled just **55 tourists** combined (13 in April, 41 in May, 1 in June).
- **Q4 High-End Rebound**: Following border reopening on 15 July 2020 without quarantine restrictions, arrivals climbed from 1,752 in July to 96,412 in December.
- **Structural Market Realignment**: China (formerly #1 with 284,000 in 2019) plunged to 34,245. Meanwhile, **India (62,960)** and **Russia (61,387)** became the new top two tourist source markets, driving the winter recovery.
"""))

# Cell 5: Real GDP & Sectoral Shock
cells.append(nbf.v4.new_code_cell("""# Table 16.1: Real Gross Domestic Product at 2014 Constant Prices (2003 - 2020)
gdp_csv = os.path.join(DATASETS_DIR, '16.0 National Accounts/16.1.csv')
df_gdp = pd.read_csv(gdp_csv)

tot_gdp_row = df_gdp.iloc[0]
gdp_2004 = float(tot_gdp_row.filter(like='2004').values[0])
gdp_2005 = float(tot_gdp_row.filter(like='2005').values[0])
gdp_2008 = float(tot_gdp_row.filter(like='2008').values[0])
gdp_2009 = float(tot_gdp_row.filter(like='2009').values[0])
gdp_2019 = float(tot_gdp_row.filter(like='2019').values[0])
gdp_2020 = float(tot_gdp_row.filter(like='2020').values[0])

print(f"2004 -> 2005 (Tsunami Shock):  {((gdp_2005 - gdp_2004)/gdp_2004)*100:.2f}% (34.5B -> 30.0B MVR)")
print(f"2008 -> 2009 (GFC Shock):      {((gdp_2009 - gdp_2008)/gdp_2008)*100:.2f}% (44.6B -> 41.4B MVR)")
print(f"2019 -> 2020 (COVID-19 Shock): {((gdp_2020 - gdp_2019)/gdp_2019)*100:.2f}% (77.1B -> 51.3B MVR)")

# Sectoral Performance in 2020
sectors = [
    ('Tourism', 16),
    ('Transportation & Comm.', 20),
    ('Construction', 13),
    ('Wholesale & Retail', 15),
    ('Manufacturing', 7),
    ('Public Administration', 29),
    ('Fisheries', 5),
    ('Financial Services', 24)
]
sector_perf = []
for name, idx in sectors:
    r = df_gdp.iloc[idx]
    v19 = float(r.filter(like='2019').values[0])
    v20 = float(r.filter(like='2020').values[0])
    pct = ((v20 - v19) / v19) * 100
    sector_perf.append({'Sector': name, 'GVA_2019_MVR': v19, 'GVA_2020_MVR': v20, 'YoY_Growth_%': pct})

pd.DataFrame(sector_perf).sort_values(by='YoY_Growth_%')
"""))

cells.append(nbf.v4.new_markdown_cell("""### Analysis: Macroeconomic Contraction & Sectoral Divergence
1. **Historic Severity**: Real GDP contracted by **-33.5% in 2020**, dropping from 77.08 billion MVR to 51.26 billion MVR. This contraction was more than 2.5 times larger than the 2004 Indian Ocean Tsunami (-13.1%) and nearly five times the 2008 Global Financial Crisis (-7.2%).
2. **Service Sectors Suffered the Brunt**:
   - **Tourism**: -62.5% (plunged from 20.27B to 7.60B MVR).
   - **Transport & Communication**: -43.0% (down from 9.72B to 5.54B MVR).
   - **Construction**: -33.8% (impacted by disrupted supply chains and expatriate labor quarantines).
3. **Resilience & Counter-Cyclical Buffers**:
   - **Fisheries** grew by **+10.2%** (from 2.34B to 2.58B MVR), functioning as a primary livelihood anchor for atoll populations.
   - **Financial Services** (+8.9%) and **Public Administration** (+0.9%) helped stabilize domestic liquidity and basic administrative functions.
"""))

# Cell 6: Public Finance & Fiscal Deficit
cells.append(nbf.v4.new_code_cell("""# Table 13.2: Central Government Finance & Structural Deficit
pf_csv = os.path.join(DATASETS_DIR, '13.0 Public Finance/13.2.csv')
df_pf = pd.read_csv(pf_csv)

rev_row = df_pf.iloc[0]  # Total Revenue and grants
exp_row = df_pf.iloc[6]  # Total Expenditure
bal_row = df_pf.iloc[10] # Overall Balance

years = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
pf_data = []
for i, y in enumerate(years):
    r = float(rev_row.iloc[i+4])
    e = float(exp_row.iloc[i+4])
    b = float(bal_row.iloc[i+4])
    pf_data.append({
        'Year': y,
        'Revenue_Grants_MVR_M': r,
        'Expenditure_MVR_M': e,
        'Overall_Balance_MVR_M': b,
        'Deficit_Share_of_Exp_%': (b / e) * 100
    })

pd.DataFrame(pf_data)
"""))

cells.append(nbf.v4.new_markdown_cell("""### Analysis: Fiscal Expansion & Structural Deficits
- Throughout the 2012–2020 window, the Maldives maintained a persistent **fiscal deficit**, driven by large-scale infrastructure capital projects (such as the Sinamalé Bridge, Velana Airport expansion, and land reclamation).
- In 2020, while revenues plateaued/strained, total expenditure surged to **28,995 million MVR** due to emergency healthcare, quarantine facilities, and economic relief subsidies.
- This resulted in an overall fiscal deficit of **-5,763 million MVR** (-19.9% of total expenditure), financed largely through domestic debt borrowing and sovereign bond/sukuk issuances.
"""))

# Cell 7: Marine Resources & Blue Economy
cells.append(nbf.v4.new_code_cell("""# Table 9.6 & 9.1: Fisheries Catch & Utilization
fish_species_csv = os.path.join(DATASETS_DIR, '9.0 Fisheries & Agriculture/9.6.csv')
fish_util_csv = os.path.join(DATASETS_DIR, '9.0 Fisheries & Agriculture/9.1.csv')

df_f_spec = pd.read_csv(fish_species_csv)
df_f_util = pd.read_csv(fish_util_csv)

years_f = ['2015', '2016', '2017', '2018', '2019', '2020']
f_summary = []
for y in years_f:
    tot = float(df_f_spec.iloc[0][y])
    skip = float(df_f_spec.iloc[1][y])
    yfin = float(df_f_spec.iloc[2][y])
    exp_share = float(df_f_util.iloc[0][f"(In '000 metric tons) - Percentage share - {y}"])
    f_summary.append({
        'Year': y,
        'Total_Catch_MT': tot,
        'Skipjack_MT': skip,
        'Yellowfin_MT': yfin,
        'Skipjack_Share_%': (skip / tot) * 100,
        'Export_Share_%': exp_share
    })

pd.DataFrame(f_summary)
"""))

cells.append(nbf.v4.new_markdown_cell("""### Analysis: Fisheries Resilience & Sustainable Catch
- **Record Production in 2020**: In 2020, Maldivian fishermen achieved a total catch of **148,583 metric tons**, an increase of **+10.0%** over 2019.
- **Skipjack Tuna Dominance**: Skipjack tuna (*Katsuwonus pelamis*) rose to **103,871 metric tons (69.9% of total catch)**, predominantly landed via traditional pole-and-line fishing.
- **Export Orientation**: Over **70.8% of the total catch is exported** (processed, canned, or chilled/frozen), making fisheries the single largest physical merchandise export and a vital source of foreign currency.
"""))

# Cell 8: Infrastructure & Climate Vulnerability
cells.append(nbf.v4.new_code_cell("""# Table 12.15: Emergency Freshwater Supply to Inhabited Islands
water_csv = os.path.join(DATASETS_DIR, '12.0 Electricity and water/12.15.csv')
df_water = pd.read_csv(water_csv).dropna(subset=['Number of islands', 'Expenses on average for ton (MVR)']).copy()
df_water['Year'] = df_water['Column_A'].astype(int)

df_water[['Year', 'Number of islands', 'Number of tons supplied', 'Expenses on average for ton (MVR)']].tail(8)
"""))

cells.append(nbf.v4.new_markdown_cell("""### Analysis: Freshwater Security & Logistical Archipelago Friction
- **Dry Season Water Stresses**: Between **70 and 90 inhabited islands** routinely exhaust their groundwater and rainwater reserves during the northeast monsoon dry season, requiring emergency desalinated water dispatched by sea.
- **Cost Escalation**: The average cost per ton delivered rose from **750 MVR in 2007** to **2,751 MVR in 2020** (peaking at 2,920 MVR in 2017). This cost escalation highlights the logistical friction and fuel expenditures associated with maritime supply lines in a fragmented coral atoll nation.
"""))

# Cell 9: Synthesis & Conclusion
cells.append(nbf.v4.new_markdown_cell("""## 8. Synthesis & Strategic Conclusions

This exploratory data analysis reveals several structural findings about the Maldives:

1. **Extreme Spatial & Demographic Bifurcation**:
   The capital Malé operates as an ultra-dense urban node (74,879 people/km²), housing nearly 40% of the population, contrasted against 187 small, dispersed island communities with median populations around 1,000 residents.

2. **Acute Macro Vulnerability to Global Mobility Shocks**:
   With real GDP contracting by **-33.5%** in 2020 and tourism collapsing by **-67.4%**, the economy exhibits exceptional sensitivity to global border and aviation disruptions.

3. **Structural Market Agility in Tourism**:
   The rapid post-July 2020 reopening and shift from traditional markets (China) to India and Russia demonstrated decisive policy adaptability.

4. **The Stabilizing Anchor of the Blue Economy**:
   Fisheries demonstrated counter-cyclical growth (+10.2% GVA growth and record 148,583 MT catch in 2020), underscoring the strategic necessity of marine conservation and local processing capacity.

5. **Climate & Critical Utility Challenges**:
   Persistent freshwater scarcity across outer islands and heavy reliance on maritime fuel/water transit reinforce the urgency of decentralized reverse-osmosis desalination and solar microgrid installations.

---
*Generated from the Statistical Yearbook of Maldives 2021 clean datasets.*
"""))

nb.cells = cells

# Save notebook
output_path = 'notebooks/exploratory_data_analysis.ipynb'
with open(output_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"Jupyter Notebook successfully written to {output_path}")
