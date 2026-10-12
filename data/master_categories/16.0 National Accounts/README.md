# 16.0 National Accounts — Master Multi-Year Dataset

This directory houses the consolidated multi-year datasets for **16.0 National Accounts**, harmonizing data across all official Maldives Statistical Yearbook editions published between **2008 and 2026** by the National Bureau of Statistics (NBS).

## Available Formats
- **Consolidated Panel Dataset ([`master_panel.csv`](master_panel.csv))**: Long-format tabular dataset (41,508 rows) with schema: `[category, table_id, table_title, item_name, metric_name, year, value, unit, edition_year]`.
- **Category SQLite Database ([`16_0_national_accounts.db`](16_0_national_accounts.db))**: Fully indexed local database containing `master_panel` plus dedicated SQL tables for every individual harmonized table.
- **Harmonized Wide CSVs ([`tables/`](tables/))**: 22 individual multi-year CSV tables with continuous year columns.

## Category Summary
- **Time Horizon Covered**: **1995 – 2026**
- **Total Harmonized Tables**: 22
- **Total Time-Series Observations**: 41,508
- **SQLite Database**: [`16_0_national_accounts.db`](16_0_national_accounts.db)

## Harmonized Tables Catalog

| Table ID | Title | Time Span | Rows | Cols | Wide CSV | Metadata |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **16.1** | Table 16.1 : GROSS DOMESTIC PRODUCT, BY KIND OF ACTIVITY , 2003 - 2010 (Estimated using production approach) | 1995 – 2026 | 40 | 122 | [`16.1.csv`](tables/16.1.csv) | [`16.1.json`](tables/16.1.json) |
| **16.10** | Table 16.10 : QUARTERLY GROSS DOMESTIC PRODUCT (AT CONSTANT PRICES),GROWTH RATES (CORRESPONDING QUARTER), BY KIND OF ACTIVITY, 2004 - 2018 | 2003 – 2023 | 30 | 96 | [`16.10.csv`](tables/16.10.csv) | [`16.10.json`](tables/16.10.json) |
| **16.11** | Table 16.11 : GROSS DOMESTIC PRODUCT (AT CONSTANT PRICES),GROWTH RATES (PRECEDING QUARTER), BY KIND OF ACTIVITY, 2003 - 2018 | 2003 – 2023 | 30 | 85 | [`16.11.csv`](tables/16.11.csv) | [`16.11.json`](tables/16.11.json) |
| **16.12** | Table 16.12 : GROSS DOMESTIC PRODUCT (AT CONSTANT PRICES),GROWTH RATES (PRECEDING QUARTER), BY KIND OF ACTIVITY, 2003 - 2019 | 2003 – 2023 | 30 | 90 | [`16.12.csv`](tables/16.12.csv) | [`16.12.json`](tables/16.12.json) |
| **16.13** | Table 16.13: SUPPLY AND USE TABLE FOR MALDIVES 2014 - Aggregated by industry and Product (In million MVR) | 2003 – 2026 | 66 | 229 | [`16.13.csv`](tables/16.13.csv) | [`16.13.json`](tables/16.13.json) |
| **16.14** | Table 16.14: GROSS DOMESTIC PRODUCT (AT CONSTANT PRICES), BY KIND OF ACTIVITY, 2014 - 2019 | 2003 – 2026 | 30 | 147 | [`16.14.csv`](tables/16.14.csv) | [`16.14.json`](tables/16.14.json) |
| **16.15** | Table 16.15: GROSS DOMESTIC PRODUCT (AT CONSTANT PRICES), BY KIND OF ACTIVITY, 2015 -2019 | 2004 – 2026 | 30 | 138 | [`16.15.csv`](tables/16.15.csv) | [`16.15.json`](tables/16.15.json) |
| **16.16** | Table 16.16: GROSS DOMESTIC PRODUCT (AT CURRENTPRICES), BY KIND OF ACTIVITY, 2014-2019 | 2003 – 2026 | 29 | 102 | [`16.16.csv`](tables/16.16.csv) | [`16.16.json`](tables/16.16.json) |
| **16.17** | Table 16.17: GROSS DOMESTIC PRODUCT (AT CURRENT PRICES), BY KIND OF ACTIVITY, 2015 - 2019 | 2004 – 2026 | 30 | 138 | [`16.17.csv`](tables/16.17.csv) | [`16.17.json`](tables/16.17.json) |
| **16.18** | TABLE 16.18: GROSS DOMESTIC PRODUCT (AT CURRENT PRICES), BY KIND OF ACTIVITY , 2014Q1 - 2025Q4 | 2014 – 2026 | 15 | 50 | [`16.18.csv`](tables/16.18.csv) | [`16.18.json`](tables/16.18.json) |
| **16.19** | TABLE 16.19: GROSS DOMESTIC PRODUCT (AT CURRENT PRICES), PERCENTAGE SHARE, BY KIND OF ACTIVITY, 2014Q1 - 2025Q4 | 2014 – 2026 | 15 | 50 | [`16.19.csv`](tables/16.19.csv) | [`16.19.json`](tables/16.19.json) |
| **16.2** | Table 16.2 : GROSS DOMESTIC PRODUCT,GROWTH RATES, BY KIND OF ACTIVITY, 2004 - 2010 (Estimated using production approach) | 1995 – 2026 | 25 | 110 | [`16.2.csv`](tables/16.2.csv) | [`16.2.json`](tables/16.2.json) |
| **16.20** | TABLE 16.20: GROSS DOMESTIC PRODUCT (AT CURRENT PRICES), GROWTH RATES (CORRESPONDING QUARTER), BY KIND OF ACTIVITY, 2015Q1 - 2025Q4 | 2015 – 2026 | 15 | 46 | [`16.20.csv`](tables/16.20.csv) | [`16.20.json`](tables/16.20.json) |
| **16.21** | TABLE 16.21: GROSS DOMESTIC PRODUCT (AT CURRENT PRICES), GROWTH RATES (PRECEDING QUARTER), BY KIND OF ACTIVITY, 2014Q2 - 2025Q4 | 2014 – 2026 | 15 | 49 | [`16.21.csv`](tables/16.21.csv) | [`16.21.json`](tables/16.21.json) |
| **16.22** | TABLE 16.22: GROSS DOMESTIC PRODUCT (AT CURRENT), CONTRIBUTION TO GROWTH, BY KIND OF ACTIVITY, 2015Q1 - 2025Q4 | 2015 – 2026 | 15 | 46 | [`16.22.csv`](tables/16.22.csv) | [`16.22.json`](tables/16.22.json) |
| **16.3** | Table 16.3 : PERCENTAGE SHARES OF GROSS DOMESTIC PRODUCT, BY KIND OF ACTIVITY, 2004 - 2010 (Estimated using production approach) | 1995 – 2026 | 21 | 112 | [`16.3.csv`](tables/16.3.csv) | [`16.3.json`](tables/16.3.json) |
| **16.4** | Table 16.4: SUPPLY AND USE TABLE FOR MALDIVES 2003 - Aggregated by industry and Product (In million Rf) | 2003 – 2026 | 68 | 134 | [`16.4.csv`](tables/16.4.csv) | [`16.4.json`](tables/16.4.json) |
| **16.5** | Table 16.5 : GROSS DOMESTIC PRODUCT (AT CURRENT PRICES),GROWTH RATES, BY KIND OF ACTIVITY, 2003 - 2011 | 2003 – 2026 | 23 | 85 | [`16.5.csv`](tables/16.5.csv) | [`16.5.json`](tables/16.5.json) |
| **16.6** | Table 16.6 : PERCENTAGE SHARES OF GROSS DOMESTIC PRODUCT(AT CURRENT PRICES), BY KIND OF ACTIVITY, 2003 - 2011 | 2003 – 2026 | 21 | 86 | [`16.6.csv`](tables/16.6.csv) | [`16.6.json`](tables/16.6.json) |
| **16.7** | Table 16.7: SUPPLY AND USE TABLE FOR MALDIVES 2003 - Aggregated by industry and Product (In million Rf) | 1996 – 2026 | 98 | 248 | [`16.7.csv`](tables/16.7.csv) | [`16.7.json`](tables/16.7.json) |
| **16.8** | Table 16.8 : QUARTERLY GROSS DOMESTIC PRODUCT (AT CONSTANT PRICES), BY KIND OF ACTIVITY, 2003 - 2018 | 2003 – 2026 | 20 | 98 | [`16.8.csv`](tables/16.8.csv) | [`16.8.json`](tables/16.8.json) |
| **16.9** | Table 16.9 : PERCENTAGE SHARES OF QUARTERLY GROSS DOMESTIC PRODUCT (AT CONSTANT PRICES), BY KIND OF ACTIVITY, 2003 - 2018 | 2003 – 2024 | 30 | 125 | [`16.9.csv`](tables/16.9.csv) | [`16.9.json`](tables/16.9.json) |

## Example SQLite Usage (Python)
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('16_0_national_accounts.db')

# Query any metric across all years in milliseconds:
df = pd.read_sql('''
    SELECT item_name, year, value, unit
    FROM master_panel
    WHERE table_id = '10.1' AND year >= 2010
    ORDER BY item_name, year
''', conn)
print(df.head())
```
