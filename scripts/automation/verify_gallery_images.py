#!/usr/bin/env python3
import sys
import re
from pathlib import Path
import subprocess

gallery_md = Path('docs/travelogue/index.md')
missing = []
not_tracked = []

# Regex to find image src and data-full-image attributes
img_pattern = re.compile(r'(src|data-full-image)="([^"]+)"')

if not gallery_md.exists():
    print(f"ERROR: {gallery_md} not found.")
    sys.exit(1)

with gallery_md.open() as f:
    content = f.read()
    for match in img_pattern.finditer(content):
        rel_path = match.group(2).replace('..', 'docs')
        img_path = Path(rel_path)
        if not img_path.exists():
            missing.append(rel_path)
        else:
            # Check if file is tracked by git
            result = subprocess.run(['git', 'ls-files', '--error-unmatch', str(img_path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                not_tracked.append(rel_path)

if missing:
    print("ERROR: Missing images referenced in gallery:")
    for m in missing:
        print(f"  {m}")
    sys.exit(2)
if not_tracked:
    print("ERROR: Untracked images referenced in gallery:")
    for n in not_tracked:
        print(f"  {n}")
    sys.exit(3)

print("All gallery images are present and tracked.")
sys.exit(0)
