# 2.0 Environment — Master Multi-Year Dataset

This directory houses the consolidated multi-year datasets for **2.0 Environment**, harmonizing data across all official Maldives Statistical Yearbook editions published between **2008 and 2026** by the National Bureau of Statistics (NBS).

## Available Formats
- **Consolidated Panel Dataset ([`master_panel.csv`](master_panel.csv))**: Long-format tabular dataset (4,365 rows) with schema: `[category, table_id, table_title, item_name, metric_name, year, value, unit, edition_year]`.
- **Category SQLite Database ([`2_0_environment.db`](2_0_environment.db))**: Fully indexed local database containing `master_panel` plus dedicated SQL tables for every individual harmonized table.
- **Harmonized Wide CSVs ([`tables/`](tables/))**: 14 individual multi-year CSV tables with continuous year columns.

## Category Summary
- **Time Horizon Covered**: **2001 – 2025**
- **Total Harmonized Tables**: 14
- **Total Time-Series Observations**: 4,365
- **SQLite Database**: [`2_0_environment.db`](2_0_environment.db)

## Harmonized Tables Catalog

| Table ID | Title | Time Span | Rows | Cols | Wide CSV | Metadata |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **2.1** | Table 2.1 : LIST OF THE PROTECTED AREAS AS OF 2005 | 2018 – 2025 | 98 | 19 | [`2.1.csv`](tables/2.1.csv) | [`2.1.json`](tables/2.1.json) |
| **2.11** | Table 2.11: WASTE TRANSPORTED TO THILAFUSHI , 2016-2018, (in tons) | 2016 – 2018 | 1 | 4 | [`2.11.csv`](tables/2.11.csv) | [`2.11.json`](tables/2.11.json) |
| **2.2** | Table 2.2 : NUMBER OF ISLAND THAT HAVE REPORTED SEVERE EROSION TILL JULY, 2009 | 2009 – 2024 | 42 | 30 | [`2.2.csv`](tables/2.2.csv) | [`2.2.json`](tables/2.2.json) |
| **2.3** | Table 2.3 : NUMBER OF ISLAND THAT HAVE WASTE MANAGEMENT CENTRES 2009 | 2009 – 2024 | 25 | 26 | [`2.3.csv`](tables/2.3.csv) | [`2.3.json`](tables/2.3.json) |
| **2.3&2.4** | Table 2.4: NUMBER OF ENVIRONMENTAL IMPACT ASSESSMENT REPORTS SUBMITTED FOR DEVELOPMENT PROJECT , 2009 | 2009 | 20 | 5 | [`2.3&2.4.csv`](tables/2.3&2.4.csv) | [`2.3&2.4.json`](tables/2.3&2.4.json) |
| **2.4** | Table 2.4: WASTE TRANSPORTED TO THILAFUSHI FROM MALE' , 2003-2009, (in tons) | 2001 – 2020 | 18 | 20 | [`2.4.csv`](tables/2.4.csv) | [`2.4.json`](tables/2.4.json) |
| **2.5** | Table 2.5: WASTE TRANSPORTED TO THILAFUSHI FROM MALE' , 2003-2008, (in tons) | 2001 – 2024 | 36 | 32 | [`2.5.csv`](tables/2.5.csv) | [`2.5.json`](tables/2.5.json) |
| **2.6** | Table 2.6 : METHOD OF WASTE DISPOSAL BY LOCALITY, CENSUS 2006 | 2010 – 2021 | 27 | 45 | [`2.6.csv`](tables/2.6.csv) | [`2.6.json`](tables/2.6.json) |
| **2.6&fig2.1** | Table: 2.6 WASTE TRANSPORTED TO THILAFUSHI, 2002-2008 | 2002 – 2008 | 8 | 8 | [`2.6&fig2.1.csv`](tables/2.6&fig2.1.csv) | [`2.6&fig2.1.json`](tables/2.6&fig2.1.json) |
| **2.7** | Table 2.7 : METHOD OF WASTE DISPOSAL BY LOCALITY, CENSUS 2006 | 2009 – 2024 | 26 | 52 | [`2.7.csv`](tables/2.7.csv) | [`2.7.json`](tables/2.7.json) |
| **2.8** | Table 2.8 : HOUSEHOLDS BY TYPE OF SANITATION USED , CENSUS 2006 | 2009 – 2013 | 23 | 38 | [`2.8.csv`](tables/2.8.csv) | [`2.8.json`](tables/2.8.json) |
| **2.8FIG2.2** | Table 2.8 :TYPE OF FUEL USED FOR COOKING, CENSUS 2006 | 2011 | 23 | 8 | [`2.8FIG2.2.csv`](tables/2.8FIG2.2.csv) | [`2.8FIG2.2.json`](tables/2.8FIG2.2.json) |
| **2.9** | TABLE 2.9: NUMBER OF TREES PROTECTED IN THE MALDIVES, 2013 - 2015 | 2013 – 2015 | 23 | 4 | [`2.9.csv`](tables/2.9.csv) | [`2.9.json`](tables/2.9.json) |
| **2.9&fig2.2** | Table 2.9 :TYPE OF FUEL USED FOR COOKING, CENSUS 2006 | 2009 | 23 | 8 | [`2.9&fig2.2.csv`](tables/2.9&fig2.2.csv) | [`2.9&fig2.2.json`](tables/2.9&fig2.2.json) |

## Example SQLite Usage (Python)
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('2_0_environment.db')

# Query any metric across all years in milliseconds:
df = pd.read_sql('''
    SELECT item_name, year, value, unit
    FROM master_panel
    WHERE table_id = '10.1' AND year >= 2010
    ORDER BY item_name, year
''', conn)
print(df.head())
```
