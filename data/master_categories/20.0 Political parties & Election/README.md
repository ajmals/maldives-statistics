# 20.0 Political parties & Election — Master Multi-Year Dataset

This directory houses the consolidated multi-year datasets for **20.0 Political parties & Election**, harmonizing data across all official Maldives Statistical Yearbook editions published between **2008 and 2026** by the National Bureau of Statistics (NBS).

## Available Formats
- **Consolidated Panel Dataset ([`master_panel.csv`](master_panel.csv))**: Long-format tabular dataset (19,169 rows) with schema: `[category, table_id, table_title, item_name, metric_name, year, value, unit, edition_year]`.
- **Category SQLite Database ([`20_0_political_parties_election.db`](20_0_political_parties_election.db))**: Fully indexed local database containing `master_panel` plus dedicated SQL tables for every individual harmonized table.
- **Harmonized Wide CSVs ([`tables/`](tables/))**: 9 individual multi-year CSV tables with continuous year columns.

## Category Summary
- **Time Horizon Covered**: **2008 – 2025**
- **Total Harmonized Tables**: 9
- **Total Time-Series Observations**: 19,169
- **SQLite Database**: [`20_0_political_parties_election.db`](20_0_political_parties_election.db)

## Harmonized Tables Catalog

| Table ID | Title | Time Span | Rows | Cols | Wide CSV | Metadata |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **20.1** |  | 2012 – 2020 | 21 | 134 | [`20.1.csv`](tables/20.1.csv) | [`20.1.json`](tables/20.1.json) |
| **20.2** | TABLE 20.2: EXPENDITURE ON ELECTIONS, 2008 - 2011 | 2008 – 2025 | 7 | 25 | [`20.2.csv`](tables/20.2.csv) | [`20.2.json`](tables/20.2.json) |
| **20.3** | TABLE 20.3: PRESIDENTIAL ELECTION, 2008 | 2013 – 2023 | 6 | 14 | [`20.3.csv`](tables/20.3.csv) | [`20.3.json`](tables/20.3.json) |
| **20.4** | TABLE 20.4: DETAILS OF THE BALLOT BOXES KEPT DURING PRESIDENTIAL ELECTIONS 2008 | 2013 – 2025 | 267 | 56 | [`20.4.csv`](tables/20.4.csv) | [`20.4.json`](tables/20.4.json) |
| **20.5** | TABLE 205.5: NUMBER OF PERSONS VOTED IN PARLIMENTARY ELECTIONS, 2009 | 2013 – 2025 | 88 | 71 | [`20.5.csv`](tables/20.5.csv) | [`20.5.json`](tables/20.5.json) |
| **20.6** | TABLE 20.6: NUMBER OF PARLIMENT MEMBERS ELECTED, 2012 | 2012 – 2025 | 3 | 27 | [`20.6.csv`](tables/20.6.csv) | [`20.6.json`](tables/20.6.json) |
| **20.7** | TABLE 20.7: NUMBER OF PARLIAMENT MEMBERS ELECTED AND FINANCIAL RESOURCES, 2011- 2012 | 2011 – 2024 | 6 | 48 | [`20.7.csv`](tables/20.7.csv) | [`20.7.json`](tables/20.7.json) |
| **20.8** | TABLE 20.8: LOCAL COUNCIL MEMBERS BY SEX, 2012 | 2013 – 2024 | 5 | 76 | [`20.8.csv`](tables/20.8.csv) | [`20.8.json`](tables/20.8.json) |
| **20.9** | TABLE 20.9: ELECTED LOCAL COUNCIL MEMBERS BY ATOLL AND FINANCIAL RESOURCES, 2011-2012 | 2011 – 2024 | 27 | 113 | [`20.9.csv`](tables/20.9.csv) | [`20.9.json`](tables/20.9.json) |

## Example SQLite Usage (Python)
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('20_0_political_parties_election.db')

# Query any metric across all years in milliseconds:
df = pd.read_sql('''
    SELECT item_name, year, value, unit
    FROM master_panel
    WHERE table_id = '10.1' AND year >= 2010
    ORDER BY item_name, year
''', conn)
print(df.head())
```
