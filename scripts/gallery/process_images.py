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
WORKSPACE_ROOT = Path(__file__).parent.parent.resolve()
print(f"Workspace root: {WORKSPACE_ROOT}")
HOT_FOLDER = WORKSPACE_ROOT / "hot_folder"
print(f"Hot folder: {HOT_FOLDER}")
NEW_IMAGES = HOT_FOLDER / "new_images"
print(f"New images folder: {NEW_IMAGES}")
THUMBNAILS_DIR = WORKSPACE_ROOT / "docs/assets/travelogue/thumbnails"
print(f"Thumbnails directory: {THUMBNAILS_DIR}")
FULL_DIR = WORKSPACE_ROOT / "docs/assets/travelogue/full"
print(f"Full images directory: {FULL_DIR}")
CAPTIONS_FOLDER = HOT_FOLDER / "captions"
THUMBNAILS_DIR = WORKSPACE_ROOT / "docs/assets/travelogue/thumbnails"
FULL_DIR = WORKSPACE_ROOT / "docs/assets/travelogue/full"
GALLERY_MD = WORKSPACE_ROOT / "docs/travelogue/index.md"
METADATA_FILE = HOT_FOLDER / "gallery_metadata.yml"

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
    # Read existing content before the gallery
    header_content = ""
    if GALLERY_MD.exists():
        with open(GALLERY_MD, 'r') as f:
            content = f.read()
            header_end = content.find('<div class="gallery-grid">')
            if header_end != -1:
                header_content = content[:header_end]
            else:
                header_content = content
    
    # Generate gallery items
    gallery_items = []
    for image_name, data in sorted(metadata.items(), key=lambda x: x[1].get('date', ''), reverse=True):
        item = f'''    <div class="gallery-item" 
         data-full-image="/assets/travelogue/full/{image_name}"
         data-full-caption="{data.get('full_caption', '')}">
        <img class="gallery-thumbnail" src="/assets/travelogue/thumbnails/{image_name}" alt="{data.get('alt_text', '')}">
        <div class="gallery-caption">{data.get('short_caption', '')}</div>
    </div>'''
        gallery_items.append(item)
    
    # Combine content
    gallery_content = '<div class="gallery-grid">\n'
    gallery_content += '\n\n'.join(gallery_items)
    gallery_content += '\n</div>'
    
    # Write the complete file
    with open(GALLERY_MD, 'w') as f:
        f.write(f"{header_content.strip()}\n\n{gallery_content}")

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
            
        # Only process image files
        if not event.src_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            return
            
        image_path = Path(event.src_path)
        image_name = image_path.name
        
        print(f"Processing new image: {image_name}")
        
        try:
            # Create thumbnails directory if it doesn't exist
            THUMBNAILS_DIR.mkdir(parents=True, exist_ok=True)
            FULL_DIR.mkdir(parents=True, exist_ok=True)
            
            # Process the image
            thumbnail_path = THUMBNAILS_DIR / image_name
            full_path = FULL_DIR / image_name
            
            # Create thumbnail and optimize full image
            create_thumbnail(image_path, thumbnail_path)
            optimize_full_image(image_path, full_path)
            
            # Load existing metadata
            metadata = load_metadata()
            
            # Check for caption file
            caption_file = CAPTIONS_FOLDER / f"{image_path.stem}.yml"
            if caption_file.exists():
                with open(caption_file, 'r') as f:
                    image_metadata = yaml.safe_load(f)
            else:
                # Create template caption file
                image_metadata = {
                    'short_caption': 'Add a short caption here',
                    'full_caption': 'Add a detailed description here',
                    'alt_text': 'Add alt text here',
                    'date': time.strftime('%Y-%m-%d')
                }
                with open(caption_file, 'w') as f:
                    yaml.dump(image_metadata, f, default_flow_style=False)
            
            # Update metadata
            metadata[image_name] = image_metadata
            save_metadata(metadata)
            
            # Update gallery markdown
            update_gallery_markdown(metadata)
            
            # Move processed image to an archive folder
            archive_dir = HOT_FOLDER / "processed"
            archive_dir.mkdir(exist_ok=True)
            shutil.move(image_path, archive_dir / image_name)
            
            print(f"Successfully processed {image_name}")
            
        except Exception as e:
            print(f"Error processing {image_name}: {str(e)}")

def main():
    # Create necessary directories
    NEW_IMAGES.mkdir(parents=True, exist_ok=True)
    CAPTIONS_FOLDER.mkdir(parents=True, exist_ok=True)
    THUMBNAILS_DIR.mkdir(parents=True, exist_ok=True)
    FULL_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"Checking for existing images...")
    for image_path in NEW_IMAGES.glob("*.jp*g"):
        print(f"Found existing image: {image_path}")
        event = type('Event', (), {'src_path': str(image_path), 'is_directory': False})()
        ImageHandler().on_created(event)
    
    # Set up the observer
    observer = Observer()
    observer.schedule(ImageHandler(), str(NEW_IMAGES), recursive=False)
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