import os
import json
import glob

root_datasets = 'datasets'
catalog = []

for ch in sorted(os.listdir(root_datasets)):
    ch_dir = os.path.join(root_datasets, ch)
    if not os.path.isdir(ch_dir):
        continue
    jsons = sorted(glob.glob(os.path.join(ch_dir, '*.json')))
    for j_path in jsons:
        with open(j_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
            rel_csv = os.path.relpath(j_path.replace('.json', '.csv'), root_datasets)
            meta['chapter'] = ch
            meta['csv_file'] = rel_csv
            catalog.append(meta)

with open('datasets/catalog.json', 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=2, ensure_ascii=False)

readme_lines = [
    '# Statistical Year Book of Maldives 2021 — Clean Datasets',
    '',
    'This directory contains clean, machine-readable CSV datasets and structured JSON metadata converted from the official Statistical Yearbook of Maldives 2021 published by the National Bureau of Statistics (NBS).',
    '',
    '## Dataset Overview',
    f'- **Total Chapters**: 20',
    f'- **Total Tables / CSV Files**: {len(catalog)}',
    f'- **Encoding**: UTF-8',
    f'- **Format**: Clean Tabular Matrix (English headers, pure numeric/category data rows, chart clutter and empty spacer columns stripped)',
    f'- **Metadata**: Companion `.json` for each table capturing Table ID, English Title, Dhivehi Title, Units, Source citations, and Footnotes.',
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

with open('datasets/README.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(readme_lines) + '\n')

print(f"Catalog and README generated with {len(catalog)} entries.")
