"""
generate_eda_visualizations.py
Generates clean publication-grade EDA visualizations and statistical summaries
from the Maldives Statistical Year Book 2021 clean datasets.
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# Set visual style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = 'Helvetica, Arial, DejaVu Sans, sans-serif'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#EEEEEE'
plt.rcParams['grid.linestyle'] = '--'

OUTPUT_DIR = "figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. CATALOG ARCHITECTURE & DOMAIN BREAKDOWN
# -------------------------------------------------------------
def plot_catalog_breakdown():
    print("Generating Figure 1: Catalog Architecture...")
    with open('datasets/catalog.json', 'r') as f:
        catalog = json.load(f)
    
    chapter_counts = {}
    for item in catalog:
        ch = item.get('chapter', 'Unknown')
        chapter_counts[ch] = chapter_counts.get(ch, 0) + 1
        
    df = pd.DataFrame(list(chapter_counts.items()), columns=['Chapter', 'Tables'])
    # Extract chapter number and name
    df['Num'] = df['Chapter'].apply(lambda x: float(x.split(' ')[0]))
    df = df.sort_values(by='Num', ascending=True).reset_index(drop=True)
    
    # Categorize into broader domains
    domain_map = {
        '1.0 Geography': 'Environment & Geography',
        '2.0 Environment': 'Environment & Geography',
        '3.0 population': 'Social & Demographics',
        '4.0 Housing and public infrastructure': 'Infrastructure & Utilities',
        '5.0 Employment': 'Productive Sectors',
        '6.0 Health': 'Social & Demographics',
        '7.0 Education': 'Social & Demographics',
        '8.0 Law & Order': 'Social & Demographics',
        '9.0 Fisheries & Agriculture': 'Productive Sectors',
        '10.0 Tourism': 'Macro & External Economy',
        '11.0 Transport and Communication': 'Infrastructure & Utilities',
        '12.0 Electricity and water': 'Infrastructure & Utilities',
        '13.0 Public Finance': 'Macro & External Economy',
        '14.0 Money and banking': 'Macro & External Economy',
        '15.0 Foreign trade & Balance of payments': 'Macro & External Economy',
        '16.0 National Accounts': 'Macro & External Economy',
        '17.0 Prices': 'Macro & External Economy',
        '18.0 Pension & social protection': 'Social & Demographics',
        '19.0 Human rights': 'Social & Demographics',
        '20.0 Political parties & Election': 'Social & Demographics'
    }
    df['Domain'] = df['Chapter'].map(domain_map)
    
    palette = {
        'Macro & External Economy': '#1f77b4',
        'Social & Demographics': '#2ca02c',
        'Productive Sectors': '#ff7f0e',
        'Infrastructure & Utilities': '#9467bd',
        'Environment & Geography': '#17becf'
    }
    
    fig, ax = plt.subplots(figsize=(12, 8), dpi=200)
    
    bars = ax.barh(df['Chapter'], df['Tables'], color=[palette[d] for d in df['Domain']], edgecolor='none', height=0.7)
    
    # Annotate bar values
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.5, bar.get_y() + bar.get_height()/2, f"{int(w)}",
                ha='left', va='center', fontsize=9, fontweight='bold', color='#333333')
                
    ax.set_title("Maldives Statistical Yearbook 2021: Dataset Distribution (303 Tables)",
                 fontsize=14, fontweight='bold', pad=15, color='#111111')
    ax.set_xlabel("Number of Structured Datasets (Tables)", fontsize=11, labelpad=10)
    ax.set_xlim(0, 45)
    ax.invert_yaxis()  # Highest chapter number at bottom
    
    # Custom legend
    handles = [plt.Rectangle((0,0),1,1, color=color) for color in palette.values()]
    ax.legend(handles, palette.keys(), title="Socio-Economic Domain", loc='lower right', frameon=True, framealpha=0.9)
    
    plt.tight_layout()
    fig_path = os.path.join(OUTPUT_DIR, "fig1_catalog_breakdown.png")
    plt.savefig(fig_path)
    plt.close()
    print(f"Saved: {fig_path}")

# -------------------------------------------------------------
# 2. GEOGRAPHIC CONCENTRATION & DENSITY
# -------------------------------------------------------------
def plot_geographic_concentration():
    print("Generating Figure 2: Geographic & Urban Concentration...")
    df_geo = pd.read_csv('datasets/1.0 Geography/1.5.csv')
    valid = df_geo.dropna(subset=['Locality', 'Population (census 2014) - Resident Population']).copy()
    valid['Locality'] = valid['Locality'].str.replace('*', '').str.strip()
    valid = valid.sort_values(by='Population (census 2014) - Resident Population', ascending=False).reset_index(drop=True)
    
    total_pop = valid['Population (census 2014) - Resident Population'].sum()
    top10 = valid.head(10).copy()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), dpi=200)
    
    # 1. Top 10 Populated Islands
    colors = ['#d62728' if loc == "Male'" else '#1f77b4' for loc in top10['Locality']]
    bars = ax1.barh(top10['Locality'], top10['Population (census 2014) - Resident Population'], color=colors, height=0.65)
    for bar in bars:
        w = bar.get_width()
        pct = (w / total_pop) * 100
        ax1.text(w + 1500, bar.get_y() + bar.get_height()/2, f"{int(w):,} ({pct:.1f}%)",
                 ha='left', va='center', fontsize=9, fontweight='semibold', color='#333333')
                 
    ax1.set_title("Top 10 Populated Islands (Census 2014)\nHighlighting Capital Primacy of Malé City",
                  fontsize=12, fontweight='bold', pad=12)
    ax1.set_xlabel("Resident Population", fontsize=10)
    ax1.set_xlim(0, 180000)
    ax1.invert_yaxis()
    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x/1000)}k" if x > 0 else "0"))
    
    # 2. Extreme Density Disparity (Log scale)
    valid['Density_km2'] = valid['Population Density (population per hectar) - Resident Population'] * 100
    top_dens = valid.sort_values(by='Density_km2', ascending=False).head(10).copy()
    
    dens_colors = ['#d62728' if loc in ["Male'", "Villingili"] else '#2ca02c' for loc in top_dens['Locality']]
    bars2 = ax2.barh(top_dens['Locality'], top_dens['Density_km2'], color=dens_colors, height=0.65)
    for bar in bars2:
        w = bar.get_width()
        ax2.text(w * 1.08, bar.get_y() + bar.get_height()/2, f"{int(w):,} /km²",
                 ha='left', va='center', fontsize=9, fontweight='semibold', color='#333333')
                 
    ax2.set_xscale('log')
    ax2.set_title("Island Population Density (Persons per km²)\nMalé City (74,879/km²) vs Outer Atoll Localities",
                  fontsize=12, fontweight='bold', pad=12)
    ax2.set_xlabel("Population Density per km² (Logarithmic Scale)", fontsize=10)
    ax2.set_xlim(100, 200000)
    ax2.invert_yaxis()
    
    plt.tight_layout()
    fig_path = os.path.join(OUTPUT_DIR, "fig2_geographic_concentration.png")
    plt.savefig(fig_path)
    plt.close()
    print(f"Saved: {fig_path}")

# -------------------------------------------------------------
# 3. TOURISM DYNAMICS & THE 2020 COVID SHOCK
# -------------------------------------------------------------
def plot_tourism_dynamics():
    print("Generating Figure 3: Tourism Collapse & Structural Market Shift...")
    # 1. Total arrivals 2012-2020
    df_tour = pd.read_csv('datasets/10.0 Tourism/10.1.csv')
    tot_row = df_tour[df_tour['Country of Nationality'].str.strip() == 'Total'].iloc[0]
    
    years = ['2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']
    cols = ['2012', '2013', '2014', '2015', 'No. of Tourists - 2016', 'No. of Tourists - 2017',
            'No. of Tourists - 2018', 'No. of Tourists - 2019', 'No. of Tourists - 2020']
    arrivals = [float(tot_row[c]) for c in cols]
    
    # 2. 2020 Monthly profile
    df_monthly = pd.read_csv('datasets/10.0 Tourism/10.11.csv')
    m_tot = df_monthly[df_monthly['Country of Nationality'].str.strip() == 'Total'].iloc[0]
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_vals = [float(m_tot[m]) for m in months]
    
    # 3. Market share shifts (2019 vs 2020)
    countries = ['India', 'Russia', 'United Kingdom', 'Italy', 'Germany', 'China', 'France', 'U.S.A']
    c_2019, c_2020 = [], []
    for c in countries:
        r = df_tour[df_tour['Country of Nationality'].str.strip() == c].iloc[0]
        c_2019.append(float(r['No. of Tourists - 2019']))
        c_2020.append(float(r['No. of Tourists - 2020']))
        
    fig = plt.figure(figsize=(15, 10), dpi=200)
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.1])
    
    # Plot 1: Annual arrivals
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(years, [a/1000 for a in arrivals], marker='o', linewidth=2.5, color='#1f77b4', markersize=7)
    ax1.fill_between(years, [a/1000 for a in arrivals], color='#1f77b4', alpha=0.15)
    
    # Annotate peak and trough
    ax1.annotate('Peak: 1,702,887\n(+14.7% YoY)', xy=('2019', 1702.887), xytext=('2018', 1750),
                 arrowprops=dict(arrowstyle='->', color='#333333', lw=1.2), fontweight='bold')
    ax1.annotate('COVID Collapse: 555,494\n(-67.4% YoY)', xy=('2020', 555.494), xytext=('2019', 800),
                 arrowprops=dict(arrowstyle='->', color='#d62728', lw=1.2), color='#d62728', fontweight='bold')
                 
    ax1.set_title("Annual Tourist Arrivals to the Maldives (2012 - 2020): Decade Expansion vs Pandemic Contraction",
                  fontsize=13, fontweight='bold', pad=12)
    ax1.set_ylabel("Arrivals ('000 Tourists)", fontsize=10)
    ax1.set_ylim(0, 2000)
    
    # Plot 2: 2020 Monthly Dynamics
    ax2 = fig.add_subplot(gs[1, 0])
    bar_colors = ['#1f77b4' if v > 50000 else '#d62728' if v < 5000 else '#ff7f0e' for v in monthly_vals]
    ax2.bar(months, [v/1000 for v in monthly_vals], color=bar_colors, edgecolor='none', width=0.65)
    ax2.set_title("2020 Monthly Tourist Arrivals:\nBorder Lockdown (Apr-Jun) & High-End Winter Rebound",
                  fontsize=11, fontweight='bold', pad=10)
    ax2.set_ylabel("Monthly Arrivals ('000)", fontsize=10)
    ax2.text(3.5, 50, "Border Closed\n27 Mar - 15 Jul", ha='center', color='#d62728', fontsize=9, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#ffebee', edgecolor='#d62728', lw=0.8))
             
    # Plot 3: Market Shift (Grouped Horizontal Bar)
    ax3 = fig.add_subplot(gs[1, 1])
    y = np.arange(len(countries))
    h = 0.35
    ax3.barh(y - h/2, [v/1000 for v in c_2019], height=h, label='2019', color='#aec7e8')
    ax3.barh(y + h/2, [v/1000 for v in c_2020], height=h, label='2020', color='#1f77b4')
    ax3.set_yticks(y)
    ax3.set_yticklabels(countries, fontsize=9)
    ax3.invert_yaxis()
    ax3.set_title("Top Source Markets: 2019 vs 2020\nRise of India & Russia as China Plunges",
                  fontsize=11, fontweight='bold', pad=10)
    ax3.set_xlabel("Tourists ('000)", fontsize=10)
    ax3.legend(loc='lower right', frameon=True)
    
    plt.tight_layout()
    fig_path = os.path.join(OUTPUT_DIR, "fig3_tourism_shock_2020.png")
    plt.savefig(fig_path)
    plt.close()
    print(f"Saved: {fig_path}")

# -------------------------------------------------------------
# 4. REAL GDP & SECTORAL MACROECONOMIC IMPACT
# -------------------------------------------------------------
def plot_macro_gdp():
    print("Generating Figure 4: Macroeconomic Real GDP Trajectory...")
    df_gdp = pd.read_csv('datasets/16.0 National Accounts/16.1.csv')
    act_col = df_gdp.columns[1]
    
    # Total GDP row
    tot_row = df_gdp.iloc[0]
    gdp_cols = [c for c in df_gdp.columns if 'Industry / Economic Activity - 20' in c]
    years = [int(c.split(' - ')[-1].split(' ')[0]) for c in gdp_cols]
    gdp_vals = [float(tot_row[c]) / 1000 for c in gdp_cols]  # In Billion MVR
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 9), dpi=200, gridspec_kw={'height_ratios': [1.2, 1]})
    
    # 1. Long-term Real GDP (2003-2020)
    ax1.plot(years, gdp_vals, marker='s', color='#2ca02c', linewidth=2.5, markersize=6)
    ax1.fill_between(years, gdp_vals, color='#2ca02c', alpha=0.12)
    
    # Annotate crises
    ax1.annotate('2004 Tsunami\n(-13.1% in 2005)', xy=(2005, 29.98), xytext=(2003.5, 24),
                 arrowprops=dict(arrowstyle='->', color='#d62728'), color='#d62728', fontweight='bold', fontsize=9)
    ax1.annotate('2008 Global Financial Crisis\n(-7.2% in 2009)', xy=(2009, 41.36), xytext=(2007.5, 33),
                 arrowprops=dict(arrowstyle='->', color='#ff7f0e'), color='#ff7f0e', fontweight='bold', fontsize=9)
    ax1.annotate('COVID-19 Pandemic\n-33.5% in 2020\n(77.1B -> 51.3B MVR)', xy=(2020, 51.26), xytext=(2017, 44),
                 arrowprops=dict(arrowstyle='->', color='#d62728', lw=1.5), color='#d62728', fontweight='bold', fontsize=10)
                 
    ax1.set_title("Maldives Real Gross Domestic Product at 2014 Constant Prices (2003 - 2020)",
                  fontsize=13, fontweight='bold', pad=12)
    ax1.set_ylabel("Real GDP (Billion MVR)", fontsize=10)
    ax1.set_ylim(20, 85)
    ax1.set_xticks(years)
    ax1.set_xticklabels(years, rotation=45)
    
    # 2. Sectoral YoY Contraction / Growth in 2020
    key_sectors = [
        ('Tourism', 16),
        ('Transportation & Comm.', 20),
        ('Construction', 13),
        ('Wholesale & Retail', 15),
        ('Manufacturing', 7),
        ('Public Administration', 29),
        ('Fisheries', 5),
        ('Financial Services', 24)
    ]
    sector_names = []
    pct_changes = []
    for name, idx in key_sectors:
        row = df_gdp.iloc[idx]
        v19 = float(row.filter(like='2019').values[0])
        v20 = float(row.filter(like='2020').values[0])
        pct = ((v20 - v19) / v19) * 100
        sector_names.append(name)
        pct_changes.append(pct)
        
    bar_colors = ['#2ca02c' if p > 0 else '#d62728' for p in pct_changes]
    bars = ax2.barh(sector_names, pct_changes, color=bar_colors, height=0.6)
    for bar in bars:
        w = bar.get_width()
        x_pos = w + (1.5 if w > 0 else -1.5)
        align = 'left' if w > 0 else 'right'
        ax2.text(x_pos, bar.get_y() + bar.get_height()/2, f"{w:+.1f}%",
                 ha=align, va='center', fontsize=9, fontweight='bold', color='#222222')
                 
    ax2.axvline(0, color='#333333', linewidth=1, linestyle='--')
    ax2.set_title("2020 Economic Sector Performance (% Change Year-over-Year)\nService Sector Plunge vs Resilient Marine & Financial Stabilizers",
                  fontsize=11, fontweight='bold', pad=10)
    ax2.set_xlabel("YoY Growth Rate (%)", fontsize=10)
    ax2.set_xlim(-75, 20)
    ax2.invert_yaxis()
    
    plt.tight_layout()
    fig_path = os.path.join(OUTPUT_DIR, "fig4_gdp_structural_shock.png")
    plt.savefig(fig_path)
    plt.close()
    print(f"Saved: {fig_path}")

# -------------------------------------------------------------
# 5. PUBLIC FINANCE & FISCAL DEFICIT
# -------------------------------------------------------------
def plot_public_finance():
    print("Generating Figure 5: Public Finance Deficit & Tourism Revenue Share...")
    df_pf = pd.read_csv('datasets/13.0 Public Finance/13.2.csv')
    
    years = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
    rev_row = df_pf.iloc[0]  # Total Revenue and grants
    exp_row = df_pf.iloc[6]  # Total Expenditure
    bal_row = df_pf.iloc[10] # Overall Balance
    
    rev_vals = [float(rev_row.iloc[i+4]) / 1000 for i in range(len(years))]
    exp_vals = [float(exp_row.iloc[i+4]) / 1000 for i in range(len(years))]
    bal_vals = [float(bal_row.iloc[i+4]) / 1000 for i in range(len(years))]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), dpi=200)
    
    # 1. Revenue vs Expenditure
    ax1.plot(years, rev_vals, marker='o', label='Total Revenue & Grants', color='#1f77b4', lw=2.2)
    ax1.plot(years, exp_vals, marker='s', label='Total Government Expenditure', color='#d62728', lw=2.2)
    ax1.fill_between(years, rev_vals, exp_vals, where=np.array(exp_vals)>=np.array(rev_vals),
                     color='#d62728', alpha=0.15, label='Fiscal Deficit')
    ax1.set_title("Central Government Revenue vs Expenditure (2012 - 2020)", fontsize=12, fontweight='bold', pad=12)
    ax1.set_ylabel("Billion MVR", fontsize=10)
    ax1.set_xlabel("Year", fontsize=10)
    ax1.legend(loc='upper left', frameon=True)
    
    # 2. Fiscal Balance Expansion
    bar_cols = ['#d62728' for _ in bal_vals]
    bars = ax2.bar(years, bal_vals, color=bar_cols, width=0.6)
    for bar in bars:
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, h - 0.35, f"{h:.1f}B",
                 ha='center', va='top', fontsize=8.5, fontweight='bold', color='#333333')
    ax2.axhline(0, color='#333333', lw=1)
    ax2.set_title("Government Fiscal Deficit (Overall Balance in Billion MVR)\nWidening Structural Deficit to -5.8 Billion MVR in 2020",
                  fontsize=12, fontweight='bold', pad=12)
    ax2.set_ylabel("Overall Balance (Billion MVR)", fontsize=10)
    ax2.set_ylim(-7.5, 1)
    
    plt.tight_layout()
    fig_path = os.path.join(OUTPUT_DIR, "fig5_public_finance_deficit.png")
    plt.savefig(fig_path)
    plt.close()
    print(f"Saved: {fig_path}")

# -------------------------------------------------------------
# 6. FISHERIES: SPECIES CATCH & EXPORT UTILIZATION
# -------------------------------------------------------------
def plot_fisheries():
    print("Generating Figure 6: Fisheries Catch & Utilization...")
    df_f = pd.read_csv('datasets/9.0 Fisheries & Agriculture/9.6.csv')
    df_u = pd.read_csv('datasets/9.0 Fisheries & Agriculture/9.1.csv')
    
    years = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
    skipjack = [float(df_f.iloc[1][str(y)]) / 1000 for y in years]
    yellowfin = [float(df_f.iloc[2][str(y)]) / 1000 for y in years]
    others = [(float(df_f.iloc[0][str(y)]) - float(df_f.iloc[1][str(y)]) - float(df_f.iloc[2][str(y)])) / 1000 for y in years]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), dpi=200)
    
    # 1. Stacked fish catch
    ax1.bar(years, skipjack, label='Skipjack Tuna (Katsuwonus pelamis)', color='#1f77b4', width=0.6)
    ax1.bar(years, yellowfin, bottom=skipjack, label='Yellowfin Tuna (Thunnus albacares)', color='#ff7f0e', width=0.6)
    ax1.bar(years, others, bottom=np.array(skipjack) + np.array(yellowfin), label='Other Marine Species', color='#2ca02c', width=0.6)
    
    # Annotate total catch in 2020
    tot_2020 = skipjack[-1] + yellowfin[-1] + others[-1]
    ax1.text(2020, tot_2020 + 3, f"Total:\n{tot_2020:.1f}k MT", ha='center', fontweight='bold', fontsize=9, color='#111111')
    
    ax1.set_title("Annual Fish Catch by Major Species (2013 - 2020)\nRecord Catch in 2020 Driven by Skipjack Surge",
                  fontsize=12, fontweight='bold', pad=12)
    ax1.set_ylabel("Catch ('000 Metric Tons)", fontsize=10)
    ax1.set_ylim(0, 170)
    ax1.legend(loc='upper left', frameon=True)
    
    # 2. Utilization: Export vs Domestic
    u_years = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
    exp_share = [float(df_u.iloc[0][f"(In '000 metric tons) - Percentage share - {y}"]) for y in u_years]
    loc_share = [float(df_u.iloc[1][f"(In '000 metric tons) - Percentage share - {y}"]) for y in u_years]
    
    ax2.plot(u_years, exp_share, marker='o', label='Export Share (%)', color='#1f77b4', lw=2.2)
    ax2.plot(u_years, loc_share, marker='s', label='Local Consumption Share (%)', color='#2ca02c', lw=2.2)
    ax2.set_title("Fish Catch Utilization: Export Orientation (2011 - 2020)\n>70% Consistently Directed to Global Export Markets",
                  fontsize=12, fontweight='bold', pad=12)
    ax2.set_ylabel("Share of Total Catch (%)", fontsize=10)
    ax2.set_ylim(10, 90)
    ax2.legend(loc='center right', frameon=True)
    
    plt.tight_layout()
    fig_path = os.path.join(OUTPUT_DIR, "fig6_fisheries_production_utilization.png")
    plt.savefig(fig_path)
    plt.close()
    print(f"Saved: {fig_path}")

# -------------------------------------------------------------
# 7. CRITICAL INFRASTRUCTURE: EMERGENCY WATER VULNERABILITY
# -------------------------------------------------------------
def plot_water_vulnerability():
    print("Generating Figure 7: Emergency Freshwater Supply Vulnerability...")
    df_w = pd.read_csv('datasets/12.0 Electricity and water/12.15.csv')
    df_w = df_w.dropna(subset=['Number of islands', 'Expenses on average for ton (MVR)']).copy()
    df_w['Year'] = df_w['Column_A'].astype(int)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), dpi=200)
    
    # 1. Islands supplied
    bars = ax1.bar(df_w['Year'], df_w['Number of islands'], color='#17becf', edgecolor='none', width=0.65)
    for bar in bars:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h + 1.5, f"{int(h)}",
                 ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#333333')
    ax1.set_title("Islands Requiring Emergency Freshwater Supply (2005 - 2020)\nAcute Dry Season Water Stress across 70 - 90 Inhabited Islands",
                  fontsize=12, fontweight='bold', pad=12)
    ax1.set_ylabel("Number of Affected Islands", fontsize=10)
    ax1.set_ylim(0, 110)
    
    # 2. Cost per ton escalation
    ax2.plot(df_w['Year'], df_w['Expenses on average for ton (MVR)'], marker='o', color='#e377c2', lw=2.2)
    ax2.fill_between(df_w['Year'], df_w['Expenses on average for ton (MVR)'], color='#e377c2', alpha=0.15)
    
    ax2.annotate('Escalation: 750 MVR -> 2,841 MVR/ton\nDriven by Sea-Freight Logistics',
                 xy=(2019, 2841), xytext=(2011, 2600),
                 arrowprops=dict(arrowstyle='->', color='#333333', lw=1.2), fontweight='bold', fontsize=9.5)
                 
    ax2.set_title("Average Cost of Emergency Water Delivery (MVR per Ton)\nLogistical Challenges of Maritime Archipelago Transport",
                  fontsize=12, fontweight='bold', pad=12)
    ax2.set_ylabel("Cost per Ton (MVR)", fontsize=10)
    ax2.set_ylim(0, 3500)
    
    plt.tight_layout()
    fig_path = os.path.join(OUTPUT_DIR, "fig7_emergency_water_vulnerability.png")
    plt.savefig(fig_path)
    plt.close()
    print(f"Saved: {fig_path}")

if __name__ == '__main__':
    print("Starting EDA Visualizations generation...")
    plot_catalog_breakdown()
    plot_geographic_concentration()
    plot_tourism_dynamics()
    plot_macro_gdp()
    plot_public_finance()
    plot_fisheries()
    plot_water_vulnerability()
    print("All 7 visualizations generated successfully!")
