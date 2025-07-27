#!/usr/bin/env python3
"""
Improve Celtic model quality and add optimized PNG variants
"""

import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import json

def create_enhanced_celtic_prompts():
    """Create enhanced prompts based on Midjourney quality."""
    
    enhanced_prompts = {
        "celtic_enhanced": {
            "description": "Enhanced Celtic style with Midjourney-quality aesthetics",
            "prompt": """Create a mythic glyph featuring {subject}. Use only bold, hand-drawn golden lines on a pure black background. The design should be highly abstract yet recognizable, with flowing organic forms, intricate swirling patterns, spiral motifs, and stylized eyes. Incorporate dynamic movement, sacred geometry, and tribal ornamentation. Channel the energy of ancient illuminated manuscripts, visionary art, and ritual symbols. The composition should be balanced, with strong contrast between the golden lines and black background. No text, no color except gold, create a powerful silhouette suitable for sacred art and spiritual practice. Make it beautiful, detailed, and evocative like high-quality Midjourney art.""",
            
            "variations": [
                "Create a sacred glyph representing {subject}. Use flowing golden lines on pure black background. Design should be abstract yet recognizable, with organic curves, spiral patterns, and mystical elements. Channel ancient Celtic art, sacred geometry, and visionary aesthetics. Make it beautiful and detailed.",
                
                "Design a mythic symbol for {subject}. Use bold golden strokes on black background. Create flowing, organic forms with intricate patterns, spiral motifs, and stylized eyes. Evoke ancient ritual art, tribal ornamentation, and sacred geometry. Make it abstract but meaningful, with dynamic movement and spiritual energy.",
                
                "Craft a visionary glyph featuring {subject}. Use golden lines on pure black background. Incorporate swirling patterns, spiral forms, and mystical elements. Design should be abstract yet recognizable, with flowing organic shapes and sacred geometry. Channel ancient art traditions and spiritual symbolism. Make it beautiful and evocative."
            ]
        },
        
        "gold_on_black": {
            "description": "Classic gold on black aesthetic with enhanced quality",
            "prompt": """Create a mythic glyph in the style of ancient ritual symbols and sacred geometry, featuring {subject}. Use only bold, hand-drawn golden lines on a pure black background. The design should be symmetrical or near-symmetrical, highly abstract but still recognizable, and richly ornamented with intricate patterns, geometric and floral motifs. Channel the energy of shamanic art, visionary illustrations, and illuminated manuscripts. Make it beautiful, detailed, and powerful. No text, no color except gold, strong silhouette, suitable for sacred art and spiritual practice. Create flowing, organic forms with dynamic movement and spiritual energy.""",
            
            "variations": [
                "Design a sacred symbol representing {subject}. Use golden lines on black background. Create symmetrical, abstract forms with intricate patterns and geometric motifs. Channel ancient ritual art and spiritual symbolism. Make it beautiful and meaningful.",
                
                "Craft a mythic glyph for {subject}. Use bold golden strokes on pure black background. Design should be balanced, abstract yet recognizable, with flowing patterns and sacred geometry. Evoke ancient art traditions and spiritual energy. Make it detailed and powerful."
            ]
        },
        
        "tribal_enhanced": {
            "description": "Enhanced tribal style with flowing organic forms",
            "prompt": """Create a tribal glyph featuring {subject}. Use bold golden lines on pure black background. Design should be organic and flowing, with dynamic curves, spiral patterns, and stylized elements. Channel ancient tribal art, shamanic symbols, and ritual ornamentation. Make it abstract yet recognizable, with strong movement and spiritual energy. The composition should be balanced and powerful, with intricate details and flowing forms. No text, no color except gold, create a beautiful and evocative sacred symbol.""",
            
            "variations": [
                "Design a tribal symbol for {subject}. Use golden lines on black background. Create organic, flowing forms with spiral patterns and mystical elements. Channel ancient tribal art and spiritual symbolism. Make it dynamic and meaningful.",
                
                "Craft a shamanic glyph representing {subject}. Use bold golden strokes on pure black background. Design should be organic and flowing, with intricate patterns and spiritual energy. Evoke ancient ritual art and tribal ornamentation. Make it beautiful and powerful."
            ]
        }
    }
    
    # Save enhanced prompts
    prompts_path = Path("prompts/enhanced_celtic_prompts.json")
    prompts_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(prompts_path, 'w') as f:
        json.dump(enhanced_prompts, f, indent=2)
    
    print(f"✅ Enhanced prompts saved: {prompts_path}")
    return enhanced_prompts

