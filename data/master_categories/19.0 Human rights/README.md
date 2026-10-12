# 19.0 Human rights — Master Multi-Year Dataset

This directory houses the consolidated multi-year datasets for **19.0 Human rights**, harmonizing data across all official Maldives Statistical Yearbook editions published between **2008 and 2026** by the National Bureau of Statistics (NBS).

## Available Formats
- **Consolidated Panel Dataset ([`master_panel.csv`](master_panel.csv))**: Long-format tabular dataset (7,083 rows) with schema: `[category, table_id, table_title, item_name, metric_name, year, value, unit, edition_year]`.
- **Category SQLite Database ([`19_0_human_rights.db`](19_0_human_rights.db))**: Fully indexed local database containing `master_panel` plus dedicated SQL tables for every individual harmonized table.
- **Harmonized Wide CSVs ([`tables/`](tables/))**: 13 individual multi-year CSV tables with continuous year columns.

## Category Summary
- **Time Horizon Covered**: **1972 – 2026**
- **Total Harmonized Tables**: 13
- **Total Time-Series Observations**: 7,083
- **SQLite Database**: [`19_0_human_rights.db`](19_0_human_rights.db)

## Harmonized Tables Catalog

| Table ID | Title | Time Span | Rows | Cols | Wide CSV | Metadata |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **19.1** |  | 1983 – 2025 | 71 | 31 | [`19.1.csv`](tables/19.1.csv) | [`19.1.json`](tables/19.1.json) |
| **19.10** |  | 1980 | 33 | 10 | [`19.10.csv`](tables/19.10.csv) | [`19.10.json`](tables/19.10.json) |
| **19.11** |  | 1995 | 17 | 10 | [`19.11.csv`](tables/19.11.csv) | [`19.11.json`](tables/19.11.json) |
| **19.12** |  | 1992 | 19 | 11 | [`19.12.csv`](tables/19.12.csv) | [`19.12.json`](tables/19.12.json) |
| **19.13** |  | 1999 | 5 | 12 | [`19.13.csv`](tables/19.13.csv) | [`19.13.json`](tables/19.13.json) |
| **19.2** | Table 2: FISH CATCH BY MONTH, 1985 - 2009 (In metric tons) | 2007 – 2025 | 29 | 35 | [`19.2.csv`](tables/19.2.csv) | [`19.2.json`](tables/19.2.json) |
| **19.3** |  | 1994 – 2026 | 126 | 95 | [`19.3.csv`](tables/19.3.csv) | [`19.3.json`](tables/19.3.json) |
| **19.4** |  | 1972 | 37 | 10 | [`19.4.csv`](tables/19.4.csv) | [`19.4.json`](tables/19.4.json) |
| **19.5** |  | 1995 – 2010 | 26 | 17 | [`19.5.csv`](tables/19.5.csv) | [`19.5.json`](tables/19.5.json) |
| **19.6** |  | 2004 | 25 | 3 | [`19.6.csv`](tables/19.6.csv) | [`19.6.json`](tables/19.6.json) |
| **19.7** |  | 1994 | 19 | 14 | [`19.7.csv`](tables/19.7.csv) | [`19.7.json`](tables/19.7.json) |
| **19.8** |  | 1984 | 32 | 13 | [`19.8.csv`](tables/19.8.csv) | [`19.8.json`](tables/19.8.json) |
| **19.9** |  | 1985 – 2006 | 24 | 16 | [`19.9.csv`](tables/19.9.csv) | [`19.9.json`](tables/19.9.json) |

## Example SQLite Usage (Python)
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('19_0_human_rights.db')

# Query any metric across all years in milliseconds:
df = pd.read_sql('''
    SELECT item_name, year, value, unit
    FROM master_panel
    WHERE table_id = '10.1' AND year >= 2010
    ORDER BY item_name, year
''', conn)
print(df.head())
```
