#!/usr/bin/env python3
"""
Optimize PNG file sizes for dreamscape performance
"""

import sys
from pathlib import Path
from PIL import Image
import numpy as np

def optimize_png_size(input_path: Path, output_path: Path = None, 
                     max_size: tuple = (256, 256), quality: int = 85):
    """Optimize PNG size while maintaining transparency."""
    try:
        # Load the image
        img = Image.open(input_path)
        
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Resize if larger than max_size
        if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            print(f"📏 Resized from {img.size} to {max_size}")
        
        # Save with maximum compression
        if output_path is None:
            output_path = input_path.parent / f"{input_path.stem}_optimized{input_path.suffix}"
        
        img.save(output_path, 'PNG', optimize=True, compress_level=9)
        
        # Get file sizes
        original_size = input_path.stat().st_size
        optimized_size = output_path.stat().st_size
        compression_ratio = (1 - optimized_size / original_size) * 100
        
        print(f"✅ Optimized {input_path.name}")
        print(f"   Original: {original_size/1024:.1f}KB")
        print(f"   Optimized: {optimized_size/1024:.1f}KB")
        print(f"   Compression: {compression_ratio:.1f}%")
        
        return output_path
        
    except Exception as e:
        print(f"❌ Error optimizing {input_path.name}: {e}")
        return None

def create_webp_version(input_path: Path, output_path: Path = None, quality: int = 85):
    """Create WebP version with transparency for even smaller files."""
    try:
        # Load the image
        img = Image.open(input_path)
        
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Create WebP path
        if output_path is None:
            output_path = input_path.parent / f"{input_path.stem}.webp"
        
        # Save as WebP with transparency
        img.save(output_path, 'WEBP', quality=quality, method=6)
        
        # Get file sizes
        original_size = input_path.stat().st_size
        webp_size = output_path.stat().st_size
        compression_ratio = (1 - webp_size / original_size) * 100
        
        print(f"✅ Created WebP: {output_path.name}")
        print(f"   Original PNG: {original_size/1024:.1f}KB")
        print(f"   WebP: {webp_size/1024:.1f}KB")
        print(f"   Compression: {compression_ratio:.1f}%")
        
        return output_path
        
    except Exception as e:
        print(f"❌ Error creating WebP {input_path.name}: {e}")
        return None

def create_multiple_sizes(input_path: Path, sizes: list = [(256, 256), (128, 128), (64, 64)]):
    """Create multiple sizes for different zoom levels."""
    try:
        img = Image.open(input_path)
        
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        results = {}
        
        for size in sizes:
            # Create resized version
            resized = img.copy()
            resized.thumbnail(size, Image.Resampling.LANCZOS)
            
            # Save optimized version
            output_path = input_path.parent / f"{input_path.stem}_{size[0]}x{size[1]}.png"
            resized.save(output_path, 'PNG', optimize=True, compress_level=9)
            
            file_size = output_path.stat().st_size
            results[f"{size[0]}x{size[1]}"] = {
                'path': output_path,
                'size': file_size,
                'size_kb': file_size / 1024
            }
            
            print(f"✅ Created {size[0]}x{size[1]}: {file_size/1024:.1f}KB")
        
        return results
        
    except Exception as e:
        print(f"❌ Error creating multiple sizes: {e}")
        return None

def batch_optimize():
    """Optimize all PNG files in the archetypal directory."""
    png_dir = Path("assets/glyphs/archetypal/png")
    
    if not png_dir.exists():
        print(f"❌ PNG directory not found: {png_dir}")
        return
    
    # Get all PNG files (excluding already optimized ones)
    png_files = [f for f in png_dir.glob("*.png") 
                 if not any(suffix in f.name for suffix in ['_optimized', '_256x256', '_128x128', '_64x64'])]
    
    if not png_files:
        print("❌ No PNG files to optimize")
        return
    
    print(f"🎨 Optimizing {len(png_files)} PNG files for dreamscape performance...")
    
    total_original_size = 0
    total_optimized_size = 0
    
    for png_file in png_files:
        print(f"\n📁 Processing: {png_file.name}")
        
        # Get original size
        original_size = png_file.stat().st_size
        total_original_size += original_size
        
        # Create optimized versions
        optimized_png = optimize_png_size(png_file, max_size=(256, 256))
        webp_version = create_webp_version(png_file, quality=85)
        multiple_sizes = create_multiple_sizes(png_file)
        
        if optimized_png:
            total_optimized_size += optimized_png.stat().st_size
    
    # Summary
    print(f"\n{'='*50}")
    print(f"📊 OPTIMIZATION SUMMARY")
    print(f"{'='*50}")
    print(f"Total original size: {total_original_size/1024/1024:.1f}MB")
    print(f"Total optimized size: {total_optimized_size/1024/1024:.1f}MB")
    print(f"Space saved: {(total_original_size - total_optimized_size)/1024/1024:.1f}MB")
    
    # Performance recommendations
    print(f"\n🚀 PERFORMANCE RECOMMENDATIONS:")
    print(f"• Use 64x64 PNG for distant symbols (zoom out)")
    print(f"• Use 128x128 PNG for medium distance")
    print(f"• Use 256x256 PNG for close-up symbols")
    print(f"• Use WebP for modern browsers (smallest size)")
    print(f"• Implement lazy loading for symbols outside viewport")

def test_optimization():
    """Test optimization on a single file."""
    test_file = Path("assets/glyphs/archetypal/png/celtic_png_test_house_transparent.png")
    
    if not test_file.exists():
        print(f"❌ Test file not found: {test_file}")
        return
    
    print("🧪 Testing PNG optimization...")
    
    # Test different optimization strategies
    print("\n1️⃣ Testing size optimization:")
    optimized = optimize_png_size(test_file, max_size=(256, 256))
    
    print("\n2️⃣ Testing WebP conversion:")
    webp = create_webp_version(test_file, quality=85)
    
    print("\n3️⃣ Testing multiple sizes:")
    sizes = create_multiple_sizes(test_file)
    
    if sizes:
        print("\n📊 Size comparison:")
        for size_name, info in sizes.items():
            print(f"  {size_name}: {info['size_kb']:.1f}KB")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_optimization()
    else:
        batch_optimize() 