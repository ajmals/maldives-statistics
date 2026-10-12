#!/usr/bin/env python3
"""
Multi-Year Maldives Statistical Yearbook Raw Data Processor
Extracts, cleans, and standardizes yearbook tables across all years (2008 - 2026).
Supports .xlsx, .xls, and .htm/.html formats.
Outputs clean CSV tables, JSON metadata, per-year catalogs, and master multi-year catalog.
"""

import os
import re
import json
import csv
import glob
import time
from bs4 import BeautifulSoup
import openpyxl
import xlrd

THAANA_REGEX = re.compile(r'[\u0780-\u07BF]')

LEGACY_FONTS = {
    'faseyha', 'faruma', 'randhoo', 'kuredhi', 'waheed', 'voguepsmt',
    'a_faseyha', 'a_faruma', 'a_randhoo', 'mv_faseyha', 'mv_faruma',
    'mv_waheed', 'mv_kuredhi'
}

LEGACY_WORDS = {
    'clwvwt', 'ulwvwt', 'cnunemihob', 'cscnijed', 'cnehirif', 'cnehcnwa', 
    'wlcmuj', 'cnwt', 'elwm', 'cnwg', 'udwminwh', 'udcawk', 'udcaedwk',
    'idwbwa', 'cswdcnurwhwa', 'wrufurumua', 'cswkwhwvudurwhwa', 'urwvcnim',
    'ctcneswp', 'ckirwt', 'urwhwa'
}

def is_dhivehi_font(font_name):
    if not font_name:
        return False
    fn = font_name.lower()
    return any(lf in fn for lf in LEGACY_FONTS)

def is_pure_dhivehi_cell(val, font_name=''):
    if val is None:
        return False
    val_str = str(val).strip()
    if not val_str:
        return False
    if isinstance(val, (int, float)) or re.match(r'^-?[\d,.]+$', val_str):
        return False
    if THAANA_REGEX.search(val_str):
        if not re.search(r'[A-Za-z]{3,}', val_str):
            return True
    if is_dhivehi_font(font_name):
        return True
    words = re.findall(r'[a-zA-Z]+', val_str.lower())
    if words and all(w in LEGACY_WORDS for w in words):
        return True
    return False

def clean_val(val):
    if val is None:
        return ""
    if isinstance(val, float):
        if val.is_integer():
            return str(int(val))
        val_rounded = round(val, 8)
        val_str = f"{val_rounded:f}".rstrip('0').rstrip('.')
        return val_str
    if isinstance(val, int):
        return str(val)
    val_str = str(val).strip()
    val_str = re.sub(r'\s+', ' ', val_str)
    return val_str

def clean_english_cell_text(val):
    if not val:
        return ""
    val_str = clean_val(val)
    val_str = THAANA_REGEX.sub('', val_str).strip()
    pattern = r'\b(' + '|'.join(LEGACY_WORDS) + r')\b'
    val_str = re.sub(pattern, '', val_str, flags=re.IGNORECASE).strip()
    val_str = re.sub(r'\s+', ' ', val_str)
    return val_str

def is_multi_year_subtitle(txt):
    if not txt:
        return False
    return bool(re.search(r'\d{4}\s*,\s*\d{4}', txt) or re.search(r'\d{4}\s+AND\s+\d{4}', txt, re.IGNORECASE))

