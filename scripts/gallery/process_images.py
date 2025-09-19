# Configuration for travelogue_ingest workflow
#!/usr/bin/env python3
import os
import sys
import time
import shutil
from pathlib import Path
import yaml
from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WORKSPACE_ROOT = Path(__file__).parent.parent.parent.resolve()
#!/usr/bin/env python3

import os
import sys
import time
import yaml
import shutil
from pathlib import Path
from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
def find_project_root(start_path):
    current = start_path.resolve()
    while current != current.parent:
        if (current / "mkdocs.yml").exists():
            return current
        current = current.parent
    return start_path.resolve()

WORKSPACE_ROOT = find_project_root(Path(__file__))
print(f"Workspace root: {WORKSPACE_ROOT}")
print(f"Workspace root: {WORKSPACE_ROOT}")
HOT_FOLDER = WORKSPACE_ROOT / "hot_folder"
TRAVELOGUE_INGEST = WORKSPACE_ROOT / "travelogue_ingest"
NEW_IMAGES = TRAVELOGUE_INGEST / "new_images"
PROCESSED_DIR = TRAVELOGUE_INGEST / "processed"
CAPTIONS_DIR = TRAVELOGUE_INGEST / "captions"
LOGS_DIR = TRAVELOGUE_INGEST / "logs"
THUMBNAILS_DIR = WORKSPACE_ROOT / "docs/assets/travelogue/thumbnails"
FULL_DIR = WORKSPACE_ROOT / "docs/assets/travelogue/full"
GALLERY_MD = WORKSPACE_ROOT / "docs/travelogue/index.md"
METADATA_FILE = CAPTIONS_DIR / "gallery_metadata.yml"
ERROR_LOG = LOGS_DIR / "errors.log"

# Image processing settings
THUMBNAIL_SIZE = (500, 500)
MAX_FULL_WIDTH = 2000

