import os
import re
import json
import csv
import openpyxl
from openpyxl.utils import get_column_letter

THAANA_REGEX = re.compile(r'[\u0780-\u07BF]')

def is_thaana_or_legacy(val, font_name=''):
    if not val:
        return False
    val_str = str(val).strip()
    if not val_str:
        return False
    # If contains unicode Thaana
    if THAANA_REGEX.search(val_str):
        return True
    # If font name indicates legacy Dhivehi font
    if font_name and any(f in font_name.lower() for f in ['faseyha', 'faruma', 'randhoo', 'kuredhi', 'waheed']):
        # If it doesn't look like a standard number or English word
        return True
    return False

def clean_cell_value(val):
    if val is None:
        return ""
    if isinstance(val, float):
        # Format clean float without unnecessary precision artifacts
        if val.is_integer():
            return str(int(val))
        # Round very small precision errors e.g. 2731.4999999999995 -> 2731.5
        val_rounded = round(val, 8)
        val_str = f"{val_rounded:f}".rstrip('0').rstrip('.')
        return val_str
    if isinstance(val, int):
        return str(val)
    val_str = str(val).strip()
    # Normalize internal newlines/spaces
    val_str = re.sub(r'\s+', ' ', val_str)
    return val_str

def parse_excel_table(xlsx_path):
    wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    
    # Choose visible sheet matching filename or active
    target_sheet = None
    base_name = os.path.splitext(os.path.basename(xlsx_path))[0].strip()
    
    for sheet_name in wb.sheetnames:
        sheet = wb[sheet_name]
        if sheet.sheet_state != 'hidden':
            if sheet_name.strip() == base_name:
                target_sheet = sheet
                break
    if not target_sheet:
        for sheet_name in wb.sheetnames:
            sheet = wb[sheet_name]
            if sheet.sheet_state != 'hidden':
                target_sheet = sheet
                break
                
    sheet = target_sheet
    
    # 1. Parse Print Area if available to bound columns and rows
    max_col = sheet.max_column
    max_row = sheet.max_row
    min_col = 1
    min_row = 1
    
    if sheet.print_area:
        pa = sheet.print_area
        if isinstance(pa, list) and pa:
            pa = pa[0]
        # parse e.g. '1.1'!$A$1:$AB$61 or $A$1:$K$289
        m = re.search(r'\$?([A-Z]+)\$?(\d+):\$?([A-Z]+)\$?(\d+)', str(pa))
        if m:
            c1, r1, c2, r2 = m.groups()
            min_col = openpyxl.utils.column_index_from_string(c1)
            min_row = int(r1)
            max_col = openpyxl.utils.column_index_from_string(c2)
            max_row = int(r2)

    # Read all cell values and font names within bounds
    grid = []
    font_grid = []
    for r in range(min_row, max_row + 1):
        row_vals = []
        row_fonts = []
        for c in range(min_col, max_col + 1):
            cell = sheet.cell(r, c)
            val = cell.value
            font_name = cell.font.name if cell.font and cell.font.name else ''
            row_vals.append(val)
            row_fonts.append(font_name)
        grid.append(row_vals)
        font_grid.append(row_fonts)

    # 2. Extract Title, Metadata, Source, Notes
    title_en = ""
    title_dv = ""
    unit_info = ""
    notes = []
    source = ""
    
    header_start_idx = -1
    data_end_idx = len(grid)
    
    for idx, row in enumerate(grid):
        non_empty = [(c, clean_cell_value(val)) for c, val in enumerate(row) if val is not None and clean_cell_value(val) != ""]
        if not non_empty:
            continue
        first_val = non_empty[0][1]
        
        # Check title patterns
        if re.search(r'Table\s+\d+(\.\d+)?[a-z]?\s*:', first_val, re.IGNORECASE):
            title_en = first_val
            continue
        elif re.search(r'ތާވަލ[ުް]?\s+\d+(\.\d+)?[a-z]?\s*:', first_val) or (first_val.endswith('clwvWt') or 'clwvWt :' in first_val or 'ulwvWt :' in first_val):
            title_dv = first_val
            continue
        elif re.match(r'^\([A-Za-z0-9\s,%_/\-]+\)$', first_val) and not title_en:
            unit_info = first_val
            continue
            
        # Check source and notes at bottom
        if any(kw in first_val.lower() for kw in ['source:', 'source :', 'ﻤﻌﻠﻮﻣﺎﺕ', 'މައުލޫމާތު']):
            source = first_val
            if data_end_idx == len(grid):
                data_end_idx = idx
            continue
        elif any(first_val.lower().startswith(kw) for kw in ['note:', 'note :', '* note', '1_/', '2_/', '3_/']):
            notes.append(first_val)
            if data_end_idx == len(grid):
                data_end_idx = idx
            continue
        elif data_end_idx < len(grid):
            # Already in notes section
            notes.append(first_val)

    # Find header start row: first row after title that has column descriptors
    for idx, row in enumerate(grid[:min(10, data_end_idx)]):
        non_empty = [clean_cell_value(val) for val in row if val is not None and clean_cell_value(val) != ""]
        if not non_empty:
            continue
        line_text = " ".join(non_empty)
        # Check if row is not title and has headers like Locality, Year, No., Age, Sex, etc.
        if (title_en and title_en in line_text) or (title_dv and title_dv in line_text):
            continue
        if len(non_empty) >= 1:
            header_start_idx = idx
            break
            
    return {
        "title_en": title_en,
        "title_dv": title_dv,
        "unit_info": unit_info,
        "source": source,
        "notes": notes,
        "header_start_idx": header_start_idx,
        "data_end_idx": data_end_idx,
        "grid_shape": (len(grid), len(grid[0]) if grid else 0)
    }

if __name__ == '__main__':
    for f in ['raw_stats_data/1.0 Geography /1.1.xlsx', 'raw_stats_data/1.0 Geography /1.5.xlsx', 'raw_stats_data/3.0 population /3.1.xlsx']:
        info = parse_excel_table(f)
        print(f, info)
