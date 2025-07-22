#!/usr/bin/env python3
"""
Test Emotion Coloring System
Standalone test for emotion-based SVG coloring
"""
import sys
import os
sys.path.append('data/emotions')

from emotion_processor import emotion_processor, analyze_dream_emotions
import re
from pathlib import Path
from typing import Dict

def hex_to_rgb(hex_color):
    """Convert hex to RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_gradient_colors(primary_hex, secondary_hex=None):
    """Create color palette from emotion colors"""
    primary_rgb = hex_to_rgb(primary_hex)
    
    if secondary_hex:
        secondary_rgb = hex_to_rgb(secondary_hex)
        mid_rgb = tuple((primary_rgb[i] + secondary_rgb[i]) // 2 for i in range(3))
        gradient_hex = f"#{mid_rgb[0]:02x}{mid_rgb[1]:02x}{mid_rgb[2]:02x}"
    else:
        lighter_rgb = tuple(min(255, int(c * 1.3)) for c in primary_rgb)
        gradient_hex = f"#{lighter_rgb[0]:02x}{lighter_rgb[1]:02x}{lighter_rgb[2]:02x}"
    
    return {
        "primary": primary_hex,
        "secondary": secondary_hex or gradient_hex,
        "gradient": gradient_hex,
        "light": f"#{min(255, int(primary_rgb[0] * 1.2)):02x}{min(255, int(primary_rgb[1] * 1.2)):02x}{min(255, int(primary_rgb[2] * 1.2)):02x}",
        "dark": f"#{max(0, int(primary_rgb[0] * 0.8)):02x}{max(0, int(primary_rgb[1] * 0.8)):02x}{max(0, int(primary_rgb[2] * 0.8)):02x}"
    }

def analyze_emotion_colors(text):
    """Analyze text and return emotion with colors"""
    emotions = analyze_dream_emotions(text)
    
    if not emotions:
        return {
            "dominant_emotion": {"core": "Neutral", "hex": "#808080"},
            "color_palette": create_gradient_colors("#808080")
        }
    
    # Get most specific emotion
    dominant = emotions[0]
    for emotion in emotions:
        if emotion["level"] == "tertiary":
            dominant = emotion
            break
        elif emotion["level"] == "secondary" and dominant["level"] == "core":
            dominant = emotion
    
    # Secondary emotion for blending
    secondary_emotion = emotions[1] if len(emotions) > 1 else None
    
    primary_hex = dominant["hex"]
    secondary_hex = secondary_emotion["hex"] if secondary_emotion else None
    
    color_palette = create_gradient_colors(primary_hex, secondary_hex)
    
    return {
        "dominant_emotion": dominant,
        "secondary_emotion": secondary_emotion,
        "all_emotions": emotions,
        "color_palette": color_palette
    }

def colorize_svg_solid(svg_content, color):
    """Apply solid color to SVG"""
    svg_content = re.sub(r'fill="#000000?"', f'fill="{color}"', svg_content)
    svg_content = re.sub(r'fill="black"', f'fill="{color}"', svg_content)
    svg_content = re.sub(r'stroke="#000000?"', f'stroke="{color}"', svg_content)
    svg_content = re.sub(r'stroke="black"', f'stroke="{color}"', svg_content)
    return svg_content

def colorize_svg_gradient(svg_content, color_palette):
    """Apply gradient to SVG"""
    gradient_id = "emotionGradient"
    gradient_def = f'''<defs>
    <linearGradient id="{gradient_id}" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:{color_palette['primary']};stop-opacity:1" />
        <stop offset="50%" style="stop-color:{color_palette['gradient']};stop-opacity:1" />
        <stop offset="100%" style="stop-color:{color_palette['secondary']};stop-opacity:1" />
    </linearGradient>
</defs>'''
    
    # Insert gradient properly after opening SVG tag
    if '<defs>' in svg_content:
        # Replace existing defs
        svg_content = re.sub(r'<defs>.*?</defs>', gradient_def, svg_content, flags=re.DOTALL)
    else:
        # Insert after SVG opening tag
        svg_content = re.sub(r'(<svg[^>]*>)', rf'\1\n{gradient_def}', svg_content)
    
    # Apply gradient
    svg_content = re.sub(r'fill="#000000?"', f'fill="url(#{gradient_id})"', svg_content)
    svg_content = re.sub(r'fill="black"', f'fill="url(#{gradient_id})"', svg_content)
    
    return svg_content

def colorize_svg_radial(svg_content, color_palette):
    """Apply radial emotional blend"""
    gradient_id = "emotionalBlend"
    gradient_def = f'''<defs>
    <radialGradient id="{gradient_id}" cx="50%" cy="50%" r="50%">
        <stop offset="0%" style="stop-color:{color_palette['primary']};stop-opacity:0.9" />
        <stop offset="70%" style="stop-color:{color_palette['secondary']};stop-opacity:0.7" />
        <stop offset="100%" style="stop-color:{color_palette['dark']};stop-opacity:1" />
    </radialGradient>
</defs>'''
    
    # Insert gradient properly after opening SVG tag
    if '<defs>' in svg_content:
        # Replace existing defs
        svg_content = re.sub(r'<defs>.*?</defs>', gradient_def, svg_content, flags=re.DOTALL)
    else:
        # Insert after SVG opening tag  
        svg_content = re.sub(r'(<svg[^>]*>)', rf'\1\n{gradient_def}', svg_content)
    
    svg_content = re.sub(r'fill="#000000?"', f'fill="url(#{gradient_id})"', svg_content)
    svg_content = re.sub(r'fill="black"', f'fill="url(#{gradient_id})"', svg_content)
    
    return svg_content

def test_emotion_coloring(text, svg_path):
    """Test all coloring styles on an SVG"""
    
    print(f"🎨 Testing emotion coloring on: {Path(svg_path).name}")
    print(f"📝 Emotion text: '{text}'")
    print("=" * 60)
    
    # Analyze emotions
    emotion_analysis = analyze_emotion_colors(text)
    dominant = emotion_analysis["dominant_emotion"]
    
    emotion_path = " → ".join(dominant.get("path", [dominant["core"]]))
    print(f"😊 Detected emotion: {emotion_path}")
    print(f"🎨 Primary color: {emotion_analysis['color_palette']['primary']}")
    print(f"🎨 Color palette: {emotion_analysis['color_palette']}")
    
    # Check if SVG exists
    svg_file = Path(svg_path)
    if not svg_file.exists():
        print(f"❌ SVG not found: {svg_path}")
        return
    
    # Read original SVG
    with open(svg_file, 'r') as f:
        original_svg = f.read()
    
    print(f"\n📄 Original SVG size: {len(original_svg)} characters")
    
    # Create colored versions
    styles = {
        "solid": colorize_svg_solid,
        "gradient": colorize_svg_gradient,
        "radial": colorize_svg_radial
    }
    
    for style_name, colorize_func in styles.items():
        try:
            if style_name == "solid":
                colored_svg = colorize_func(original_svg, emotion_analysis['color_palette']['primary'])
            else:
                colored_svg = colorize_func(original_svg, emotion_analysis['color_palette'])
            
            # Save colored version
            timestamp = svg_file.stem.split('_')[-1] if '_' in svg_file.stem else "test"
            colored_filename = f"colored_{dominant['core'].lower()}_{style_name}_{timestamp}.svg"
            colored_path = svg_file.parent / colored_filename
            
            with open(colored_path, 'w') as f:
                f.write(colored_svg)
            
            print(f"✅ {style_name.title()} style: {colored_filename}")
            
        except Exception as e:
            print(f"❌ Failed {style_name}: {e}")
    
    return emotion_analysis

if __name__ == "__main__":
    # Test cases
    test_cases = [
        {
            "text": "I felt overwhelming joy and happiness dancing in the sunlight",
            "emotion": "Joy"
        },
        {
            "text": "Deep melancholy and sadness consumed my heart",
            "emotion": "Sadness"
        },
        {
            "text": "Terrifying fear and panic gripped me in darkness",
            "emotion": "Fear"
        },
        {
            "text": "Burning rage and fury exploded within me",
            "emotion": "Anger"
        },
        {
            "text": "Tender love and compassion filled my soul",
            "emotion": "Love"
        }
    ]
    
    # Find an SVG to test with
    glyph_dir = Path("results/glyphs")
    svg_files = list(glyph_dir.glob("*.svg"))
    
    if not svg_files:
        print("❌ No SVG files found in results/glyphs/")
        exit(1)
    
    test_svg = svg_files[0]  # Use first available SVG
    
    print("🎨 EMOTION-BASED GLYPH COLORING TEST")
    print("=" * 60)
    print(f"🔧 Using test glyph: {test_svg.name}")
    print()
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n🧪 TEST {i}: {case['emotion']} Emotion")
        print("-" * 40)
        emotion_analysis = test_emotion_coloring(case["text"], str(test_svg))
        
        if i < len(test_cases):
            input("\n⏎ Press Enter for next test...")
    
    print(f"\n🎉 All tests complete! Check results/glyphs/ for colored SVGs") 