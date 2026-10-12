# general — Master Multi-Year Dataset

This directory houses the consolidated multi-year datasets for **general**, harmonizing data across all official Maldives Statistical Yearbook editions published between **2008 and 2026** by the National Bureau of Statistics (NBS).

## Available Formats
- **Consolidated Panel Dataset ([`master_panel.csv`](master_panel.csv))**: Long-format tabular dataset (1,293 rows) with schema: `[category, table_id, table_title, item_name, metric_name, year, value, unit, edition_year]`.
- **Category SQLite Database ([`general.db`](general.db))**: Fully indexed local database containing `master_panel` plus dedicated SQL tables for every individual harmonized table.
- **Harmonized Wide CSVs ([`tables/`](tables/))**: 7 individual multi-year CSV tables with continuous year columns.

## Category Summary
- **Time Horizon Covered**: **2018 – 2025**
- **Total Harmonized Tables**: 7
- **Total Time-Series Observations**: 1,293
- **SQLite Database**: [`general.db`](general.db)

## Harmonized Tables Catalog

| Table ID | Title | Time Span | Rows | Cols | Wide CSV | Metadata |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **21.2** | Table 21.2: STUDENT ENROLMENT IN TECHNICAL EDUCATION, BY TYPE OF TRAINING AND SEX, 2018 - 2023 | 2018 – 2024 | 95 | 22 | [`21.2.csv`](tables/21.2.csv) | [`21.2.json`](tables/21.2.json) |
| **21.3** | TABLE 21.3: STUDENT ENROLMENT AND GRADUATE OUTPUT IN HIGHER EDUCATION INSTITUTIONS IN MALDIVES BY SEX, 2020 | 2021 | 15 | 13 | [`21.3.csv`](tables/21.3.csv) | [`21.3.json`](tables/21.3.json) |
| **21.4** | Table 21.4: Number of higher education institutions, 2019 | 2024 – 2025 | 2 | 5 | [`21.4.csv`](tables/21.4.csv) | [`21.4.json`](tables/21.4.json) |
| **21.5** | Table 21.5: Number of staff by gender, nationality and type of employment, 2019 | 2024 – 2025 | 3 | 7 | [`21.5.csv`](tables/21.5.csv) | [`21.5.json`](tables/21.5.json) |
| **21.6** | TABLE 21.6: STUDENT ENROLLMENT IN UNIVERSITIES AND COLLEGES, 2019 | 2021 | 10 | 3 | [`21.6.csv`](tables/21.6.csv) | [`21.6.json`](tables/21.6.json) |
| **21.7** | TABLE 21.7: STUDENT ENROLMENT AND GRADUATE OUTPUT IN HIGHER EDUCATION INSTITUTIONS IN MALDIVES BY SEX, 2019 | 2021 | 12 | 14 | [`21.7.csv`](tables/21.7.csv) | [`21.7.json`](tables/21.7.json) |
| **21.8** | TABLE 21.8: HIGHER EDUCATION ENROLLMENT BY LEVELS OF MALDIVES NATIONAL QUALIFICATIONS FRAMEWORK, 2019 | 2021 | 13 | 13 | [`21.8.csv`](tables/21.8.csv) | [`21.8.json`](tables/21.8.json) |

## Example SQLite Usage (Python)
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('general.db')

# Query any metric across all years in milliseconds:
df = pd.read_sql('''
    SELECT item_name, year, value, unit
    FROM master_panel
    WHERE table_id = '10.1' AND year >= 2010
    ORDER BY item_name, year
''', conn)
print(df.head())
```
