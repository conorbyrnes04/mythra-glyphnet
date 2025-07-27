#!/usr/bin/env python3
"""
Generate PNG variants for existing Celtic symbols
"""

import sys
from pathlib import Path
from PIL import Image
import numpy as np

def create_png_variants(input_path: Path, output_dir: Path, symbol_name: str):
    """Create optimized PNG variants with different color schemes."""
    
    try:
        # Load the original image
        img = Image.open(input_path)
        
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Create variants
        variants = {}
        
        # 1. Black variant (original with transparency)
        black_variant = img.copy()
        variants['black'] = black_variant
        
        # 2. Gold on black variant
        gold_variant = create_gold_on_black(img)
        variants['gold_on_black'] = gold_variant
        
        # 3. Emotional color variants
        emotions = {
            'passion': '#FF4444',      # Red
            'wisdom': '#4444FF',       # Blue  
            'growth': '#44FF44',       # Green
            'spirit': '#FF44FF',       # Magenta
            'earth': '#8B4513',        # Brown
            'water': '#0066CC',        # Blue
            'fire': '#FF6600',         # Orange
            'air': '#CCCCFF',          # Light blue
            'sacred': '#FFD700',       # Gold
            'mystic': '#9932CC'        # Purple
        }
        
        for emotion, color_hex in emotions.items():
            emotion_variant = create_emotional_color(img, color_hex)
            variants[emotion] = emotion_variant
        
        # Save all variants
        for variant_name, variant_img in variants.items():
            filename = f"{symbol_name}_{variant_name}.png"
            output_path = output_dir / filename
            
            variant_img.save(output_path, 'PNG', optimize=True, compress_level=9)
            
            file_size = output_path.stat().st_size
            print(f"   ✅ {variant_name}: {file_size/1024:.1f}KB")
        
        return variants
        
    except Exception as e:
        print(f"❌ Error creating variants for {input_path.name}: {e}")
        return None

def create_gold_on_black(img: Image.Image) -> Image.Image:
    """Create gold on black variant."""
    
    img_rgba = img.convert('RGBA')
    data = np.array(img_rgba)
    
    gold_img = Image.new('RGBA', img.size, (0, 0, 0, 255))
    gold_color = (255, 215, 0, 255)
    
    non_transparent = data[:, :, 3] > 0
    gold_data = np.array(gold_img)
    gold_data[non_transparent] = gold_color
    
    return Image.fromarray(gold_data, 'RGBA')

def create_emotional_color(img: Image.Image, color_hex: str) -> Image.Image:
    """Create emotional color variant."""
    
    color_hex = color_hex.lstrip('#')
    color_rgb = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
    color_rgba = color_rgb + (255,)
    
    img_rgba = img.convert('RGBA')
    data = np.array(img_rgba)
    
    emotion_img = Image.new('RGBA', img.size, (0, 0, 0, 255))
    
    non_transparent = data[:, :, 3] > 0
    emotion_data = np.array(emotion_img)
    emotion_data[non_transparent] = color_rgba
    
    return Image.fromarray(emotion_data, 'RGBA')

def main():
    """Generate variants for all Celtic symbols."""
    
    celtic_dir = Path("assets/glyphs/celtic/png/original")
    variants_dir = Path("assets/glyphs/celtic/png/variants")
    
    if not celtic_dir.exists():
        print(f"❌ Celtic directory not found: {celtic_dir}")
        return
    
    variants_dir.mkdir(parents=True, exist_ok=True)
    
    png_files = list(celtic_dir.glob("*.png"))
    
    if not png_files:
        print("❌ No PNG files found")
        return
    
    print(f"🎨 Generating variants for {len(png_files)} Celtic symbols...")
    
    for png_file in png_files:
        symbol_name = png_file.stem
        print(f"
🖼️ Processing: {symbol_name}")
        
        create_png_variants(png_file, variants_dir, symbol_name)
    
    print(f"
🎉 Variants generated successfully!")

if __name__ == "__main__":
    main()
