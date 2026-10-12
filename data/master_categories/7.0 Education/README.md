# 7.0 Education — Master Multi-Year Dataset

This directory houses the consolidated multi-year datasets for **7.0 Education**, harmonizing data across all official Maldives Statistical Yearbook editions published between **2008 and 2026** by the National Bureau of Statistics (NBS).

## Available Formats
- **Consolidated Panel Dataset ([`master_panel.csv`](master_panel.csv))**: Long-format tabular dataset (83,751 rows) with schema: `[category, table_id, table_title, item_name, metric_name, year, value, unit, edition_year]`.
- **Category SQLite Database ([`7_0_education.db`](7_0_education.db))**: Fully indexed local database containing `master_panel` plus dedicated SQL tables for every individual harmonized table.
- **Harmonized Wide CSVs ([`tables/`](tables/))**: 39 individual multi-year CSV tables with continuous year columns.

## Category Summary
- **Time Horizon Covered**: **1998 – 2026**
- **Total Harmonized Tables**: 39
- **Total Time-Series Observations**: 83,751
- **SQLite Database**: [`7_0_education.db`](7_0_education.db)

## Harmonized Tables Catalog

| Table ID | Title | Time Span | Rows | Cols | Wide CSV | Metadata |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **7.1** | Table 7.1 : STUDENT ENROLMENT AND SCHOOLS IN MALE' AND ATOLLS BY TYPE OF EDUCATIONAL INSTITUTION, 2009 | 2010 – 2026 | 36 | 111 | [`7.1.csv`](tables/7.1.csv) | [`7.1.json`](tables/7.1.json) |
| **7.1&fig7.1** | Table 7.1 : STUDENT ENROLMENT AND SCHOOLS IN MALE' AND ATOLLS BY TYPE OF EDUCATIONAL INSTITUTION, 2008 | 2009 | 23 | 9 | [`7.1&fig7.1.csv`](tables/7.1&fig7.1.csv) | [`7.1&fig7.1.json`](tables/7.1&fig7.1.json) |
| **7.1-1** | Table 7.1 : STUDENT ENROLMENT AND SCHOOLS IN MALE' AND ATOLLS BY TYPE OF EDUCATIONAL INSTITUTION, 2018 | 2019 | 23 | 9 | [`7.1-1.csv`](tables/7.1-1.csv) | [`7.1-1.json`](tables/7.1-1.json) |
| **7.10** | TABLE 7.10 : POPULATION 6 YEARS OF AGE AND OVER BY EDUCATIONAL ATTAINMENT, CENSUS 2006 | 2009 – 2021 | 50 | 127 | [`7.10.csv`](tables/7.10.csv) | [`7.10.json`](tables/7.10.json) |
| **7.11** | Table 7.11 : SUMMARY OF STUDENT ENROLMENT IN TECHNICAL EDUCATION, BY SEX, 2007 - 2008 | 2007 – 2021 | 34 | 139 | [`7.11.csv`](tables/7.11.csv) | [`7.11.json`](tables/7.11.json) |
| **7.12** | Table 7.12 : STUDENTS WHO RECEIVED SCHOLARSHIPS , DURING 1998 - 2008 | 2009 – 2021 | 293 | 170 | [`7.12.csv`](tables/7.12.csv) | [`7.12.json`](tables/7.12.json) |
| **7.13** | Table 7.13 : STUDENT ENROLMENT IN MALE' AND ATOLLS, BY GRADE AND SEX, 2008 | 2009 – 2021 | 53 | 263 | [`7.13.csv`](tables/7.13.csv) | [`7.13.json`](tables/7.13.json) |
| **7.14** | Table 7.14 : STUDENT ENROLMENT IN SCHOOLS OF MALE', BY TYPE OF INSTITUTION AND SEX, 2007-2008 | 2007 – 2021 | 520 | 149 | [`7.14.csv`](tables/7.14.csv) | [`7.14.json`](tables/7.14.json) |
| **7.15** | Table 7.15 : STUDENT ENROLMENT IN GOVERNMENT SCHOOLS OF ATOLLS, BY EDUCATIONAL LEVEL AND SEX , 2008 | 2009 – 2019 | 24 | 81 | [`7.15.csv`](tables/7.15.csv) | [`7.15.json`](tables/7.15.json) |
| **7.16** | Table 7.16: TEACHERS SERVING IN SCHOOLS OF MALE' AND ATOLLS BY LOCALITY AND SEX, 2008 | 2005 – 2019 | 62 | 35 | [`7.16.csv`](tables/7.16.csv) | [`7.16.json`](tables/7.16.json) |
| **7.17** | Table 7.17 : STUDENT ENROLMENT IN TECHNICAL EDUCATION, BY TYPE OF TRAINING AND SEX, 2007-2008 | 2005 – 2019 | 74 | 37 | [`7.17.csv`](tables/7.17.csv) | [`7.17.json`](tables/7.17.json) |
| **7.18** | Table 7.18: SINGLE SESSION SCHOOLS, 2009 | 2008 – 2019 | 130 | 25 | [`7.18.csv`](tables/7.18.csv) | [`7.18.json`](tables/7.18.json) |
| **7.19** | Table 7.19: NUMBER OF STUDENTS SAT AND PASSED IN THE O'LEVEL EXAMINATION BY ATOLLS 2007 - 2009 | 2007 – 2019 | 57 | 49 | [`7.19.csv`](tables/7.19.csv) | [`7.19.json`](tables/7.19.json) |
| **7.2** | Table 7.2 : STUDENT ENROLMENT BY EDUCATIONAL LEVEL AND SEX, 2009 | 2010 – 2026 | 274 | 146 | [`7.2.csv`](tables/7.2.csv) | [`7.2.json`](tables/7.2.json) |
| **7.2&fig7.2** | Table 7.2 : STUDENT ENROLMENT BY EDUCATIONAL LEVEL AND SEX, 2008 | 2009 | 8 | 8 | [`7.2&fig7.2.csv`](tables/7.2&fig7.2.csv) | [`7.2&fig7.2.json`](tables/7.2&fig7.2.json) |
| **7.20** | Table 7.20 : PASS PERCENTAGE OF STUDENTS, 2008 - 2009 | 2008 – 2018 | 43 | 46 | [`7.20.csv`](tables/7.20.csv) | [`7.20.json`](tables/7.20.json) |
| **7.21** | Table 7.21: NUMBER OF CANDIDATES SAT AND PASSED IN O'LEVEL BY SUBJECT, 2007 - 2009 | 2007 – 2024 | 69 | 76 | [`7.21.csv`](tables/7.21.csv) | [`7.21.json`](tables/7.21.json) |
| **7.22** | Table 7.22: STUDENT ENROLMENT IN TECHNICAL EDUCATION, BY TYPE OF TRAINING AND SEX 2010-2012 | 2010 – 2024 | 88 | 53 | [`7.22.csv`](tables/7.22.csv) | [`7.22.json`](tables/7.22.json) |
| **7.23** | Table 7.23: STUDENT ENROLMENT IN TECHNICAL EDUCATION, BY TYPE OF TRAINING AND SEX, 2010 - 2011 | 2010 – 2018 | 68 | 46 | [`7.23.csv`](tables/7.23.csv) | [`7.23.json`](tables/7.23.json) |
| **7.24** | TABLE 7.24: STUDENT ENROLMENT AND GRADUATE OUTPUT IN HIGHER EDUCATION INSTITUTIONS IN MALDIVES, 2011 | 2011 – 2022 | 40 | 71 | [`7.24.csv`](tables/7.24.csv) | [`7.24.json`](tables/7.24.json) |
| **7.25** | TABLE 7.24: STUDENT ENROLMENT AND GRADUATE OUTPUT IN SELECTED HIGHER EDUCATION INSTITUTIONS IN MALDIVES, 2010 - 2011 | 2010 – 2022 | 124 | 45 | [`7.25.csv`](tables/7.25.csv) | [`7.25.json`](tables/7.25.json) |
| **7.26** | TABLE 7.26: STUDENT ENROLMENT AND GRADUATE OUTPUT IN HIGHER EDUCATION INSTITUTIONS IN MALDIVES BY SEX, 2020 | 2021 | 15 | 13 | [`7.26.csv`](tables/7.26.csv) | [`7.26.json`](tables/7.26.json) |
| **7.27** | Table 7.27: Number of higher education institutions, 2019 | 2020 – 2022 | 2 | 7 | [`7.27.csv`](tables/7.27.csv) | [`7.27.json`](tables/7.27.json) |
| **7.28** | Table 7.28: Number of staff by gender, nationality and type of employment, 2019 | 2020 – 2022 | 3 | 10 | [`7.28.csv`](tables/7.28.csv) | [`7.28.json`](tables/7.28.json) |
| **7.29** | TABLE 7.29: STUDENT ENROLLMENT IN UNIVERSITIES AND COLLEGES, 2019 | 2020 – 2021 | 13 | 7 | [`7.29.csv`](tables/7.29.csv) | [`7.29.json`](tables/7.29.json) |
| **7.3** | Table 7.3: STUDENT ENROLMENT IN MALE' AND ATOLLS BY TYPE OF LEVEL AND INSTITUTION , 2008 | 2009 – 2026 | 30 | 222 | [`7.3.csv`](tables/7.3.csv) | [`7.3.json`](tables/7.3.json) |
| **7.3-1** | Table 7.3: STUDENT ENROLMENT IN MALE' AND ATOLLS BY TYPE OF LEVEL AND INSTITUTION , 2018 | 2019 | 23 | 18 | [`7.3-1.csv`](tables/7.3-1.csv) | [`7.3-1.json`](tables/7.3-1.json) |
| **7.30** | TABLE 7.30: STUDENT ENROLMENT AND GRADUATE OUTPUT IN HIGHER EDUCATION INSTITUTIONS IN MALDIVES BY SEX, 2019 | 2019 – 2021 | 13 | 43 | [`7.30.csv`](tables/7.30.csv) | [`7.30.json`](tables/7.30.json) |
| **7.31** | TABLE 7.31: HIGHER EDUCATION ENROLLMENT BY LEVELS OF MALDIVES NATIONAL QUALIFICATIONS FRAMEWORK, 2019 | 2019 – 2021 | 13 | 40 | [`7.31.csv`](tables/7.31.csv) | [`7.31.json`](tables/7.31.json) |
| **7.4** | Table 7.4 : TEACHERS AND STUDENTS OF EDUCATIONAL INSTITUTIONS, BY LOCALITY, 2008 | 2009 – 2026 | 28 | 163 | [`7.4.csv`](tables/7.4.csv) | [`7.4.json`](tables/7.4.json) |
| **7.5** | Table 7.5 : GROSS ENROLMENT RATIO BY LEVEL AND SEX, 2000 - 2009 | 1998 – 2026 | 26 | 63 | [`7.5.csv`](tables/7.5.csv) | [`7.5.json`](tables/7.5.json) |
| **7.5&7.6** | Table 7.6 : NET ENROLMENT RATIO BY LEVEL AND SEX, 2000 - 2008 | 1998 – 2008 | 5 | 12 | [`7.5&7.6.csv`](tables/7.5&7.6.csv) | [`7.5&7.6.json`](tables/7.5&7.6.json) |
| **7.5-1** | Table 7.5 :GROSS ENROLMENT RATIO BY LEVEL AND SEX, 2006 - 2018 | 2006 – 2018 | 3 | 14 | [`7.5-1.csv`](tables/7.5-1.csv) | [`7.5-1.json`](tables/7.5-1.json) |
| **7.6** | Table 7.6 : NET ENROLMENT RATIO BY LEVEL AND SEX, 2000 - 2009 | 1998 – 2026 | 26 | 39 | [`7.6.csv`](tables/7.6.csv) | [`7.6.json`](tables/7.6.json) |
| **7.6-1** | TABLE 7.6: NUMBER OF SCHOOLS, ENROLMENT AND TEACHERS BY LOCALITY, 2021 - 2022 | 2022 | 23 | 11 | [`7.6-1.csv`](tables/7.6-1.csv) | [`7.6-1.json`](tables/7.6-1.json) |
| **7.7** | Table 7.7 : STUDENTS AND TEACHERS SERVING AT DIFFERENT LEVELS IN MALE' AND ATOLLS , 2009 | 2010 – 2026 | 214 | 174 | [`7.7.csv`](tables/7.7.csv) | [`7.7.json`](tables/7.7.json) |
| **7.7&fig7.9** | Table 7.7 : STUDENTS AND TEACHERS SERVING AT DIFFERENT LEVELS IN MALE' AND ATOLLS , 2008 | 2009 | 8 | 11 | [`7.7&fig7.9.csv`](tables/7.7&fig7.9.csv) | [`7.7&fig7.9.json`](tables/7.7&fig7.9.json) |
| **7.8** | TABLE 7.8: LOCAL AND EXPATRIATE TEACHERS SERVING IN SCHOOLS OF MALE' AND ATOLLS BY LOCALITY, 2008 | 2006 – 2026 | 31 | 119 | [`7.8.csv`](tables/7.8.csv) | [`7.8.json`](tables/7.8.json) |
| **7.9** | TABLE 7.9 : POPULATION 6 YEARS OF AGE AND OVER BY LITERACY AGE GROUP AND SEX, CENSUS 2006 | 2006 – 2026 | 61 | 184 | [`7.9.csv`](tables/7.9.csv) | [`7.9.json`](tables/7.9.json) |

## Example SQLite Usage (Python)
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('7_0_education.db')

# Query any metric across all years in milliseconds:
df = pd.read_sql('''
    SELECT item_name, year, value, unit
    FROM master_panel
    WHERE table_id = '10.1' AND year >= 2010
    ORDER BY item_name, year
''', conn)
print(df.head())
```
