import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

BLOGS_DIR = Path('docs/blogs')
SCRIPT_PATH = Path('scripts/publish_entry.py')

class BlogHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.md'):
            print(f"New blog file detected: {event.src_path}")
            subprocess.run(['python', str(SCRIPT_PATH)])
            print("Blog index updated.")

def main():
    observer = Observer()
    event_handler = BlogHandler()
    observer.schedule(event_handler, str(BLOGS_DIR), recursive=False)
    observer.start()
    print(f"Watching {BLOGS_DIR} for new blog files...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    main()
