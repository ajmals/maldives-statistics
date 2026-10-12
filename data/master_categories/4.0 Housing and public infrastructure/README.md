# 4.0 Housing and public infrastructure — Master Multi-Year Dataset

This directory houses the consolidated multi-year datasets for **4.0 Housing and public infrastructure**, harmonizing data across all official Maldives Statistical Yearbook editions published between **2008 and 2026** by the National Bureau of Statistics (NBS).

## Available Formats
- **Consolidated Panel Dataset ([`master_panel.csv`](master_panel.csv))**: Long-format tabular dataset (4,530 rows) with schema: `[category, table_id, table_title, item_name, metric_name, year, value, unit, edition_year]`.
- **Category SQLite Database ([`4_0_housing_and_public_infrastructure.db`](4_0_housing_and_public_infrastructure.db))**: Fully indexed local database containing `master_panel` plus dedicated SQL tables for every individual harmonized table.
- **Harmonized Wide CSVs ([`tables/`](tables/))**: 9 individual multi-year CSV tables with continuous year columns.

## Category Summary
- **Time Horizon Covered**: **2002 – 2025**
- **Total Harmonized Tables**: 9
- **Total Time-Series Observations**: 4,530
- **SQLite Database**: [`4_0_housing_and_public_infrastructure.db`](4_0_housing_and_public_infrastructure.db)

## Harmonized Tables Catalog

| Table ID | Title | Time Span | Rows | Cols | Wide CSV | Metadata |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **4.1** | Table 4.1 : HOUSEHOLDS CLASSIFIED BY STRUCTURE TYPE, CENSUS 2006 | 2009 – 2025 | 28 | 59 | [`4.1.csv`](tables/4.1.csv) | [`4.1.json`](tables/4.1.json) |
| **4.2** | Table 4.2: RENTED AND OWNER OCCUPIED HOUSEHOLD, CENSUS 2006 | 2009 – 2025 | 36 | 37 | [`4.2.csv`](tables/4.2.csv) | [`4.2.json`](tables/4.2.json) |
| **4.3** | Table 4.3: OWNERSHIP OF SELECTED HOUSEHOLD GOODS, CENSUS 2006 | 2009 – 2013 | 23 | 71 | [`4.3.csv`](tables/4.3.csv) | [`4.3.json`](tables/4.3.json) |
| **4.4** | Table 4.4 : BUILDINGS AUTHORISED FOR CONSTRUCTION AND COMPLETED | 2002 – 2022 | 6 | 40 | [`4.4.csv`](tables/4.4.csv) | [`4.4.json`](tables/4.4.json) |
| **4.5** | TABLE 4.5: SUPPLY OF HOUSING UNITS IN HULHUMALE', 2009 - 2010 | 2011 – 2022 | 26 | 48 | [`4.5.csv`](tables/4.5.csv) | [`4.5.json`](tables/4.5.json) |
| **4.6** | TABLE 4.6: HOUSING FINANCE/LOANS PROVIDED, 2009 - 2010 | 2009 – 2016 | 16 | 33 | [`4.6.csv`](tables/4.6.csv) | [`4.6.json`](tables/4.6.json) |
| **4.7** |  | 2010 – 2017 | 23 | 34 | [`4.7.csv`](tables/4.7.csv) | [`4.7.json`](tables/4.7.json) |
| **4.8** | TABLE 4.8: COMPLETED HARBOUR, SHORE PROTECTION AND RECLAMATION PROJECTS IN 2013 | 2016 | 23 | 5 | [`4.8.csv`](tables/4.8.csv) | [`4.8.json`](tables/4.8.json) |
| **4.9** | TABLE 4.9: ONGOING HARBOUR, SHORE PROTECTION AND RECLAMATION PROJECTS IN 2013 | 2016 | 47 | 7 | [`4.9.csv`](tables/4.9.csv) | [`4.9.json`](tables/4.9.json) |

## Example SQLite Usage (Python)
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('4_0_housing_and_public_infrastructure.db')

# Query any metric across all years in milliseconds:
df = pd.read_sql('''
    SELECT item_name, year, value, unit
    FROM master_panel
    WHERE table_id = '10.1' AND year >= 2010
    ORDER BY item_name, year
''', conn)
print(df.head())
```
