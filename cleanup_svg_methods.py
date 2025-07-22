#!/usr/bin/env python3
"""
Cleanup Script: Keep only OTSU SVGs
Remove simple and aggressive method SVGs, keep only OTSU
"""
from pathlib import Path

def cleanup_svg_methods():
    """Remove non-OTSU SVG files"""
    
    results_dir = Path("results/glyphs")
    
    # Find all simple and aggressive SVG files
    simple_files = list(results_dir.glob("*_simple.svg"))
    aggressive_files = list(results_dir.glob("*_aggressive.svg"))
    
    removed_count = 0
    
    print("🧹 Cleaning up non-OTSU SVG files...")
    
    for file in simple_files + aggressive_files:
        try:
            file.unlink()
            print(f"🗑️  Removed: {file.name}")
            removed_count += 1
        except Exception as e:
            print(f"❌ Failed to remove {file.name}: {e}")
    
    # Rename OTSU files to remove the method suffix
    otsu_files = list(results_dir.glob("*_otsu.svg"))
    renamed_count = 0
    
    for otsu_file in otsu_files:
        new_name = otsu_file.name.replace("_otsu.svg", ".svg")
        new_path = otsu_file.parent / new_name
        
        if not new_path.exists():
            try:
                otsu_file.rename(new_path)
                print(f"📝 Renamed: {otsu_file.name} → {new_name}")
                renamed_count += 1
            except Exception as e:
                print(f"❌ Failed to rename {otsu_file.name}: {e}")
    
    print(f"\n✅ Cleanup complete!")
    print(f"   Removed: {removed_count} files")
    print(f"   Renamed: {renamed_count} files")
    print(f"   Now using OTSU method exclusively")

if __name__ == "__main__":
    cleanup_svg_methods()
