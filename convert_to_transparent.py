#!/usr/bin/env python3
"""
Convert PNG files with black backgrounds to transparent backgrounds
"""

import sys
from pathlib import Path
from PIL import Image
import numpy as np

def convert_to_transparent(input_path: Path, output_path: Path = None, threshold: int = 30):
    """Convert PNG with black background to transparent background."""
    try:
        # Load the image
        img = Image.open(input_path)
        
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Convert to numpy array for processing
        data = np.array(img)
        
        # Create a mask for black pixels (background)
        # Check if R, G, B are all below threshold (black)
        black_mask = np.all(data[:, :, :3] <= threshold, axis=2)
        
        # Set alpha channel to 0 for black pixels (transparent)
        data[black_mask, 3] = 0
        
        # Convert back to PIL Image
        transparent_img = Image.fromarray(data)
        
        # Save with transparent background
        if output_path is None:
            output_path = input_path.parent / f"{input_path.stem}_transparent{input_path.suffix}"
        
        transparent_img.save(output_path, 'PNG')
        
        print(f"✅ Converted {input_path.name} to transparent background")
        return output_path
        
    except Exception as e:
        print(f"❌ Error converting {input_path.name}: {e}")
        return None

def batch_convert_pngs():
    """Convert all PNG files in the archetypal directory."""
    png_dir = Path("assets/glyphs/archetypal/png")
    
    if not png_dir.exists():
        print(f"❌ PNG directory not found: {png_dir}")
        return
    
    png_files = list(png_dir.glob("*.png"))
    
    if not png_files:
        print("❌ No PNG files found")
        return
    
    print(f"🎨 Converting {len(png_files)} PNG files to transparent backgrounds...")
    
    converted_count = 0
    for png_file in png_files:
        # Skip files that already have "_transparent" in the name
        if "_transparent" in png_file.name:
            continue
            
        # Convert to transparent
        result = convert_to_transparent(png_file)
        if result:
            converted_count += 1
    
    print(f"✅ Successfully converted {converted_count} PNG files")
    
    # Show the results
    print("\n📁 Transparent PNG files:")
    transparent_files = list(png_dir.glob("*_transparent.png"))
    for file in transparent_files:
        print(f"  - {file.name}")

def test_conversion():
    """Test conversion on a single file."""
    test_file = Path("assets/glyphs/archetypal/png/celtic_png_test_house.png")
    
    if not test_file.exists():
        print(f"❌ Test file not found: {test_file}")
        return
    
    print("🧪 Testing PNG to transparent conversion...")
    result = convert_to_transparent(test_file)
    
    if result:
        print(f"✅ Test successful! Transparent file: {result.name}")
        
        # Check file properties
        try:
            img = Image.open(result)
            print(f"📊 Image mode: {img.mode}")
            print(f"📊 Image size: {img.size}")
            print(f"📊 Has transparency: {'Yes' if img.mode == 'RGBA' else 'No'}")
        except Exception as e:
            print(f"❌ Error checking file properties: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_conversion()
    else:
        batch_convert_pngs() 