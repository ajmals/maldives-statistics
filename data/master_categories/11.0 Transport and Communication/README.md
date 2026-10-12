# 11.0 Transport and Communication — Master Multi-Year Dataset

This directory houses the consolidated multi-year datasets for **11.0 Transport and Communication**, harmonizing data across all official Maldives Statistical Yearbook editions published between **2008 and 2026** by the National Bureau of Statistics (NBS).

## Available Formats
- **Consolidated Panel Dataset ([`master_panel.csv`](master_panel.csv))**: Long-format tabular dataset (45,136 rows) with schema: `[category, table_id, table_title, item_name, metric_name, year, value, unit, edition_year]`.
- **Category SQLite Database ([`11_0_transport_and_communication.db`](11_0_transport_and_communication.db))**: Fully indexed local database containing `master_panel` plus dedicated SQL tables for every individual harmonized table.
- **Harmonized Wide CSVs ([`tables/`](tables/))**: 40 individual multi-year CSV tables with continuous year columns.

## Category Summary
- **Time Horizon Covered**: **1990 – 2026**
- **Total Harmonized Tables**: 40
- **Total Time-Series Observations**: 45,136
- **SQLite Database**: [`11_0_transport_and_communication.db`](11_0_transport_and_communication.db)

## Harmonized Tables Catalog

