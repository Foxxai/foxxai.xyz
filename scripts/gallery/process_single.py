#!/usr/bin/env python3

import os
import sys
from pathlib import Path
from PIL import Image

# Configuration
WORKSPACE_ROOT = Path('/home/foxxai/Github/foxxai.xyz')
NEW_IMAGES = WORKSPACE_ROOT / "hot_folder" / "new_images"
print(f"WORKSPACE_ROOT: {WORKSPACE_ROOT}")
print(f"NEW_IMAGES: {NEW_IMAGES}")
THUMBNAILS_DIR = WORKSPACE_ROOT / "docs/assets/travelogue/thumbnails"
FULL_DIR = WORKSPACE_ROOT / "docs/assets/travelogue/full"

# Image processing settings
THUMBNAIL_SIZE = (500, 500)
MAX_FULL_WIDTH = 2000

def process_image(image_path):
    """Process a single image."""
    print(f"Processing image: {image_path}")
    
    try:
        # Create output directories
        THUMBNAILS_DIR.mkdir(parents=True, exist_ok=True)
        FULL_DIR.mkdir(parents=True, exist_ok=True)
        
        image_name = image_path.name
        thumbnail_path = THUMBNAILS_DIR / image_name
        full_path = FULL_DIR / image_name
        
        print(f"Creating thumbnail at: {thumbnail_path}")
        # Create thumbnail
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
            img.save(thumbnail_path, "JPEG", quality=85, optimize=True)
        
        print(f"Creating optimized full-size image at: {full_path}")
        # Process full-size image
        with Image.open(image_path) as img:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            width, height = img.size
            if width > MAX_FULL_WIDTH:
                ratio = MAX_FULL_WIDTH / width
                new_size = (MAX_FULL_WIDTH, int(height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            img.save(full_path, "JPEG", quality=85, optimize=True)
        
        print(f"Successfully processed {image_name}")
        return True
        
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return False

def main():
    print(f"Looking for images in: {NEW_IMAGES}")
    if not NEW_IMAGES.exists():
        print(f"Directory does not exist: {NEW_IMAGES}")
        return
    
    # Process all images in the directory
    for ext in ['*.jpg', '*.jpeg', '*.png']:
        for image_path in NEW_IMAGES.glob(ext):
            print(f"Found image with extension {ext}: {image_path}")
        print(f"Found image: {image_path}")
        if process_image(image_path):
            print(f"Successfully processed: {image_path}")
        else:
            print(f"Failed to process: {image_path}")

if __name__ == "__main__":
    main()