def create_png_variants(input_path: Path, output_dir: Path, symbol_name: str):
    """Create optimized PNG variants with different color schemes."""
    
    try:
        # Load the original image
        img = Image.open(input_path)
        
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Get image data
        data = np.array(img)
        
        # Create variants
        variants = {}
        
        # 1. Black variant (original with transparency)
        black_variant = img.copy()
        variants['black'] = black_variant
        
        # 2. Gold on black variant
        gold_variant = create_gold_on_black(img)
        variants['gold_on_black'] = gold_variant
        
        # 3. Emotional color variants (example with different emotions)
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
            # Create filename
            filename = f"{symbol_name}_{variant_name}.png"
            output_path = output_dir / filename
            
            # Save with optimization
            variant_img.save(output_path, 'PNG', optimize=True, compress_level=9)
            
            file_size = output_path.stat().st_size
            print(f"   ✅ {variant_name}: {file_size/1024:.1f}KB")
        
        return variants
        
    except Exception as e:
        print(f"❌ Error creating variants for {input_path.name}: {e}")
        return None

def create_gold_on_black(img: Image.Image) -> Image.Image:
    """Create gold on black variant."""
    
    # Convert to RGBA
    img_rgba = img.convert('RGBA')
    data = np.array(img_rgba)
    
    # Create new image with black background
    gold_img = Image.new('RGBA', img.size, (0, 0, 0, 255))
    
    # Convert non-transparent pixels to gold
    # Gold color: #FFD700
    gold_color = (255, 215, 0, 255)
    
    # Find non-transparent pixels (where alpha > 0)
    non_transparent = data[:, :, 3] > 0
    
    # Create gold image
    gold_data = np.array(gold_img)
    gold_data[non_transparent] = gold_color
    
    return Image.fromarray(gold_data, 'RGBA')

def create_emotional_color(img: Image.Image, color_hex: str) -> Image.Image:
    """Create emotional color variant."""
    
    # Convert hex to RGB
    color_hex = color_hex.lstrip('#')
    color_rgb = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
    color_rgba = color_rgb + (255,)
    
    # Convert to RGBA
    img_rgba = img.convert('RGBA')
    data = np.array(img_rgba)
    
    # Create new image with black background
    emotion_img = Image.new('RGBA', img.size, (0, 0, 0, 255))
    
    # Find non-transparent pixels
    non_transparent = data[:, :, 3] > 0
    
    # Apply emotional color
    emotion_data = np.array(emotion_img)
    emotion_data[non_transparent] = color_rgba
    
    return Image.fromarray(emotion_data, 'RGBA')