def create_thumbnail(image_path, output_path):
    """Create a square thumbnail of the image."""
    with Image.open(image_path) as img:
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Calculate dimensions for square crop
        width, height = img.size
        size = min(width, height)
        left = (width - size) // 2
        top = (height - size) // 2
        right = left + size
        bottom = top + size
        
        # Crop to square and resize
        img = img.crop((left, top, right, bottom))
        img.thumbnail(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
        img.save(output_path, "JPEG", quality=85, optimize=True)

def optimize_full_image(image_path, output_path):
    """Optimize the full-size image while maintaining quality."""
    with Image.open(image_path) as img:
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Calculate new size if width exceeds maximum
        width, height = img.size
        if width > MAX_FULL_WIDTH:
            ratio = MAX_FULL_WIDTH / width
            new_size = (MAX_FULL_WIDTH, int(height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Save with optimization
        img.save(output_path, "JPEG", quality=85, optimize=True)

def load_metadata():
    """Load existing metadata from YAML file."""
    if METADATA_FILE.exists():
        with open(METADATA_FILE, 'r') as f:
            return yaml.safe_load(f) or {}
    return {}

def save_metadata(metadata):
    """Save metadata to YAML file."""
    with open(METADATA_FILE, 'w') as f:
        yaml.dump(metadata, f, default_flow_style=False)

def update_gallery_markdown(metadata):
    """Update the gallery markdown file with all images."""
    # Overwrite the entire markdown file with header and single grid
    header_content = (
        "# Academic Travelogue\n\n"
        "A chronicle of academic journeys, conferences, research visits, and collaborative endeavors across the globe.\n"
    )
    gallery_items = []
    import time
    cache_bust = int(time.time())
    for image_name, data in sorted(metadata.items(), key=lambda x: x[1].get('date', ''), reverse=True):
        item = f'''<div class="gallery-item" 
     data-full-image="../assets/travelogue/full/{image_name}?v={cache_bust}"
     data-full-caption="{data.get('full_caption', '')}">
<img class="gallery-thumbnail" src="../assets/travelogue/thumbnails/{image_name}?v={cache_bust}" alt="{data.get('alt_text', '')}">
<div class="gallery-caption">{data.get('short_caption', '')}</div>
</div>'''
        gallery_items.append(item)
    with open(GALLERY_MD, 'w') as f:
        f.write(header_content)
        f.write('\n<div class="gallery-grid">\n')
        f.write('\n'.join(gallery_items))
        f.write('\n</div>\n')
    
class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        # Only process image files
        if not event.src_path.lower().endswith((".jpg", ".jpeg", ".png")):
            return
        image_path = Path(event.src_path)
        image_name = image_path.name
        print(f"Processing new image: {image_name}")
        try:
            THUMBNAILS_DIR.mkdir(parents=True, exist_ok=True)
            FULL_DIR.mkdir(parents=True, exist_ok=True)
            # Archive existing thumbnail
            archive_thumb_dir = THUMBNAILS_DIR / "archive"
            archive_thumb_dir.mkdir(parents=True, exist_ok=True)
            thumbnail_path = THUMBNAILS_DIR / image_name
            if thumbnail_path.exists():
                ts = time.strftime('%Y%m%d%H%M%S')
                archived_thumb = archive_thumb_dir / f"{image_path.stem}_{ts}.jpg"
                shutil.move(str(thumbnail_path), str(archived_thumb))
            # Archive existing full image
            archive_full_dir = FULL_DIR / "archive"
            archive_full_dir.mkdir(parents=True, exist_ok=True)
            full_path = FULL_DIR / image_name
            if full_path.exists():
                ts = time.strftime('%Y%m%d%H%M%S')
                archived_full = archive_full_dir / f"{image_path.stem}_{ts}.jpg"
                shutil.move(str(full_path), str(archived_full))
            create_thumbnail(image_path, thumbnail_path)
            optimize_full_image(image_path, full_path)
            metadata = load_metadata()
            if image_name in metadata:
                image_metadata = metadata[image_name]
            else:
                image_metadata = {
                    'short_caption': f'Photo: {image_path.stem}',
                    'full_caption': f'Detailed caption for {image_path.stem}',
                    'alt_text': image_path.stem,
                    'date': time.strftime('%Y-%m-%d')
                }
            metadata[image_name] = image_metadata
            save_metadata(metadata)
            update_gallery_markdown(metadata)
            PROCESSED_DIR.mkdir(exist_ok=True)
            shutil.move(str(image_path), str(PROCESSED_DIR / image_name))
            print(f"Successfully processed {image_name}")
            # Trigger MkDocs rebuild after processing
            mkdocs_venv = WORKSPACE_ROOT / ".venv-mkdocs" / "bin" / "mkdocs"
            if mkdocs_venv.exists():
                import subprocess
                try:
                    result = subprocess.run([str(mkdocs_venv), "build"], cwd=str(WORKSPACE_ROOT), capture_output=True, text=True)
                    print("MkDocs rebuild output:", result.stdout)
                    if result.returncode != 0:
                        print("MkDocs rebuild error:", result.stderr)
                except Exception as e:
                    print(f"Error triggering MkDocs rebuild: {e}")
            else:
                print("MkDocs executable not found in .venv-mkdocs/bin/")
        except Exception as e:
            print(f"Error processing {image_name}: {str(e)}")
            LOGS_DIR.mkdir(exist_ok=True)
            with open(ERROR_LOG, "a") as logf:
                logf.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} Error processing {image_name}: {str(e)}\n")

def main():
    # Create necessary directories
    NEW_IMAGES.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    CAPTIONS_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    THUMBNAILS_DIR.mkdir(parents=True, exist_ok=True)
    FULL_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Regenerating gallery markdown from all metadata...")
    metadata = load_metadata()
    update_gallery_markdown(metadata)
    print(f"Gallery markdown updated with {len(metadata)} images.")
    # Continue to process new images as before
    handler = ImageHandler()
    for ext in ["*.jpg", "*.jpeg", "*.png"]:
        for image_path in NEW_IMAGES.glob(ext):
            print(f"Found existing image: {image_path}")
            event = type('Event', (), {'src_path': str(image_path), 'is_directory': False})()
            handler.on_created(event)
    # Set up the observer
    observer = Observer()
    observer.schedule(handler, str(NEW_IMAGES), recursive=False)
    observer.start()
    print(f"Watching for new images in {NEW_IMAGES}")
    print("Press Ctrl+C to stop")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()