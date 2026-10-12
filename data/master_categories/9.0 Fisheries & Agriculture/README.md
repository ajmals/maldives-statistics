# 9.0 Fisheries & Agriculture — Master Multi-Year Dataset

This directory houses the consolidated multi-year datasets for **9.0 Fisheries & Agriculture**, harmonizing data across all official Maldives Statistical Yearbook editions published between **2008 and 2026** by the National Bureau of Statistics (NBS).

## Available Formats
- **Consolidated Panel Dataset ([`master_panel.csv`](master_panel.csv))**: Long-format tabular dataset (20,336 rows) with schema: `[category, table_id, table_title, item_name, metric_name, year, value, unit, edition_year]`.
- **Category SQLite Database ([`9_0_fisheries_agriculture.db`](9_0_fisheries_agriculture.db))**: Fully indexed local database containing `master_panel` plus dedicated SQL tables for every individual harmonized table.
- **Harmonized Wide CSVs ([`tables/`](tables/))**: 23 individual multi-year CSV tables with continuous year columns.

## Category Summary
- **Time Horizon Covered**: **2001 – 2026**
- **Total Harmonized Tables**: 23
- **Total Time-Series Observations**: 20,336
- **SQLite Database**: [`9_0_fisheries_agriculture.db`](9_0_fisheries_agriculture.db)

## Harmonized Tables Catalog