def load_grid_from_xlsx(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    base_name = os.path.splitext(os.path.basename(path))[0].strip()
    base_name_clean = base_name.replace(' ', '')

    target_sheet = None
    for name in wb.sheetnames:
        sheet = wb[name]
        if sheet.sheet_state != 'hidden' and name.strip().replace(' ', '') == base_name_clean:
            target_sheet = sheet
            break
    if not target_sheet:
        for name in wb.sheetnames:
            sheet = wb[name]
            if sheet.sheet_state != 'hidden':
                target_sheet = sheet
                break

    sheet = target_sheet
    min_col, min_row = 1, 1
    max_col, max_row = sheet.max_column, sheet.max_row

    if sheet.print_area:
        pa = sheet.print_area
        if isinstance(pa, list) and pa:
            pa = pa[0]
        m = re.search(r'\$?([A-Z]+)\$?(\d+):\$?([A-Z]+)\$?(\d+)', str(pa))
        if m:
            c1, r1, c2, r2 = m.groups()
            min_col = openpyxl.utils.column_index_from_string(c1)
            min_row = int(r1)
            max_col = openpyxl.utils.column_index_from_string(c2)
            max_row = int(r2)

    grid = [[None for _ in range(max_col - min_col + 1)] for _ in range(max_row - min_row + 1)]
    font_grid = [["" for _ in range(max_col - min_col + 1)] for _ in range(max_row - min_row + 1)]

    for r_idx, r in enumerate(range(min_row, max_row + 1)):
        for c_idx, c in enumerate(range(min_col, max_col + 1)):
            cell = sheet.cell(r, c)
            grid[r_idx][c_idx] = cell.value
            font_grid[r_idx][c_idx] = cell.font.name if cell.font and cell.font.name else ""

    for rng in sheet.merged_cells.ranges:
        r_start = max(min_row, rng.min_row) - min_row
        r_end = min(max_row, rng.max_row) - min_row
        c_start = max(min_col, rng.min_col) - min_col
        c_end = min(max_col, rng.max_col) - min_col

        top_val = sheet.cell(rng.min_row, rng.min_col).value
        top_font = sheet.cell(rng.min_row, rng.min_col).font
        fname = top_font.name if top_font and top_font.name else ""

        for r_i in range(r_start, r_end + 1):
            for c_i in range(c_start, c_end + 1):
                if 0 <= r_i < len(grid) and 0 <= c_i < len(grid[0]):
                    grid[r_i][c_i] = top_val
                    font_grid[r_i][c_i] = fname

    return grid, font_grid, base_name_clean

def load_grid_from_xls(path):
    wb = xlrd.open_workbook(path, formatting_info=True)
    base_name = os.path.splitext(os.path.basename(path))[0].strip()
    base_name_clean = base_name.replace(' ', '')

    target_sheet = None
    for name in wb.sheet_names():
        if name.strip().replace(' ', '') == base_name_clean:
            target_sheet = wb.sheet_by_name(name)
            break
    if not target_sheet:
        target_sheet = wb.sheet_by_index(0)

    sheet = target_sheet
    nrows, ncols = sheet.nrows, sheet.ncols
    grid = [[None for _ in range(ncols)] for _ in range(nrows)]
    font_grid = [["" for _ in range(ncols)] for _ in range(nrows)]

    for r in range(nrows):
        for c in range(ncols):
            cell = sheet.cell(r, c)
            val = cell.value
            if cell.ctype == xlrd.XL_CELL_NUMBER and isinstance(val, float) and val.is_integer():
                val = int(val)
            elif cell.ctype == xlrd.XL_CELL_EMPTY:
                val = None
            grid[r][c] = val

            try:
                xf_idx = sheet.cell_xf_index(r, c)
                font_idx = wb.xf_list[xf_idx].font_index
                font_grid[r][c] = wb.font_list[font_idx].name
            except Exception:
                font_grid[r][c] = ""

    for (rlo, rhi, clo, chi) in sheet.merged_cells:
        top_val = grid[rlo][clo]
        top_font = font_grid[rlo][clo]
        for r_i in range(rlo, rhi):
            for c_i in range(clo, chi):
                if r_i < len(grid) and c_i < len(grid[0]):
                    grid[r_i][c_i] = top_val
                    font_grid[r_i][c_i] = top_font

    return grid, font_grid, base_name_clean

def load_grid_from_htm(path):
    base_name = os.path.splitext(os.path.basename(path))[0].strip()
    base_name_clean = base_name.replace(' ', '')

    with open(path, 'r', encoding='latin-1', errors='ignore') as f:
        soup = BeautifulSoup(f.read(), 'lxml')

    table = soup.find('table')
    if not table:
        return [], [], base_name_clean

    rows = table.find_all('tr')
    grid = []
    font_grid = []

    for r_idx, tr in enumerate(rows):
        c_idx = 0
        if len(grid) <= r_idx:
            grid.append([])
            font_grid.append([])

        for td in tr.find_all(['td', 'th']):
            while c_idx < len(grid[r_idx]) and grid[r_idx][c_idx] is not None:
                c_idx += 1

            rowspan = int(td.get('rowspan', 1))
            colspan = int(td.get('colspan', 1))
            text = td.get_text(' ', strip=True)

            style = td.get('style', '')
            font_match = re.search(r'font-family:\s*([^;]+)', style, re.IGNORECASE)
            fname = font_match.group(1).strip() if font_match else ''

            for ro in range(rowspan):
                tr_idx = r_idx + ro
                while len(grid) <= tr_idx:
                    grid.append([])
                    font_grid.append([])
                for co in range(colspan):
                    tc_idx = c_idx + co
                    while len(grid[tr_idx]) <= tc_idx:
                        grid[tr_idx].append(None)
                        font_grid[tr_idx].append('')
                    grid[tr_idx][tc_idx] = text
                    font_grid[tr_idx][tc_idx] = fname

            c_idx += colspan

    max_c = max((len(r) for r in grid), default=0)
    for r in grid:
        while len(r) < max_c:
            r.append(None)
    for f in font_grid:
        while len(f) < max_c:
            f.append('')

    return grid, font_grid, base_name_clean

def process_table_grid(grid, font_grid, base_name_clean, output_dir):
    if not grid or not grid[0]:
        raise ValueError("Empty table grid")

    title_en = ""
    title_dv = ""
    unit_info = ""
    notes = []
    source = ""
    data_end_row = len(grid)

    for r_idx, row in enumerate(grid):
        non_empty = [(c, clean_val(v), font_grid[r_idx][c]) for c, v in enumerate(row) if v is not None and clean_val(v) != ""]
        if not non_empty:
            continue
        first_c, first_v, first_f = non_empty[0]

        if re.search(r'Table\s+\d+(\.\d+)?[a-z]?\s*:', first_v, re.IGNORECASE):
            title_en = first_v
            continue
        if re.search(r'ތާވަލ[ުް]?\s+\d+(\.\d+)?[a-z]?\s*:', first_v) or first_v.endswith('clwvWt') or 'clwvWt :' in first_v or 'ulwvWt :' in first_v:
            title_dv = first_v
            continue
        if re.match(r'^\([A-Za-z0-9\s,%_/\-]+\)$', first_v) and not title_en:
            unit_info = first_v
            continue

        lower_v = first_v.lower()
        if any(kw in lower_v for kw in ['source:', 'source :', 'source ;', 'ﻤﻌﻠﻮﻣﺎﺕ', 'މައުލޫމާތު']):
            source = first_v
            if data_end_row == len(grid):
                data_end_row = r_idx
            continue
        if any(lower_v.startswith(kw) for kw in ['note:', 'note :', '* note', '1_/', '2_/', '3_/', '4_/', '5_/']):
            notes.append(first_v)
            if data_end_row == len(grid):
                data_end_row = r_idx
            continue
        if data_end_row < len(grid):
            notes.append(first_v)

    if not title_en:
        for r_idx in range(min(5, len(grid))):
            for c_idx, v in enumerate(grid[r_idx]):
                if v and isinstance(v, str) and 'Table' in v:
                    title_en = clean_val(v)
                    break
            if title_en:
                break

    header_start_row = -1
    data_start_row = -1

    for r_idx in range(min(15, data_end_row)):
        row = grid[r_idx]
        cells = [clean_val(v) for v in row if v is not None and clean_val(v) != ""]
        if not cells:
            continue
        line_str = " ".join(cells)
        if title_en and title_en in line_str:
            continue
        if title_dv and title_dv in line_str:
            continue
        if len(cells) == 1 and line_str.startswith('(') and line_str.endswith(')'):
            continue
        if is_multi_year_subtitle(line_str) and len(cells) == 1:
            continue

        nums = [v for v in row if v is not None and (isinstance(v, (int, float)) or re.match(r'^-?[\d,.]+$', clean_val(v)))]
        all_years = False
        if nums:
            all_years = all((isinstance(v, int) and 1900 <= v <= 2050) or (isinstance(v, str) and re.match(r'^(19|20)\d\d$', v.strip())) for v in nums)

        if nums and not all_years:
            data_start_row = r_idx
            break
        else:
            if header_start_row == -1 and len(cells) >= 1:
                header_start_row = r_idx

    if data_start_row == -1:
        data_start_row = min(header_start_row + 1, data_end_row)
    if header_start_row == -1:
        header_start_row = 0

    header_rows = grid[header_start_row:data_start_row]
    header_fonts = font_grid[header_start_row:data_start_row]
    raw_data_rows = grid[data_start_row:data_end_row]
    raw_data_fonts = font_grid[data_start_row:data_end_row]

    data_rows = []
    data_font_rows = []
    for r_idx, r in enumerate(raw_data_rows):
        has_num = any(isinstance(v, (int, float)) or (isinstance(v, str) and re.match(r'^-?[\d,.]+$', v.strip())) for v in r if v is not None)
        non_empty = [v for v in r if v is not None and clean_val(v) != ""]
        if not non_empty:
            continue
        if not has_num:
            all_dv = all(is_pure_dhivehi_cell(v, raw_data_fonts[r_idx][c]) for c, v in enumerate(r) if v is not None and clean_val(v) != "")
            if all_dv:
                continue
        data_rows.append(r)
        data_font_rows.append(raw_data_fonts[r_idx])

    num_cols = len(grid[0]) if grid else 0

    keep_cols = []
    for c in range(num_cols):
        col_data = [r[c] for r in data_rows if r[c] is not None and clean_val(r[c]) != ""]
        col_header = [clean_val(r[c]) for r in header_rows if r[c] is not None and clean_val(r[c]) != ""]
        if not col_data and not col_header:
            continue

        all_col_cells = [(r[c], data_font_rows[i][c]) for i, r in enumerate(data_rows) if r[c] is not None and clean_val(r[c]) != ""]
        all_col_cells += [(r[c], header_fonts[i][c]) for i, r in enumerate(header_rows) if r[c] is not None and clean_val(r[c]) != ""]

        is_col_dhivehi = True
        for val, fname in all_col_cells:
            v_str = clean_val(val)
            if isinstance(val, (int, float)) or re.match(r'^-?[\d,.]+$', v_str):
                is_col_dhivehi = False
                break
            if not is_pure_dhivehi_cell(val, fname):
                is_col_dhivehi = False
                break

        if not is_col_dhivehi:
            keep_cols.append(c)

    filtered_keep_cols = []
    for i, c in enumerate(keep_cols):
        if i > 0:
            prev_c = keep_cols[i - 1]
            prev_vals = [clean_val(r[prev_c]) for r in data_rows]
            curr_vals = [clean_val(r[c]) for r in data_rows]
            if prev_vals and curr_vals and prev_vals == curr_vals:
                continue
        filtered_keep_cols.append(c)
    keep_cols = filtered_keep_cols

    expanded_header_rows = []
    for h_idx, h_row in enumerate(header_rows):
        exp_row = [None] * num_cols
        last_val = None
        for c in range(num_cols):
            if c > 0 and (c - 1) not in keep_cols:
                last_val = None

            val = h_row[c]
            fname = header_fonts[h_idx][c]
            if val is not None and not is_pure_dhivehi_cell(val, fname):
                txt = clean_english_cell_text(val)
                if title_en and txt.lower() == title_en.lower():
                    txt = ""
                if is_multi_year_subtitle(txt):
                    txt = ""
                if txt:
                    exp_row[c] = txt
                    if c > 0:
                        last_val = txt
                else:
                    if last_val and c > 0 and c in keep_cols:
                        exp_row[c] = last_val
            else:
                if last_val and c > 0 and c in keep_cols:
                    exp_row[c] = last_val
        expanded_header_rows.append(exp_row)

    col_names = []
    for c in keep_cols:
        parts = []
        for r_idx in range(len(expanded_header_rows)):
            val = expanded_header_rows[r_idx][c]
            if val:
                txt = clean_english_cell_text(val)
                if txt and not txt.startswith("Table ") and txt not in parts:
                    parts.append(txt)
        col_header = " - ".join(parts).strip()
        if not col_header:
            col_header = f"Column_{c + 1}"
        col_names.append(col_header)

    seen = {}
    unique_col_names = []
    for name in col_names:
        if name in seen:
            seen[name] += 1
            unique_col_names.append(f"{name}_{seen[name]}")
        else:
            seen[name] = 1
            unique_col_names.append(name)

    output_rows = []
    for r_idx, r in enumerate(data_rows):
        row_cells = []
        is_empty = True
        non_empty_cells = [(c, clean_val(r[c])) for c in keep_cols if r[c] is not None and clean_val(r[c]) != ""]
        if len(non_empty_cells) == 1 and not isinstance(r[non_empty_cells[0][0]], (int, float)):
            txt = clean_english_cell_text(non_empty_cells[0][1])
            if txt and not re.match(r'^-?[\d,.]+$', txt):
                row_cells = [txt if i == 0 else "" for i in range(len(keep_cols))]
                output_rows.append(row_cells)
                continue

        for c in keep_cols:
            val = r[c]
            fname = data_font_rows[r_idx][c]
            if val is not None and not is_pure_dhivehi_cell(val, fname):
                v_clean = clean_english_cell_text(val)
                row_cells.append(v_clean)
                if v_clean:
                    is_empty = False
            else:
                row_cells.append("")

        if not is_empty:
            output_rows.append(row_cells)

    final_cols_idx = []
    for col_i in range(len(unique_col_names)):
        has_any_data = any(row[col_i] != "" for row in output_rows)
        if has_any_data:
            final_cols_idx.append(col_i)

    final_col_names = [unique_col_names[i] for i in final_cols_idx]
    final_output_rows = [[row[i] for i in final_cols_idx] for row in output_rows]

    meta = {
        "table_id": base_name_clean,
        "title_en": title_en,
        "title_dv": title_dv,
        "unit": unit_info,
        "source": source,
        "notes": notes,
        "columns": final_col_names,
        "row_count": len(final_output_rows)
    }

    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, f"{base_name_clean}.csv")
    json_path = os.path.join(output_dir, f"{base_name_clean}.json")

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(final_col_names)
        writer.writerows(final_output_rows)

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    return meta, csv_path, json_path

