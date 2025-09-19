#!/usr/bin/env python3
import time
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DOCS_DIR = Path(__file__).parent.parent.parent / "docs"
MKDOCS_BIN = Path(__file__).parent.parent.parent / ".venv-mkdocs/bin/mkdocs"

import threading
import time

class DocsChangeHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.cooldown_until = 0

    def on_modified(self, event):
        if event.is_directory:
            return
        relevant_exts = ('.md', '.markdown', '.yml', '.yaml', '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg')
        is_relevant = event.src_path.endswith(relevant_exts)
        if is_relevant:
            rel_path = Path(event.src_path).relative_to(str(DOCS_DIR))
            parts = rel_path.parts
            if any(part.startswith('_') for part in parts):
                return
            if parts and parts[0] == "site":
                return
            now = time.time()
            if now < self.cooldown_until:
                return
            print(f"Change detected: {event.src_path}. Rebuilding MkDocs...")
            subprocess.run([str(MKDOCS_BIN), "build"], cwd=str(DOCS_DIR.parent))
            self.cooldown_until = now + 3  # 3 second cooldown after rebuild

    # Ignore all other events
    def on_created(self, event):
        pass
    def on_deleted(self, event):
        pass
    def on_moved(self, event):
        pass

if __name__ == "__main__":
    event_handler = DocsChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, str(DOCS_DIR), recursive=True)
    observer.start()
    print(f"Watching {DOCS_DIR} for changes. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
