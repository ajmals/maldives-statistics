# 13.0 Public Finance — Master Multi-Year Dataset

This directory houses the consolidated multi-year datasets for **13.0 Public Finance**, harmonizing data across all official Maldives Statistical Yearbook editions published between **2008 and 2026** by the National Bureau of Statistics (NBS).

## Available Formats
- **Consolidated Panel Dataset ([`master_panel.csv`](master_panel.csv))**: Long-format tabular dataset (26,545 rows) with schema: `[category, table_id, table_title, item_name, metric_name, year, value, unit, edition_year]`.
- **Category SQLite Database ([`13_0_public_finance.db`](13_0_public_finance.db))**: Fully indexed local database containing `master_panel` plus dedicated SQL tables for every individual harmonized table.
- **Harmonized Wide CSVs ([`tables/`](tables/))**: 14 individual multi-year CSV tables with continuous year columns.

## Category Summary
- **Time Horizon Covered**: **2001 – 2027**
- **Total Harmonized Tables**: 14
- **Total Time-Series Observations**: 26,545
- **SQLite Database**: [`13_0_public_finance.db`](13_0_public_finance.db)

## Harmonized Tables Catalog

| Table ID | Title | Time Span | Rows | Cols | Wide CSV | Metadata |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **13.1** | Table 13.1 : TOTAL REVENUE AND EXPENDITURE OF GOVERNMENT BUDGET BY SOURCE,2007 - 2011 | 2007 – 2027 | 64 | 69 | [`13.1.csv`](tables/13.1.csv) | [`13.1.json`](tables/13.1.json) |
| **13.10** | Table 13.10 : FOREIGN LOANS BY LENDING AGENCY, 2005 - 2011 (In million Rf) | 2005 – 2025 | 47 | 53 | [`13.10.csv`](tables/13.10.csv) | [`13.10.json`](tables/13.10.json) |
| **13.11** | Table 13.11 : FOREIGN GRANTS BY PRINCIPAL DONORS, 2005 - 2011 | 2005 – 2025 | 116 | 83 | [`13.11.csv`](tables/13.11.csv) | [`13.11.json`](tables/13.11.json) |
| **13.12** |  | 2011 – 2025 | 119 | 77 | [`13.12.csv`](tables/13.12.csv) | [`13.12.json`](tables/13.12.json) |
| **13.13** |  | 2011 – 2025 | 112 | 75 | [`13.13.csv`](tables/13.13.csv) | [`13.13.json`](tables/13.13.json) |
| **13.14** |  | 2011 – 2018 | 56 | 37 | [`13.14.csv`](tables/13.14.csv) | [`13.14.json`](tables/13.14.json) |
| **13.2** | Table 13.2 : SUMMARY OF CENTRAL GOVERNMENT FINANCE, 2007 - 2011 | 2007 – 2026 | 61 | 80 | [`13.2.csv`](tables/13.2.csv) | [`13.2.json`](tables/13.2.json) |
| **13.3** | Table 13.3 : GOVERNMENT REVENUE, 2007-2011 | 2007 – 2027 | 84 | 61 | [`13.3.csv`](tables/13.3.csv) | [`13.3.json`](tables/13.3.json) |
| **13.4** | Table 13.4 : ECONOMIC CLASSIFICATION OF CENTRAL GOVERNMENT EXPENDITURE AND NET LENDING, 2007 - 2011 | 2007 – 2027 | 52 | 88 | [`13.4.csv`](tables/13.4.csv) | [`13.4.json`](tables/13.4.json) |
| **13.5** | Table 13.5 : FUNCTIONAL CLASSIFICATION OF CENTRAL GOVERNMENT EXPENDITURE,2007- 2011 | 2007 – 2019 | 155 | 100 | [`13.5.csv`](tables/13.5.csv) | [`13.5.json`](tables/13.5.json) |
| **13.6** | Table 13.6 : FUNCTIONAL CLASSIFICATION OF CENTRAL GOVERNMENT CURRENT EXPENDITURE, 2007- 2011 | 2004 – 2025 | 154 | 140 | [`13.6.csv`](tables/13.6.csv) | [`13.6.json`](tables/13.6.json) |
| **13.7** | Table 13.7 : FUNCTIONAL CLASSIFICATION OF CENTRAL GOVERNMENT CAPITAL EXPENDITURE, 2007-2011 | 2004 – 2027 | 349 | 103 | [`13.7.csv`](tables/13.7.csv) | [`13.7.json`](tables/13.7.json) |
| **13.8** | Table 13.8 : SUMMARY OF EXTERNAL PUBLIC DEBT, 2001 - 2011 | 2001 – 2027 | 51 | 90 | [`13.8.csv`](tables/13.8.csv) | [`13.8.json`](tables/13.8.json) |
| **13.9** | Table 13.9 : EXPENDITURE ON MAJOR PROJECTS FINANCED BY FOREIGN LOANS, 2005 - 2011 | 2005 – 2025 | 171 | 74 | [`13.9.csv`](tables/13.9.csv) | [`13.9.json`](tables/13.9.json) |

## Example SQLite Usage (Python)
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('13_0_public_finance.db')

# Query any metric across all years in milliseconds:
df = pd.read_sql('''
    SELECT item_name, year, value, unit
    FROM master_panel
    WHERE table_id = '10.1' AND year >= 2010
    ORDER BY item_name, year
''', conn)
print(df.head())
```
