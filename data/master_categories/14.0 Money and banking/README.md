# 14.0 Money and banking — Master Multi-Year Dataset

This directory houses the consolidated multi-year datasets for **14.0 Money and banking**, harmonizing data across all official Maldives Statistical Yearbook editions published between **2008 and 2026** by the National Bureau of Statistics (NBS).

## Available Formats
- **Consolidated Panel Dataset ([`master_panel.csv`](master_panel.csv))**: Long-format tabular dataset (20,445 rows) with schema: `[category, table_id, table_title, item_name, metric_name, year, value, unit, edition_year]`.
- **Category SQLite Database ([`14_0_money_and_banking.db`](14_0_money_and_banking.db))**: Fully indexed local database containing `master_panel` plus dedicated SQL tables for every individual harmonized table.
- **Harmonized Wide CSVs ([`tables/`](tables/))**: 17 individual multi-year CSV tables with continuous year columns.

## Category Summary
- **Time Horizon Covered**: **2001 – 2025**
- **Total Harmonized Tables**: 17
- **Total Time-Series Observations**: 20,445
- **SQLite Database**: [`14_0_money_and_banking.db`](14_0_money_and_banking.db)

## Harmonized Tables Catalog

| Table ID | Title | Time Span | Rows | Cols | Wide CSV | Metadata |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **14.1** | Table 14.1: ASSETS AND LIABILITIES OF MALDIVES MONETARY AUTHORITY 2008 - 2009 (In millions of Rufiyaa; end of period) | 2008 – 2025 | 67 | 101 | [`14.1.csv`](tables/14.1.csv) | [`14.1.json`](tables/14.1.json) |
| **14.10** | Table 14.10: Interest Rates, 2001 - 2014 | 2001 – 2025 | 30 | 37 | [`14.10.csv`](tables/14.10.csv) | [`14.10.json`](tables/14.10.json) |
| **14.11** | Table 14.11: Financial Soundness Indicator, 2015 - 2020 | 2015 – 2025 | 20 | 45 | [`14.11.csv`](tables/14.11.csv) | [`14.11.json`](tables/14.11.json) |
| **14.12** | Table 14.12: Financial Access Survey, 2004 - 2019 | 2004 – 2025 | 15 | 23 | [`14.12.csv`](tables/14.12.csv) | [`14.12.json`](tables/14.12.json) |
| **14.13** | Table 14.13: Key Indicators of General Insurance Business, 2015 - 2020 | 2015 – 2025 | 14 | 45 | [`14.13.csv`](tables/14.13.csv) | [`14.13.json`](tables/14.13.json) |
| **14.14** | Table 14.14: Insurance Premium and Claims by Class, 2015 - 2020 | 2015 – 2025 | 12 | 45 | [`14.14.csv`](tables/14.14.csv) | [`14.14.json`](tables/14.14.json) |
| **14.15** | Table 14.15: Assets and Liabilities of Insurance Corporations, 2015 - 2020 | 2015 – 2025 | 15 | 45 | [`14.15.csv`](tables/14.15.csv) | [`14.15.json`](tables/14.15.json) |
| **14.16** | Table 14.16: RESERVE DATA TEMPLATE, 2015 - 2020 1/ | 2015 – 2025 | 17 | 45 | [`14.16.csv`](tables/14.16.csv) | [`14.16.json`](tables/14.16.json) |
| **14.2** | Table 14.2: CENTRAL BANK SURVEY, 2008 - 2009 (In millions of Rufiyaa; end of period) | 2008 – 2025 | 37 | 102 | [`14.2.csv`](tables/14.2.csv) | [`14.2.json`](tables/14.2.json) |
| **14.3** | Table 14.3 :ASSETS AND LIABILITIES OF OTHER DEPOSITORY CORPORATIONS, 2008 - 2009 (In millions of Rufiyaa; end of period) | 2008 – 2025 | 62 | 94 | [`14.3.csv`](tables/14.3.csv) | [`14.3.json`](tables/14.3.json) |
| **14.4** | Table 14.4 :OTHER DEPOSITORY CORPORATIONS SURVEY , 2008 - 2009 (In millions of Rufiyaa; end of period) | 2008 – 2025 | 60 | 95 | [`14.4.csv`](tables/14.4.csv) | [`14.4.json`](tables/14.4.json) |
| **14.5** | Table 14.5 : DEPOSITORY CORPORATIONS SURVEY, 2008 - 2009 (In millions of Rufiyaa; end of period) | 2008 – 2025 | 57 | 112 | [`14.5.csv`](tables/14.5.csv) | [`14.5.json`](tables/14.5.json) |
| **14.6** | Table 14.6 : OTHER DEPOSITORY CORPORATIONS PRIVATE SECTOR LOANS & ADVANCES BY ECONOMIC GROUP, 2008 - 2009 (In millions of Rufiyaa; end of period) | 2008 – 2025 | 46 | 115 | [`14.6.csv`](tables/14.6.csv) | [`14.6.json`](tables/14.6.json) |
| **14.7** | Table 14.7: Interest Rates, 2001 - 2012 | 2001 – 2025 | 50 | 82 | [`14.7.csv`](tables/14.7.csv) | [`14.7.json`](tables/14.7.json) |
| **14.7-1** | Table 14.7 :ASSETS AND LIABILITIES OF OTHER DEPOSITORY CORPORATIONS, 2015 - 2018 | 2015 – 2019 | 29 | 17 | [`14.7-1.csv`](tables/14.7-1.csv) | [`14.7-1.json`](tables/14.7-1.json) |
| **14.8** | Table 14.8: ASSETS AND LIABILITIES OF OTHER FINANCIAL CORPORATIONS, 2011 - 2014 | 2012 – 2025 | 20 | 75 | [`14.8.csv`](tables/14.8.csv) | [`14.8.json`](tables/14.8.json) |
| **14.9** | Table 14.9 : OTHER DEPOSITORY CORPORATIONS PRIVATE SECTOR LOANS & ADVANCES BY ECONOMIC GROUP, 2011 - 2014 | 2012 – 2025 | 19 | 63 | [`14.9.csv`](tables/14.9.csv) | [`14.9.json`](tables/14.9.json) |

## Example SQLite Usage (Python)
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('14_0_money_and_banking.db')

# Query any metric across all years in milliseconds:
df = pd.read_sql('''
    SELECT item_name, year, value, unit
    FROM master_panel
    WHERE table_id = '10.1' AND year >= 2010
    ORDER BY item_name, year
''', conn)
print(df.head())
```
