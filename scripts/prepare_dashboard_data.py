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
    df_geo = pd.read_csv('datasets/1.0 Geography/1.5.csv')
    valid_geo = df_geo.dropna(subset=['Locality', 'Population (census 2014) - Resident Population']).copy()
    valid_geo['Locality_Clean'] = valid_geo['Locality'].str.replace('*', '').str.strip()
    
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

    localities = []
    for _, r in valid_geo.iterrows():
        pop = clean_float(r['Population (census 2014) - Resident Population'])
        if pop is None:
            continue
        area = clean_float(r['Locality - Land Area ( in hectares )_2'])
        dens_ha = clean_float(r['Population Density (population per hectar) - Resident Population'])
        dens_km2 = dens_ha * 100 if dens_ha else None
        dist = clean_float(r["Population Density (population per hectar) - Distance to Male' ( in km)"])
        
        localities.append({
            'name': r['Locality_Clean'],
            'is_capital': r['Locality_Clean'] in ["Male'", "Villingili", "Hulhumale'"],
            'population': int(pop),
            'land_area_ha': round(area, 2) if area else None,
            'density_km2': round(dens_km2, 1) if dens_km2 else None,
            'distance_km': round(dist, 1) if dist else 0.0
        })
        
    localities.sort(key=lambda x: x['population'], reverse=True)
    total_pop = sum(x['population'] for x in localities)
    male_item = next(x for x in localities if x['name'] == "Male'")
    
    geo_data = {
        'total_resident_pop': total_pop,
        'male_pop': male_item['population'],
        'male_pct': round((male_item['population'] / total_pop) * 100, 1),
        'male_density_km2': male_item['density_km2'],
        'median_island_pop': int(np.median([x['population'] for x in localities if not x['is_capital']])),
        'total_inhabited_islands': len(localities),
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

    # 7. CURATED INTERESTING FACTS & TRIVIA
    interesting_facts = [
        {
            'category': 'Urban Density',
            'headline': "Malé is ~3.7× Denser Than Paris and 2.7× Denser than Manhattan",
            'detail': "Malé Island packs 153,904 residents onto only 2.05 km² (74,879 people/km²). If the entire global population lived at Malé's density, all 8 billion humans could fit inside the state of Ohio!",
            'icon': 'building'
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
