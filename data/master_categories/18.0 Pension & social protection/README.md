# 18.0 Pension & social protection — Master Multi-Year Dataset

This directory houses the consolidated multi-year datasets for **18.0 Pension & social protection**, harmonizing data across all official Maldives Statistical Yearbook editions published between **2008 and 2026** by the National Bureau of Statistics (NBS).

## Available Formats
- **Consolidated Panel Dataset ([`master_panel.csv`](master_panel.csv))**: Long-format tabular dataset (60,226 rows) with schema: `[category, table_id, table_title, item_name, metric_name, year, value, unit, edition_year]`.
- **Category SQLite Database ([`18_0_pension_social_protection.db`](18_0_pension_social_protection.db))**: Fully indexed local database containing `master_panel` plus dedicated SQL tables for every individual harmonized table.
- **Harmonized Wide CSVs ([`tables/`](tables/))**: 31 individual multi-year CSV tables with continuous year columns.

## Category Summary
- **Time Horizon Covered**: **2009 – 2026**
- **Total Harmonized Tables**: 31
- **Total Time-Series Observations**: 60,226
- **SQLite Database**: [`18_0_pension_social_protection.db`](18_0_pension_social_protection.db)

## Harmonized Tables Catalog

| Table ID | Title | Time Span | Rows | Cols | Wide CSV | Metadata |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **18..25** | Table 18.25 : EXPENDITURE UNDER HEALTH INSURANCE SCHEMES BY ISLAND, 2014 - 2021 | 2014 – 2022 | 213 | 18 | [`18..25.csv`](tables/18..25.csv) | [`18..25.json`](tables/18..25.json) |
| **18.1** | Table 18.1: PUBLIC SECTOR INVESTMENT PROGRAMME, (PSIP), 2010-2011 | 2010 – 2024 | 395 | 206 | [`18.1.csv`](tables/18.1.csv) | [`18.1.json`](tables/18.1.json) |
| **18.10** | TABLE 18.10: AMOUNT OF CONTRIBUTION TO RETIREMENT PENSION SCHEME BY SECTOR, 2010 - 2014 | 2015 – 2026 | 17 | 57 | [`18.10.csv`](tables/18.10.csv) | [`18.10.json`](tables/18.10.json) |
| **18.10-1** | TABLE 18.10: AMOUNT OF CONTRIBUTION TO RETIREMENT PENSION SCHEME BY SECTOR, 2010 - 2018 | 2019 | 9 | 6 | [`18.10-1.csv`](tables/18.10-1.csv) | [`18.10-1.json`](tables/18.10-1.json) |
| **18.11** | TABLE 18.11: NUMBER OF MEMBERS CONTRIBUTING TO RETIREMENT PENSION SCHEME BY SECTOR AND SEX, 2010-2014 | 2015 – 2025 | 37 | 129 | [`18.11.csv`](tables/18.11.csv) | [`18.11.json`](tables/18.11.json) |
| **18.12** | TABLE 18.12: ESTABLISHMENTS REGISTERED IN THE RETIREMENT PENSION SCHEME, BY EMPLOYMENT SIZE, END 2014 | 2015 – 2026 | 43 | 90 | [`18.12.csv`](tables/18.12.csv) | [`18.12.json`](tables/18.12.json) |
| **18.13** | TABLE 18.13: EMPLOYEES REGISTERED IN THE RETIREMENT PENSION SCHEME, BY EMPLOYMENT SIZE, END 2014 | 2015 – 2026 | 27 | 78 | [`18.13.csv`](tables/18.13.csv) | [`18.13.json`](tables/18.13.json) |
| **18.14** | TABLE 18.13: EMPLOYEES REGISTERED IN THE RETIREMENT PENSION SCHEME, BY EMPLOYMENT SIZE, END 2014 | 2015 – 2026 | 29 | 62 | [`18.14.csv`](tables/18.14.csv) | [`18.14.json`](tables/18.14.json) |
| **18.15** | TABLE 18.15: EMPLOYEES REGISTERED IN THE RETIREMENT PENSION SCHEME, BY TYPE OF EMPLOYER, END OF 2014 | 2012 – 2026 | 40 | 72 | [`18.15.csv`](tables/18.15.csv) | [`18.15.json`](tables/18.15.json) |
| **18.16** | Table 18.16 : NUMBER OF PERSONS COVERED UNDER DIFFERENT SOCIAL PROTECTION SCHEMES BY ISLAND, 2014 | 2016 – 2026 | 52 | 161 | [`18.16.csv`](tables/18.16.csv) | [`18.16.json`](tables/18.16.json) |
| **18.17** | Table 18.15 : NUMBER OF PERSONS COVERED UNDER DIFFERENT SOCIAL PROTECTION SCHEMES BY ISLAND, 2014 | 2016 – 2025 | 222 | 93 | [`18.17.csv`](tables/18.17.csv) | [`18.17.json`](tables/18.17.json) |
| **18.18** | Table 18.18 : GOVERNMENT EXPENDITURE ON DIFFERENT SOCIAL PROTECTION SCHEMES BY TYPE (in MVR), 2014 | 2016 – 2026 | 40 | 57 | [`18.18.csv`](tables/18.18.csv) | [`18.18.json`](tables/18.18.json) |
| **18.19** | Table 18.19 : EXPENDITURE ON AASANDHA SERVICES BY TYPE OF INSTITUTION , 2014 | 2016 – 2026 | 202 | 78 | [`18.19.csv`](tables/18.19.csv) | [`18.19.json`](tables/18.19.json) |
| **18.2** | Table 18.2: PUBLIC SECTOR INVESTMENT PROGRAMME, NEW PROJECTS (PSIP), 2010-2011 ( In million Rf) | 2010 – 2025 | 241 | 83 | [`18.2.csv`](tables/18.2.csv) | [`18.2.json`](tables/18.2.json) |
| **18.20** | Table 18.20 : EXPENDITURE ON AASANDHA SERVICES BY TYPE OF INSTITUTION AND ATOLL , 2014 | 2016 – 2026 | 220 | 91 | [`18.20.csv`](tables/18.20.csv) | [`18.20.json`](tables/18.20.json) |
| **18.21** | Table 18.21 : EXPENDITURE ON PERSONS COVERED UNDER AASANDHA POLICIES BY TYPE OF SERVICE, 2014 - 2016 | 2011 – 2026 | 31 | 57 | [`18.21.csv`](tables/18.21.csv) | [`18.21.json`](tables/18.21.json) |
| **18.22** | Table 18.22 : EXPENDITURE UNDER HEALTH INSURANCE SCHEMES BY ATOLLS, 2014 - 2016 | 2012 – 2026 | 29 | 58 | [`18.22.csv`](tables/18.22.csv) | [`18.22.json`](tables/18.22.json) |
| **18.23** | Table 18.23 : EXPENDITURE UNDER HEALTH INSURANCE SCHEMES BY ISLAND, 2014 - 2016 | 2010 – 2026 | 225 | 94 | [`18.23.csv`](tables/18.23.csv) | [`18.23.json`](tables/18.23.json) |
| **18.24** | Table 18.24 : EXPENDITURE UNDER HEALTH INSURANCE SCHEMES BY ATOLLS, 2014 - 2020 | 2011 – 2025 | 36 | 28 | [`18.24.csv`](tables/18.24.csv) | [`18.24.json`](tables/18.24.json) |
| **18.25** | Table 18.25 : EXPENDITURE UNDER HEALTH INSURANCE SCHEMES BY ISLAND, 2014 - 2020 | 2012 – 2025 | 201 | 16 | [`18.25.csv`](tables/18.25.csv) | [`18.25.json`](tables/18.25.json) |
| **18.26** | Table 18.26: Aasandha Services provided by type, 2018 -2020 | 2014 – 2025 | 218 | 23 | [`18.26.csv`](tables/18.26.csv) | [`18.26.json`](tables/18.26.json) |
| **18.27** | Table 18.27: Aasandha Services provided by type and Atoll, 2020 | 2018 – 2024 | 28 | 16 | [`18.27.csv`](tables/18.27.csv) | [`18.27.json`](tables/18.27.json) |
| **18.28** | Table 18.28: Aasandha Services provided by type and Atoll, 2022 | 2023 – 2025 | 24 | 13 | [`18.28.csv`](tables/18.28.csv) | [`18.28.json`](tables/18.28.json) |
| **18.3** | TABLE 18.3: BUDGET ALLOCATED FOR CONSTRUCTION OF MOSQUES, 2010-2011 ( In million Rf) | 2010 – 2025 | 69 | 120 | [`18.3.csv`](tables/18.3.csv) | [`18.3.json`](tables/18.3.json) |
| **18.4** | TABLE 18.4: BUDGET ALLOCATED FOR CONSTRUCTION AND RENOVATION OF ISLAND OFFICES, ACCOMODATION BLOCKS AND COURTS, 2010 - 2011 ( In million Rf) | 2009 – 2025 | 39 | 80 | [`18.4.csv`](tables/18.4.csv) | [`18.4.json`](tables/18.4.json) |
| **18.5** | Table 18.5: BUDGET ALLOCATED FOR CONSTRUCTION AND RENOVATION OF SCHOOLS AND RESIDENTIAL LEARNING CENTRES, 2010 - 2011 ( In million Rf) | 2010 – 2025 | 62 | 98 | [`18.5.csv`](tables/18.5.csv) | [`18.5.json`](tables/18.5.json) |
| **18.6** | TABLE 18.6: BUDGET ALLOCATED FOR CONSTRUCTION OF HABOURS, 2010 - 2011 ( In million Rf) | 2010 – 2025 | 42 | 85 | [`18.6.csv`](tables/18.6.csv) | [`18.6.json`](tables/18.6.json) |
| **18.7** | Table18.7: ALLOCATIONS FOR DEVELOPMENT PROJECTS, BY MINISTRIES, 2009 | 2010 – 2019 | 36 | 27 | [`18.7.csv`](tables/18.7.csv) | [`18.7.json`](tables/18.7.json) |
| **18.8** | Table 18.8: REPORTED EXPENDITURE FOR DEVELOPMENT PROJECTS, MINISTRIES, 2009 | 2010 – 2026 | 229 | 70 | [`18.8.csv`](tables/18.8.csv) | [`18.8.json`](tables/18.8.json) |
| **18.9** | Table18.9: ALLOCATION FOR DEVELOPMENT PROJECTS, BY MINISTRIES, 2010 | 2010 – 2025 | 229 | 23 | [`18.9.csv`](tables/18.9.csv) | [`18.9.json`](tables/18.9.json) |
| **18.9-1** | TABLE 18.9: PERSONS CONTRIBUTING TO THE RETIREMENT PENSION SCHEME AND CONTRIBUTIONS , 2014 - 2018 | 2014 – 2018 | 5 | 6 | [`18.9-1.csv`](tables/18.9-1.csv) | [`18.9-1.json`](tables/18.9-1.json) |

## Example SQLite Usage (Python)
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('18_0_pension_social_protection.db')

# Query any metric across all years in milliseconds:
df = pd.read_sql('''
    SELECT item_name, year, value, unit
    FROM master_panel
    WHERE table_id = '10.1' AND year >= 2010
    ORDER BY item_name, year
''', conn)
print(df.head())
```
