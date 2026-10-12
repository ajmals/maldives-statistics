# 6.0 Health — Master Multi-Year Dataset

This directory houses the consolidated multi-year datasets for **6.0 Health**, harmonizing data across all official Maldives Statistical Yearbook editions published between **2008 and 2026** by the National Bureau of Statistics (NBS).

## Available Formats
- **Consolidated Panel Dataset ([`master_panel.csv`](master_panel.csv))**: Long-format tabular dataset (43,603 rows) with schema: `[category, table_id, table_title, item_name, metric_name, year, value, unit, edition_year]`.
- **Category SQLite Database ([`6_0_health.db`](6_0_health.db))**: Fully indexed local database containing `master_panel` plus dedicated SQL tables for every individual harmonized table.
- **Harmonized Wide CSVs ([`tables/`](tables/))**: 29 individual multi-year CSV tables with continuous year columns.

## Category Summary
- **Time Horizon Covered**: **1999 – 2026**
- **Total Harmonized Tables**: 29
- **Total Time-Series Observations**: 43,603
- **SQLite Database**: [`6_0_health.db`](6_0_health.db)

## Harmonized Tables Catalog

| Table ID | Title | Time Span | Rows | Cols | Wide CSV | Metadata |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **6.1** | Table 6.1 : DISTRIBUTION OF MEDICAL STAFF IN MALE' AND ATOLLS, 2006-2007 | 2006 – 2026 | 46 | 145 | [`6.1.csv`](tables/6.1.csv) | [`6.1.json`](tables/6.1.json) |
| **6.10** | Table 6.10: ESTIMATED IMMUNIZATION COVERAGE, 2008 | 2009 – 2026 | 88 | 106 | [`6.10.csv`](tables/6.10.csv) | [`6.10.json`](tables/6.10.json) |
| **6.11** | Table 6.11 : CLIENT STATUS IN DRUG REHABILITATION CENTRE, BY SEX, 2006 - 2007 | 2005 – 2026 | 231 | 107 | [`6.11.csv`](tables/6.11.csv) | [`6.11.json`](tables/6.11.json) |
| **6.12** | Table 6.12 : DRUG ABUSE CASES REPORTED, BY AGE GROUP, 2001-2007 | 2007 – 2026 | 49 | 88 | [`6.12.csv`](tables/6.12.csv) | [`6.12.json`](tables/6.12.json) |
| **6.13** | Table 6.13 : CONTRACEPTIVE USER RATE BY SEX AND LOCALITY, 2003 - 2009 | 2003 – 2026 | 23 | 59 | [`6.13.csv`](tables/6.13.csv) | [`6.13.json`](tables/6.13.json) |
| **6.13&6.14** | Table 6.14 : CONTRACEPTIVE USER RATE BY LOCALITY,2002- 2008 | 2002 – 2008 | 28 | 8 | [`6.13&6.14.csv`](tables/6.13&6.14.csv) | [`6.13&6.14.json`](tables/6.13&6.14.json) |
| **6.13&fig6.1** | Table 6.13 : DRUG ABUSE CASES REPORTED, BY AGE GROUP, 2001-2007 | 2011 | 8 | 6 | [`6.13&fig6.1.csv`](tables/6.13&fig6.1.csv) | [`6.13&fig6.1.json`](tables/6.13&fig6.1.json) |
| **6.13-1** | Table 6.13: Number of registered thalassaemia cases by Age group and sex, 2020 | 2025 | 3 | 6 | [`6.13-1.csv`](tables/6.13-1.csv) | [`6.13-1.json`](tables/6.13-1.json) |
| **6.14** | Table 6.14 : CONTRACEPTIVE USER RATE BY LOCALITY, 2003 - 2009 | 2003 – 2026 | 84 | 57 | [`6.14.csv`](tables/6.14.csv) | [`6.14.json`](tables/6.14.json) |
| **6.14&6.15** | Table 6.15 : CONTRACEPTIVE USER RATE BY LOCALITY, 2004 - 2010 | 2004 – 2010 | 3 | 8 | [`6.14&6.15.csv`](tables/6.14&6.15.csv) | [`6.14&6.15.json`](tables/6.14&6.15.json) |
| **6.15** | Table 6.15 : TUBERCULOSIS CASES BY SEX, 2003-2008 | 2003 – 2018 | 32 | 54 | [`6.15.csv`](tables/6.15.csv) | [`6.15.json`](tables/6.15.json) |
| **6.16** | Table 6.16 : LOCALLY TRAINED AND CERTIFIED HEALTH PERSONNEL BY TYPE OF TRAINING, 2004-2008 | 2003 – 2020 | 240 | 62 | [`6.16.csv`](tables/6.16.csv) | [`6.16.json`](tables/6.16.json) |
| **6.17** | Table 6.17 : TOTAL NO. OF REPORTED CASES BY SELECTED DISEASES BY LOCALITY , 2008 | 2008 – 2026 | 277 | 130 | [`6.17.csv`](tables/6.17.csv) | [`6.17.json`](tables/6.17.json) |
| **6.18** | Table 6.18 : DENTAL CARE SERVICES BY THE DENTAL CLINIC, 2003-2007 | 2001 – 2026 | 253 | 94 | [`6.18.csv`](tables/6.18.csv) | [`6.18.json`](tables/6.18.json) |
| **6.19** | Table 6.19 : REGISTERED CASES OF FILARIA , 2000-2008 | 1999 – 2026 | 126 | 96 | [`6.19.csv`](tables/6.19.csv) | [`6.19.json`](tables/6.19.json) |
| **6.2** | Table 6.2 : HEALTH PERSONNEL BY EXPATRIATES AND LOCALS, 2008 - (only public sectors) | 2009 – 2026 | 39 | 168 | [`6.2.csv`](tables/6.2.csv) | [`6.2.json`](tables/6.2.json) |
| **6.20** | Table 6.20 : NEW CASES OF FILARIA, BY AGE GROUP, 2000-2008 | 1999 – 2026 | 232 | 70 | [`6.20.csv`](tables/6.20.csv) | [`6.20.json`](tables/6.20.json) |
| **6.21** | Table 6.21 : CLIENT STATUS IN DRUG REHABILITATION CENTRE, BY SEX, 2007 | 2004 – 2025 | 42 | 44 | [`6.21.csv`](tables/6.21.csv) | [`6.21.json`](tables/6.21.json) |
| **6.22** | Table 6.22: NUMBER OF COUNSELLING SERVICE BY TYPE OF ISSUE AND SEX, 2011- 2012 | 2004 – 2025 | 31 | 40 | [`6.22.csv`](tables/6.22.csv) | [`6.22.json`](tables/6.22.json) |
| **6.23** | Table 6.23: TOTAL NO. OF REPORTED CASES BY SELECTED DISEASES BY ISLAND, 2010 | 2011 – 2013 | 216 | 20 | [`6.23.csv`](tables/6.23.csv) | [`6.23.json`](tables/6.23.json) |
| **6.3** | Table 6.3 : OUT- PATIENT FLOW, INPATIENT FLOW AND BED OCCUPANCY RATE OF GOVERNMENT HOSPITALS, | 2008 – 2023 | 82 | 29 | [`6.3.csv`](tables/6.3.csv) | [`6.3.json`](tables/6.3.json) |
| **6.4** | Table 6.4 : IN - PATIENT HEALTH CARE IN INDIRA GANDHI MEMORIAL HOSPITAL, 2002-2008 | 2002 – 2017 | 38 | 17 | [`6.4.csv`](tables/6.4.csv) | [`6.4.json`](tables/6.4.json) |
| **6.4&6.5** | Table 6.5 : OUT - PATIENT HEALTH CARE IN MALE' HEALTH CENTRE, 2004-2010 | 2004 – 2010 | 4 | 8 | [`6.4&6.5.csv`](tables/6.4&6.5.csv) | [`6.4&6.5.json`](tables/6.4&6.5.json) |
| **6.5** | Table 6.5 : PATIENTS BY TYPE OF SURGICAL INTERVENTION, 2001 - 2008 | 2001 – 2025 | 75 | 29 | [`6.5.csv`](tables/6.5.csv) | [`6.5.json`](tables/6.5.json) |
| **6.6** | Table 6.6 : TUBERCULOSIS CASES, BY AGE GROUP, 2009 | 2002 – 2025 | 31 | 31 | [`6.6.csv`](tables/6.6.csv) | [`6.6.json`](tables/6.6.json) |
| **6.7** | Table 6.7 : LEPROSY CASES BY AGE AND SEX, 2001-2008 | 2000 – 2025 | 50 | 53 | [`6.7.csv`](tables/6.7.csv) | [`6.7.json`](tables/6.7.json) |
| **6.8** | Table 6.8 : REGISTERED THALASSAEMIA CASES IN MALE' AND ATOLLS, 2004 - 2009 | 2002 – 2025 | 58 | 37 | [`6.8.csv`](tables/6.8.csv) | [`6.8.json`](tables/6.8.json) |
| **6.8&6.9** | Table 6.9 : PERSONS SCREENED FOR THALASSAEMIA, 2001 - 2008 | 2003 – 2009 | 15 | 9 | [`6.8&6.9.csv`](tables/6.8&6.9.csv) | [`6.8&6.9.json`](tables/6.8&6.9.json) |
| **6.9** | Table 6.9 : PERSONS SCREENED FOR THALASSAEMIA, 2001 - 2009 | 2005 – 2026 | 85 | 50 | [`6.9.csv`](tables/6.9.csv) | [`6.9.json`](tables/6.9.json) |

## Example SQLite Usage (Python)
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('6_0_health.db')

# Query any metric across all years in milliseconds:
df = pd.read_sql('''
    SELECT item_name, year, value, unit
    FROM master_panel
    WHERE table_id = '10.1' AND year >= 2010
    ORDER BY item_name, year
''', conn)
print(df.head())
```
