# 8.0 Law & Order — Master Multi-Year Dataset

This directory houses the consolidated multi-year datasets for **8.0 Law & Order**, harmonizing data across all official Maldives Statistical Yearbook editions published between **2008 and 2026** by the National Bureau of Statistics (NBS).

## Available Formats
- **Consolidated Panel Dataset ([`master_panel.csv`](master_panel.csv))**: Long-format tabular dataset (45,422 rows) with schema: `[category, table_id, table_title, item_name, metric_name, year, value, unit, edition_year]`.
- **Category SQLite Database ([`8_0_law_order.db`](8_0_law_order.db))**: Fully indexed local database containing `master_panel` plus dedicated SQL tables for every individual harmonized table.
- **Harmonized Wide CSVs ([`tables/`](tables/))**: 85 individual multi-year CSV tables with continuous year columns.

## Category Summary
- **Time Horizon Covered**: **2002 – 2026**
- **Total Harmonized Tables**: 85
- **Total Time-Series Observations**: 45,422
- **SQLite Database**: [`8_0_law_order.db`](8_0_law_order.db)

## Harmonized Tables Catalog

| Table ID | Title | Time Span | Rows | Cols | Wide CSV | Metadata |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **8.1** | Table 8.1: CASES DEALT BY JUDICIAL COURTS IN MALE' AND ATOLLS, 2008 & 2009 | 2008 – 2025 | 29 | 56 | [`8.1.csv`](tables/8.1.csv) | [`8.1.json`](tables/8.1.json) |
| **8.1&fig8.1** | Table 8.1 : CASES DEALT BY JUDICIAL COURTS IN MALE' AND ISLANDS, 2002 - 2010 | 2002 – 2010 | 8 | 10 | [`8.1&fig8.1.csv`](tables/8.1&fig8.1.csv) | [`8.1&fig8.1.json`](tables/8.1&fig8.1.json) |
| **8.10** | Table 8.10: NUMBER OF REPEATED DETAINEES BY TYPE OF OFFENCE, SEX AND AGE GROUP, 2009 | 2010 – 2025 | 41 | 69 | [`8.10.csv`](tables/8.10.csv) | [`8.10.json`](tables/8.10.json) |
| **8.11** | Table 8.11: SUMMARY OF ALL CASES FILED IN COURTS IN MALE' AND ISLANDS, 2009 - 2010 | 2009 – 2025 | 38 | 40 | [`8.11.csv`](tables/8.11.csv) | [`8.11.json`](tables/8.11.json) |
| **8.12** | Table 8.12: NUMBER OF CRIMINAL CASES FILED BY CATERGORIES, 2007 - 2010 | 2007 – 2024 | 25 | 39 | [`8.12.csv`](tables/8.12.csv) | [`8.12.json`](tables/8.12.json) |
| **8.13** | Table 8.13: NUMBER OF CIVIL CASES FILED BY CATERGORIES, 2007 - 2010 | 2007 – 2024 | 34 | 54 | [`8.13.csv`](tables/8.13.csv) | [`8.13.json`](tables/8.13.json) |
| **8.14** | Table 8.14: NUMBER OF DETAINEES BY NUMBER OF TIMES ARRESTED, 2009 - 2014 | 2009 – 2025 | 235 | 24 | [`8.14.csv`](tables/8.14.csv) | [`8.14.json`](tables/8.14.json) |
| **8.14fig8.6** | Table 8.14: Trend showing logged cases from 1992 to 2010 | 2011 | 19 | 2 | [`8.14fig8.6.csv`](tables/8.14fig8.6.csv) | [`8.14fig8.6.json`](tables/8.14fig8.6.json) |
| **8.15** | Table 8.15: NUMBER OF REPORTED CHILD ABUSE CASES BY TYPE, 2010 | 2009 – 2025 | 43 | 69 | [`8.15.csv`](tables/8.15.csv) | [`8.15.json`](tables/8.15.json) |
| **8.15-1** | Table 8.15: NUMBER OF DETAINEES BY NUMBER OF TIMES ARRESTED, 2016 - 2018 | 2016 – 2019 | 16 | 5 | [`8.15-1.csv`](tables/8.15-1.csv) | [`8.15-1.json`](tables/8.15-1.json) |
| **8.16** | Table: 8.16 NUMBER OF LOCAL AND FOREIGN DETAINEES BY TYPE OF OFFENCES, 2011 - 2014 | 2010 – 2025 | 26 | 71 | [`8.16.csv`](tables/8.16.csv) | [`8.16.json`](tables/8.16.json) |
| **8.16-2** | Table 8.16: NUMBER OF DETAINEES REPORTED BY TYPE OF OFFENCES, GENDER AND AGE GROUP, 2018 | 2019 | 22 | 13 | [`8.16-2.csv`](tables/8.16-2.csv) | [`8.16-2.json`](tables/8.16-2.json) |
| **8.17** | TABLE 8.17: POLICE PERSONNEL BY SEX AND FINANCIAL RESOURCES, 2010 - 2014 | 2010 – 2023 | 29 | 55 | [`8.17.csv`](tables/8.17.csv) | [`8.17.json`](tables/8.17.json) |
| **8.17-1** | Table: 8.17 NUMBER OF LOCAL AND FOREIGN DETAINEES BY TYPE OF OFFENCES, 2016 - 2018 | 2016 – 2018 | 24 | 10 | [`8.17-1.csv`](tables/8.17-1.csv) | [`8.17-1.json`](tables/8.17-1.json) |
| **8.18** | Table 8.18: NUMBER OF REPORTED CHILD ABUSE CASES BY TYPE, 2010 | 2002 – 2024 | 18 | 38 | [`8.18.csv`](tables/8.18.csv) | [`8.18.json`](tables/8.18.json) |
| **8.18-1** | TABLE 8.18: POLICE PERSONNEL BY SEX AND FINANCIAL RESOURCES, 2013 - 2018 | 2013 – 2018 | 4 | 7 | [`8.18-1.csv`](tables/8.18-1.csv) | [`8.18-1.json`](tables/8.18-1.json) |
| **8.19** | Table 8.19: CASES HANDLED BY THE HIGH COURT, 2014 - 2015 | 2008 – 2024 | 33 | 102 | [`8.19.csv`](tables/8.19.csv) | [`8.19.json`](tables/8.19.json) |
| **8.19-1** | Table 8.19: NUMBER OF VICTIMS BY TYPE OF OFFENCE AND SEX, 2016 - 2018 | 2017 – 2019 | 26 | 13 | [`8.19-1.csv`](tables/8.19-1.csv) | [`8.19-1.json`](tables/8.19-1.json) |
| **8.2** | Table 8.2 : PERSONS SENTENCED, BY AGE AND SEX, 2008 - 2009 | 2008 – 2025 | 34 | 88 | [`8.2.csv`](tables/8.2.csv) | [`8.2.json`](tables/8.2.json) |
| **8.2&fig8.3** | Table 8.2: LOGGED CASES FROM THE YEAR 2009 - 2010 | 2008 – 2010 | 14 | 6 | [`8.2&fig8.3.csv`](tables/8.2&fig8.3.csv) | [`8.2&fig8.3.json`](tables/8.2&fig8.3.json) |
| **8.20** | Table 8.20 : CASES DEALT BY JUDICIAL COURTS IN MALE' AND ISLANDS, 2010 - 2017 | 2010 – 2025 | 28 | 75 | [`8.20.csv`](tables/8.20.csv) | [`8.20.json`](tables/8.20.json) |
| **8.20-1** | Table 8.20: NUMBER OF VICTIMS BY TYPE OF OFFENCES, GENDER AND AGE GROUP, 2018 | 2019 | 20 | 13 | [`8.20-1.csv`](tables/8.20-1.csv) | [`8.20-1.json`](tables/8.20-1.json) |
| **8.21** | Table 8.21: SUMMARY OF ALL NEW CASES FILED IN COURTS IN MALE' AND ATOLLS, 2014 - 2015 | 2009 – 2025 | 55 | 50 | [`8.21.csv`](tables/8.21.csv) | [`8.21.json`](tables/8.21.json) |
| **8.21-1** | Table 8.21 : CASES DEALT BY JUDICIAL COURTS IN MALE' AND ISLANDS, 2010 - 2018 | 2010 – 2018 | 9 | 10 | [`8.21-1.csv`](tables/8.21-1.csv) | [`8.21-1.json`](tables/8.21-1.json) |
| **8.22** | Table 8.22: NUMBER OF CRIMINAL CASES FILED BY CATERGORIES, 2007 - 2015 | 2007 – 2025 | 60 | 79 | [`8.22.csv`](tables/8.22.csv) | [`8.22.json`](tables/8.22.json) |
| **8.23** | Table 8.23: NUMBER OF CIVIL CASES FILED BY CATERGORIES, 2007 - 2015 | 2007 – 2023 | 74 | 92 | [`8.23.csv`](tables/8.23.csv) | [`8.23.json`](tables/8.23.json) |
| **8.24** | TABLE 8.24: NUMBER OF CASES SENT TO COURT TRIAL, 2013 - 2014 | 2011 – 2021 | 93 | 60 | [`8.24.csv`](tables/8.24.csv) | [`8.24.json`](tables/8.24.json) |
| **8.25** | TABLE 8.25: NUMBER OF CASES SUBMITTED AND COMPLETED, 2011 - 2014 | 2011 – 2023 | 43 | 20 | [`8.25.csv`](tables/8.25.csv) | [`8.25.json`](tables/8.25.json) |
| **8.26** | TABLE 8.26: PROSECUTION PERSONNEL BY SEX AND FINANCIAL RESOURCES, 2010 - 2014 | 2010 – 2023 | 177 | 22 | [`8.26.csv`](tables/8.26.csv) | [`8.26.json`](tables/8.26.json) |
| **8.27** | TABLE 8.27: NUMBER OF ASSIGNED MAGISTRATES , 2014 - 2016 | 2012 – 2023 | 182 | 19 | [`8.27.csv`](tables/8.27.csv) | [`8.27.json`](tables/8.27.json) |
| **8.28** | TABLE 8.28: JUDGES BY SEX AND FINANCIAL RESOURCES FOR COURTS , 2013 - 2016 | 2010 – 2024 | 23 | 33 | [`8.28.csv`](tables/8.28.csv) | [`8.28.json`](tables/8.28.json) |
| **8.28-1** | Table 8.28: Age distribution of cases filed in the Drug Court 2016-2018 | 2016 – 2019 | 7 | 5 | [`8.28-1.csv`](tables/8.28-1.csv) | [`8.28-1.json`](tables/8.28-1.json) |
| **8.29** | TABLE 8.29: REGISTERED LAWYERS IN SERVICE, BY QUALIFICATION AND SEX, 2014 - 2016 | 2012 – 2023 | 187 | 28 | [`8.29.csv`](tables/8.29.csv) | [`8.29.json`](tables/8.29.json) |
| **8.3** | Table 8.3: LOGGED CASES FROM THE YEAR 2008 - 2009 | 2008 – 2020 | 32 | 107 | [`8.3.csv`](tables/8.3.csv) | [`8.3.json`](tables/8.3.json) |
| **8.3&fig8.4** | Table 8.3: LOGGED CASES 2009 - 2010 | 2007 – 2010 | 13 | 5 | [`8.3&fig8.4.csv`](tables/8.3&fig8.4.csv) | [`8.3&fig8.4.json`](tables/8.3&fig8.4.json) |
| **8.30** | TABLE 8.30: JUDGES BY SEX AND FINANCIAL RESOURCES FOR COURTS , 2013 - 2017 | 2010 – 2023 | 13 | 25 | [`8.30.csv`](tables/8.30.csv) | [`8.30.json`](tables/8.30.json) |
| **8.31** | TABLE 8.31: REGISTERED LAWYERS IN SERVICE, BY QUALIFICATION AND SEX, 2014 - 2017 | 2008 – 2024 | 21 | 123 | [`8.31.csv`](tables/8.31.csv) | [`8.31.json`](tables/8.31.json) |
| **8.32** | TABLE 8.32: NUMBER OF CASES REPORTED ON CORRUPTION BY LOCALITY, 2013 - 2017 | 2010 – 2024 | 54 | 91 | [`8.32.csv`](tables/8.32.csv) | [`8.32.json`](tables/8.32.json) |
| **8.33** | Table 8.33: Cases registered by type, 2015 - 2017 | 2011 – 2023 | 45 | 82 | [`8.33.csv`](tables/8.33.csv) | [`8.33.json`](tables/8.33.json) |
| **8.34** | Table 8.34: Number of investigation completed cases, 2014 - 2017 | 2015 – 2023 | 295 | 14 | [`8.34.csv`](tables/8.34.csv) | [`8.34.json`](tables/8.34.json) |
| **8.35** | TABLE 8.35: TYPE OF OFFENSES SENT TO PROSECUTOR GENERAL'S OFFICE , 2011 - 2017 | 2011 – 2022 | 41 | 18 | [`8.35.csv`](tables/8.35.csv) | [`8.35.json`](tables/8.35.json) |
| **8.36** | TABLE 8.36: NUMBER OF CASES REPORTED TO THE COMMISSION BY ADDRESSEE, 2014 - 2017 | 2010 – 2023 | 36 | 21 | [`8.36.csv`](tables/8.36.csv) | [`8.36.json`](tables/8.36.json) |
| **8.37** | TABLE 8.37: NUMBER OF CASES REPORTED ON CORRUPTION BY LOCALITY, 2013 - 2018 | 2010 – 2024 | 35 | 22 | [`8.37.csv`](tables/8.37.csv) | [`8.37.json`](tables/8.37.json) |
| **8.38** | TABLE 8.38: NUMBER OF ASSIGNED MAGISTRATES , 2017 - 2020 | 2017 – 2023 | 166 | 8 | [`8.38.csv`](tables/8.38.csv) | [`8.38.json`](tables/8.38.json) |
| **8.39** | Table 8.39 : PERSONS SENTENCED, BY AGE AND SEX, 2014 - 2017 | 2010 – 2023 | 21 | 32 | [`8.39.csv`](tables/8.39.csv) | [`8.39.json`](tables/8.39.json) |
| **8.4** | Table 8.4: LOGGED CASES 2007 - 2009 | 2007 – 2026 | 29 | 259 | [`8.4.csv`](tables/8.4.csv) | [`8.4.json`](tables/8.4.json) |
| **8.40** | Table 8.40 : PERSONS SENTENCED, BY TYPE AND PERIOD, 2016 - 2017 | 2011 – 2023 | 26 | 39 | [`8.40.csv`](tables/8.40.csv) | [`8.40.json`](tables/8.40.json) |
| **8.41** | Table 8.41: NUMBER OF REPORTED CHILD ABUSE CASES (UNDER 18) BY TYPE, 2009 - 2017 | 2009 – 2018 | 45 | 11 | [`8.41.csv`](tables/8.41.csv) | [`8.41.json`](tables/8.41.json) |
| **8.42** | Table 8.42 : PERSONS SENTENCED, BY AGE AND SEX, 2014 - 2016 | 2011 – 2023 | 35 | 49 | [`8.42.csv`](tables/8.42.csv) | [`8.42.json`](tables/8.42.json) |
| **8.43** | Table 8.43 : PERSONS SENTENCED, BY TYPE AND PERIOD, 2014 - 2016 | 2014 – 2023 | 34 | 39 | [`8.43.csv`](tables/8.43.csv) | [`8.43.json`](tables/8.43.json) |
| **8.44** | Table 8.44: Number of cases reported regarding behavioural problems of children by sex, 2017 | 2009 – 2024 | 286 | 18 | [`8.44.csv`](tables/8.44.csv) | [`8.44.json`](tables/8.44.json) |
| **8.45** | Table 8.45: Number of cases reported to Atoll Social Protection Service Centers by age group and sex, 2014 - 2017 | 2011 – 2024 | 300 | 32 | [`8.45.csv`](tables/8.45.csv) | [`8.45.json`](tables/8.45.json) |
| **8.46** | Table 8.46: Number of cases reported to ministry by age group and sex, 2014 - 2017 | 2011 – 2023 | 35 | 51 | [`8.46.csv`](tables/8.46.csv) | [`8.46.json`](tables/8.46.json) |
| **8.47** | Table 8.47: Number of cases reported to Family and Children Service Centers by Atolls, 2013 - 2016 | 2010 – 2023 | 37 | 45 | [`8.47.csv`](tables/8.47.csv) | [`8.47.json`](tables/8.47.json) |
| **8.48** | Table 8.48 : Number of children at Childrens Shelter, K.Villingili, by age group and sex, 2014 - 2017 | 2014 – 2020 | 17 | 23 | [`8.48.csv`](tables/8.48.csv) | [`8.48.json`](tables/8.48.json) |
| **8.49** | Table 8.33 : PERSONS SENTENCED, BY TYPE AND PERIOD, 2018 - 2020 | 2018 – 2024 | 21 | 23 | [`8.49.csv`](tables/8.49.csv) | [`8.49.json`](tables/8.49.json) |
| **8.5** | Table 8.5 : CASES HANDLED BY THE HIGH COURT, 2007 -2009 | 2007 – 2025 | 18 | 32 | [`8.5.csv`](tables/8.5.csv) | [`8.5.json`](tables/8.5.json) |
| **8.5&fig8.5** | Table 8.5 : PERSONS SENTENCED, BY TYPE AND PERIOD, 2009 - 2010 | 2009 – 2010 | 9 | 13 | [`8.5&fig8.5.csv`](tables/8.5&fig8.5.csv) | [`8.5&fig8.5.json`](tables/8.5&fig8.5.json) |
| **8.50** | Table 8.50: Number of children at Childrens Shelter, K.Villimale', 2011 - 2017 | 2010 – 2022 | 50 | 42 | [`8.50.csv`](tables/8.50.csv) | [`8.50.json`](tables/8.50.json) |
| **8.51** | Table 8.51 : Number of children at Childrens Shelter, K.Villingili, by age group and sex, 2016 - 2018 | 2014 – 2022 | 21 | 27 | [`8.51.csv`](tables/8.51.csv) | [`8.51.json`](tables/8.51.json) |
| **8.52** | Table 8.52: School attendance of children at Childrens Shelter, K.Villingili, by age group and sex, 2017 | 2015 – 2023 | 36 | 35 | [`8.52.csv`](tables/8.52.csv) | [`8.52.json`](tables/8.52.json) |
| **8.53** | Table 8.53: School attendance of children at Childrens Shelter, Fiyavathi, by age group and sex, 2016 | 2010 – 2022 | 57 | 29 | [`8.53.csv`](tables/8.53.csv) | [`8.53.json`](tables/8.53.json) |
| **8.54** | TABLE 8.54: REPORTED CASES ON VIOLENCE AGAINST WOMEN BY TYPE, 2011 - 2017 | 2011 – 2022 | 62 | 17 | [`8.54.csv`](tables/8.54.csv) | [`8.54.json`](tables/8.54.json) |
| **8.55** | TABLE 8.55: Gender based violence and domestic violence, 2017 | 2011 – 2022 | 35 | 22 | [`8.55.csv`](tables/8.55.csv) | [`8.55.json`](tables/8.55.json) |
| **8.56** | Table 8.56: Gender distribution of cases filed in the Drug Court 2016 - 2017 | 2011 – 2024 | 45 | 20 | [`8.56.csv`](tables/8.56.csv) | [`8.56.json`](tables/8.56.json) |
| **8.57** | Table 8.57: Age distribution of cases filed in the Drug Court 2016-2017 | 2011 – 2023 | 61 | 21 | [`8.57.csv`](tables/8.57.csv) | [`8.57.json`](tables/8.57.json) |
| **8.58** | TABLE 8.58: Number of reported gender based violence and domestic violence, 2018 | 2011 – 2023 | 22 | 28 | [`8.58.csv`](tables/8.58.csv) | [`8.58.json`](tables/8.58.json) |
| **8.59** | TABLE 8.59: Number of cases reported related to person with disability and elderly perosn by sex, 2018 | 2019 – 2024 | 22 | 30 | [`8.59.csv`](tables/8.59.csv) | [`8.59.json`](tables/8.59.json) |
| **8.59-1** | TABLE 8.59: Number of cases reported related to person with disability and elderly perosn by sex, 2018 | 2019 | 3 | 4 | [`8.59-1.csv`](tables/8.59-1.csv) | [`8.59-1.json`](tables/8.59-1.json) |
| **8.6** | Table 8.6 : PERSONS SENTENCED, BY TYPE AND PERIOD, 2009 | 2008 – 2026 | 57 | 28 | [`8.6.csv`](tables/8.6.csv) | [`8.6.json`](tables/8.6.json) |
| **8.6-1** | Table 8.6: TREND SHOWING LOGGED CASES, 1992 - 2018 | 2019 | 27 | 2 | [`8.6-1.csv`](tables/8.6-1.csv) | [`8.6-1.json`](tables/8.6-1.json) |
| **8.60** | Table 8.60: Number of person commited in Human Trafficking, 2018 - 2019 | 2009 – 2024 | 15 | 23 | [`8.60.csv`](tables/8.60.csv) | [`8.60.json`](tables/8.60.json) |
| **8.61** | Table 8.61: Number of cases filed and concluded in Human Trafficking 2018 - 2019 | 2017 – 2022 | 12 | 21 | [`8.61.csv`](tables/8.61.csv) | [`8.61.json`](tables/8.61.json) |
| **8.62** | Table 8.62: NUMBER OF REPORTED CHILD ABUSE CASES BY TYPE AND AGE OF CHILD, 2019 | 2021 – 2023 | 11 | 25 | [`8.62.csv`](tables/8.62.csv) | [`8.62.json`](tables/8.62.json) |
| **8.63** | Table 8.63: Number of cases reported regarding behavioural problems of children by sex, 2020 | 2018 – 2023 | 24 | 22 | [`8.63.csv`](tables/8.63.csv) | [`8.63.json`](tables/8.63.json) |
| **8.64** | Table 8.64: Number of cases reported to Atoll Social Protection Service Centers by age group and sex, 2016 - 2019 | 2015 – 2023 | 11 | 22 | [`8.64.csv`](tables/8.64.csv) | [`8.64.json`](tables/8.64.json) |
| **8.65** | Table 8.65: Number of cases reported to ministry by age group and sex, 2014 - 2019 | 2014 – 2023 | 16 | 31 | [`8.65.csv`](tables/8.65.csv) | [`8.65.json`](tables/8.65.json) |
| **8.66** | Table 8.66: Number of cases reported to Family and Children Service Centers by Atolls, 2018 - 2020 | 2016 – 2023 | 23 | 25 | [`8.66.csv`](tables/8.66.csv) | [`8.66.json`](tables/8.66.json) |
| **8.67** | TABLE 8.67: REPORTED CASES ON VIOLENCE AGAINST WOMEN BY TYPE, 2015 - 2020 | 2011 – 2022 | 4 | 19 | [`8.67.csv`](tables/8.67.csv) | [`8.67.json`](tables/8.67.json) |
| **8.68** | TABLE 8.68: Number of reported gender based violence and domestic violence, 2018 - 2020 | 2018 – 2022 | 9 | 16 | [`8.68.csv`](tables/8.68.csv) | [`8.68.json`](tables/8.68.json) |
| **8.69** | TABLE 8.69: Number of cases reported related to person with disability and elderly perosn by sex, 2018 | 2020 – 2022 | 3 | 7 | [`8.69.csv`](tables/8.69.csv) | [`8.69.json`](tables/8.69.json) |
| **8.7** | Table 8.7: NUMBER OF DETAINEES REPORTED BY TYPE OF OFFENCE AND SEX, 2008 - 2009 | 2008 – 2025 | 31 | 45 | [`8.7.csv`](tables/8.7.csv) | [`8.7.json`](tables/8.7.json) |
| **8.7-1** | Table 8.7: THEFT CASES LOGGED BY TYPE, 2016 - 2018 | 2011 – 2018 | 8 | 11 | [`8.7-1.csv`](tables/8.7-1.csv) | [`8.7-1.json`](tables/8.7-1.json) |
| **8.8** | Table 8.8: NUMBER OF REPEATED DETAINEES BY TYPE OF OFFENCE AND SEX, 2008 - 2009 | 2008 – 2025 | 22 | 58 | [`8.8.csv`](tables/8.8.csv) | [`8.8.json`](tables/8.8.json) |
| **8.9** | Table 8.9: Number of detainees reported by type of offences, sex and agegroup, 2009 | 2009 – 2025 | 19 | 52 | [`8.9.csv`](tables/8.9.csv) | [`8.9.json`](tables/8.9.json) |

## Example SQLite Usage (Python)
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('8_0_law_order.db')

# Query any metric across all years in milliseconds:
df = pd.read_sql('''
    SELECT item_name, year, value, unit
    FROM master_panel
    WHERE table_id = '10.1' AND year >= 2010
    ORDER BY item_name, year
''', conn)
print(df.head())
```