def process_file(file_path, output_dir):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.xlsx':
        grid, font_grid, base_name = load_grid_from_xlsx(file_path)
    elif ext == '.xls':
        grid, font_grid, base_name = load_grid_from_xls(file_path)
    elif ext in ('.htm', '.html'):
        grid, font_grid, base_name = load_grid_from_htm(file_path)
    else:
        raise ValueError(f"Unsupported format: {ext}")

    return process_table_grid(grid, font_grid, base_name, output_dir)

def generate_year_catalog(year, processed_year_dir):
    catalog = []
    for ch in sorted(os.listdir(processed_year_dir)):
        ch_dir = os.path.join(processed_year_dir, ch)
        if not os.path.isdir(ch_dir):
            continue
        jsons = sorted(glob.glob(os.path.join(ch_dir, '*.json')))
        for j_path in jsons:
            with open(j_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)
                rel_csv = os.path.relpath(j_path.replace('.json', '.csv'), processed_year_dir)
                meta['chapter'] = ch
                meta['csv_file'] = rel_csv
                catalog.append(meta)

    catalog_path = os.path.join(processed_year_dir, 'catalog.json')
    with open(catalog_path, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    chapters_count = len(set(item['chapter'] for item in catalog))
    readme_lines = [
        f'# Statistical Year Book of Maldives {year} — Clean Datasets',
        '',
        f'This directory contains clean, machine-readable CSV datasets and structured JSON metadata converted from the official Statistical Yearbook of Maldives {year} published by the National Bureau of Statistics (NBS).',
        '',
        '## Dataset Overview',
        f'- **Total Chapters**: {chapters_count}',
        f'- **Total Tables / CSV Files**: {len(catalog)}',
        '- **Encoding**: UTF-8',
        '- **Format**: Clean Tabular Matrix (English headers, pure numeric/category data rows, chart clutter and empty spacer columns stripped)',
        '- **Metadata**: Companion `.json` for each table capturing Table ID, English Title, Dhivehi Title, Units, Source citations, and Footnotes.',
        '',
        '## Table of Contents',
        '',
        '| Chapter | Table ID | Table Title | Rows | Cols | CSV File |',
        '| :--- | :--- | :--- | :--- | :--- | :--- |'
    ]

    for item in catalog:
        title = item['title_en'] if item['title_en'] else f"Table {item['table_id']}"
        title_display = title.replace('|', '/')
        fname = os.path.basename(item['csv_file'])
        readme_lines.append(f"| {item['chapter']} | {item['table_id']} | {title_display} | {item['row_count']} | {len(item['columns'])} | [`{fname}`]({item['csv_file']}) |")

    readme_path = os.path.join(processed_year_dir, 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(readme_lines) + '\n')

    return catalog

def process_year(year, raw_base_dir='data/raw', processed_base_dir='data/processed'):
    raw_year_dir = os.path.join(raw_base_dir, year)
    processed_year_dir = os.path.join(processed_base_dir, year)
    os.makedirs(processed_year_dir, exist_ok=True)

    print(f"\n========================================================")
    print(f"PROCESSING YEAR: {year}")
    print(f"========================================================")

    # Discover chapters / subdirectories
    subdirs = sorted([d for d in os.listdir(raw_year_dir) if os.path.isdir(os.path.join(raw_year_dir, d))])
    
    year_stats = {
        'year': year,
        'total_files': 0,
        'success': 0,
        'failed': 0,
        'chapters': {}
    }

    start_year_time = time.time()

    for ch in subdirs:
        # Ignore non-data internal folders
        if ch.startswith('yearbook') and ch != 'yearbook2008' and not any(os.path.splitext(f)[1].lower() in ('.xlsx', '.xls', '.htm', '.html') for f in os.listdir(os.path.join(raw_year_dir, ch))):
            continue

        ch_raw_dir = os.path.join(raw_year_dir, ch)
        ch_out_dir = os.path.join(processed_year_dir, ch)

        # Collect data files
        valid_exts = {'.xlsx', '.xls', '.htm', '.html'}
        data_files = sorted([
            os.path.join(ch_raw_dir, f) for f in os.listdir(ch_raw_dir)
            if os.path.splitext(f)[1].lower() in valid_exts and not f.startswith('~$')
        ])

        if not data_files:
            continue

        ch_success = 0
        ch_failed = 0

        for fpath in data_files:
            fname = os.path.basename(fpath)
            year_stats['total_files'] += 1
            try:
                meta, cp, jp = process_file(fpath, ch_out_dir)
                ch_success += 1
                year_stats['success'] += 1
                print(f"  [{year} | {ch[:20]}] OK: {fname:<20} -> {meta['row_count']:>3} rows, {len(meta['columns']):>2} cols")
            except Exception as e:
                ch_failed += 1
                year_stats['failed'] += 1
                print(f"  [{year} | {ch[:20]}] FAIL: {fname}: {e}")

        year_stats['chapters'][ch] = {
            'total': len(data_files),
            'success': ch_success,
            'failed': ch_failed
        }

    catalog = generate_year_catalog(year, processed_year_dir)
    elapsed = time.time() - start_year_time
    print(f"\n[SUMMARY {year}] Processed: {year_stats['total_files']} | OK: {year_stats['success']} | Fail: {year_stats['failed']} | Catalog entries: {len(catalog)} | Time: {elapsed:.1f}s")
    return year_stats, catalog

def build_master_multi_year_catalog(processed_base_dir='data/processed'):
    years = sorted([y for y in os.listdir(processed_base_dir) if os.path.isdir(os.path.join(processed_base_dir, y)) and re.match(r'^\d{4}$', y)])
    
    master_catalog = {}
    master_summary = []
    
    total_tables_all_years = 0
    total_chapters_all_years = 0

    for y in years:
        cat_file = os.path.join(processed_base_dir, y, 'catalog.json')
        if os.path.exists(cat_file):
            with open(cat_file, 'r', encoding='utf-8') as f:
                cat = json.load(f)
                master_catalog[y] = cat
                ch_set = set(item['chapter'] for item in cat)
                total_tables_all_years += len(cat)
                total_chapters_all_years += len(ch_set)
                master_summary.append({
                    'year': y,
                    'chapters': len(ch_set),
                    'tables': len(cat),
                    'catalog_path': f"{y}/catalog.json",
                    'readme_path': f"{y}/README.md"
                })

    master_cat_path = os.path.join(processed_base_dir, 'multi_year_catalog.json')
    with open(master_cat_path, 'w', encoding='utf-8') as f:
        json.dump(master_catalog, f, indent=2, ensure_ascii=False)

    # Master README
    readme_lines = [
        '# Maldives Statistical Yearbooks (Multi-Year Archive: 2008 – 2026)',
        '',
        'This directory hosts clean, standardized, machine-readable datasets extracted from official Statistical Yearbooks of Maldives published by the **National Bureau of Statistics (NBS)**.',
        '',
        '## Repository Summary',
        f'- **Total Years Covered**: {len(master_summary)} (2008 – 2026)',
        f'- **Total Clean Tables Converted**: {total_tables_all_years:,}',
        '- **Formats Provided**: Clean Tabular UTF-8 CSVs + Structured Companion JSON Metadata',
        '- **Standardization**: Stripped pure Dhivehi & Thaana script columns/rows, unified English column headers, resolved merged header hierarchies, removed chart/graphic artifacts, preserved full numerical precision.',
        '',
        '## Year-by-Year Catalog Breakdown',
        '',
        '| Year | Chapters | Converted Tables | Catalog JSON | Year Documentation |',
        '| :---: | :---: | :---: | :--- | :--- |'
    ]

    for item in master_summary:
        readme_lines.append(
            f"| **{item['year']}** | {item['chapters']} | {item['tables']} | [`catalog.json`]({item['catalog_path']}) | [`README.md`]({item['readme_path']}) |"
        )

    master_readme_path = os.path.join(processed_base_dir, 'README.md')
    with open(master_readme_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(readme_lines) + '\n')

    print(f"\n========================================================")
    print(f"MASTER CATALOG BUILT ACROSS {len(master_summary)} YEARS: {total_tables_all_years} TOTAL TABLES")
    print(f"========================================================")

def main():
    raw_base = 'data/raw'
    proc_base = 'data/processed'

    all_raw_years = sorted([
        d for d in os.listdir(raw_base)
        if os.path.isdir(os.path.join(raw_base, d)) and re.match(r'^\d{4}$', d)
    ])

    print(f"Found {len(all_raw_years)} raw year directories: {all_raw_years}")

    # Note: 2021 is already in data/processed/2021. If catalog.json exists, we preserve it or we can process others.
    # The new raw data are all the other years:
    new_years = [y for y in all_raw_years if y != '2021']

    total_start = time.time()
    results = []

    for y in new_years:
        stats, cat = process_year(y, raw_base, proc_base)
        results.append(stats)

    # Re-generate/ensure 2021 catalog is up to date if needed
    if os.path.exists(os.path.join(proc_base, '2021')):
        generate_year_catalog('2021', os.path.join(proc_base, '2021'))

    build_master_multi_year_catalog(proc_base)

    total_time = time.time() - total_start
    print(f"\nALL YEARS COMPLETED in {total_time:.1f} seconds!")

if __name__ == '__main__':
    main()
