# 5.0 Employment — Master Multi-Year Dataset

This directory houses the consolidated multi-year datasets for **5.0 Employment**, harmonizing data across all official Maldives Statistical Yearbook editions published between **2008 and 2026** by the National Bureau of Statistics (NBS).

## Available Formats
- **Consolidated Panel Dataset ([`master_panel.csv`](master_panel.csv))**: Long-format tabular dataset (35,854 rows) with schema: `[category, table_id, table_title, item_name, metric_name, year, value, unit, edition_year]`.
- **Category SQLite Database ([`5_0_employment.db`](5_0_employment.db))**: Fully indexed local database containing `master_panel` plus dedicated SQL tables for every individual harmonized table.
- **Harmonized Wide CSVs ([`tables/`](tables/))**: 19 individual multi-year CSV tables with continuous year columns.

## Category Summary
- **Time Horizon Covered**: **2007 – 2026**
- **Total Harmonized Tables**: 19
- **Total Time-Series Observations**: 35,854
- **SQLite Database**: [`5_0_employment.db`](5_0_employment.db)

## Harmonized Tables Catalog

| Table ID | Title | Time Span | Rows | Cols | Wide CSV | Metadata |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **5.1** | Table 5.1 : PERMANENT EMPLOYEES OF CIVIL SERVICE, BY SECTOR, 2008 | 2009 – 2026 | 251 | 155 | [`5.1.csv`](tables/5.1.csv) | [`5.1.json`](tables/5.1.json) |
| **5.10** | Table 5.10 : EXPATRIATE EMPLOYMENT BY INDUSTRY AND SEX, 2010 | 2011 – 2024 | 258 | 80 | [`5.10.csv`](tables/5.10.csv) | [`5.10.json`](tables/5.10.json) |
| **5.11** | Table 5.11: Number of establishments and employment by industry and establishment size, 2007 | 2011 – 2022 | 1412 | 42 | [`5.11.csv`](tables/5.11.csv) | [`5.11.json`](tables/5.11.json) |
| **5.12** |  | 2007 – 2022 | 113 | 44 | [`5.12.csv`](tables/5.12.csv) | [`5.12.json`](tables/5.12.json) |
| **5.13** | Table 5.13: Civil Servants Classified by Civil Service Job Structure, 2010 | 2010 – 2025 | 224 | 36 | [`5.13.csv`](tables/5.13.csv) | [`5.13.json`](tables/5.13.json) |
| **5.14** | Table 5.14: Civil servants classified by age and sex, 2010 | 2011 – 2015 | 40 | 28 | [`5.14.csv`](tables/5.14.csv) | [`5.14.json`](tables/5.14.json) |
| **5.15** | Table 5.15: Civil Servants Classified by Office, 2010 | 2010 – 2015 | 731 | 11 | [`5.15.csv`](tables/5.15.csv) | [`5.15.json`](tables/5.15.json) |
| **5.16** | TABLE 5.16: EMPLOYMENT IN POLITICAL POSTS CLASSIFIED BY OFFICE, 2010 | 2010 – 2015 | 60 | 11 | [`5.16.csv`](tables/5.16.csv) | [`5.16.json`](tables/5.16.json) |
| **5.17** | TABLE 5.17: EMPLOYMENT IN POLITICAL POSTS CLASSIFIED BY OFFICE, 2014 | 2014 – 2015 | 63 | 5 | [`5.17.csv`](tables/5.17.csv) | [`5.17.json`](tables/5.17.json) |
| **5.18** | TABLE 5.18: NUMBER OF VACANT JOBS BY SECTOR, 2012 - 2014 | 2012 – 2014 | 4 | 4 | [`5.18.csv`](tables/5.18.csv) | [`5.18.json`](tables/5.18.json) |
| **5.2** | Table 5.2 : EXPATRIATE EMPLOYMENT BY INDUSTRY AND NATIONALITY, 2008 | 2009 – 2026 | 39 | 173 | [`5.2.csv`](tables/5.2.csv) | [`5.2.json`](tables/5.2.json) |
| **5.3** | Table 5.3 : EXPATRIATE EMPLOYMENT BY INDUSTRY AND OCCUPATION, 2008 | 2009 – 2026 | 54 | 117 | [`5.3.csv`](tables/5.3.csv) | [`5.3.json`](tables/5.3.json) |
| **5.4** | Table 5.4 : POPULATION 15 YEARS OF AGE AND OVER BY TYPE OF ACTIVITY, CROSS CLASSIFIED BY AGE AND SEX, CENSUS 2006 | 2009 – 2025 | 236 | 95 | [`5.4.csv`](tables/5.4.csv) | [`5.4.json`](tables/5.4.json) |
| **5.5** | Table 5.5 : EMPLOYED POPULATION BY INDUSTRY, OCCUPATION AND SEX, CENSUS 2006 | 2009 – 2026 | 38 | 148 | [`5.5.csv`](tables/5.5.csv) | [`5.5.json`](tables/5.5.json) |
| **5.6** | Table 5.6 : EXPATRIATE EMPLOYMENT BY OCCUPATION AND SEX, 2008 | 2009 – 2026 | 91 | 121 | [`5.6.csv`](tables/5.6.csv) | [`5.6.json`](tables/5.6.json) |
| **5.7** | Table 5.7 : EXPATRIATE EMPLOYMENT BY INDUSTRY AND SEX, 2008 | 2009 – 2023 | 116 | 127 | [`5.7.csv`](tables/5.7.csv) | [`5.7.json`](tables/5.7.json) |
| **5.8** | Table 5.8: NUMBER OF ESTABLISHMENTS AND EMPLOYMENT BY INDUSTRY AND ESTABLISHMENT SIZE, 2007 | 2007 – 2023 | 111 | 117 | [`5.8.csv`](tables/5.8.csv) | [`5.8.json`](tables/5.8.json) |
| **5.8cont** | Table 5.8 (continued ) | 2011 | 13 | 25 | [`5.8cont.csv`](tables/5.8cont.csv) | [`5.8cont.json`](tables/5.8cont.json) |
| **5.9** | Table 5.9: EMPLOYMENT IN ESTABLISHMENTS BY INDUSTRY, 2007 | 2010 – 2024 | 230 | 120 | [`5.9.csv`](tables/5.9.csv) | [`5.9.json`](tables/5.9.json) |

## Example SQLite Usage (Python)
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('5_0_employment.db')

# Query any metric across all years in milliseconds:
df = pd.read_sql('''
    SELECT item_name, year, value, unit
    FROM master_panel
    WHERE table_id = '10.1' AND year >= 2010
    ORDER BY item_name, year
''', conn)
print(df.head())
```
