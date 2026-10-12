# Maldives Statistical Yearbooks — Master Multi-Year Category Archive

This archive provides **consolidated, harmonized longitudinal datasets** for every statistical category across all published editions of the **Statistical Yearbook of Maldives (2008 – 2026)** by the **National Bureau of Statistics (NBS)**.

## Key Capabilities & Structure
- **Total Categories**: 22
- **Total Time-Series Observations**: 958,949
- **Master SQLite Database ([`maldives_statistics_master.db`](maldives_statistics_master.db))**: A unified, high-performance database containing all tables, indexes, and the complete `all_stats_panel` repository across all 19 editions.
- **Category Tidy Panel CSVs (`master_panel.csv`)**: Long-format master files for each category containing all variables and all years.
- **Harmonized Wide CSVs (`tables/<table_id>.csv`)**: Multi-year tables with continuous chronological year columns, merging historical overlap with latest official revisions taking precedence.
- **Per-Category SQLite Databases (`<category>.db`)**: Standalone self-contained database for each specific domain.

## Category Breakdown & Quick Links

| Category | Time Span | Harmonized Tables | Panel Observations | SQLite Database | Category Directory |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **1.0 Geography** | 2006 – 2026 | 10 | 21,751 | [`1_0_geography.db`](1.0 Geography/1_0_geography.db) | [`1.0 Geography/`](1.0 Geography/) |
| **10.0 Tourism** | 2002 – 2027 | 18 | 54,882 | [`10_0_tourism.db`](10.0 Tourism/10_0_tourism.db) | [`10.0 Tourism/`](10.0 Tourism/) |
| **11.0 Transport and Communication** | 1990 – 2026 | 40 | 45,136 | [`11_0_transport_and_communication.db`](11.0 Transport and Communication/11_0_transport_and_communication.db) | [`11.0 Transport and Communication/`](11.0 Transport and Communication/) |
| **12.0 Electricity and water** | 1999 – 2026 | 27 | 31,429 | [`12_0_electricity_and_water.db`](12.0 Electricity and water/12_0_electricity_and_water.db) | [`12.0 Electricity and water/`](12.0 Electricity and water/) |
| **13.0 Public Finance** | 2001 – 2027 | 14 | 26,545 | [`13_0_public_finance.db`](13.0 Public Finance/13_0_public_finance.db) | [`13.0 Public Finance/`](13.0 Public Finance/) |
| **14.0 Money and banking** | 2001 – 2025 | 17 | 20,445 | [`14_0_money_and_banking.db`](14.0 Money and banking/14_0_money_and_banking.db) | [`14.0 Money and banking/`](14.0 Money and banking/) |
| **15.0 Foreign trade & Balance of payments** | 2000 – 2026 | 14 | 26,643 | [`15_0_foreign_trade_balance_of_payments.db`](15.0 Foreign trade & Balance of payments/15_0_foreign_trade_balance_of_payments.db) | [`15.0 Foreign trade & Balance of payments/`](15.0 Foreign trade & Balance of payments/) |
| **16.0 National Accounts** | 1995 – 2026 | 22 | 41,508 | [`16_0_national_accounts.db`](16.0 National Accounts/16_0_national_accounts.db) | [`16.0 National Accounts/`](16.0 National Accounts/) |
| **17.0 Prices** | 1998 – 2025 | 17 | 22,248 | [`17_0_prices.db`](17.0 Prices/17_0_prices.db) | [`17.0 Prices/`](17.0 Prices/) |
| **18.0 Pension & social protection** | 2009 – 2026 | 31 | 60,226 | [`18_0_pension_social_protection.db`](18.0 Pension & social protection/18_0_pension_social_protection.db) | [`18.0 Pension & social protection/`](18.0 Pension & social protection/) |
| **19.0 Human rights** | 1972 – 2026 | 13 | 7,083 | [`19_0_human_rights.db`](19.0 Human rights/19_0_human_rights.db) | [`19.0 Human rights/`](19.0 Human rights/) |
| **2.0 Environment** | 2001 – 2025 | 14 | 4,365 | [`2_0_environment.db`](2.0 Environment/2_0_environment.db) | [`2.0 Environment/`](2.0 Environment/) |
| **20.0 Political parties & Election** | 2008 – 2025 | 9 | 19,169 | [`20_0_political_parties_election.db`](20.0 Political parties & Election/20_0_political_parties_election.db) | [`20.0 Political parties & Election/`](20.0 Political parties & Election/) |
| **3.0 Population** | 1985 – 2030 | 39 | 329,213 | [`3_0_population.db`](3.0 Population/3_0_population.db) | [`3.0 Population/`](3.0 Population/) |
| **4.0 Housing and public infrastructure** | 2002 – 2025 | 9 | 4,530 | [`4_0_housing_and_public_infrastructure.db`](4.0 Housing and public infrastructure/4_0_housing_and_public_infrastructure.db) | [`4.0 Housing and public infrastructure/`](4.0 Housing and public infrastructure/) |
| **5.0 Employment** | 2007 – 2026 | 19 | 35,854 | [`5_0_employment.db`](5.0 Employment/5_0_employment.db) | [`5.0 Employment/`](5.0 Employment/) |
| **6.0 Health** | 1999 – 2026 | 29 | 43,603 | [`6_0_health.db`](6.0 Health/6_0_health.db) | [`6.0 Health/`](6.0 Health/) |
| **7.0 Education** | 1998 – 2026 | 39 | 83,751 | [`7_0_education.db`](7.0 Education/7_0_education.db) | [`7.0 Education/`](7.0 Education/) |
| **8.0 Law & Order** | 2002 – 2026 | 85 | 45,422 | [`8_0_law_order.db`](8.0 Law & Order/8_0_law_order.db) | [`8.0 Law & Order/`](8.0 Law & Order/) |
| **9.0 Fisheries & Agriculture** | 2001 – 2026 | 23 | 20,336 | [`9_0_fisheries_agriculture.db`](9.0 Fisheries & Agriculture/9_0_fisheries_agriculture.db) | [`9.0 Fisheries & Agriculture/`](9.0 Fisheries & Agriculture/) |
| **general** | 2018 – 2025 | 7 | 1,293 | [`general.db`](general/general.db) | [`general/`](general/) |
| **indicators** | 1990 – 2021 | 26 | 13,517 | [`indicators.db`](indicators/indicators.db) | [`indicators/`](indicators/) |

## How to Query the Master SQLite Database

### 1. From Python (Pandas)
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('data/master_categories/maldives_statistics_master.db')

# Query any metric across categories and years in milliseconds:
df = pd.read_sql('''
    SELECT category, table_id, item_name, metric_name, year, value, unit
    FROM all_stats_panel
    WHERE category = '10.0 Tourism' AND item_name = 'Germany' AND year >= 2010
    ORDER BY year ASC
''', conn)
print(df)
```

### 2. From Command Line
```bash
sqlite3 data/master_categories/maldives_statistics_master.db "SELECT year, value FROM all_stats_panel WHERE metric_name LIKE '%Tourist%' AND item_name = 'Total' ORDER BY year ASC;"
```
