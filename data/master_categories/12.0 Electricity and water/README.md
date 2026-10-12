# 12.0 Electricity and water — Master Multi-Year Dataset

This directory houses the consolidated multi-year datasets for **12.0 Electricity and water**, harmonizing data across all official Maldives Statistical Yearbook editions published between **2008 and 2026** by the National Bureau of Statistics (NBS).

## Available Formats
- **Consolidated Panel Dataset ([`master_panel.csv`](master_panel.csv))**: Long-format tabular dataset (31,429 rows) with schema: `[category, table_id, table_title, item_name, metric_name, year, value, unit, edition_year]`.
- **Category SQLite Database ([`12_0_electricity_and_water.db`](12_0_electricity_and_water.db))**: Fully indexed local database containing `master_panel` plus dedicated SQL tables for every individual harmonized table.
- **Harmonized Wide CSVs ([`tables/`](tables/))**: 27 individual multi-year CSV tables with continuous year columns.

## Category Summary
- **Time Horizon Covered**: **1999 – 2026**
- **Total Harmonized Tables**: 27
- **Total Time-Series Observations**: 31,429
- **SQLite Database**: [`12_0_electricity_and_water.db`](12_0_electricity_and_water.db)

## Harmonized Tables Catalog

| Table ID | Title | Time Span | Rows | Cols | Wide CSV | Metadata |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **12.1** | Table 12.1 : ELECTRICITY UTILIZATION IN MALE', 2006 - 2009 | 2006 – 2025 | 11 | 21 | [`12.1.csv`](tables/12.1.csv) | [`12.1.json`](tables/12.1.json) |
| **12.1&fig12.1** | Table 12.1 : ELECTRICITY UTILIZATION IN MALE', 2006 - 2010 | 2003 – 2010 | 8 | 7 | [`12.1&fig12.1.csv`](tables/12.1&fig12.1.csv) | [`12.1&fig12.1.json`](tables/12.1&fig12.1.json) |
| **12.10** | Table 12.10 : WATER DISTRIBUTION IN VILLINGILI BY MONTH, 2006 - 2009 (In '000 metric tons) | 2006 – 2025 | 17 | 50 | [`12.10.csv`](tables/12.10.csv) | [`12.10.json`](tables/12.10.json) |
| **12.11** | Table 12.11 : NUMBER OF CUSTOMERS USING WATER IN VILLINGILI BY TYPE, 2006 - 2009 | 2001 – 2025 | 18 | 38 | [`12.11.csv`](tables/12.11.csv) | [`12.11.json`](tables/12.11.json) |
| **12.12** | Table 12.12 : BILLED WATER CONSUMPTION IN HULHUMALE', 2006 - 2009 (In '000 metric tons) | 1999 – 2025 | 20 | 46 | [`12.12.csv`](tables/12.12.csv) | [`12.12.json`](tables/12.12.json) |
| **12.12-1** | Table 12.12 : NUMBER OF CUSTOMERS USING WATER IN MALE' BY TYPE, 2010 - 2018 | 2010 – 2018 | 7 | 10 | [`12.12-1.csv`](tables/12.12-1.csv) | [`12.12-1.json`](tables/12.12-1.json) |
| **12.13** | Table 12.13 : NUMBER OF CUSTOMERS USING WATER IN HULHUMALE BY TYPE, 2006 - 2009 | 2006 – 2025 | 18 | 39 | [`12.13.csv`](tables/12.13.csv) | [`12.13.json`](tables/12.13.json) |
| **12.13-1** | Table 12.13 : NUMBER OF CUSTOMERS USING WATER IN VILIMALE' BY TYPE, 2010 - 2018 | 2010 – 2018 | 6 | 10 | [`12.13-1.csv`](tables/12.13-1.csv) | [`12.13-1.json`](tables/12.13-1.json) |
| **12.14** | Table 12.14 : WATER DISTRIBUTION IN HULHUMALE' BY MONTH, 2006 - 2009 (In '000 metric tons) | 1999 – 2025 | 20 | 29 | [`12.14.csv`](tables/12.14.csv) | [`12.14.json`](tables/12.14.json) |
| **12.14-1** | Table 12.14 : NUMBER OF CUSTOMERS USING WATER IN HULHUMALE' BY TYPE, 2010 - 2018 | 2010 – 2018 | 6 | 10 | [`12.14-1.csv`](tables/12.14-1.csv) | [`12.14-1.json`](tables/12.14-1.json) |
| **12.15** |  | 2006 – 2025 | 46 | 87 | [`12.15.csv`](tables/12.15.csv) | [`12.15.json`](tables/12.15.json) |
| **12.16** | Table 12.16 : MONTHLY ELECTRICITY PRODUCTION BY ISLAND, 2010 | 2007 – 2026 | 178 | 38 | [`12.16.csv`](tables/12.16.csv) | [`12.16.json`](tables/12.16.json) |
| **12.17** | TABLE 12.17: SUPPLY OF WATER ON EMERGENCY BY NUMBER OF ISLANDS , QUANTITY AND EXPENDITURE , 2005 - 2012 | 2013 – 2025 | 50 | 33 | [`12.17.csv`](tables/12.17.csv) | [`12.17.json`](tables/12.17.json) |
| **12.18** | Table 12.18: Islands supplied with emergency water and quanity supplied, 2012 | 2013 – 2023 | 99 | 10 | [`12.18.csv`](tables/12.18.csv) | [`12.18.json`](tables/12.18.json) |
| **12.19** | Table 12.19: Number of Islands and quanity of emergency water supplied by Atolls, 2012 - 2013 | 2012 – 2022 | 41 | 11 | [`12.19.csv`](tables/12.19.csv) | [`12.19.json`](tables/12.19.json) |
| **12.2** | Table 12.2 : MONTHLY ELECTRICITY PRODUCTION BY PUBLIC SECTOR, 2009 (In ' 000 kWh) | 2010 – 2026 | 217 | 197 | [`12.2.csv`](tables/12.2.csv) | [`12.2.json`](tables/12.2.json) |
| **12.2-1** | Table 12.2 : MONTHLY ELECTRICITY PRODUCTION BY PUBLIC SECTOR, 2018 | 2019 | 37 | 14 | [`12.2-1.csv`](tables/12.2-1.csv) | [`12.2-1.json`](tables/12.2-1.json) |
| **12.20** | TABLE 12.19: Imports of Mineral water, 2010 - 2014 | 2015 – 2020 | 34 | 7 | [`12.20.csv`](tables/12.20.csv) | [`12.20.json`](tables/12.20.json) |
| **12.21** | TABLE 12.20: Imports of Mineral waterby Country, 2014 | 2015 – 2019 | 42 | 7 | [`12.21.csv`](tables/12.21.csv) | [`12.21.json`](tables/12.21.json) |
| **12.3** | Table 12.3: TYPE OF LIGHTING USED BY HOUSEHOLDS, CENSUS 2006 | 2010 – 2026 | 61 | 178 | [`12.3.csv`](tables/12.3.csv) | [`12.3.json`](tables/12.3.json) |
| **12.4** | Table 12.4 : BILLED WATER CONSUMPTION IN MALE', 2004 - 2009 | 2004 – 2026 | 68 | 178 | [`12.4.csv`](tables/12.4.csv) | [`12.4.json`](tables/12.4.json) |
| **12.4&fig12.2** | Table 12.4 : BILLED WATER CONSUMPTION IN MALE', 2004 - 2009 | 2001 – 2009 | 7 | 9 | [`12.4&fig12.2.csv`](tables/12.4&fig12.2.csv) | [`12.4&fig12.2.json`](tables/12.4&fig12.2.json) |
| **12.5** | Table 12.5 : WATER DISTRIBUTION IN MALE', BY MONTH 2004 - 2009 (In '000 metric tons) | 2001 – 2025 | 27 | 75 | [`12.5.csv`](tables/12.5.csv) | [`12.5.json`](tables/12.5.json) |
| **12.6** | Table 12.6 : MONTHLY CONSUMPTION OF FUEL FOR ELECTRICITY GENERATION IN SELECTED LOCALITIES BY PUBLIC SECTOR, 2009 (In '000 litres) | 2008 – 2025 | 50 | 62 | [`12.6.csv`](tables/12.6.csv) | [`12.6.json`](tables/12.6.json) |
| **12.7** | Table 12.7 : MONTHLY CONSUMPTION OF LUB OIL FOR ELECTRICITY GENERATION IN SELECTED LOCALITIES BY PUBLIC SECTOR, 2009 (In '000 litres) | 2008 – 2025 | 58 | 56 | [`12.7.csv`](tables/12.7.csv) | [`12.7.json`](tables/12.7.json) |
| **12.8** | Table 12.8 : NUMBER OF CUSTOMERS USING WATER IN MALE' BY TYPE, 2003 - 2009 | 1999 – 2025 | 10 | 57 | [`12.8.csv`](tables/12.8.csv) | [`12.8.json`](tables/12.8.json) |
| **12.9** | Table 12.9 : BILLED WATER CONSUMPTION IN VILLINGILI, 2007 - 2009 | 2001 – 2025 | 20 | 59 | [`12.9.csv`](tables/12.9.csv) | [`12.9.json`](tables/12.9.json) |

## Example SQLite Usage (Python)
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('12_0_electricity_and_water.db')

# Query any metric across all years in milliseconds:
df = pd.read_sql('''
    SELECT item_name, year, value, unit
    FROM master_panel
    WHERE table_id = '10.1' AND year >= 2010
    ORDER BY item_name, year
''', conn)
print(df.head())
```
