# 15.0 Foreign trade & Balance of payments — Master Multi-Year Dataset

This directory houses the consolidated multi-year datasets for **15.0 Foreign trade & Balance of payments**, harmonizing data across all official Maldives Statistical Yearbook editions published between **2008 and 2026** by the National Bureau of Statistics (NBS).

## Available Formats
- **Consolidated Panel Dataset ([`master_panel.csv`](master_panel.csv))**: Long-format tabular dataset (26,643 rows) with schema: `[category, table_id, table_title, item_name, metric_name, year, value, unit, edition_year]`.
- **Category SQLite Database ([`15_0_foreign_trade_balance_of_payments.db`](15_0_foreign_trade_balance_of_payments.db))**: Fully indexed local database containing `master_panel` plus dedicated SQL tables for every individual harmonized table.
- **Harmonized Wide CSVs ([`tables/`](tables/))**: 14 individual multi-year CSV tables with continuous year columns.

## Category Summary
- **Time Horizon Covered**: **2000 – 2026**
- **Total Harmonized Tables**: 14
- **Total Time-Series Observations**: 26,643
- **SQLite Database**: [`15_0_foreign_trade_balance_of_payments.db`](15_0_foreign_trade_balance_of_payments.db)

## Harmonized Tables Catalog

| Table ID | Title | Time Span | Rows | Cols | Wide CSV | Metadata |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **15.1** | Table 15.1 : IMPORTS BY COUNTRY OF CONSIGNMENT, 2005 - 2009 | 2003 – 2025 | 40 | 77 | [`15.1.csv`](tables/15.1.csv) | [`15.1.json`](tables/15.1.json) |
| **15.10** | Table 15.10 : BALANCE OF PAYMENTS, 2011 - 2015 | 2011 – 2025 | 82 | 29 | [`15.10.csv`](tables/15.10.csv) | [`15.10.json`](tables/15.10.json) |
| **15.11** | Table 15.11: Monthly Exports, millions, 2020 - 2024 | 2020 – 2025 | 13 | 7 | [`15.11.csv`](tables/15.11.csv) | [`15.11.json`](tables/15.11.json) |
| **15.12** | Table 15.12 : BALANCE OF PAYMENTS, 2011 - 2024 | 2011 – 2024 | 22 | 15 | [`15.12.csv`](tables/15.12.csv) | [`15.12.json`](tables/15.12.json) |
| **15.1fig15.1** | Table 15.1 : IMPORTS BY COUNTRY OF CONSIGNMENT, 2006 - 2010 | 2003 – 2011 | 39 | 13 | [`15.1fig15.1.csv`](tables/15.1fig15.1.csv) | [`15.1fig15.1.json`](tables/15.1fig15.1.json) |
| **15.2** | Table 15:2 : SUMMARY OF IMPORTS CLASSIFIED BY HARMONIZED SYSTEM ,2006 - 2009 | 2006 – 2026 | 22 | 106 | [`15.2.csv`](tables/15.2.csv) | [`15.2.json`](tables/15.2.json) |
| **15.3** | Table 15.3 : EXPORTS BY COMMODITY, 2009 | 2010 – 2026 | 224 | 28 | [`15.3.csv`](tables/15.3.csv) | [`15.3.json`](tables/15.3.json) |
| **15.3&fig15.2** | Table 15.3 : EXPORTS BY COMMODITY, 2010 | 2011 | 73 | 8 | [`15.3&fig15.2.csv`](tables/15.3&fig15.2.csv) | [`15.3&fig15.2.json`](tables/15.3&fig15.2.json) |
| **15.4** | Table 15.4 : EXPORTS BY COUNTRY OF DESTINATION, 2005 - 2009 | 2003 – 2026 | 35 | 60 | [`15.4.csv`](tables/15.4.csv) | [`15.4.json`](tables/15.4.json) |
| **15.5** | Table 15.5 : MARINE PRODUCT EXPORTS BY THE PRIVATE SECTOR BY COUNTRY OF DESTINATION, 2005 - 2009 | 2003 – 2024 | 57 | 58 | [`15.5.csv`](tables/15.5.csv) | [`15.5.json`](tables/15.5.json) |
| **15.6** | Table 15.6 : BALANCE OF PAYMENTS, 2007 - 2009 (In millions of U.S. dollars) | 2000 – 2024 | 129 | 37 | [`15.6.csv`](tables/15.6.csv) | [`15.6.json`](tables/15.6.json) |
| **15.7** | Table 15.7 : IMPORTS CLASSIFIED BY HARMONIZED SYSTEM , 2005 - 2009 | 2000 – 2025 | 138 | 150 | [`15.7.csv`](tables/15.7.csv) | [`15.7.json`](tables/15.7.json) |
| **15.8** | Table 15.8 : IMPORTS CLASSIFIED BY HARMONIZED SYSTEM , 2006 - 2010 | 2005 – 2025 | 135 | 78 | [`15.8.csv`](tables/15.8.csv) | [`15.8.json`](tables/15.8.json) |
| **15.9** | Table 5.9: IMPORTS OF TOBACCO, 2000 - 2010 | 2011 – 2026 | 43 | 64 | [`15.9.csv`](tables/15.9.csv) | [`15.9.json`](tables/15.9.json) |

## Example SQLite Usage (Python)
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('15_0_foreign_trade_balance_of_payments.db')

# Query any metric across all years in milliseconds:
df = pd.read_sql('''
    SELECT item_name, year, value, unit
    FROM master_panel
    WHERE table_id = '10.1' AND year >= 2010
    ORDER BY item_name, year
''', conn)
print(df.head())
```
