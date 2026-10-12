# 10.0 Tourism — Master Multi-Year Dataset

This directory houses the consolidated multi-year datasets for **10.0 Tourism**, harmonizing data across all official Maldives Statistical Yearbook editions published between **2008 and 2026** by the National Bureau of Statistics (NBS).

## Available Formats
- **Consolidated Panel Dataset ([`master_panel.csv`](master_panel.csv))**: Long-format tabular dataset (54,882 rows) with schema: `[category, table_id, table_title, item_name, metric_name, year, value, unit, edition_year]`.
- **Category SQLite Database ([`10_0_tourism.db`](10_0_tourism.db))**: Fully indexed local database containing `master_panel` plus dedicated SQL tables for every individual harmonized table.
- **Harmonized Wide CSVs ([`tables/`](tables/))**: 18 individual multi-year CSV tables with continuous year columns.

## Category Summary
- **Time Horizon Covered**: **2002 – 2027**
- **Total Harmonized Tables**: 18
- **Total Time-Series Observations**: 54,882
- **SQLite Database**: [`10_0_tourism.db`](10_0_tourism.db)

## Harmonized Tables Catalog

| Table ID | Title | Time Span | Rows | Cols | Wide CSV | Metadata |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **10.1** | Table 10.1 : FLOW OF TOURISTS BY NATIONALITY, 2006 - 2008 | 2005 – 2025 | 68 | 85 | [`10.1.csv`](tables/10.1.csv) | [`10.1.json`](tables/10.1.json) |
| **10.10** | Table 10.10 : BED CAPACITY OF TOURIST RESORTS AND THE DISTANCE FROM MALE' INTERNATIONAL AIRPORT, 2007-2010 | 2003 – 2027 | 361 | 88 | [`10.10.csv`](tables/10.10.csv) | [`10.10.json`](tables/10.10.json) |
| **10.11** | Table 10.11 :NEW ISLANDS LEASED FOR RESORT/HOTEL DEVELOPMENT AND THEIR ESTIMATED OPENING DATE | 2010 – 2026 | 228 | 130 | [`10.11.csv`](tables/10.11.csv) | [`10.11.json`](tables/10.11.json) |
| **10.12** | Table 10.12 : BED CAPACITY OF TOURIST RESORTS BY ATOLL, 2012 - 2017 | 2009 – 2025 | 20 | 34 | [`10.12.csv`](tables/10.12.csv) | [`10.12.json`](tables/10.12.json) |
| **10.13** | Table 10.13 : MONTHLY DISTRIBUTION OF TOURIST ARRIVALS BY NATIONALITY, 2017 | 2018 – 2026 | 87 | 105 | [`10.13.csv`](tables/10.13.csv) | [`10.13.json`](tables/10.13.json) |
| **10.13-1** | Table 10.13 : MONTHLY DISTRIBUTION OF TOURIST ARRIVALS BY NATIONALITY, 2018 | 2019 | 86 | 14 | [`10.13-1.csv`](tables/10.13-1.csv) | [`10.13-1.json`](tables/10.13-1.json) |
| **10.14** | Table 10.14 BED CAPACITY OF TOURIST RESORTS AND THE DISTANCE FROM MALE' INTERNATIONAL AIRPORT, 2013 - 2017 | 2007 – 2026 | 187 | 72 | [`10.14.csv`](tables/10.14.csv) | [`10.14.json`](tables/10.14.json) |
| **10.15** | Table 10.15: Number of Maldivian and Foreigners in the Resort Employment by Atoll and sex, Census 2014 | 2018 – 2026 | 153 | 52 | [`10.15.csv`](tables/10.15.csv) | [`10.15.json`](tables/10.15.json) |
| **10.2** | Table 10.2 : TOTAL REGISTERED BED CAPACITY AND NUMBER OF ACCOMMODATION ESTABLISHMENTS, BY TYPE, 2004 - 2009 | 2002 – 2025 | 7 | 91 | [`10.2.csv`](tables/10.2.csv) | [`10.2.json`](tables/10.2.json) |
| **10.2-1** | Table 10.2 : TOTAL REGISTERED BED CAPACITY AND NUMBER OF ACCOMMODATION ESTABLISHMENTS, BY TYPE, 2012 - 2018 (end year) | 2018 | 5 | 8 | [`10.2-1.csv`](tables/10.2-1.csv) | [`10.2-1.json`](tables/10.2-1.json) |
| **10.3** | Table 10.3 : BED CAPACITY AND UTILIZATION OF RESORTS AND HOTELS BY MONTH, 2008 - 2009 | 2008 – 2025 | 15 | 133 | [`10.3.csv`](tables/10.3.csv) | [`10.3.json`](tables/10.3.json) |
| **10.4** | Table 10.4 : RESORTS BY TYPE OF LEASE HOLDER AND MANAGEMENT, 2008 - 2009 | 2008 – 2025 | 21 | 88 | [`10.4.csv`](tables/10.4.csv) | [`10.4.json`](tables/10.4.json) |
| **10.4-1** | Table 10.4: BED CAPACITY AND UTILIZATION OF RESORTS BY MONTH, 2017 - 2018 | 2017 – 2018 | 13 | 11 | [`10.4-1.csv`](tables/10.4-1.csv) | [`10.4-1.json`](tables/10.4-1.json) |
| **10.5** | Table 10.5 : TOURIST ARRIVALS, AVERAGE DURATION OF STAY AND TOURIST BED-NIGHTS BY MONTH, 2009 | 2009 – 2025 | 16 | 91 | [`10.5.csv`](tables/10.5.csv) | [`10.5.json`](tables/10.5.json) |
| **10.6** | Table 10.6 : PROPORTION OF TOURISM REVENUE AND EXPENDITURE TO CENTRAL GOVERNMENT BUDGET, 2004 - 2011 (In Million Rf) | 2003 – 2025 | 23 | 107 | [`10.6.csv`](tables/10.6.csv) | [`10.6.json`](tables/10.6.json) |
| **10.7** | Table 10.7 : MONTHLY DISTRIBUTION OF TOURIST ARRIVALS BY NATIONALITY, 2009 | 2010 – 2025 | 60 | 163 | [`10.7.csv`](tables/10.7.csv) | [`10.7.json`](tables/10.7.json) |
| **10.8** | Table 10.8 : BED CAPACITY OF TOURIST RESORTS AND THE DISTANCE FROM MALE' INTERNATIONAL AIRPORT, 2006-2008 | 2005 – 2026 | 178 | 164 | [`10.8.csv`](tables/10.8.csv) | [`10.8.json`](tables/10.8.json) |
| **10.9** | Table 10.9 :NEW ISLANDS LEASED FOR RESORT/HOTEL DEVELOPMENT AND THEIR ESTIMATED OPENING DATE | 2009 – 2025 | 120 | 163 | [`10.9.csv`](tables/10.9.csv) | [`10.9.json`](tables/10.9.json) |

## Example SQLite Usage (Python)
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('10_0_tourism.db')

# Query any metric across all years in milliseconds:
df = pd.read_sql('''
    SELECT item_name, year, value, unit
    FROM master_panel
    WHERE table_id = '10.1' AND year >= 2010
    ORDER BY item_name, year
''', conn)
print(df.head())
```
