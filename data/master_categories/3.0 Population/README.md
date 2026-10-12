# 3.0 Population — Master Multi-Year Dataset

This directory houses the consolidated multi-year datasets for **3.0 Population**, harmonizing data across all official Maldives Statistical Yearbook editions published between **2008 and 2026** by the National Bureau of Statistics (NBS).

## Available Formats
- **Consolidated Panel Dataset ([`master_panel.csv`](master_panel.csv))**: Long-format tabular dataset (329,213 rows) with schema: `[category, table_id, table_title, item_name, metric_name, year, value, unit, edition_year]`.
- **Category SQLite Database ([`3_0_population.db`](3_0_population.db))**: Fully indexed local database containing `master_panel` plus dedicated SQL tables for every individual harmonized table.
- **Harmonized Wide CSVs ([`tables/`](tables/))**: 39 individual multi-year CSV tables with continuous year columns.

## Category Summary
- **Time Horizon Covered**: **1985 – 2030**
- **Total Harmonized Tables**: 39
- **Total Time-Series Observations**: 329,213
- **SQLite Database**: [`3_0_population.db`](3_0_population.db)

## Harmonized Tables Catalog

| Table ID | Title | Time Span | Rows | Cols | Wide CSV | Metadata |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **3.1** | Table 3.1 : CENSUS POPULATION BY SEX AND SEX - RATIO, AND INTER-CENSAL VARIATION OF POPULATION, 1911 - 2006 | 2009 – 2026 | 60 | 138 | [`3.1.csv`](tables/3.1.csv) | [`3.1.json`](tables/3.1.json) |
| **3.10** | Table 3.10 : DEATHS BY AGE GROUP AND SEX, 2007 - 2009 | 2003 – 2026 | 35 | 57 | [`3.10.csv`](tables/3.10.csv) | [`3.10.json`](tables/3.10.json) |
| **3.10&3.11** | Table 3.11 : INFANT DEATHS BY AGE AND SEX, 2007 -2008 | 2003 – 2008 | 17 | 6 | [`3.10&3.11.csv`](tables/3.10&3.11.csv) | [`3.10&3.11.json`](tables/3.10&3.11.json) |
| **3.11** | Table 3.11 : INFANT DEATHS BY AGE AND SEX, 2007-2009 | 2003 – 2025 | 14 | 42 | [`3.11.csv`](tables/3.11.csv) | [`3.11.json`](tables/3.11.json) |
| **3.12** | Table 3.12 : PROJECTED MID-YEAR POPULATION OF MALDIVES BY AGE AND SEX, 2006-2025 | 2006 – 2024 | 45 | 109 | [`3.12.csv`](tables/3.12.csv) | [`3.12.json`](tables/3.12.json) |
| **3.13** | Table 3.13 : MARRIAGES AND DIVORCES IN MALE' AND ATOLLS, 2006 - 2007 | 2006 – 2030 | 57 | 141 | [`3.13.csv`](tables/3.13.csv) | [`3.13.json`](tables/3.13.json) |
| **3.14** | Table 3.14 :NUMBER OF PERSONS MARRIED AND DIVORCED,IN MALE', BY AGE GROUP OF BRIDE AND GROOM, 2005-2007 | 2009 – 2030 | 73 | 136 | [`3.14.csv`](tables/3.14.csv) | [`3.14.json`](tables/3.14.json) |
| **3.15** | Table 3.15 : POPULATION MIGRATED AND REGISTERED IN MALE' BY ATOLLS OF | 2004 – 2030 | 138 | 1249 | [`3.15.csv`](tables/3.15.csv) | [`3.15.json`](tables/3.15.json) |
| **3.16** | Table 3.16: DEATHS BY AGE AND SEX, BY MAJOR ADMINISTRATIVE UNITS, 2008 | 2009 – 2030 | 149 | 1261 | [`3.16.csv`](tables/3.16.csv) | [`3.16.json`](tables/3.16.json) |
| **3.17** | Table 3.17 : ACCIDENTAL DEATHS BY CAUSE AND SEX , 2006-2007 | 2006 – 2026 | 118 | 1218 | [`3.17.csv`](tables/3.17.csv) | [`3.17.json`](tables/3.17.json) |
| **3.18** | TABLE 3.18: NUMBER OF MARRIAGES BY NUMBER OF TIMES MARRIED BY SEX, 2013 - 2015 | 2016 – 2026 | 44 | 80 | [`3.18.csv`](tables/3.18.csv) | [`3.18.json`](tables/3.18.json) |
| **3.19** | TABLE 3.19: NUMBER OF TIMES MARRIED IN MALE' AND ATOLLS , 2015 | 2016 – 2026 | 40 | 55 | [`3.19.csv`](tables/3.19.csv) | [`3.19.json`](tables/3.19.json) |
| **3.2** | Table 3.2 : POPULATION BY AGE AND SEX, CENSUS, 1995, 2000 AND 2006 | 1995 – 2022 | 25 | 24 | [`3.2.csv`](tables/3.2.csv) | [`3.2.json`](tables/3.2.json) |
| **3.2&fig3.1** | Table 3.2 : POPULATION BY AGE AND SEX, CENSUS, 1995, 2000 AND 2006 | 1995 – 2006 | 24 | 10 | [`3.2&fig3.1.csv`](tables/3.2&fig3.1.csv) | [`3.2&fig3.1.json`](tables/3.2&fig3.1.json) |
| **3.20** | TABLE 3.20: NUMBER OF MARRIAGES, 2014 - 2015 | 2014 – 2026 | 79 | 65 | [`3.20.csv`](tables/3.20.csv) | [`3.20.json`](tables/3.20.json) |
| **3.21** | TABLE 3.21: NUMBER OF PERSONS MARRIED & DIVORCE BY AGE, 2015 | 2015 – 2026 | 69 | 85 | [`3.21.csv`](tables/3.21.csv) | [`3.21.json`](tables/3.21.json) |
| **3.22** | TABLE 3.22: NUMBER OF MARRIAGES, 2015 - 2016 | 2015 – 2026 | 28 | 102 | [`3.22.csv`](tables/3.22.csv) | [`3.22.json`](tables/3.22.json) |
| **3.23** | TABLE 3.23: NUMBER OF PERSONS MARRIED & DIVORCE BY AGE, 2016 | 2015 – 2026 | 26 | 59 | [`3.23.csv`](tables/3.23.csv) | [`3.23.json`](tables/3.23.json) |
| **3.24** | TABLE 3.24: NUMBER OF PERSONS MARRIED & DIVORCE BY AGE, 2017 | 2018 – 2026 | 26 | 110 | [`3.24.csv`](tables/3.24.csv) | [`3.24.json`](tables/3.24.json) |
| **3.25** | TABLE 3.25: NUMBER OF MARRIAGES AND DIVORCES BY ISLAND , 2019 | 2019 – 2026 | 202 | 33 | [`3.25.csv`](tables/3.25.csv) | [`3.25.json`](tables/3.25.json) |
| **3.26** | TABLE 3.26: NUMBER OF MARRIAGES AND DIVORCES BY ISLAND , 2019- 2024 | 2019 – 2024 | 194 | 13 | [`3.26.csv`](tables/3.26.csv) | [`3.26.json`](tables/3.26.json) |
| **3.3** | Table 3.3 : POPULATION, ANNUAL POPULATION GROWTH RATE AND REGISTERED POPULATION BY ATOLLS - 2000 AND 2006 | 2000 – 2026 | 426 | 162 | [`3.3.csv`](tables/3.3.csv) | [`3.3.json`](tables/3.3.json) |
| **3.3-revised** | Table 3.3 : TOTAL MALDIVIAN POPULATION BY ISLANDS, census 2006، 2014 and registered population 2014 | 2000 – 2016 | 221 | 18 | [`3.3-revised.csv`](tables/3.3-revised.csv) | [`3.3-revised.json`](tables/3.3-revised.json) |
| **3.4** | Table 3.4 : NUMBER OF INHABITED ISLANDS BY SIZE OF POPULATION | 1985 – 2025 | 66 | 23 | [`3.4.csv`](tables/3.4.csv) | [`3.4.json`](tables/3.4.json) |
| **3.4&fig3.2** | Table 3.4 : NUMBER OF INHABITED ISLANDS BY SIZE AND CLASS OF POPULATION | 1985 – 2006 | 15 | 6 | [`3.4&fig3.2.csv`](tables/3.4&fig3.2.csv) | [`3.4&fig3.2.json`](tables/3.4&fig3.2.json) |
| **3.5** | Table 3.5 : SEX RATIO OF POPULATION BY LOCALITY, 1985, 1990, 1995,2000 AND 2006 (Males per 100 female) | 1985 – 2026 | 213 | 16 | [`3.5.csv`](tables/3.5.csv) | [`3.5.json`](tables/3.5.json) |
| **3.5&fig3.3** | Table 3.5 : SEX RATIO OF POPULATION BY LOCALITY, 1985, 1990, 1995,2000 AND 2006 | 1985 – 2006 | 24 | 6 | [`3.5&fig3.3.csv`](tables/3.5&fig3.3.csv) | [`3.5&fig3.3.json`](tables/3.5&fig3.3.json) |
| **3.6** | Table 3.6 : ABRIDGE LIFE TABLE OF MALDIVES,2005,2006,2007 AND 2008 | 1985 – 2022 | 85 | 52 | [`3.6.csv`](tables/3.6.csv) | [`3.6.json`](tables/3.6.json) |
| **3.6-a** | Table 3.6 a: ABRIDGE LIFE TABLE OF MALDIVES BY SEX FOR INTERCENSAL YEARS, 1989 - 2015 | 1989 – 2013 | 22 | 16 | [`3.6-a.csv`](tables/3.6-a.csv) | [`3.6-a.json`](tables/3.6-a.json) |
| **3.6-b** | Table 3.6b: Improved life expectancy at birth series for Maldives, 1990-2015 | 2024 | 26 | 4 | [`3.6-b.csv`](tables/3.6-b.csv) | [`3.6-b.json`](tables/3.6-b.json) |
| **3.6a** | Table 3.6 a: ABRIDGE LIFE TABLE OF MALDIVES BY SEX FOR INTERCENSAL YEARS, 1989 - 2015 | 1989 – 2013 | 22 | 16 | [`3.6a.csv`](tables/3.6a.csv) | [`3.6a.json`](tables/3.6a.json) |
| **3.6b** | Table 3.6b: Improved life expectancy at birth series for Maldives, 1990-2015 | 2021 – 2023 | 26 | 10 | [`3.6b.csv`](tables/3.6b.csv) | [`3.6b.json`](tables/3.6b.json) |
| **3.7** | Table 3.7 : MONTHLY RECORDS OF BIRTHS AND DEATHS, 2007-2009 | 1985 – 2025 | 37 | 92 | [`3.7.csv`](tables/3.7.csv) | [`3.7.json`](tables/3.7.json) |
| **3.7&fig3.4** | Table 3.7 : MONTHLY RECORDS OF BIRTHS AND DEATHS, 2006-2008 | 2006 – 2009 | 13 | 16 | [`3.7&fig3.4.csv`](tables/3.7&fig3.4.csv) | [`3.7&fig3.4.json`](tables/3.7&fig3.4.json) |
| **3.8** | Table 3.8 : BIRTHS AND DEATHS, BY SEX AND LOCALITY, 2008 | 2009 – 2025 | 32 | 90 | [`3.8.csv`](tables/3.8.csv) | [`3.8.json`](tables/3.8.json) |
| **3.8a** | Table 3.8 a: ABRIDGE LIFE TABLE OF MALDIVES BY SEX FOR INTERCENSAL YEARS, 1989 - 2015 | 1989 – 2013 | 22 | 16 | [`3.8a.csv`](tables/3.8a.csv) | [`3.8a.json`](tables/3.8a.json) |
| **3.8b** | Table 3.8b: Improved life expectancy at birth series for Maldives, 1990-2015 | 2026 | 26 | 4 | [`3.8b.csv`](tables/3.8b.csv) | [`3.8b.json`](tables/3.8b.json) |
| **3.9** | Table 3.9 : LIVE BIRTHS AND INFANT DEATHS, 2007 - 2009 | 2007 – 2025 | 22 | 94 | [`3.9.csv`](tables/3.9.csv) | [`3.9.json`](tables/3.9.json) |
| **3.9&fig3.5** | Table 3.9 : LIVE BIRTHS AND INFANT DEATHS, 2006 - 2008 | 2006 – 2009 | 6 | 16 | [`3.9&fig3.5.csv`](tables/3.9&fig3.5.csv) | [`3.9&fig3.5.json`](tables/3.9&fig3.5.json) |

## Example SQLite Usage (Python)
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('3_0_population.db')

# Query any metric across all years in milliseconds:
df = pd.read_sql('''
    SELECT item_name, year, value, unit
    FROM master_panel
    WHERE table_id = '10.1' AND year >= 2010
    ORDER BY item_name, year
''', conn)
print(df.head())
```
