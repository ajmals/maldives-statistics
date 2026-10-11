"""
prepare_dashboard_data.py
Extracts and structures data from datasets/ into clean JSON and JS format
for the interactive GitHub Pages dashboard.
"""

import os
import json
import numpy as np
import pandas as pd

def extract_all():
    print("Extracting catalog...")
    with open('datasets/catalog.json', 'r') as f:
        catalog = json.load(f)
        
    # Simplify catalog for client-side search
    compact_catalog = []
    for item in catalog:
        compact_catalog.append({
            'id': item.get('table_id', ''),
            'title': item.get('title_en', ''),
            'title_dv': item.get('title_dv', ''),
            'chapter': item.get('chapter', ''),
            'rows': item.get('row_count', 0),
            'cols': len(item.get('columns', [])),
            'file': item.get('csv_file', '')
        })

    # 1. GEOGRAPHY & POPULATION
    print("Extracting geography & demographics...")
    
    ATOLL_METADATA = {
        'Male': {
            'code': 'Male',
            'atoll_name': "Malé City",
            'geo_name': "Malé City",
            'full_name': "Malé City",
            'short_prefix': ''
        },
        'HA': {
            'code': 'HA',
            'atoll_name': 'Haa Alifu',
            'geo_name': 'North Thiladhunmathi',
            'full_name': 'Haa Alifu (North Thiladhunmathi)',
            'short_prefix': 'HA.'
        },
        'HDh': {
            'code': 'HDh',
            'atoll_name': 'Haa Dhaalu',
            'geo_name': 'South Thiladhunmathi',
            'full_name': 'Haa Dhaalu (South Thiladhunmathi)',
            'short_prefix': 'HDh.'
        },
        'Sh': {
            'code': 'Sh',
            'atoll_name': 'Shaviyani',
            'geo_name': 'North Miladhunmadulu',
            'full_name': 'Shaviyani (North Miladhunmadulu)',
            'short_prefix': 'Sh.'
        },
        'N': {
            'code': 'N',
            'atoll_name': 'Noonu',
            'geo_name': 'South Miladhunmadulu',
            'full_name': 'Noonu (South Miladhunmadulu)',
            'short_prefix': 'N.'
        },
        'R': {
            'code': 'R',
            'atoll_name': 'Raa',
            'geo_name': 'North Maalhosmadulu',
            'full_name': 'Raa (North Maalhosmadulu)',
            'short_prefix': 'R.'
        },
        'B': {
            'code': 'B',
            'atoll_name': 'Baa',
            'geo_name': 'South Maalhosmadulu',
            'full_name': 'Baa (South Maalhosmadulu)',
            'short_prefix': 'B.'
        },
        'Lh': {
            'code': 'Lh',
            'atoll_name': 'Lhaviyani',
            'geo_name': 'Faadhippolhu',
            'full_name': 'Lhaviyani (Faadhippolhu)',
            'short_prefix': 'Lh.'
        },
        'K': {
            'code': 'K',
            'atoll_name': 'Kaafu',
            'geo_name': "Male' Atoll",
            'full_name': "Kaafu (Male' Atoll)",
            'short_prefix': 'K.'
        },
        'AA': {
            'code': 'AA',
            'atoll_name': 'Alif Alif',
            'geo_name': 'North Ari Atoll',
            'full_name': 'Alif Alif (North Ari Atoll)',
            'short_prefix': 'AA.'
        },
        'ADh': {
            'code': 'ADh',
            'atoll_name': 'Alif Dhaal',
            'geo_name': 'South Ari Atoll',
            'full_name': 'Alif Dhaal (South Ari Atoll)',
            'short_prefix': 'ADh.'
        },
        'V': {
            'code': 'V',
            'atoll_name': 'Vaavu',
            'geo_name': 'Felidhu Atoll',
            'full_name': 'Vaavu (Felidhu Atoll)',
            'short_prefix': 'V.'
        },
        'M': {
            'code': 'M',
            'atoll_name': 'Meemu',
            'geo_name': 'Mulakatholhu',
            'full_name': 'Meemu (Mulakatholhu)',
            'short_prefix': 'M.'
        },
        'F': {
            'code': 'F',
            'atoll_name': 'Faafu',
            'geo_name': 'North Nilandhe Atoll',
            'full_name': 'Faafu (North Nilandhe Atoll)',
            'short_prefix': 'F.'
        },
        'Dh': {
            'code': 'Dh',
            'atoll_name': 'Dhaalu',
            'geo_name': 'South Nilandhe Atoll',
            'full_name': 'Dhaalu (South Nilandhe Atoll)',
            'short_prefix': 'Dh.'
        },
        'Th': {
            'code': 'Th',
            'atoll_name': 'Thaa',
            'geo_name': 'Kolhumadulu',
            'full_name': 'Thaa (Kolhumadulu)',
            'short_prefix': 'Th.'
        },
        'L': {
            'code': 'L',
            'atoll_name': 'Laamu',
            'geo_name': 'Hadhdhunmathi',
            'full_name': 'Laamu (Hadhdhunmathi)',
            'short_prefix': 'L.'
        },
        'GA': {
            'code': 'GA',
            'atoll_name': 'Gaafu Alifu',
            'geo_name': 'North Huvadhu Atoll',
            'full_name': 'Gaafu Alifu (North Huvadhu Atoll)',
            'short_prefix': 'GA.'
        },
        'GDh': {
            'code': 'GDh',
            'atoll_name': 'Gaafu Dhaalu',
            'geo_name': 'South Huvadhu Atoll',
            'full_name': 'Gaafu Dhaalu (South Huvadhu Atoll)',
            'short_prefix': 'GDh.'
        },
        'Gn': {
            'code': 'Gn',
            'atoll_name': 'Gnaviyani',
            'geo_name': 'Fuvahmulah',
            'full_name': 'Gnaviyani (Fuvahmulah)',
            'short_prefix': 'Gn.'
        },
        'S': {
            'code': 'S',
            'atoll_name': 'Seenu (Addu City)',
            'geo_name': 'Addu Atoll',
            'full_name': 'Seenu / Addu City (Addu Atoll)',
            'short_prefix': 'S.'
        }
    }

    import re
    df_geo = pd.read_csv('datasets/1.0 Geography/1.5.csv')
    
    def clean_float(val):
        if pd.isna(val):
            return None
        val_str = str(val).strip().replace(',', '')
        if val_str in ['-', '', 'nan', 'None']:
            return None
        try:
            return float(val_str)
        except ValueError:
            return None

    current_code = 'Male'
    localities = []

    for idx, r in df_geo.iterrows():
        col_a = str(r['Column_A']).strip() if pd.notna(r['Column_A']) else ''
        loc = str(r['Locality']).strip() if pd.notna(r['Locality']) else ''
        pop = clean_float(r['Population (census 2014) - Resident Population'])
        
        if 'Table 1.5' in col_a:
            continue
            
        m = re.search(r'\(([A-Za-z]+)\)', col_a)
        if m and pop is None:
            current_code = m.group(1)
            continue
            
        if pop is not None and loc:
            is_atoll_cap = '*' in loc
            clean_name = loc.replace('*', '').strip()
            atoll_info = ATOLL_METADATA.get(current_code, {})
            short_p = atoll_info.get('short_prefix', '')
            display_name = f"{short_p} {clean_name}".strip() if short_p else clean_name
            
            area = clean_float(r['Locality - Land Area ( in hectares )_2'])
            dens_ha = clean_float(r['Population Density (population per hectar) - Resident Population'])
            dens_km2 = dens_ha * 100 if dens_ha else None
            dist = clean_float(r["Population Density (population per hectar) - Distance to Male' ( in km)"])
            
            localities.append({
                'name': clean_name,
                'display_name': display_name,
                'atoll_code': atoll_info.get('code', current_code),
                'atoll_name': atoll_info.get('atoll_name', ''),
                'atoll_geo': atoll_info.get('geo_name', ''),
                'is_capital': clean_name in ["Male'", "Villingili", "Hulhumale'"],
                'is_atoll_capital': is_atoll_cap,
                'population': int(pop),
                'land_area_ha': round(area, 2) if area else None,
                'density_km2': round(dens_km2, 1) if dens_km2 else None,
                'distance_km': round(dist, 1) if dist else 0.0
            })
            
    localities.sort(key=lambda x: x['population'], reverse=True)
    total_pop = sum(x['population'] for x in localities)
    male_item = next(x for x in localities if x['name'] == "Male'")
    
    # Atolls list in geographic sequence (North to South)
    atoll_order = ['Male', 'HA', 'HDh', 'Sh', 'N', 'R', 'B', 'Lh', 'K', 'AA', 'ADh', 'V', 'M', 'F', 'Dh', 'Th', 'L', 'GA', 'GDh', 'Gn', 'S']
    atolls_summary = []
    for code in atoll_order:
        meta = ATOLL_METADATA[code]
        atoll_locs = [l for l in localities if l['atoll_code'] == code]
        atolls_summary.append({
            'code': meta['code'],
            'name': meta['atoll_name'],
            'geo_name': meta['geo_name'],
            'short_prefix': meta['short_prefix'],
            'island_count': len(atoll_locs),
            'total_population': sum(l['population'] for l in atoll_locs)
        })

    geo_data = {
        'total_resident_pop': total_pop,
        'male_pop': male_item['population'],
        'male_pct': round((male_item['population'] / total_pop) * 100, 1),
        'male_density_km2': male_item['density_km2'],
        'median_island_pop': int(np.median([x['population'] for x in localities if not x['is_capital']])),
        'total_inhabited_islands': len(localities),
        'atolls': atolls_summary,
        'localities': localities,
        'global_benchmarks': [
            {'entity': "Malé City (Maldives)", 'density': 74879, 'highlight': True, 'type': 'Capital Island'},
            {'entity': "Manila (Philippines)", 'density': 43000, 'highlight': False, 'type': 'Global City'},
            {'entity': "Dhaka (Bangladesh)", 'density': 30093, 'highlight': False, 'type': 'Global City'},
            {'entity': "Manhattan (NYC, USA)", 'density': 28100, 'highlight': False, 'type': 'Global City Borough'},
            {'entity': "Paris (France)", 'density': 20400, 'highlight': False, 'type': 'Global City'},
            {'entity': "Tokyo 23 Wards (Japan)", 'density': 15400, 'highlight': False, 'type': 'Global City'},
            {'entity': "London (UK)", 'density': 5600, 'highlight': False, 'type': 'Global City'},
            {'entity': "Outer Atoll Median (Maldives)", 'density': 1980, 'highlight': True, 'type': 'Outer Islands'}
        ]
    }

    # 2. TOURISM & COVID SHOCK
    print("Extracting tourism...")
    df_tour = pd.read_csv('datasets/10.0 Tourism/10.1.csv')
    df_m_tour = pd.read_csv('datasets/10.0 Tourism/10.11.csv')
    
    tot_row = df_tour[df_tour['Country of Nationality'].str.strip() == 'Total'].iloc[0]
    years_t = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
    cols_t = ['2012', '2013', '2014', '2015', 'No. of Tourists - 2016', 'No. of Tourists - 2017', 'No. of Tourists - 2018', 'No. of Tourists - 2019', 'No. of Tourists - 2020']
    
    annual_arrivals = []
    for y, c in zip(years_t, cols_t):
        annual_arrivals.append({'year': y, 'arrivals': int(float(tot_row[c]))})
        
    m_row = df_m_tour[df_m_tour['Country of Nationality'].str.strip() == 'Total'].iloc[0]
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_2020 = []
    for m in months:
        monthly_2020.append({'month': m, 'arrivals': int(float(m_row[m]))})
        
    top_countries = ['India', 'Russia', 'United Kingdom', 'Italy', 'Germany', 'China', 'France', 'U.S.A', 'Switzerland', 'Japan']
    market_shifts = []
    for c in top_countries:
        cr = df_tour[df_tour['Country of Nationality'].str.strip() == c]
        if not cr.empty:
            r = cr.iloc[0]
            market_shifts.append({
                'country': c,
                '2018': int(float(r['No. of Tourists - 2018'])),
                '2019': int(float(r['No. of Tourists - 2019'])),
                '2020': int(float(r['No. of Tourists - 2020']))
            })
            
    tourism_data = {
        'annual_arrivals': annual_arrivals,
        'monthly_2020': monthly_2020,
        'market_shifts': market_shifts,
        'global_benchmarks': [
            {'entity': 'Maldives', 'decline': -67.4, 'highlight': True, 'arrivals_2020': 555494, 'tourists_per_resident': 3.4},
            {'entity': 'Global Average (UNWTO)', 'decline': -73.0, 'highlight': False, 'arrivals_2020': None, 'tourists_per_resident': 0.18},
            {'entity': 'Asia-Pacific', 'decline': -84.0, 'highlight': False, 'arrivals_2020': None, 'tourists_per_resident': 0.08},
            {'entity': 'Europe', 'decline': -68.0, 'highlight': False, 'arrivals_2020': None, 'tourists_per_resident': 0.65},
            {'entity': 'Caribbean Islands', 'decline': -67.0, 'highlight': False, 'arrivals_2020': None, 'tourists_per_resident': 1.10},
            {'entity': 'Spain', 'decline': -77.3, 'highlight': False, 'arrivals_2020': 18900000, 'tourists_per_resident': 1.8},
            {'entity': 'Thailand', 'decline': -83.2, 'highlight': False, 'arrivals_2020': 6700000, 'tourists_per_resident': 0.57}
        ]
    }

    # 3. MACROECONOMIC REAL GDP
    print("Extracting National Accounts...")
    df_gdp = pd.read_csv('datasets/16.0 National Accounts/16.1.csv')
    gdp_cols = [c for c in df_gdp.columns if 'Industry / Economic Activity - 20' in c]
    years_gdp = [int(c.split(' - ')[-1].split(' ')[0]) for c in gdp_cols]
    
    tot_gdp_row = df_gdp.iloc[0]
    gdp_series = []
    for y, c in zip(years_gdp, gdp_cols):
        gdp_series.append({'year': y, 'real_gdp_mvr_m': round(float(tot_gdp_row[c]), 1)})
        
    sectors_config = [
        ('Tourism', 16),
        ('Transportation & Comm.', 20),
        ('Construction', 13),
        ('Wholesale & Retail Trade', 15),
        ('Manufacturing', 7),
        ('Public Administration', 29),
        ('Financial Services', 24),
        ('Fisheries', 5),
        ('Real Estate', 27)
    ]
    sectoral_growth = []
    for s_name, s_idx in sectors_config:
        row = df_gdp.iloc[s_idx]
        v19 = float(row.filter(like='2019').values[0])
        v20 = float(row.filter(like='2020').values[0])
        growth = ((v20 - v19) / v19) * 100
        sectoral_growth.append({
            'sector': s_name,
            'gva_2019': round(v19, 1),
            'gva_2020': round(v20, 1),
            'growth_pct': round(growth, 1)
        })
    sectoral_growth.sort(key=lambda x: x['growth_pct'])
    
    gdp_data = {
        'series': gdp_series,
        'sectoral_growth': sectoral_growth,
        'global_gdp_benchmarks': [
            {'country': 'Maldives', 'growth_2020': -33.5, 'highlight': True, 'note': 'Steepest contraction among sovereign economies'},
            {'country': 'Fiji', 'growth_2020': -17.2, 'highlight': False, 'note': 'Tourism island peer'},
            {'country': 'Spain', 'growth_2020': -11.2, 'highlight': False, 'note': 'Major tourism economy'},
            {'country': 'Seychelles', 'growth_2020': -10.7, 'highlight': False, 'note': 'Indian Ocean island peer'},
            {'country': 'United Kingdom', 'growth_2020': -10.4, 'highlight': False, 'note': 'Services hub'},
            {'country': 'India', 'growth_2020': -5.8, 'highlight': False, 'note': 'Regional neighbor'},
            {'country': 'World Average', 'growth_2020': -3.1, 'highlight': False, 'note': 'Global aggregate'},
            {'country': 'United States', 'growth_2020': -2.8, 'highlight': False, 'note': 'Diversified economy'},
            {'country': 'China', 'growth_2020': 2.2, 'highlight': False, 'note': 'Early recovery'}
        ]
    }

    # 4. FISHERIES & BLUE ECONOMY
    print("Extracting fisheries...")
    df_f_spec = pd.read_csv('datasets/9.0 Fisheries & Agriculture/9.6.csv')
    df_f_util = pd.read_csv('datasets/9.0 Fisheries & Agriculture/9.1.csv')
    
    years_f = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
    fisheries_catch = []
    for y in years_f:
        tot = float(df_f_spec.iloc[0][str(y)])
        skip = float(df_f_spec.iloc[1][str(y)])
        yfin = float(df_f_spec.iloc[2][str(y)])
        oth = tot - skip - yfin
        fisheries_catch.append({
            'year': y,
            'total_mt': round(tot, 1),
            'skipjack_mt': round(skip, 1),
            'yellowfin_mt': round(yfin, 1),
            'other_mt': round(oth, 1)
        })
        
    years_u = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
    fisheries_util = []
    for y in years_u:
        exp_p = float(df_f_util.iloc[0][f"(In '000 metric tons) - Percentage share - {y}"])
        loc_p = float(df_f_util.iloc[1][f"(In '000 metric tons) - Percentage share - {y}"])
        fisheries_util.append({
            'year': y,
            'export_share': round(exp_p, 1),
            'local_share': round(loc_p, 1)
        })
        
    fisheries_data = {
        'catch': fisheries_catch,
        'utilization': fisheries_util,
        'global_consumption_benchmarks': [
            {'country': 'Maldives', 'consumption_kg_per_capita': 142.0, 'highlight': True, 'rank': 1},
            {'country': 'Iceland', 'consumption_kg_per_capita': 91.0, 'highlight': False, 'rank': 2},
            {'country': 'Portugal', 'consumption_kg_per_capita': 56.8, 'highlight': False, 'rank': 3},
            {'country': 'Japan', 'consumption_kg_per_capita': 45.5, 'highlight': False, 'rank': 6},
            {'country': 'Spain', 'consumption_kg_per_capita': 42.1, 'highlight': False, 'rank': 8},
            {'country': 'USA', 'consumption_kg_per_capita': 22.4, 'highlight': False, 'rank': 25},
            {'country': 'World Average', 'consumption_kg_per_capita': 20.5, 'highlight': False, 'rank': 'Avg'},
            {'country': 'India', 'consumption_kg_per_capita': 7.0, 'highlight': False, 'rank': 80}
        ]
    }

    # 5. PUBLIC FINANCE
    print("Extracting public finance...")
    df_pf = pd.read_csv('datasets/13.0 Public Finance/13.2.csv')
    df_tour_pf = pd.read_csv('datasets/10.0 Tourism/10.10.csv')
    
    pf_years = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
    public_finance_series = []
    for i, y in enumerate(pf_years):
        rev = float(df_pf.iloc[0].iloc[i+4])
        exp = float(df_pf.iloc[6].iloc[i+4])
        bal = float(df_pf.iloc[10].iloc[i+4])
        public_finance_series.append({
            'year': y,
            'revenue_mvr_m': round(rev, 1),
            'expenditure_mvr_m': round(exp, 1),
            'deficit_mvr_m': round(bal, 1)
        })
        
    tourism_budget_share = []
    tb_years = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
    for i, y in enumerate(tb_years):
        col_idx = i + 3
        t_rev_share = float(df_tour_pf.iloc[2].iloc[col_idx])
        tourism_budget_share.append({
            'year': y,
            'share_pct': round(t_rev_share, 1)
        })
        
    public_finance_data = {
        'series': public_finance_series,
        'tourism_share': tourism_budget_share
    }

    # 6. INFRASTRUCTURE & WATER
    print("Extracting water & climate data...")
    df_w = pd.read_csv('datasets/12.0 Electricity and water/12.15.csv').dropna(subset=['Number of islands', 'Expenses on average for ton (MVR)']).copy()
    water_emergency = []
    for _, r in df_w.iterrows():
        y = int(r['Column_A'])
        islands = int(r['Number of islands'])
        tons = float(r['Number of tons supplied'])
        cost_ton = float(r['Expenses on average for ton (MVR)'])
        water_emergency.append({
            'year': y,
            'islands_supplied': islands,
            'tons_supplied': round(tons, 1),
            'cost_per_ton_mvr': round(cost_ton, 1)
        })
        
        water_data = {
        'emergency_series': water_emergency,
        'climate_facts': [
            {'metric': 'Average Elevation', 'value': '1.5 meters', 'global_context': 'Lowest nation on Earth (highest point is 2.4m)'},
            {'metric': 'Ocean vs Land Territory', 'value': '99.7% Ocean / 0.3% Land', 'global_context': '90,000 km² ocean spanning 1,192 coral islands'},
            {'metric': 'Freshwater Resources', 'value': '0 Rivers, 0 Lakes', 'global_context': '100% dependent on rainwater harvesting & reverse-osmosis desalination'},
            {'metric': 'Emergency Delivery Cost', 'value': '$178 USD / m³', 'global_context': 'Vs $2–$4 / m³ typical municipal city water cost'}
        ]
    }

    # 7. DEMOGRAPHICS & POPULATION PYRAMID (Table 3.13, 3.14, 3.15, 3.2)
    print("Extracting demographics & population pyramid series...")
    age_groups = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80+']
    age_starts = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]

    def compute_pyramid_indicators(male_arr, female_arr, total_m, total_f, total_b):
        total = total_b if total_b > 0 else (total_m + total_f)
        if total == 0:
            total = sum(male_arr) + sum(female_arr)
        
        youth = sum(male_arr[0:3]) + sum(female_arr[0:3])       # 0-14
        working = sum(male_arr[3:13]) + sum(female_arr[3:13])   # 15-64
        elderly = sum(male_arr[13:]) + sum(female_arr[13:])     # 65+
        
        sex_ratio = round((total_m / total_f * 100), 1) if total_f > 0 else 0
        dep_ratio = round(((youth + elderly) / working * 100), 1) if working > 0 else 0
        youth_dep = round((youth / working * 100), 1) if working > 0 else 0
        elderly_dep = round((elderly / working * 100), 1) if working > 0 else 0
        youth_pct = round((youth / total * 100), 1) if total > 0 else 0
        working_pct = round((working / total * 100), 1) if total > 0 else 0
        elderly_pct = round((elderly / total * 100), 1) if total > 0 else 0
        
        # Median age estimation via linear interpolation
        half = total / 2.0
        cum = 0
        median_age = 28.0
        for i in range(17):
            cohort_pop = male_arr[i] + female_arr[i]
            if cum + cohort_pop >= half and cohort_pop > 0:
                fraction = (half - cum) / cohort_pop
                median_age = round(age_starts[i] + fraction * 5, 1)
                break
            cum += cohort_pop
            
        return {
            'total': total,
            'total_male': total_m,
            'total_female': total_f,
            'sex_ratio': sex_ratio,
            'youth': youth,
            'working': working,
            'elderly': elderly,
            'youth_pct': youth_pct,
            'working_pct': working_pct,
            'elderly_pct': elderly_pct,
            'dependency_ratio': dep_ratio,
            'youth_dependency': youth_dep,
            'elderly_dependency': elderly_dep,
            'median_age': median_age
        }

    def parse_pyramid_csv(filepath):
        import csv
        with open(filepath, mode='r', encoding='utf-8') as f:
            rows = list(csv.reader(f))
        
        header = rows[0]
        years = [int(y.strip()) for y in header[1:] if y.strip().isdigit()]
        
        subpops = {'Total': {}, 'Maldivian': {}, 'Foreigner': {}}
        for sp in subpops:
            subpops[sp] = {
                'years': years,
                'age_groups': age_groups,
                'by_year': {}
            }
            for y in years:
                subpops[sp]['by_year'][y] = {
                    'male': [0] * len(age_groups),
                    'female': [0] * len(age_groups),
                    'total_male': 0,
                    'total_female': 0,
                    'total': 0,
                    'indicators': {}
                }
                
        current_sp = 'Total'
        current_gender = None
        
        for r in rows:
            if not r or not r[0].strip():
                continue
            c0 = r[0].strip()
            if 'Resident Maldivian' in c0:
                current_sp = 'Maldivian'
                current_gender = None
                continue
            elif 'Resident Foreigners' in c0 or 'Foreign' in c0:
                current_sp = 'Foreigner'
                current_gender = None
                continue
            elif c0 == 'Male':
                current_gender = 'male'
                for idx, y in enumerate(years):
                    v = float(r[idx+1].replace(',', '')) if idx+1 < len(r) and r[idx+1].strip() else 0.0
                    subpops[current_sp]['by_year'][y]['total_male'] = round(v)
                continue
            elif c0 == 'Female':
                current_gender = 'female'
                for idx, y in enumerate(years):
                    v = float(r[idx+1].replace(',', '')) if idx+1 < len(r) and r[idx+1].strip() else 0.0
                    subpops[current_sp]['by_year'][y]['total_female'] = round(v)
                continue
            elif c0 == 'Both Sexes':
                for idx, y in enumerate(years):
                    v = float(r[idx+1].replace(',', '')) if idx+1 < len(r) and r[idx+1].strip() else 0.0
                    subpops[current_sp]['by_year'][y]['total'] = round(v)
                continue
                
            c0_clean = c0.replace(' ', '')
            if c0_clean in age_groups and current_gender:
                age_idx = age_groups.index(c0_clean)
                for idx, y in enumerate(years):
                    v_str = r[idx+1].replace(',', '').strip() if idx+1 < len(r) else ''
                    v = float(v_str) if v_str else 0.0
                    subpops[current_sp]['by_year'][y][current_gender][age_idx] = round(v)

        # Compute indicators for each subpop and year
        for sp in subpops:
            for y in years:
                entry = subpops[sp]['by_year'][y]
                entry['indicators'] = compute_pyramid_indicators(
                    entry['male'],
                    entry['female'],
                    entry['total_male'],
                    entry['total_female'],
                    entry['total']
                )
        return subpops

    # Parse Census 3.2 historical data (1995, 2000, 2006, 2014)
    def parse_historical_census():
        import csv
        census_years = [1995, 2000, 2006, 2014]
        cohort_map = {
            'Less than 1 year': 0, '1 - 4': 0,
            '5': 1, '6 - 9': 1,
            '10 - 14': 2, '15 - 19': 3, '20 - 24': 4, '25 - 29': 5,
            '30 - 34': 6, '35 - 39': 7, '40 - 44': 8, '45 - 49': 9,
            '50 - 54': 10, '55 - 59': 11, '60 - 64': 12, '65 - 69': 13,
            '70 - 74': 14, '75 - 79': 15,
            '80 - 84': 16, '85 - 89': 16, '90 - 94': 16, '95 years and over': 16,
        }
        res = {
            'years': census_years,
            'age_groups': age_groups,
            'by_year': {y: {'male': [0]*17, 'female': [0]*17, 'total_male': 0, 'total_female': 0, 'total': 0, 'indicators': {}} for y in census_years}
        }
        with open('datasets/3.0 population/3.2.csv', mode='r', encoding='utf-8') as f:
            rows = list(csv.reader(f))
        for r in rows[1:]:
            ag = r[0].strip()
            if ag == 'Total':
                for idx, y in enumerate(census_years):
                    both = int(r[idx*3 + 1].replace(',', '') or 0)
                    m = int(r[idx*3 + 2].replace(',', '') or 0)
                    f_val = int(r[idx*3 + 3].replace(',', '') or 0)
                    res['by_year'][y]['total'] = both
                    res['by_year'][y]['total_male'] = m
                    res['by_year'][y]['total_female'] = f_val
            elif ag in cohort_map:
                idx_cohort = cohort_map[ag]
                for idx, y in enumerate(census_years):
                    m = int(r[idx*3 + 2].replace(',', '') or 0)
                    f_val = int(r[idx*3 + 3].replace(',', '') or 0)
                    res['by_year'][y]['male'][idx_cohort] += m
                    res['by_year'][y]['female'][idx_cohort] += f_val
        for y in census_years:
            entry = res['by_year'][y]
            entry['indicators'] = compute_pyramid_indicators(
                entry['male'],
                entry['female'],
                entry['total_male'],
                entry['total_female'],
                entry['total']
            )
        return res

    demographics_data = {
        'age_groups': age_groups,
        'years': [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030],
        'scopes': {
            'national': parse_pyramid_csv('datasets/3.0 population/3.13.csv'),
            'male_city': parse_pyramid_csv('datasets/3.0 population/3.14.csv'),
            'atolls': parse_pyramid_csv('datasets/3.0 population/3.15.csv'),
        },
        'historical_census': parse_historical_census()
    }

    # 8. CURATED INTERESTING FACTS & TRIVIA
    interesting_facts = [
        {
            'category': 'Urban Density',
            'headline': "Malé is ~3.7× Denser Than Paris and 2.7× Denser than Manhattan",
            'detail': "Malé Island packs 153,904 residents onto only 2.05 km² (74,879 people/km²). If the entire global population lived at Malé's density, all 8 billion humans could fit inside the state of Ohio!",
            'icon': 'building'
        },
        {
            'category': 'Demographic Asymmetry',
            'headline': "Expatriate Sex Ratio: 1,017 Men per 100 Women",
            'detail': "In 2020, foreign residents numbered 178,156—composed of 162,210 men and just 15,946 women (over 10:1 ratio), concentrated in construction and hospitality ages 20–39.",
            'icon': 'users'
        },
        {
            'category': 'Macroeconomic Shock',
            'headline': "Steepest Peacetime GDP Contraction Globally",
            'detail': "Maldives Real GDP plummeted by -33.5% in 2020 due to its tourism reliance. This single-year contraction was 2.5× larger than the devastating 2004 Indian Ocean Tsunami (-13.1%).",
            'icon': 'trending-down'
        },
        {
            'category': 'Tourism Footprint',
            'headline': "3.4 Tourists for Every Inhabitant",
            'detail': "In 2019, 1.70 million tourists visited the Maldives for a resident population of ~500,000. For comparison, France (the world's most visited country) receives ~1.3 tourists per resident.",
            'icon': 'plane'
        },
        {
            'category': 'Blue Economy',
            'headline': "World #1 in Per Capita Fish Consumption",
            'detail': "Maldivians eat ~142 kg of fish per person annually—nearly 7× the global average (20.5 kg). 100% of commercial tuna is caught with one-by-one pole-and-line, producing zero dolphin bycatch.",
            'icon': 'fish'
        },
        {
            'category': 'Climate Vulnerability',
            'headline': "The Lowest Nation on Earth",
            'detail': "With an average ground level of only 1.5 meters (4 ft 11 in) above sea level, 99.7% of the nation is ocean. Up to 91 inhabited islands exhaust drinkable water every dry season, requiring sea-transported relief.",
            'icon': 'droplet'
        },
        {
            'category': 'Geopolitical Market Shift',
            'headline': "India and Russia Displaced China Overnight",
            'detail': "China had been the #1 tourist market for almost a decade (284,000 arrivals in 2019). In 2020, India (62,960) and Russia (61,387) overtook all countries to keep luxury resorts afloat.",
            'icon': 'globe'
        }
    ]

    dashboard_bundle = {
        'catalog': compact_catalog,
        'geography': geo_data,
        'demographics': demographics_data,
        'tourism': tourism_data,
        'gdp': gdp_data,
        'fisheries': fisheries_data,
        'public_finance': public_finance_data,
        'water': water_data,
        'interesting_facts': interesting_facts
    }

    # Save to dashboard_data.json
    os.makedirs('docs', exist_ok=True)
    with open('docs/dashboard_data.json', 'w') as f:
        json.dump(dashboard_bundle, f, indent=2)
    with open('dashboard_data.json', 'w') as f:
        json.dump(dashboard_bundle, f, indent=2)

    # Save as JS to avoid CORS restrictions when opened locally
    js_content = f"// Generated data bundle for Maldives Statistical Year Book 2021 Dashboard\nwindow.MALDIVES_DATA = {json.dumps(dashboard_bundle)};\n"
    with open('docs/dashboard_data.js', 'w') as f:
        f.write(js_content)
    with open('dashboard_data.js', 'w') as f:
        f.write(js_content)

    print("Data successfully generated in docs/ and root!")

if __name__ == '__main__':
    extract_all()
