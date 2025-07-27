#!/usr/bin/env python3
"""
Glyph Migration Script
Migrates existing glyphs to the new project structure.
"""

import json
import shutil
import sys
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.processors.svg import SVGProcessor

def migrate_glyphs():
    """Migrate existing glyphs to new structure."""
    # Get absolute path to project root
    project_root = Path.cwd()
    print(f"\n🔍 Project root: {project_root}")
    
    # Source directories
    old_base = project_root / "results/gGlyphs_codex/archetypal_53"
    old_webp = old_base / "webp"
    old_svg = old_base / "svg_bw"
    old_colored = old_base / "svg_colored"
    old_metadata = old_base / "metadata"
    
    print(f"📁 Source directories:")
    print(f"- WebP: {old_webp}")
    print(f"- SVG: {old_svg}")
    print(f"- Colored: {old_colored}")
    print(f"- Metadata: {old_metadata}")
    
    # New directories
    new_base = project_root / "assets/glyphs/archetypal"
    new_webp = new_base / "webp"
    new_svg = new_base / "svg"
    new_colored = new_base / "colored"
    new_metadata = project_root / "assets/metadata"
    
    print(f"\n📁 Target directories:")
    print(f"- WebP: {new_webp}")
    print(f"- SVG: {new_svg}")
    print(f"- Colored: {new_colored}")
    print(f"- Metadata: {new_metadata}")
    
    # Create new directories
    for dir in [new_webp, new_svg, new_colored, new_metadata]:
        dir.mkdir(parents=True, exist_ok=True)
    
    # Load symbol codex for metadata
    try:
        with open(project_root / "results/gGlyphs_codex/archetypal_symbol_codex_complete.json", 'r') as f:
            codex = json.load(f)
    except:
        print("⚠️ Could not load complete codex, proceeding without it")
        codex = []
    
    # Initialize SVG processor for repairs if needed
    svg_processor = SVGProcessor()
    
    # Track migration statistics
    stats = {
        'total': 0,
        'success': 0,
        'failed': 0,
        'skipped': 0
    }
    
    # Process each glyph
    print("\n🔄 Starting glyph migration...")
    
    # Get list of all glyphs from webp directory
    glyphs = [f.stem for f in old_webp.glob("*.webp")]
    stats['total'] = len(glyphs)
    
    for glyph_name in glyphs:
        try:
            print(f"\n📦 Migrating {glyph_name}...")
            
            # Source files
            old_webp_file = old_webp / f"{glyph_name}.webp"
            old_svg_file = old_svg / f"{glyph_name}.svg"
            old_colored_file = old_colored / f"{glyph_name}_colored.svg"
            old_metadata_file = old_metadata / f"{glyph_name}.json"
            
            print(f"\n🔍 Source files:")
            print(f"- WebP: {old_webp_file} (exists: {old_webp_file.exists()})")
            print(f"- SVG: {old_svg_file} (exists: {old_svg_file.exists()})")
            print(f"- Colored: {old_colored_file} (exists: {old_colored_file.exists()})")
            print(f"- Metadata: {old_metadata_file} (exists: {old_metadata_file.exists()})")
            
            # Target files (ensure clean names)
            safe_name = glyph_name.replace(' ', '_').lower()
            new_webp_file = new_webp / f"{safe_name}.webp"
            new_svg_file = new_svg / f"{safe_name}.svg"
            new_colored_file = new_colored / f"{safe_name}_colored.svg"
            new_metadata_file = new_metadata / f"{safe_name}.json"
            
            print(f"\n🔍 Target files:")
            print(f"- WebP: {new_webp_file}")
            print(f"- SVG: {new_svg_file}")
            print(f"- Colored: {new_colored_file}")
            print(f"- Metadata: {new_metadata_file}")
            
            # Get metadata from codex
            glyph_metadata = None
            for symbol in codex:
                if symbol.get('name', '').lower() == glyph_name.lower():
                    glyph_metadata = symbol
                    break
            
            # Copy files
            if old_webp_file.exists():
                print(f"\n📝 Copying WebP file...")
                shutil.copy2(old_webp_file, new_webp_file)
            else:
                print(f"⚠️ Missing WebP for {glyph_name}")
                stats['skipped'] += 1
                continue
            
            if old_svg_file.exists():
                print(f"📝 Copying SVG file...")
                shutil.copy2(old_svg_file, new_svg_file)
            else:
                print(f"⚠️ Missing SVG for {glyph_name}, attempting repair...")
                if not svg_processor.convert_to_svg(new_webp_file, new_svg_file):
                    print(f"❌ Could not repair SVG for {glyph_name}")
                    stats['failed'] += 1
                    continue
            
            # Create colored version
            emotion_hex = glyph_metadata.get('emotion_hex', '#000000') if glyph_metadata else '#000000'
            if old_colored_file.exists():
                print(f"📝 Copying colored SVG file...")
                shutil.copy2(old_colored_file, new_colored_file)
            else:
                print(f"⚠️ Missing colored SVG for {glyph_name}, generating...")
                if not svg_processor.apply_color(new_svg_file, new_colored_file, emotion_hex):
                    print(f"❌ Could not create colored SVG for {glyph_name}")
            
            # Create or update metadata
            metadata = {
                "name": glyph_name.replace('_', ' ').title(),
                "meaning": "",
                "interpretation": "",
                "emotion_hex": emotion_hex,
                "files": {
                    "webp": str(new_webp_file.relative_to(project_root)),
                    "svg": str(new_svg_file.relative_to(project_root)),
                    "colored": str(new_colored_file.relative_to(project_root))
                }
            }
            
            # Try to get additional metadata from old file
            if old_metadata_file.exists():
                try:
                    with open(old_metadata_file, 'r') as f:
                        old_metadata = json.load(f)
                    metadata.update({
                        "meaning": old_metadata.get("meaning", ""),
                        "interpretation": old_metadata.get("interpretation", "")
                    })
                except:
                    print(f"⚠️ Could not read old metadata for {glyph_name}")
            
            # Update with codex metadata if available
            if glyph_metadata:
                metadata.update({
                    "meaning": glyph_metadata.get("meaning", metadata["meaning"]),
                    "interpretation": glyph_metadata.get("interpretation", metadata["interpretation"])
                })
            
            # Save new metadata
            print(f"📝 Saving metadata...")
            with open(new_metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            stats['success'] += 1
            print(f"✅ Successfully migrated {glyph_name}")
            
        except Exception as e:
            print(f"❌ Error migrating {glyph_name}: {e}")
            print(f"🔍 Debug info:")
            print(f"- Project root: {project_root}")
            print(f"- Old WebP: {old_webp_file}")
            print(f"- New WebP: {new_webp_file}")
            print(f"- Old SVG: {old_svg_file}")
            print(f"- New SVG: {new_svg_file}")
            print(f"- Old colored: {old_colored_file}")
            print(f"- New colored: {new_colored_file}")
            print(f"- Old metadata: {old_metadata_file}")
            print(f"- New metadata: {new_metadata_file}")
            print(f"- Glyph metadata: {glyph_metadata}")
            stats['failed'] += 1
    
    # Print summary
    print("\n📊 Migration Summary")
    print("=" * 50)
    print(f"Total glyphs found: {stats['total']}")
    print(f"Successfully migrated: {stats['success']}")
    print(f"Failed to migrate: {stats['failed']}")
    print(f"Skipped: {stats['skipped']}")
    
    if stats['success'] > 0:
        print("\n✨ Migration completed! New structure:")
        print(f"- WebP files: {new_webp}")
        print(f"- SVG files: {new_svg}")
        print(f"- Colored SVGs: {new_colored}")
        print(f"- Metadata: {new_metadata}")

if __name__ == "__main__":
    migrate_glyphs() 