| Table ID | Title | Time Span | Rows | Cols | Wide CSV | Metadata |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **9.1** | Table 9.1 :FISH PRODUCTION BY TYPE AND UTILIZATION, 2006 - 2009 (In '000 metric tons) | 2005 – 2025 | 12 | 81 | [`9.1.csv`](tables/9.1.csv) | [`9.1.json`](tables/9.1.json) |
| **9.10** | Table 9.10: VALUE OF AGRICULTURAL PRODUCTS TRADED IN MALE' MARKET , 2008 - 2009 (In rufiyaa) | 2008 – 2026 | 54 | 71 | [`9.10.csv`](tables/9.10.csv) | [`9.10.json`](tables/9.10.json) |
| **9.11** | Table 9.11: AGRICULTURAL PRODUCTS TRADED IN MALE' MARKET BY ATOLLS 2009 (In kg) | 2004 – 2026 | 89 | 55 | [`9.11.csv`](tables/9.11.csv) | [`9.11.json`](tables/9.11.json) |
| **9.12** | Table 9.12: AGRICULTURAL PRODUCTS TRADED IN MALE' MARKET BY ATOLLS, 2009 (Value in Rf) | 2010 – 2024 | 75 | 82 | [`9.12.csv`](tables/9.12.csv) | [`9.12.json`](tables/9.12.json) |
| **9.13** | Table 9.13: IMPORTS OF FRESH AGRICULTURAL CROPS MAINLY PRODUCED IN MALDIVES FROM 2004 - 2009 (In Kgs) | 2004 – 2026 | 77 | 94 | [`9.13.csv`](tables/9.13.csv) | [`9.13.json`](tables/9.13.json) |
| **9.14** | Table 19.14: IMPORTS OF FRESH AGRICULTURAL CROPS MAINLY PRODUCED IN MALDIVES, 2009 (Value in Rf) | 2004 – 2026 | 64 | 37 | [`9.14.csv`](tables/9.14.csv) | [`9.14.json`](tables/9.14.json) |
| **9.15** | Table 9.15 : FISH CATCH BY TYPE AND FISHING METHODS, 2009 (In metric tons) | 2010 – 2025 | 52 | 37 | [`9.15.csv`](tables/9.15.csv) | [`9.15.json`](tables/9.15.json) |
| **9.16** | Table 9.16 : FISH CATCH, FISHING TRIPS AND CATCH PER UNIT EFFORT BY LOCALITY, 2009 | 2010 – 2022 | 53 | 63 | [`9.16.csv`](tables/9.16.csv) | [`9.16.json`](tables/9.16.json) |
| **9.17** | Table 9.17: COMPARISON OF IMPORTS AND MALE' MARKET DATA 2009 (MAJOR AGRICULTURAL CROPS SUPPLIED TO MALE') | 2010 – 2025 | 61 | 51 | [`9.17.csv`](tables/9.17.csv) | [`9.17.json`](tables/9.17.json) |
| **9.18** | Table 9.17: IMPORTS OF FRESH AGRICULTURAL CROPS MAINLY PRODUCED IN MALDIVES FROM, 2007 - 2014 | 2004 – 2022 | 35 | 31 | [`9.18.csv`](tables/9.18.csv) | [`9.18.json`](tables/9.18.json) |
| **9.19** | Table 9.19: AGRICULTURAL PRODUCTS TRADED IN MALE' MARKET BY ATOLLS, 2017 | 2018 – 2023 | 17 | 69 | [`9.19.csv`](tables/9.19.csv) | [`9.19.json`](tables/9.19.json) |
| **9.2** | Table 9.2 : FISH CATCH BY LOCALITY, 2006 - 2009 (In '000 metric tons) | 2005 – 2025 | 25 | 114 | [`9.2.csv`](tables/9.2.csv) | [`9.2.json`](tables/9.2.json) |
| **9.20** | Table 9.20: AGRICULTURAL PRODUCTS TRADED IN MALE' MARKET BY ATOLLS, 2017 | 2018 – 2023 | 17 | 68 | [`9.20.csv`](tables/9.20.csv) | [`9.20.json`](tables/9.20.json) |
| **9.3** | Table 9.3 : FISH LANDING BY TYPE AND LOCALITY, 2009 (In metric tons) | 2010 – 2026 | 25 | 100 | [`9.3.csv`](tables/9.3.csv) | [`9.3.json`](tables/9.3.json) |
| **9.3fig9.1** | Table 9.3 : FISH LANDING BY TYPE AND LOCALITY, 2010 | 2011 | 24 | 8 | [`9.3fig9.1.csv`](tables/9.3fig9.1.csv) | [`9.3fig9.1.json`](tables/9.3fig9.1.json) |
| **9.4** | Table 9.4 : FISH CATCH BY MONTH, 2005 - 2009 (In metric tons) | 2004 – 2025 | 15 | 65 | [`9.4.csv`](tables/9.4.csv) | [`9.4.json`](tables/9.4.json) |
| **9.4fig9.2** | Table 9.4 : FISH CATCH BY MONTH, 2006 - 2010 | 2004 – 2011 | 14 | 14 | [`9.4fig9.2.csv`](tables/9.4fig9.2.csv) | [`9.4fig9.2.json`](tables/9.4fig9.2.json) |
| **9.5** | Table 9.5 : MONTHLY FISH CATCH BY TYPE , 2009 (In metric tons) | 2010 – 2026 | 15 | 123 | [`9.5.csv`](tables/9.5.csv) | [`9.5.json`](tables/9.5.json) |
| **9.6** | Table 9.6 : FISH CATCH BY TYPE OF VESSELS AND SPECIES, 2004 - 2009 (In metric tons) | 2001 – 2025 | 15 | 41 | [`9.6.csv`](tables/9.6.csv) | [`9.6.json`](tables/9.6.json) |
| **9.7** | Table 9.7 : AVERAGE NUMBER OF VESSELS ENGAGED PER MONTH IN FISHING AND NUMBER OF FISHING TRIPS BY LOCALITY, 2009 | 2009 – 2022 | 40 | 43 | [`9.7.csv`](tables/9.7.csv) | [`9.7.json`](tables/9.7.json) |
| **9.8** | Table 9.8: MONTH:Y FRESH FISH PURCHASED , 2006 - 2009 (In metric tons) | 2006 – 2026 | 59 | 45 | [`9.8.csv`](tables/9.8.csv) | [`9.8.json`](tables/9.8.json) |
| **9.9** | Table 9.9 : MIFCO PRODUCTION, 2004 - 2009 | 2004 – 2026 | 59 | 81 | [`9.9.csv`](tables/9.9.csv) | [`9.9.json`](tables/9.9.json) |
| **9.9-1** | Table 9.9 : FISH CATCH BY TYPE AND FISHING METHODS, 2018 (In metric tons) | 2019 | 10 | 9 | [`9.9-1.csv`](tables/9.9-1.csv) | [`9.9-1.json`](tables/9.9-1.json) |

## Example SQLite Usage (Python)
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('9_0_fisheries_agriculture.db')

# Query any metric across all years in milliseconds:
df = pd.read_sql('''
    SELECT item_name, year, value, unit
    FROM master_panel
    WHERE table_id = '10.1' AND year >= 2010
    ORDER BY item_name, year
''', conn)
print(df.head())
```
