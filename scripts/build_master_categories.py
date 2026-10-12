#!/usr/bin/env python3
"""
Build Master Multi-Year Category Datasets
Aggregates and harmonizes all statistical yearbook editions (2008–2026) by category.
Outputs:
1. Per-category harmonized wide CSVs (all years as columns)
2. Per-category long-form tidy panel CSVs (master_panel.csv)
3. Per-category SQLite database (<category>.db)
4. Master unified SQLite database across all categories (maldives_statistics_master.db)
5. Comprehensive documentation & catalogs
"""

import os
import re
import json
import sqlite3
import glob
import time
from collections import defaultdict
import pandas as pd
import numpy as np

CATEGORY_NORMALIZATION = {
    '3.0 population': '3.0 Population',
    'Social Protection': '18.0 Pension & social protection'
}

def normalize_category_name(raw_name):
    clean = raw_name.strip()
    return CATEGORY_NORMALIZATION.get(clean, clean)

def slugify(text):
    s = re.sub(r'[^a-zA-Z0-9]+', '_', text).strip('_').lower()
    return s if s else 'table'

def parse_col_header(col_name):
    col_str = str(col_name).strip()
    m = re.search(r'\b(19\d\d|20\d\d)\b', col_str)
    if m:
        year = int(m.group(1))
        metric = col_str[:m.start()] + col_str[m.end():]
        metric = re.sub(r'\s*-\s*$', '', metric).strip(' -_,()')
        if not metric:
            metric = 'Value'
        return metric, year
    return col_str, None

