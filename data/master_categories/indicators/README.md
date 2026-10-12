# indicators — Master Multi-Year Dataset

This directory houses the consolidated multi-year datasets for **indicators**, harmonizing data across all official Maldives Statistical Yearbook editions published between **2008 and 2026** by the National Bureau of Statistics (NBS).

## Available Formats
- **Consolidated Panel Dataset ([`master_panel.csv`](master_panel.csv))**: Long-format tabular dataset (13,517 rows) with schema: `[category, table_id, table_title, item_name, metric_name, year, value, unit, edition_year]`.
- **Category SQLite Database ([`indicators.db`](indicators.db))**: Fully indexed local database containing `master_panel` plus dedicated SQL tables for every individual harmonized table.
- **Harmonized Wide CSVs ([`tables/`](tables/))**: 26 individual multi-year CSV tables with continuous year columns.

## Category Summary
- **Time Horizon Covered**: **1990 – 2021**
- **Total Harmonized Tables**: 26
- **Total Time-Series Observations**: 13,517
- **SQLite Database**: [`indicators.db`](indicators.db)

## Harmonized Tables Catalog

| Table ID | Title | Time Span | Rows | Cols | Wide CSV | Metadata |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **20.1** |  | 2010 | 220 | 13 | [`20.1.csv`](tables/20.1.csv) | [`20.1.json`](tables/20.1.json) |
| **20.2** |  | 2010 | 220 | 11 | [`20.2.csv`](tables/20.2.csv) | [`20.2.json`](tables/20.2.json) |
| **20.3** |  | 2010 | 221 | 10 | [`20.3.csv`](tables/20.3.csv) | [`20.3.json`](tables/20.3.json) |
| **Annual-national-accounts** |  | 2003 – 2018 | 9 | 16 | [`Annual-national-accounts.csv`](tables/Annual-national-accounts.csv) | [`Annual-national-accounts.json`](tables/Annual-national-accounts.json) |
| **Education** |  | 2006 – 2021 | 20 | 46 | [`Education.csv`](tables/Education.csv) | [`Education.json`](tables/Education.json) |
| **Electricity-and-Water** |  | 2006 – 2021 | 13 | 47 | [`Electricity-and-Water.csv`](tables/Electricity-and-Water.csv) | [`Electricity-and-Water.json`](tables/Electricity-and-Water.json) |
| **Employment** |  | 2006 – 2021 | 10 | 38 | [`Employment.csv`](tables/Employment.csv) | [`Employment.json`](tables/Employment.json) |
| **Fisheries-Agriculture** | Table Fisheries-Agriculture | 2021 | 12 | 52 | [`Fisheries-Agriculture.csv`](tables/Fisheries-Agriculture.csv) | [`Fisheries-Agriculture.json`](tables/Fisheries-Agriculture.json) |
| **Fisheries-and-Agriculture** |  | 2005 – 2017 | 11 | 14 | [`Fisheries-and-Agriculture.csv`](tables/Fisheries-and-Agriculture.csv) | [`Fisheries-and-Agriculture.json`](tables/Fisheries-and-Agriculture.json) |
| **Foreign-Trade-and-BOP** |  | 1995 – 2021 | 24 | 54 | [`Foreign-Trade-and-BOP.csv`](tables/Foreign-Trade-and-BOP.csv) | [`Foreign-Trade-and-BOP.json`](tables/Foreign-Trade-and-BOP.json) |
| **Foreign-Trade-and-Balance-of-Payment** |  | 2006 – 2017 | 22 | 13 | [`Foreign-Trade-and-Balance-of-Payment.csv`](tables/Foreign-Trade-and-Balance-of-Payment.csv) | [`Foreign-Trade-and-Balance-of-Payment.json`](tables/Foreign-Trade-and-Balance-of-Payment.json) |
| **Geography** |  | 2006 – 2021 | 14 | 39 | [`Geography.csv`](tables/Geography.csv) | [`Geography.json`](tables/Geography.json) |
| **Health** |  | 2006 – 2021 | 10 | 24 | [`Health.csv`](tables/Health.csv) | [`Health.json`](tables/Health.json) |
| **KeyIndicators_08** |  | 2008 | 1 | 16 | [`KeyIndicators_08.csv`](tables/KeyIndicators_08.csv) | [`KeyIndicators_08.json`](tables/KeyIndicators_08.json) |
| **Law-and-Order** |  | 2006 – 2021 | 9 | 42 | [`Law-and-Order.csv`](tables/Law-and-Order.csv) | [`Law-and-Order.json`](tables/Law-and-Order.json) |
| **Law-and-order** |  | 2006 – 2017 | 8 | 13 | [`Law-and-order.csv`](tables/Law-and-order.csv) | [`Law-and-order.json`](tables/Law-and-order.json) |
| **Money-and-Banking** |  | 2006 – 2021 | 24 | 33 | [`Money-and-Banking.csv`](tables/Money-and-Banking.csv) | [`Money-and-Banking.json`](tables/Money-and-Banking.json) |
| **National-Accounts** |  | 1990 – 2021 | 12 | 54 | [`National-Accounts.csv`](tables/National-Accounts.csv) | [`National-Accounts.json`](tables/National-Accounts.json) |
| **Pension-and-Social-Protection** |  | 2011 – 2021 | 13 | 18 | [`Pension-and-Social-Protection.csv`](tables/Pension-and-Social-Protection.csv) | [`Pension-and-Social-Protection.json`](tables/Pension-and-Social-Protection.json) |
| **Political-parties-Elections** |  | 2011 – 2021 | 10 | 30 | [`Political-parties-Elections.csv`](tables/Political-parties-Elections.csv) | [`Political-parties-Elections.json`](tables/Political-parties-Elections.json) |
| **Population** |  | 2006 – 2021 | 36 | 24 | [`Population.csv`](tables/Population.csv) | [`Population.json`](tables/Population.json) |
| **Poverty** |  | 2002 – 2021 | 11 | 15 | [`Poverty.csv`](tables/Poverty.csv) | [`Poverty.json`](tables/Poverty.json) |
| **Prices** |  | 2006 – 2021 | 8 | 46 | [`Prices.csv`](tables/Prices.csv) | [`Prices.json`](tables/Prices.json) |
| **Public-Finance** |  | 2006 – 2021 | 26 | 39 | [`Public-Finance.csv`](tables/Public-Finance.csv) | [`Public-Finance.json`](tables/Public-Finance.json) |
| **Tourism** |  | 2006 – 2021 | 22 | 25 | [`Tourism.csv`](tables/Tourism.csv) | [`Tourism.json`](tables/Tourism.json) |
| **Transport-and-Communication** |  | 2006 – 2021 | 19 | 27 | [`Transport-and-Communication.csv`](tables/Transport-and-Communication.csv) | [`Transport-and-Communication.json`](tables/Transport-and-Communication.json) |

## Example SQLite Usage (Python)
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('indicators.db')

# Query any metric across all years in milliseconds:
df = pd.read_sql('''
    SELECT item_name, year, value, unit
    FROM master_panel
    WHERE table_id = '10.1' AND year >= 2010
    ORDER BY item_name, year
''', conn)
print(df.head())
```