def update_celtic_interface():
    """Update the Celtic interface with enhanced prompts."""
    
    interface_path = Path("src/utils/model_interface.py")
    
    if not interface_path.exists():
        print(f"❌ Interface file not found: {interface_path}")
        return
    
    # Read the current interface
    with open(interface_path, 'r') as f:
        content = f.read()
    
    # Enhanced Celtic prompts
    enhanced_prompts = {
        "celtic_enhanced": "Create a mythic glyph featuring {subject}. Use only bold, hand-drawn golden lines on a pure black background. The design should be highly abstract yet recognizable, with flowing organic forms, intricate swirling patterns, spiral motifs, and stylized eyes. Incorporate dynamic movement, sacred geometry, and tribal ornamentation. Channel the energy of ancient illuminated manuscripts, visionary art, and ritual symbols. The composition should be balanced, with strong contrast between the golden lines and black background. No text, no color except gold, create a powerful silhouette suitable for sacred art and spiritual practice. Make it beautiful, detailed, and evocative like high-quality Midjourney art.",
        
        "gold_on_black": "Create a mythic glyph in the style of ancient ritual symbols and sacred geometry, featuring {subject}. Use only bold, hand-drawn golden lines on a pure black background. The design should be symmetrical or near-symmetrical, highly abstract but still recognizable, and richly ornamented with intricate patterns, geometric and floral motifs. Channel the energy of shamanic art, visionary illustrations, and illuminated manuscripts. Make it beautiful, detailed, and powerful. No text, no color except gold, strong silhouette, suitable for sacred art and spiritual practice. Create flowing, organic forms with dynamic movement and spiritual energy.",
        
        "tribal_enhanced": "Create a tribal glyph featuring {subject}. Use bold golden lines on pure black background. Design should be organic and flowing, with dynamic curves, spiral patterns, and stylized elements. Channel ancient tribal art, shamanic symbols, and ritual ornamentation. Make it abstract yet recognizable, with strong movement and spiritual energy. The composition should be balanced and powerful, with intricate details and flowing forms. No text, no color except gold, create a beautiful and evocative sacred symbol."
    }
    
    # Update the create_celtic_prompt method
    new_method = f'''
    def create_celtic_prompt(self, name: str, style: str = "celtic_enhanced", meaning: str = "", interpretation: str = "") -> str:
        """Create enhanced Celtic prompt with Midjourney-quality aesthetics."""
        
        enhanced_prompts = {{
            "celtic_enhanced": "Create a mythic glyph featuring {{subject}}. Use only bold, hand-drawn golden lines on a pure black background. The design should be highly abstract yet recognizable, with flowing organic forms, intricate swirling patterns, spiral motifs, and stylized eyes. Incorporate dynamic movement, sacred geometry, and tribal ornamentation. Channel the energy of ancient illuminated manuscripts, visionary art, and ritual symbols. The composition should be balanced, with strong contrast between the golden lines and black background. No text, no color except gold, create a powerful silhouette suitable for sacred art and spiritual practice. Make it beautiful, detailed, and evocative like high-quality Midjourney art.",
            "gold_on_black": "Create a mythic glyph in the style of ancient ritual symbols and sacred geometry, featuring {{subject}}. Use only bold, hand-drawn golden lines on a pure black background. The design should be symmetrical or near-symmetrical, highly abstract but still recognizable, and richly ornamented with intricate patterns, geometric and floral motifs. Channel the energy of shamanic art, visionary illustrations, and illuminated manuscripts. Make it beautiful, detailed, and powerful. No text, no color except gold, strong silhouette, suitable for sacred art and spiritual practice. Create flowing, organic forms with dynamic movement and spiritual energy.",
            "tribal_enhanced": "Create a tribal glyph featuring {{subject}}. Use bold golden lines on pure black background. Design should be organic and flowing, with dynamic curves, spiral patterns, and stylized elements. Channel ancient tribal art, shamanic symbols, and ritual ornamentation. Make it abstract yet recognizable, with strong movement and spiritual energy. The composition should be balanced and powerful, with intricate details and flowing forms. No text, no color except gold, create a beautiful and evocative sacred symbol."
        }}
        
        if style not in enhanced_prompts:
            style = "celtic_enhanced"
        
        prompt_template = enhanced_prompts[style]
        
        # Create subject description
        subject = name
        if meaning:
            subject += f" representing {{meaning}}"
        if interpretation:
            subject += f" ({{interpretation}})"
        
        return prompt_template.format(subject=subject)
'''
    
    # Replace the existing method
    import re
    
    # Find and replace the create_celtic_prompt method
    pattern = r'def create_celtic_prompt\(self, name: str, style: str = "celtic", meaning: str = "", interpretation: str = ""\) -> str:.*?return prompt_template\.format\(subject=subject\)'
    
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, new_method.strip(), content, flags=re.DOTALL)
        
        # Write back to file
        with open(interface_path, 'w') as f:
            f.write(content)
        
        print(f"✅ Updated Celtic interface with enhanced prompts")
    else:
        print(f"⚠️ Could not find create_celtic_prompt method to update")

def create_variant_generator():
    """Create a script to generate PNG variants for existing symbols."""
    
    script_content = '''#!/usr/bin/env python3
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
        print(f"\n🖼️ Processing: {symbol_name}")
        
        create_png_variants(png_file, variants_dir, symbol_name)
    
    print(f"\n🎉 Variants generated successfully!")

if __name__ == "__main__":
    main()
'''
    
    script_path = Path("scripts/generate_celtic_variants.py")
    script_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    print(f"✅ Variant generator created: {script_path}")

def main():
    """Main function to improve Celtic quality."""
    
    print("🎨 Improving Celtic Model Quality")
    print("=" * 50)
    
    # Create enhanced prompts
    print("\n📝 Creating enhanced prompts...")
    enhanced_prompts = create_enhanced_celtic_prompts()
    
    # Update Celtic interface
    print("\n🔧 Updating Celtic interface...")
    update_celtic_interface()
    
    # Create variant generator
    print("\n🖼️ Creating variant generator...")
    create_variant_generator()
    
    print("\n" + "=" * 50)
    print("🎉 CELTIC QUALITY IMPROVEMENTS COMPLETE!")
    print("=" * 50)
    
    print("\n🚀 What's New:")
    print("• Enhanced prompts with Midjourney-quality aesthetics")
    print("• Multiple style variations (celtic_enhanced, gold_on_black, tribal_enhanced)")
    print("• PNG variants: black, gold_on_black, emotional colors")
    print("• Automatic variant generation script")
    
    print("\n📋 Usage:")
    print("1. Use 'celtic_enhanced' style for best quality")
    print("2. Run 'python scripts/generate_celtic_variants.py' for variants")
    print("3. Choose from 10+ emotional color variants")
    
    print("\n🎯 Quality Improvements:")
    print("• More detailed, flowing organic forms")
    print("• Better balance and composition")
    print("• Enhanced spiritual and mystical elements")
    print("• Stronger contrast and visual impact")
    print("• Midjourney-level aesthetic quality")

if __name__ == "__main__":
    main() 