def build_category_master(cat_name, proc_dir='data/processed', out_base='data/master_categories'):
    cat_slug = slugify(cat_name)
    cat_out_dir = os.path.join(out_base, cat_name)
    tables_out_dir = os.path.join(cat_out_dir, 'tables')
    os.makedirs(tables_out_dir, exist_ok=True)

    print(f"\n========================================================")
    print(f"BUILDING MASTER DATASET FOR: {cat_name}")
    print(f"========================================================")

    years = sorted([y for y in os.listdir(proc_dir) if y.isdigit()], key=int)

    # Collect all table files for this category across all years
    table_files_by_id = defaultdict(list)
    table_meta_by_id = {}

    for y in years:
        # Check both raw cat_name and any variants
        for dir_cand in [cat_name, cat_name.lower(), cat_name.capitalize()]:
            yp = os.path.join(proc_dir, y, dir_cand)
            if os.path.isdir(yp):
                for cf in glob.glob(os.path.join(yp, '*.csv')):
                    tid = os.path.splitext(os.path.basename(cf))[0]
                    table_files_by_id[tid].append((y, cf))
                    meta_cand = os.path.join(yp, f'{tid}.json')
                    if os.path.exists(meta_cand) and tid not in table_meta_by_id:
                        try:
                            with open(meta_cand, 'r', encoding='utf-8') as jf:
                                table_meta_by_id[tid] = json.load(jf)
                        except Exception:
                            pass
                break

    if not table_files_by_id:
        print(f"  No tables found for category: {cat_name}")
        return None

    print(f"  Found {len(table_files_by_id)} unique tables across {len(years)} editions")

    # Build master panel rows
    panel_records = []
    harmonized_tables_catalog = []

    # Category SQLite DB setup
    cat_db_path = os.path.join(cat_out_dir, f"{cat_slug}.db")
    if os.path.exists(cat_db_path):
        os.remove(cat_db_path)
    cat_conn = sqlite3.connect(cat_db_path)

    for tid, files in sorted(table_files_by_id.items()):
        meta = table_meta_by_id.get(tid, {})
        title = meta.get('title_en', f'Table {tid}')
        unit = meta.get('unit', '')

        # Melt all edition data for this table
        raw_entries = []
        for y_str, fpath in sorted(files, key=lambda x: int(x[0])):
            try:
                df = pd.read_csv(fpath)
                if df.empty or len(df.columns) < 2:
                    continue
                dim_col = df.columns[0]
                for col in df.columns[1:]:
                    metric, yr = parse_col_header(col)
                    if yr is None:
                        yr = int(y_str)
                    for _, row in df.iterrows():
                        item = str(row[dim_col]).strip()
                        val = row[col]
                        if pd.notna(val) and str(val).strip() not in ('', '-', 'nan', 'NaN'):
                            val_str = str(val).replace(',', '').strip()
                            raw_entries.append({
                                'category': cat_name,
                                'table_id': tid,
                                'table_title': title,
                                'item_name': item,
                                'metric_name': metric,
                                'year': int(yr),
                                'value': val_str,
                                'unit': unit,
                                'edition_year': int(y_str)
                            })
            except Exception as e:
                print(f"    [Warn] Error parsing {fpath}: {e}")

        if not raw_entries:
            continue

        df_entries = pd.DataFrame(raw_entries)

        # Deduplicate panel records: later edition years take precedence
        df_dedup = df_entries.sort_values('edition_year').drop_duplicates(
            subset=['item_name', 'metric_name', 'year'],
            keep='last'
        )

        panel_records.extend(df_dedup.to_dict('records'))

        # Build Harmonized Wide Table
        # If the table has year-based time series:
        unique_years = sorted(df_dedup['year'].unique())
        unique_metrics = df_dedup['metric_name'].unique()

        wide_df = None
        if len(unique_metrics) == 1:
            wide_df = df_dedup.pivot_table(
                index='item_name',
                columns='year',
                values='value',
                aggfunc='last'
            ).reset_index()
            wide_df.columns.name = None
            wide_df.rename(columns={'item_name': 'Item'}, inplace=True)
        else:
            # Multi-metric wide table
            # Try to see if there's a primary metric or format as Metric - Year
            wide_df = df_dedup.pivot_table(
                index='item_name',
                columns=['metric_name', 'year'],
                values='value',
                aggfunc='last'
            )
            # Flatten multi-index columns
            wide_df.columns = [f"{m} - {y}" for m, y in wide_df.columns]
            wide_df = wide_df.reset_index()
            wide_df.rename(columns={'item_name': 'Item'}, inplace=True)

        # Save Harmonized Wide CSV & JSON
        table_csv_path = os.path.join(tables_out_dir, f"{tid}.csv")
        table_json_path = os.path.join(tables_out_dir, f"{tid}.json")

        wide_df.to_csv(table_csv_path, index=False, encoding='utf-8')

        year_min = int(min(unique_years)) if len(unique_years) else 0
        year_max = int(max(unique_years)) if len(unique_years) else 0
        time_span = f"{year_min} – {year_max}" if year_min != year_max else str(year_min)

        table_meta = {
            'table_id': tid,
            'category': cat_name,
            'title_en': title,
            'unit': unit,
            'source': meta.get('source', ''),
            'notes': meta.get('notes', []),
            'time_span': time_span,
            'year_min': year_min,
            'year_max': year_max,
            'row_count': len(wide_df),
            'column_count': len(wide_df.columns),
            'columns': list(wide_df.columns),
            'editions_covered': len(files),
            'csv_file': f"tables/{tid}.csv"
        }

        with open(table_json_path, 'w', encoding='utf-8') as jf:
            json.dump(table_meta, jf, indent=2, ensure_ascii=False)

        harmonized_tables_catalog.append(table_meta)

        # Write wide table to category SQLite DB
        sql_table_name = f"t_{slugify(tid)}"
        try:
            # Clean and deduplicate column names for SQLite
            clean_wide_df = wide_df.copy()
            cols = []
            seen_cols = {}
            for c in clean_wide_df.columns:
                slug_c = slugify(str(c))
                if slug_c in seen_cols:
                    seen_cols[slug_c] += 1
                    cols.append(f"{slug_c}_{seen_cols[slug_c]}")
                else:
                    seen_cols[slug_c] = 1
                    cols.append(slug_c)
            clean_wide_df.columns = cols
            clean_wide_df.to_sql(sql_table_name, cat_conn, if_exists='replace', index=False)
        except Exception as e:
            print(f"    [Warn] SQLite table save failed for {sql_table_name}: {e}")

    # Build Master Panel DataFrame
    master_panel_df = pd.DataFrame(panel_records)
    if not master_panel_df.empty:
        # Sort master panel cleanly
        master_panel_df.sort_values(by=['table_id', 'item_name', 'metric_name', 'year'], inplace=True)

        master_panel_csv_path = os.path.join(cat_out_dir, 'master_panel.csv')
        master_panel_df.to_csv(master_panel_csv_path, index=False, encoding='utf-8')

        # Save master_panel into SQLite DB
        master_panel_df.to_sql('master_panel', cat_conn, if_exists='replace', index=False)
        cat_conn.execute("CREATE INDEX IF NOT EXISTS idx_panel_table ON master_panel(table_id);")
        cat_conn.execute("CREATE INDEX IF NOT EXISTS idx_panel_item ON master_panel(item_name);")
        cat_conn.execute("CREATE INDEX IF NOT EXISTS idx_panel_year ON master_panel(year);")
        cat_conn.execute("CREATE INDEX IF NOT EXISTS idx_panel_metric ON master_panel(metric_name);")

        # Create convenience view
        cat_conn.execute("""
            CREATE VIEW IF NOT EXISTS v_panel AS
            SELECT table_id, table_title, item_name, metric_name, year, value, unit, edition_year
            FROM master_panel;
        """)
        cat_conn.commit()

    cat_conn.close()

    # Save category catalog.json
    cat_catalog_path = os.path.join(cat_out_dir, 'catalog.json')
    with open(cat_catalog_path, 'w', encoding='utf-8') as jf:
        json.dump(harmonized_tables_catalog, jf, indent=2, ensure_ascii=False)

    # Generate category README.md
    years_in_panel = sorted(master_panel_df['year'].unique()) if not master_panel_df.empty else []
    year_range_str = f"{min(years_in_panel)} – {max(years_in_panel)}" if years_in_panel else "N/A"

    readme_lines = [
        f"# {cat_name} — Master Multi-Year Dataset",
        '',
        f"This directory houses the consolidated multi-year datasets for **{cat_name}**, harmonizing data across all official Maldives Statistical Yearbook editions published between **2008 and 2026** by the National Bureau of Statistics (NBS).",
        '',
        '## Available Formats',
        f"- **Consolidated Panel Dataset ([`master_panel.csv`](master_panel.csv))**: Long-format tabular dataset ({len(master_panel_df):,} rows) with schema: `[category, table_id, table_title, item_name, metric_name, year, value, unit, edition_year]`.",
        f"- **Category SQLite Database ([`{cat_slug}.db`]({cat_slug}.db))**: Fully indexed local database containing `master_panel` plus dedicated SQL tables for every individual harmonized table.",
        f"- **Harmonized Wide CSVs ([`tables/`](tables/))**: {len(harmonized_tables_catalog)} individual multi-year CSV tables with continuous year columns.",
        '',
        '## Category Summary',
        f"- **Time Horizon Covered**: **{year_range_str}**",
        f"- **Total Harmonized Tables**: {len(harmonized_tables_catalog)}",
        f"- **Total Time-Series Observations**: {len(master_panel_df):,}",
        f"- **SQLite Database**: [`{cat_slug}.db`]({cat_slug}.db)",
        '',
        '## Harmonized Tables Catalog',
        '',
        '| Table ID | Title | Time Span | Rows | Cols | Wide CSV | Metadata |',
        '| :---: | :--- | :---: | :---: | :---: | :---: | :---: |'
    ]

    for item in harmonized_tables_catalog:
        title_disp = item['title_en'].replace('|', '/')
        tid = item['table_id']
        readme_lines.append(
            f"| **{tid}** | {title_disp} | {item['time_span']} | {item['row_count']} | {item['column_count']} | [`{tid}.csv`]({item['csv_file']}) | [`{tid}.json`](tables/{tid}.json) |"
        )

    readme_lines.extend([
        '',
        '## Example SQLite Usage (Python)',
        '```python',
        'import sqlite3',
        'import pandas as pd',
        '',
        f"conn = sqlite3.connect('{cat_slug}.db')",
        '',
        '# Query any metric across all years in milliseconds:',
        "df = pd.read_sql('''",
        '    SELECT item_name, year, value, unit',
        '    FROM master_panel',
        "    WHERE table_id = '10.1' AND year >= 2010",
        '    ORDER BY item_name, year',
        "''', conn)",
        'print(df.head())',
        '```'
    ])

    cat_readme_path = os.path.join(cat_out_dir, 'README.md')
    with open(cat_readme_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(readme_lines) + '\n')

    print(f"  [OK] Completed {cat_name}: {len(harmonized_tables_catalog)} tables, {len(master_panel_df):,} panel rows.")
    return {
        'category': cat_name,
        'slug': cat_slug,
        'tables_count': len(harmonized_tables_catalog),
        'panel_rows': len(master_panel_df),
        'time_span': year_range_str,
        'db_path': f"{cat_name}/{cat_slug}.db",
        'panel_csv': f"{cat_name}/master_panel.csv"
    }

