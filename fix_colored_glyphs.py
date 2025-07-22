#!/usr/bin/env python3
"""
Fix Colored Glyphs
Re-generate colored SVGs with proper emotion mapping
"""
import json
import sys
from pathlib import Path

# Add imports
sys.path.append('data/emotions')
from symbol_emotion_mapper import get_symbol_emotion
from test_emotion_coloring import analyze_emotion_colors, colorize_svg_gradient

def fix_colored_svg(symbol_name, meanings, bw_svg_path, colored_svg_path):
    """Fix a single colored SVG with proper emotion mapping"""
    
    print(f"🎨 Fixing colored SVG: {symbol_name}")
    
    try:
        # Get proper emotion mapping
        emotion_text, mapped_emotion = get_symbol_emotion(meanings)
        
        # Create emotion analysis with the mapped emotion
        emotion_analysis = {
            "dominant_emotion": mapped_emotion,
            "color_palette": {
                "primary": mapped_emotion["hex"],
                "secondary": mapped_emotion["hex"],
                "gradient": mapped_emotion["hex"],
                "light": mapped_emotion["hex"],
                "dark": mapped_emotion["hex"]
            }
        }
        
        # If we have a full color palette system, use it
        full_analysis = analyze_emotion_colors(emotion_text)
        if full_analysis["dominant_emotion"]["hex"] != "#808080":  # Not neutral
            emotion_analysis = full_analysis
        
        print(f"   🎨 Using color: {emotion_analysis['color_palette']['primary']}")
        
        # Read B&W SVG
        with open(bw_svg_path, 'r') as f:
            svg_content = f.read()
        
        # Apply proper gradient coloring
        colored_svg = colorize_svg_gradient(svg_content, emotion_analysis['color_palette'])
        
        # Save fixed colored version
        with open(colored_svg_path, 'w') as f:
            f.write(colored_svg)
        
        print(f"   ✅ Fixed: {Path(colored_svg_path).name}")
        
        return emotion_analysis
        
    except Exception as e:
        print(f"   ❌ Failed to fix {symbol_name}: {e}")
        return None

def fix_all_colored_glyphs():
    """Fix all colored glyphs in the codex"""
    
    print("🎨 Fixing All Colored gGlyph SVGs")
    print("=" * 50)
    
    # Load the codex
    codex_file = Path("results/gGlyphs_codex/gGlyph_codex.json")
    
    if not codex_file.exists():
        print("❌ Codex file not found!")
        return
    
    with open(codex_file, 'r') as f:
        codex_data = json.load(f)
    
    symbols = codex_data["symbols"]
    print(f"📊 Found {len(symbols)} symbols to fix")
    print()
    
    fixed_count = 0
    
    for symbol in symbols:
        symbol_name = symbol["name"]
        meanings = symbol["meanings"]
        bw_svg_path = symbol["files"]["svg_bw"]
        colored_svg_path = symbol["files"]["svg_colored"]
        
        # Check if files exist
        if not Path(bw_svg_path).exists():
            print(f"⚠️  B&W SVG not found for {symbol_name}: {bw_svg_path}")
            continue
        
        # Fix the colored version
        emotion_analysis = fix_colored_svg(symbol_name, meanings, bw_svg_path, colored_svg_path)
        
        if emotion_analysis:
            # Update metadata with proper emotion info
            metadata_file = Path(f"results/gGlyphs_codex/metadata/{symbol_name.lower()}_metadata.json")
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                
                metadata["emotion_analysis"] = emotion_analysis
                metadata["color_info"] = {
                    "primary_color": emotion_analysis["color_palette"]["primary"],
                    "emotion_family": emotion_analysis["dominant_emotion"]["core"],
                    "emotion_path": " → ".join(emotion_analysis["dominant_emotion"].get("path", [emotion_analysis["dominant_emotion"]["core"]]))
                }
                
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2)
            
            fixed_count += 1
        
        print()
    
    print(f"🎉 Fixed {fixed_count}/{len(symbols)} colored SVGs!")
    
    # Show color summary
    print("\n🎨 Color Summary:")
    print("-" * 30)
    
    for symbol in symbols:
        metadata_file = Path(f"results/gGlyphs_codex/metadata/{symbol['name'].lower()}_metadata.json")
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            
            color_info = metadata.get("color_info", {})
            color = color_info.get("primary_color", "#808080")
            emotion = color_info.get("emotion_family", "Neutral")
            
            print(f"   {symbol['name']:12} -> {emotion:8} ({color})")

if __name__ == "__main__":
    fix_all_colored_glyphs() 