import os
import re
import yaml
from pathlib import Path

ENTRIES_DIR = Path('docs/blogs')
INDEX_MD = ENTRIES_DIR / 'index.md'

ENTRY_PATTERN = re.compile(r'^(\d{4}-\d{2}-\d{2})_(.+)_v(\d+).md$')

def parse_yaml_header(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if lines[0].strip() != '---':
        return None
    header_lines = []
    for line in lines[1:]:
        if line.strip() == '---':
            break
        header_lines.append(line)
    header = yaml.safe_load(''.join(header_lines))
    return header

def get_title(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('# '):
                return line[2:].strip()
    return None

def format_index_entry(title, filename, date):
    from datetime import datetime, date as dt_date
    if isinstance(date, dt_date):
        month_str = date.strftime('%B')
        year_str = date.strftime('%Y')
    else:
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            month_str = date_obj.strftime('%B')
            year_str = date_obj.strftime('%Y')
        except Exception:
            month = Path(filename).stem[:7]
            month_str = month
            year_str = str(date)[:4]
    return f'- [{title}]({filename}) ({month_str} {year_str})\n'

def update_index():
    entries = []
    for md_file in ENTRIES_DIR.glob('*.md'):
        if md_file.name == 'index.md':
            continue
        match = ENTRY_PATTERN.match(md_file.name)
        if not match:
            continue
        date, stub, version = match.groups()
        header = parse_yaml_header(md_file)
        title = get_title(md_file)
        if not title:
            title = stub.replace('-', ' ').title()
        entry = format_index_entry(title, md_file.name, header.get('date', date) if header else date)
        entries.append((date, entry))
    # Sort by date descending
    entries.sort(reverse=True)
    with open(INDEX_MD, 'w', encoding='utf-8') as f:
        f.write('# Research Blog\n\nBelow is a chronological list of research notes, observations, and findings:\n\n')
        for _, entry in entries:
            f.write(entry)

if __name__ == '__main__':
    update_index()
    print('Research Blog index updated.')