def build_master_central_database(category_summaries, out_base='data/master_categories'):
    print(f"\n========================================================")
    print("CREATING MASTER CENTRAL SQLITE DATABASE & ARCHIVE OVERVIEW")
    print(f"========================================================")

    master_db_path = os.path.join(out_base, 'maldives_statistics_master.db')
    if os.path.exists(master_db_path):
        os.remove(master_db_path)

    master_conn = sqlite3.connect(master_db_path)

    total_panel_rows = 0

    # Combine all category master panels into master SQLite DB
    for summ in category_summaries:
        if not summ: continue
        cat_name = summ['category']
        panel_path = os.path.join(out_base, summ['panel_csv'])
        if os.path.exists(panel_path):
            try:
                cat_panel_df = pd.read_csv(panel_path, low_memory=False)
                cat_panel_df.to_sql('all_stats_panel', master_conn, if_exists='append', index=False)
                total_panel_rows += len(cat_panel_df)

                # Also attach the category db tables or copy key tables
                cat_db_file = os.path.join(out_base, summ['db_path'])
                if os.path.exists(cat_db_file):
                    src_conn = sqlite3.connect(cat_db_file)
                    cursor = src_conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 't_%';")
                    tables = cursor.fetchall()
                    for (tname,) in tables:
                        tbl_df = pd.read_sql(f"SELECT * FROM {tname}", src_conn)
                        master_tname = f"{summ['slug']}_{tname}"
                        tbl_df.to_sql(master_tname, master_conn, if_exists='replace', index=False)
                    src_conn.close()
            except Exception as e:
                print(f"  [Warn] Failed adding {cat_name} to master DB: {e}")

    # Build master indexes
    master_conn.execute("CREATE INDEX IF NOT EXISTS idx_master_cat ON all_stats_panel(category);")
    master_conn.execute("CREATE INDEX IF NOT EXISTS idx_master_table ON all_stats_panel(table_id);")
    master_conn.execute("CREATE INDEX IF NOT EXISTS idx_master_item ON all_stats_panel(item_name);")
    master_conn.execute("CREATE INDEX IF NOT EXISTS idx_master_year ON all_stats_panel(year);")
    master_conn.execute("CREATE INDEX IF NOT EXISTS idx_master_metric ON all_stats_panel(metric_name);")
    master_conn.commit()
    master_conn.close()

    # Generate Master Categories README.md
    readme_lines = [
        '# Maldives Statistical Yearbooks — Master Multi-Year Category Archive',
        '',
        'This archive provides **consolidated, harmonized longitudinal datasets** for every statistical category across all published editions of the **Statistical Yearbook of Maldives (2008 – 2026)** by the **National Bureau of Statistics (NBS)**.',
        '',
        '## Key Capabilities & Structure',
        f'- **Total Categories**: {len(category_summaries)}',
        f'- **Total Time-Series Observations**: {total_panel_rows:,}',
        '- **Master SQLite Database ([`maldives_statistics_master.db`](maldives_statistics_master.db))**: A unified, high-performance database containing all tables, indexes, and the complete `all_stats_panel` repository across all 19 editions.',
        '- **Category Tidy Panel CSVs (`master_panel.csv`)**: Long-format master files for each category containing all variables and all years.',
        '- **Harmonized Wide CSVs (`tables/<table_id>.csv`)**: Multi-year tables with continuous chronological year columns, merging historical overlap with latest official revisions taking precedence.',
        '- **Per-Category SQLite Databases (`<category>.db`)**: Standalone self-contained database for each specific domain.',
        '',
        '## Category Breakdown & Quick Links',
        '',
        '| Category | Time Span | Harmonized Tables | Panel Observations | SQLite Database | Category Directory |',
        '| :--- | :---: | :---: | :---: | :--- | :--- |'
    ]

    for item in category_summaries:
        if not item: continue
        readme_lines.append(
            f"| **{item['category']}** | {item['time_span']} | {item['tables_count']} | {item['panel_rows']:,} | [`{item['slug']}.db`]({item['db_path']}) | [`{item['category']}/`]({item['category']}/) |"
        )

    readme_lines.extend([
        '',
        '## How to Query the Master SQLite Database',
        '',
        '### 1. From Python (Pandas)',
        '```python',
        'import sqlite3',
        'import pandas as pd',
        '',
        "conn = sqlite3.connect('data/master_categories/maldives_statistics_master.db')",
        '',
        '# Query any metric across categories and years in milliseconds:',
        "df = pd.read_sql('''",
        '    SELECT category, table_id, item_name, metric_name, year, value, unit',
        '    FROM all_stats_panel',
        "    WHERE category = '10.0 Tourism' AND item_name = 'Germany' AND year >= 2010",
        '    ORDER BY year ASC',
        "''', conn)",
        'print(df)',
        '```',
        '',
        '### 2. From Command Line',
        '```bash',
        'sqlite3 data/master_categories/maldives_statistics_master.db "SELECT year, value FROM all_stats_panel WHERE metric_name LIKE \'%Tourist%\' AND item_name = \'Total\' ORDER BY year ASC;"',
        '```'
    ])

    master_readme_file = os.path.join(out_base, 'README.md')
    with open(master_readme_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(readme_lines) + '\n')

    master_cat_meta_file = os.path.join(out_base, 'catalog.json')
    with open(master_cat_meta_file, 'w', encoding='utf-8') as f:
        json.dump(category_summaries, f, indent=2, ensure_ascii=False)

    print(f"\nMaster database created: {master_db_path} ({total_panel_rows:,} total panel rows)")

def main():
    proc_dir = 'data/processed'
    out_base = 'data/master_categories'
    os.makedirs(out_base, exist_ok=True)

    # Discover all unique categories across all years
    years = sorted([y for y in os.listdir(proc_dir) if y.isdigit()], key=int)
    cat_names = set()
    for y in years:
        yp = os.path.join(proc_dir, y)
        for d in os.listdir(yp):
            if os.path.isdir(os.path.join(yp, d)):
                cat_names.add(normalize_category_name(d))

    sorted_categories = sorted(cat_names)
    print(f"Starting master category dataset generation for {len(sorted_categories)} categories...")

    total_start = time.time()
    summaries = []

    for cat in sorted_categories:
        summ = build_category_master(cat, proc_dir, out_base)
        if summ:
            summaries.append(summ)

    build_master_central_database(summaries, out_base)

    total_time = time.time() - total_start
    print(f"\nALL MASTER CATEGORIES COMPLETED IN {total_time:.1f} SECONDS!")

if __name__ == '__main__':
    main()
