# Blog Automation Watcher

This script (`blogs_watch.py`) monitors the `/docs/blogs/` directory for new markdown files. When a new blog post is added, it automatically runs the publishing script (`publish_entry.py`) to update the blog index.

## Usage

1. Activate your Python environment:
   ```bash
   source .venv/bin/activate
   ```
2. Run the watcher script:
   ```bash
   python scripts/blogs_watch.py
   ```
3. Add or move new blog markdown files to `/docs/blogs/`.
4. The index will be updated automatically.

## Dependencies
- Python 3
- watchdog (`pip install watchdog`)

## Notes
- Stop the watcher with `Ctrl+C` when done.
- Commit changes to GitHub to publish live.
