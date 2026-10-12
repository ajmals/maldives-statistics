# 17.0 Prices — Master Multi-Year Dataset

This directory houses the consolidated multi-year datasets for **17.0 Prices**, harmonizing data across all official Maldives Statistical Yearbook editions published between **2008 and 2026** by the National Bureau of Statistics (NBS).

## Available Formats
- **Consolidated Panel Dataset ([`master_panel.csv`](master_panel.csv))**: Long-format tabular dataset (22,248 rows) with schema: `[category, table_id, table_title, item_name, metric_name, year, value, unit, edition_year]`.
- **Category SQLite Database ([`17_0_prices.db`](17_0_prices.db))**: Fully indexed local database containing `master_panel` plus dedicated SQL tables for every individual harmonized table.
- **Harmonized Wide CSVs ([`tables/`](tables/))**: 17 individual multi-year CSV tables with continuous year columns.

## Category Summary
- **Time Horizon Covered**: **1998 – 2025**
- **Total Harmonized Tables**: 17
- **Total Time-Series Observations**: 22,248
- **SQLite Database**: [`17_0_prices.db`](17_0_prices.db)

## Harmonized Tables Catalog

| Table ID | Title | Time Span | Rows | Cols | Wide CSV | Metadata |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **17.1** | Table 17.1 : CONSUMER PRICE INDEX, 2007 - 2008 | 2004 – 2022 | 68 | 45 | [`17.1.csv`](tables/17.1.csv) | [`17.1.json`](tables/17.1.json) |
| **17.10** | Table 17.10 : PRICE CHANGES IN FUEL OIL, 2007 - 2014 | 2004 – 2021 | 27 | 25 | [`17.10.csv`](tables/17.10.csv) | [`17.10.json`](tables/17.10.json) |
| **17.11** | Table 17.11 : INDICES FOR SELECTED EXPORT ITEMS, 2004 - 2014 | 2004 – 2025 | 26 | 27 | [`17.11.csv`](tables/17.11.csv) | [`17.11.json`](tables/17.11.json) |
| **17.12** | Table 17.12 : QUANTITY, VALUE AND UNIT VALUES FOR SELECTED EXPORT ITEMS, 2006 - 2014 | 2004 – 2015 | 16 | 28 | [`17.12.csv`](tables/17.12.csv) | [`17.12.json`](tables/17.12.json) |
| **17.13** | Table 17.13 : EXCHANGE RATES, 2010 - 2014 | 2004 – 2021 | 19 | 60 | [`17.13.csv`](tables/17.13.csv) | [`17.13.json`](tables/17.13.json) |
| **17.14** | Table 17.14 : EXCHANGE RATES, 2011 - 2015 | 2010 – 2025 | 9 | 65 | [`17.14.csv`](tables/17.14.csv) | [`17.14.json`](tables/17.14.json) |
| **17.2** | Table 17.2 : CONSUMER PRICE INDEX, BY MONTH, 2006 - 2008 | 2004 – 2022 | 45 | 110 | [`17.2.csv`](tables/17.2.csv) | [`17.2.json`](tables/17.2.json) |
| **17.3** | Table 17.3 :PRICES OF SELECTED COMMODITIES,2007 - 2009 | 2004 – 2022 | 41 | 138 | [`17.3.csv`](tables/17.3.csv) | [`17.3.json`](tables/17.3.json) |
| **17.4** | Table 17.4 : EXCHANGE RATES, 2007 - 2008 | 2007 – 2022 | 44 | 156 | [`17.4.csv`](tables/17.4.csv) | [`17.4.json`](tables/17.4.json) |
| **17.5** | Table 17.5 : PRICE CHANGES IN FUEL OIL, 2003 - 2008 | 2009 – 2022 | 41 | 132 | [`17.5.csv`](tables/17.5.csv) | [`17.5.json`](tables/17.5.json) |
| **17.5-1** | Table 17.5 : CONSUMER PRICE INDEX, 2010 - 2018 | 2012 | 19 | 20 | [`17.5-1.csv`](tables/17.5-1.csv) | [`17.5-1.json`](tables/17.5-1.json) |
| **17.6** | Table 17.6 : INDICES FOR SELECTED EXPORT ITEMS, 2005 -2008 | 1998 – 2022 | 44 | 167 | [`17.6.csv`](tables/17.6.csv) | [`17.6.json`](tables/17.6.json) |
| **17.6-2** | Table 17.6 : CONSUMER PRICE INDEX, FOR MALE' AND ATOLLS BY MONTH, 2018 | 2012 | 20 | 14 | [`17.6-2.csv`](tables/17.6-2.csv) | [`17.6-2.json`](tables/17.6-2.json) |
| **17.7** | Table 17.7 : QUANTITY, VALUE AND UNIT VALUES FOR SELECTED EXPORT ITEMS, 2005 - 2008 | 2003 – 2022 | 46 | 157 | [`17.7.csv`](tables/17.7.csv) | [`17.7.json`](tables/17.7.json) |
| **17.7-1** | Table 17.7 : MONTHLY INFLATION RATE, 2018 | 2012 | 21 | 14 | [`17.7-1.csv`](tables/17.7-1.csv) | [`17.7-1.json`](tables/17.7-1.json) |
| **17.8** | Table 17.8 Producer Price Indices by Industry, 2001‐2009 | 2001 – 2019 | 60 | 159 | [`17.8.csv`](tables/17.8.csv) | [`17.8.json`](tables/17.8.json) |
| **17.9** | Table 17.9: INFLATION IN PRODUCER PRICES BY INDUSTRY, 2002 - 2009 | 2002 – 2020 | 36 | 90 | [`17.9.csv`](tables/17.9.csv) | [`17.9.json`](tables/17.9.json) |

## Example SQLite Usage (Python)
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('17_0_prices.db')

# Query any metric across all years in milliseconds:
df = pd.read_sql('''
    SELECT item_name, year, value, unit
    FROM master_panel
    WHERE table_id = '10.1' AND year >= 2010
    ORDER BY item_name, year
''', conn)
print(df.head())
```
