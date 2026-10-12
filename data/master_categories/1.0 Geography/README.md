# 1.0 Geography — Master Multi-Year Dataset

This directory houses the consolidated multi-year datasets for **1.0 Geography**, harmonizing data across all official Maldives Statistical Yearbook editions published between **2008 and 2026** by the National Bureau of Statistics (NBS).

## Available Formats
- **Consolidated Panel Dataset ([`master_panel.csv`](master_panel.csv))**: Long-format tabular dataset (21,751 rows) with schema: `[category, table_id, table_title, item_name, metric_name, year, value, unit, edition_year]`.
- **Category SQLite Database ([`1_0_geography.db`](1_0_geography.db))**: Fully indexed local database containing `master_panel` plus dedicated SQL tables for every individual harmonized table.
- **Harmonized Wide CSVs ([`tables/`](tables/))**: 10 individual multi-year CSV tables with continuous year columns.

## Category Summary
- **Time Horizon Covered**: **2006 – 2026**
- **Total Harmonized Tables**: 10
- **Total Time-Series Observations**: 21,751
- **SQLite Database**: [`1_0_geography.db`](1_0_geography.db)

## Harmonized Tables Catalog

| Table ID | Title | Time Span | Rows | Cols | Wide CSV | Metadata |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **1.1** | Table 1.1 : SUNSHINE AND RAINFALL, BY MONTH, 2008 | 2009 – 2026 | 18 | 170 | [`1.1.csv`](tables/1.1.csv) | [`1.1.json`](tables/1.1.json) |
| **1.2** | Table 1.2 : AVERAGE OF DAILY MAXIMUM AND MINIMUM TEMPERATURE , BY MONTH, 2009 | 2010 – 2026 | 6 | 183 | [`1.2.csv`](tables/1.2.csv) | [`1.2.json`](tables/1.2.json) |
| **1.2&fig1.2** | Table 1.2 : AVERAGE OF DAILY MAXIMUM AND MINIMUM TEMPERATURE , BY MONTH, 2008 | 2009 – 2011 | 6 | 27 | [`1.2&fig1.2.csv`](tables/1.2&fig1.2.csv) | [`1.2&fig1.2.json`](tables/1.2&fig1.2.json) |
| **1.3** | Table 1.3 : WIND DIRECTION AND SPEED BY MONTH , 2009 | 2010 – 2026 | 5 | 220 | [`1.3.csv`](tables/1.3.csv) | [`1.3.json`](tables/1.3.json) |
| **1.3&1.4** | Table 1.4 : RELATIVE HUMIDITY IN PERCENTAGE BY MONTH , 2008 | 2009 | 5 | 14 | [`1.3&1.4.csv`](tables/1.3&1.4.csv) | [`1.3&1.4.json`](tables/1.3&1.4.json) |
| **1.4** | Table 1.4 : RELATIVE HUMIDITY IN PERCENTAGE BY MONTH , 2009 | 2010 – 2026 | 5 | 209 | [`1.4.csv`](tables/1.4.csv) | [`1.4.json`](tables/1.4.json) |
| **1.4-1** | Table 1.4 : RELATIVE HUMIDITY IN PERCENTAGE BY MONTH , 2018 | 2019 | 5 | 14 | [`1.4-1.csv`](tables/1.4-1.csv) | [`1.4-1.json`](tables/1.4-1.json) |
| **1.5** | Table 1.5 : AREA AND DISTANCE TO MALE' AND ATOLL CAPITALS, BY LOCALITY | 2006 – 2026 | 428 | 83 | [`1.5.csv`](tables/1.5.csv) | [`1.5.json`](tables/1.5.json) |
| **1.5-1** | Table 1.5 : POPULATION , LAND AREA, POPULATION DENSITY AND DISTANCE TO MALE' AND ATOLL CAPITALS, BY LOCALITY | 2014 – 2019 | 189 | 8 | [`1.5-1.csv`](tables/1.5-1.csv) | [`1.5-1.json`](tables/1.5-1.json) |
| **1.6** | Table 1.6 : POPULATION AND AREA DISTIBUTION | 2006 – 2014 | 20 | 22 | [`1.6.csv`](tables/1.6.csv) | [`1.6.json`](tables/1.6.json) |

## Example SQLite Usage (Python)
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('1_0_geography.db')

# Query any metric across all years in milliseconds:
df = pd.read_sql('''
    SELECT item_name, year, value, unit
    FROM master_panel
    WHERE table_id = '10.1' AND year >= 2010
    ORDER BY item_name, year
''', conn)
print(df.head())
```