| Table ID | Title | Time Span | Rows | Cols | Wide CSV | Metadata |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **11.1** | Table 11.1 : VESSELS ACCORDING TO REGISTRATION BY LOCALITY, 2008 - 2009 | 2008 – 2025 | 43 | 77 | [`11.1.csv`](tables/11.1.csv) | [`11.1.json`](tables/11.1.json) |
| **11.10** | Table 11.10 : AIRCRAFT MOVEMENT AT GAN INTERNATIONAL AIRPORT BY MONTH, 2009 | 2010 – 2026 | 180 | 119 | [`11.10.csv`](tables/11.10.csv) | [`11.10.json`](tables/11.10.json) |
| **11.11** | Table 11.11 : PASSENGER MOVEMENT AT GAN INTERNATIONAL AIRPORT BY MONTH, 2009 | 2010 – 2026 | 28 | 110 | [`11.11.csv`](tables/11.11.csv) | [`11.11.json`](tables/11.11.json) |
| **11.11&11.12** | Table 11.12 : CARGO HANDLED AT MALE' INTERNATIONAL AIRPORT BY MONTH, 2010 | 2011 | 13 | 8 | [`11.11&11.12.csv`](tables/11.11&11.12.csv) | [`11.11&11.12.json`](tables/11.11&11.12.json) |
| **11.12** | Table 11.12 : CARGO HANDLED AT MALE' INTERNATIONAL AIRPORT BY MONTH, 2009 (in Kg) | 2010 – 2026 | 37 | 120 | [`11.12.csv`](tables/11.12.csv) | [`11.12.json`](tables/11.12.json) |
| **11.12-1** | Table 11.12 TRANSPORT MOVEMENTS AT GAN INTERNATIONAL AIRPORT BY AIRLINE, CROSS-CLASSIFIED BY PASSENGER, CARGO AND MAIL, 2018 | 2019 | 10 | 10 | [`11.12-1.csv`](tables/11.12-1.csv) | [`11.12-1.json`](tables/11.12-1.json) |
| **11.13** | Table 11.13 : CARGO HANDLED AT GAN INTERNATIONAL AIRPORT BY MONTH, 2009 (in Kg) | 2010 – 2026 | 13 | 70 | [`11.13.csv`](tables/11.13.csv) | [`11.13.json`](tables/11.13.json) |
| **11.13&11.14** | Table 11.14 : MAIL HANDLED AT MALE' INTERNATIONAL AIRPORT BY MONTH, 2010 | 2011 | 13 | 6 | [`11.13&11.14.csv`](tables/11.13&11.14.csv) | [`11.13&11.14.json`](tables/11.13&11.14.json) |
| **11.14** | Table 11.14 : MAIL HANDLED AT MALE' INTERNATIONAL AIRPORT BY MONTH, 2009 (in Kg) | 2009 – 2026 | 13 | 75 | [`11.14.csv`](tables/11.14.csv) | [`11.14.json`](tables/11.14.json) |
| **11.15** | Table 11.15 : CARGO HANDLED AT DOMESTIC AIRPORTS BY MONTH, 2009 ( in kg ) | 2010 – 2026 | 13 | 159 | [`11.15.csv`](tables/11.15.csv) | [`11.15.json`](tables/11.15.json) |
| **11.15&11.16** | Table 11.15 : CARGO HANDLED AT DOMESTIC AIRPORTS BY MONTH, 2010 | 2011 | 13 | 7 | [`11.15&11.16.csv`](tables/11.15&11.16.csv) | [`11.15&11.16.json`](tables/11.15&11.16.json) |
| **11.16** | Table 11.16 MAIL HANDLED AT DOMESTIC AIRPORTS BY MONTH, 2009 ( in kg ) | 2010 – 2026 | 14 | 266 | [`11.16.csv`](tables/11.16.csv) | [`11.16.json`](tables/11.16.json) |
| **11.16-1** | Table 11.16 : NUMBER OF AIRCRAFT MOVEMENTS AT DOMESTIC AIRPORTS BY MONTH, 2015-2018 | 2011 – 2019 | 13 | 61 | [`11.16-1.csv`](tables/11.16-1.csv) | [`11.16-1.json`](tables/11.16-1.json) |
| **11.17** | Table 11.17 : INCOMING AND OUTGOING MAIL AND STAMPS SOLD, 2001 - 2008 | 2010 – 2024 | 21 | 199 | [`11.17.csv`](tables/11.17.csv) | [`11.17.json`](tables/11.17.json) |
| **11.17&FIG11.2** | Table 11.17: INTERNATIONAL AND NATIONAL COMMUNICATION,2001 - 2010 | 2011 | 11 | 8 | [`11.17&FIG11.2.csv`](tables/11.17&FIG11.2.csv) | [`11.17&FIG11.2.json`](tables/11.17&FIG11.2.json) |
| **11.17-1** | Table 11.17 : AIRCRAFT MOVEMENT AT VELANA INTERNATIONAL AIRPORT BY MONTH, 2018 | 2019 | 13 | 8 | [`11.17-1.csv`](tables/11.17-1.csv) | [`11.17-1.json`](tables/11.17-1.json) |
| **11.18** | Table 11.18 : TOTAL DOMESTIC MAIL VOLUME, 2004 - 2008 | 2004 – 2026 | 34 | 90 | [`11.18.csv`](tables/11.18.csv) | [`11.18.json`](tables/11.18.json) |
| **11.18&FIG11.3** | Table 11.18: TELECOMMUNICATION SERVICES, 2003 - 2010 | 2002 – 2011 | 8 | 11 | [`11.18&FIG11.3.csv`](tables/11.18&FIG11.3.csv) | [`11.18&FIG11.3.json`](tables/11.18&FIG11.3.json) |
| **11.19** | Table 11.19: INTERNATINAL AND NATIONAL COMMUNICATION, 2001 - 2009 (in 000 mins) | 2010 – 2026 | 30 | 98 | [`11.19.csv`](tables/11.19.csv) | [`11.19.json`](tables/11.19.json) |
| **11.2** | Table 11.2 : REGISTERED AND NEWLY REGISTERED VESSELS ACCORDING TO TYPE, 2006 - 2009 | 2006 – 2018 | 28 | 29 | [`11.2.csv`](tables/11.2.csv) | [`11.2.json`](tables/11.2.json) |
| **11.20** | Table 11.20: TELECOMMUNICATION SERVICES, 2002 - 2009 | 1990 – 2026 | 44 | 119 | [`11.20.csv`](tables/11.20.csv) | [`11.20.json`](tables/11.20.json) |
| **11.21** | Table 11.21: SELECTED VEHICLES ACCORDING TO REGISTRSTION,2010 | 2011 – 2026 | 22 | 102 | [`11.21.csv`](tables/11.21.csv) | [`11.21.json`](tables/11.21.json) |
| **11.22** | TABLE 11.22: FERRY SERVICES BY THE INTEGRATED TRANSPORT NETWORK, BY NUMBER OF FERRIES AND PASSENGER CAPACITY 2009-2010 | 2009 – 2026 | 20 | 92 | [`11.22.csv`](tables/11.22.csv) | [`11.22.json`](tables/11.22.json) |
| **11.23** | TABLE 11.23: PASSENGER MOVEMENT BY FERRY BY ATOLL AND ISLAND, 2010 | 2003 – 2026 | 214 | 86 | [`11.23.csv`](tables/11.23.csv) | [`11.23.json`](tables/11.23.json) |
| **11.24** | Table 11.24: INTERNATIONAL AND NATIONAL COMMUNICATION,2001 - 2012 | 2013 – 2026 | 25 | 150 | [`11.24.csv`](tables/11.24.csv) | [`11.24.json`](tables/11.24.json) |
| **11.25** | Table 11.25: MAIL HANDLED AT DOMESTIC AIRPORTS BY MONTH, 2014 | 2010 – 2026 | 18 | 231 | [`11.25.csv`](tables/11.25.csv) | [`11.25.json`](tables/11.25.json) |
| **11.26** | Table 11.26: TELECOMMUNICATION SERVICES, 2003 - 2014 | 2003 – 2025 | 50 | 128 | [`11.26.csv`](tables/11.26.csv) | [`11.26.json`](tables/11.26.json) |
| **11.27** | Table 11.27: INTERNATIONAL AND NATIONAL COMMUNICATION, 2001 - 2014 | 2003 – 2026 | 209 | 106 | [`11.27.csv`](tables/11.27.csv) | [`11.27.json`](tables/11.27.json) |
| **11.28** | TABLE 11.28: LICENSED BROADCASTERS (end 2014) | 2015 – 2026 | 50 | 38 | [`11.28.csv`](tables/11.28.csv) | [`11.28.json`](tables/11.28.json) |
| **11.29** |  | 2003 – 2019 | 9 | 24 | [`11.29.csv`](tables/11.29.csv) | [`11.29.json`](tables/11.29.json) |
| **11.3** | Table 11.3 : REGISTERED AND NEWLY REGISTERED VEHICLES ACCORDING TO TYPE, 2003, 2004, 2005 and 2009 | 2003 – 2023 | 67 | 88 | [`11.3.csv`](tables/11.3.csv) | [`11.3.json`](tables/11.3.json) |
| **11.30** | TABLE 11.30: NUMBER OF LICENSED REBROADCASTERS BY ATOLLS, 2011 - 2014 | 2011 – 2019 | 41 | 14 | [`11.30.csv`](tables/11.30.csv) | [`11.30.json`](tables/11.30.json) |
| **11.4** | Table 11.4 : AIR TRANSPORT MOVEMENTS AT MALE' INTERNATIONAL AIRPORT BY AIRLINE, CROSS-CLASSIFIED BY PASSENGER, CARGO AND MAIL, 2009 | 2010 – 2024 | 55 | 59 | [`11.4.csv`](tables/11.4.csv) | [`11.4.json`](tables/11.4.json) |
| **11.5** | Table 11.5 GAN AIR TRANSPORT MOVEMENTS BY AIRLINE, CROSS-CLASSIFIED BY PASSENGER, CARGO AND MAIL, 2009 | 2010 – 2015 | 34 | 39 | [`11.5.csv`](tables/11.5.csv) | [`11.5.json`](tables/11.5.json) |
| **11.6** | Table 11.6 : PASSENGER MOVEMENT AT MALE' INTERNATIONAL AIRPORT BY MONTH, 2009 | 2010 – 2018 | 23 | 49 | [`11.6.csv`](tables/11.6.csv) | [`11.6.json`](tables/11.6.json) |
| **11.6-1** | TABLE 11.6: SELECTED VEHICLES ACCORDING TO REGISTRATION, 2016 end | 2018 | 10 | 9 | [`11.6-1.csv`](tables/11.6-1.csv) | [`11.6-1.json`](tables/11.6-1.json) |
| **11.7** | Table 11.7 : PASSENGER MOVEMENTS AT DOMESTIC AIRPORTS BY MONTH, 2009 | 2010 – 2017 | 17 | 19 | [`11.7.csv`](tables/11.7.csv) | [`11.7.json`](tables/11.7.json) |
| **11.8** | Table 11.8 : NUMBER OF AIRCRAFT MOVEMENTS AT DOMESTIC AIRPORTS BY MONTH, 2006 - 2009 | 2006 – 2018 | 13 | 19 | [`11.8.csv`](tables/11.8.csv) | [`11.8.json`](tables/11.8.json) |
| **11.9** | Table 11.9 : AIRCRAFT MOVEMENT AT MALE' INTERNATIONAL AIRPORT BY MONTH, 2009 | 2010 | 13 | 9 | [`11.9.csv`](tables/11.9.csv) | [`11.9.json`](tables/11.9.json) |
| **11.9&11.10** | Table 11.10 : AIRCRAFT MOVEMENT AT GAN INTERNATIONAL AIRPORT BY MONTH, 2010 | 2011 | 13 | 9 | [`11.9&11.10.csv`](tables/11.9&11.10.csv) | [`11.9&11.10.json`](tables/11.9&11.10.json) |

## Example SQLite Usage (Python)
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('11_0_transport_and_communication.db')

# Query any metric across all years in milliseconds:
df = pd.read_sql('''
    SELECT item_name, year, value, unit
    FROM master_panel
    WHERE table_id = '10.1' AND year >= 2010
    ORDER BY item_name, year
''', conn)
print(df.head())
```
