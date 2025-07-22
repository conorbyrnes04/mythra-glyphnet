#!/usr/bin/env python3
"""
Color Glyph Generator - Apply emotion-based colors to SVG glyphs
"""
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from emotion_processor import emotion_processor, analyze_dream_emotions, get_emotion_info

class ColorGlyphGenerator:
    """Generate colored versions of glyphs based on emotional analysis"""
    
    def __init__(self):
        self.emotion_processor = emotion_processor
        
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hex(self, r: int, g: int, b: int) -> str:
        """Convert RGB to hex color"""
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def create_gradient_colors(self, primary_hex: str, secondary_hex: str = None) -> Dict[str, str]:
        """Create a gradient color palette from emotion colors"""
        primary_rgb = self.hex_to_rgb(primary_hex)
        
        if secondary_hex:
            secondary_rgb = self.hex_to_rgb(secondary_hex)
            # Blend colors for gradient
            mid_rgb = tuple((primary_rgb[i] + secondary_rgb[i]) // 2 for i in range(3))
            gradient_hex = self.rgb_to_hex(*mid_rgb)
        else:
            # Create lighter/darker variations
            lighter_rgb = tuple(min(255, int(c * 1.3)) for c in primary_rgb)
            darker_rgb = tuple(max(0, int(c * 0.7)) for c in primary_rgb)
            gradient_hex = self.rgb_to_hex(*lighter_rgb)
        
        return {
            "primary": primary_hex,
            "secondary": secondary_hex or gradient_hex,
            "gradient": gradient_hex,
            "light": self.rgb_to_hex(*tuple(min(255, int(c * 1.2)) for c in primary_rgb)),
            "dark": self.rgb_to_hex(*tuple(max(0, int(c * 0.8)) for c in primary_rgb))
        }
    
    def analyze_text_emotions(self, text: str) -> Dict:
        """Analyze text and return dominant emotion with colors"""
        emotions = analyze_dream_emotions(text)
        
        if not emotions:
            return {
                "dominant_emotion": {"core": "Neutral", "hex": "#808080"},
                "all_emotions": [],
                "color_palette": self.create_gradient_colors("#808080")
            }
        
        # Get the most specific emotion
        dominant = emotions[0]
        for emotion in emotions:
            if emotion["level"] == "tertiary":
                dominant = emotion
                break
            elif emotion["level"] == "secondary" and dominant["level"] == "core":
                dominant = emotion
        
        # Get secondary emotion for blending if available
        secondary_emotion = None
        if len(emotions) > 1:
            secondary_emotion = emotions[1]
        
        # Create color palette
        primary_hex = dominant["hex"]
        secondary_hex = secondary_emotion["hex"] if secondary_emotion else None
        
        color_palette = self.create_gradient_colors(primary_hex, secondary_hex)
        
        return {
            "dominant_emotion": dominant,
            "secondary_emotion": secondary_emotion,
            "all_emotions": emotions,
            "color_palette": color_palette
        }
    
    def colorize_svg(self, svg_path: str, emotion_analysis: Dict, style: str = "gradient") -> str:
        """Apply emotion-based colors to an SVG file"""
        
        svg_file = Path(svg_path)
        if not svg_file.exists():
            raise FileNotFoundError(f"SVG file not found: {svg_path}")
        
        # Read SVG content
        with open(svg_file, 'r') as f:
            svg_content = f.read()
        
        color_palette = emotion_analysis["color_palette"]
        emotion_name = emotion_analysis["dominant_emotion"]["core"]
        
        # Create colored version based on style
        if style == "solid":
            colored_svg = self._apply_solid_color(svg_content, color_palette["primary"])
        elif style == "gradient":
            colored_svg = self._apply_gradient_color(svg_content, color_palette)
        elif style == "emotional_blend":
            colored_svg = self._apply_emotional_blend(svg_content, emotion_analysis)
        else:  # "accent"
            colored_svg = self._apply_accent_color(svg_content, color_palette)
        
        # Save colored version
        timestamp = svg_file.stem.split('_')[-1] if '_' in svg_file.stem else "colored"
        colored_filename = f"colored_{emotion_name.lower()}_{style}_{timestamp}.svg"
        colored_path = svg_file.parent / colored_filename
        
        with open(colored_path, 'w') as f:
            f.write(colored_svg)
        
        return str(colored_path)
    
    def _apply_solid_color(self, svg_content: str, color: str) -> str:
        """Apply solid emotion color to SVG"""
        # Replace black fills with emotion color
        svg_content = re.sub(r'fill="#000000?"', f'fill="{color}"', svg_content)
        svg_content = re.sub(r'fill="black"', f'fill="{color}"', svg_content)
        svg_content = re.sub(r'stroke="#000000?"', f'stroke="{color}"', svg_content)
        svg_content = re.sub(r'stroke="black"', f'stroke="{color}"', svg_content)
        
        return svg_content
    
    def _apply_gradient_color(self, svg_content: str, color_palette: Dict) -> str:
        """Apply gradient using emotion colors"""
        
        # Create gradient definition
        gradient_id = "emotionGradient"
        gradient_def = f'''
        <defs>
            <linearGradient id="{gradient_id}" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:{color_palette['primary']};stop-opacity:1" />
                <stop offset="50%" style="stop-color:{color_palette['gradient']};stop-opacity:1" />
                <stop offset="100%" style="stop-color:{color_palette['secondary']};stop-opacity:1" />
            </linearGradient>
        </defs>'''
        
        # Insert gradient definition
        if '<defs>' in svg_content:
            svg_content = svg_content.replace('<defs>', f'<defs>{gradient_def}')
        else:
            svg_content = svg_content.replace('<svg', f'<svg>{gradient_def}<svg')
        
        # Apply gradient to fills
        svg_content = re.sub(r'fill="#000000?"', f'fill="url(#{gradient_id})"', svg_content)
        svg_content = re.sub(r'fill="black"', f'fill="url(#{gradient_id})"', svg_content)
        
        return svg_content
    
    def _apply_emotional_blend(self, svg_content: str, emotion_analysis: Dict) -> str:
        """Apply complex emotional color blending"""
        
        primary_color = emotion_analysis["color_palette"]["primary"]
        secondary_color = emotion_analysis["color_palette"]["secondary"]
        
        # Create complex gradient with multiple stops
        gradient_id = "emotionalBlend"
        gradient_def = f'''
        <defs>
            <radialGradient id="{gradient_id}" cx="50%" cy="50%" r="50%">
                <stop offset="0%" style="stop-color:{primary_color};stop-opacity:0.9" />
                <stop offset="70%" style="stop-color:{secondary_color};stop-opacity:0.7" />
                <stop offset="100%" style="stop-color:{emotion_analysis["color_palette"]["dark"]};stop-opacity:1" />
            </radialGradient>
        </defs>'''
        
        # Insert gradient
        if '<defs>' in svg_content:
            svg_content = svg_content.replace('<defs>', f'<defs>{gradient_def}')
        else:
            svg_content = svg_content.replace('<svg', f'<svg>{gradient_def}<svg')
        
        # Apply gradient
        svg_content = re.sub(r'fill="#000000?"', f'fill="url(#{gradient_id})"', svg_content)
        svg_content = re.sub(r'fill="black"', f'fill="url(#{gradient_id})"', svg_content)
        
        return svg_content
    
    def _apply_accent_color(self, svg_content: str, color_palette: Dict) -> str:
        """Apply accent coloring with black base"""
        
        # Keep most black, add emotion color as accent
        svg_content = re.sub(r'stroke="#000000?"', f'stroke="{color_palette["primary"]}"', svg_content)
        svg_content = re.sub(r'stroke="black"', f'stroke="{color_palette["primary"]}"', svg_content)
        
        # Add emotion color to specific elements (circles, highlights)
        if '<circle' in svg_content:
            svg_content = re.sub(r'(<circle[^>]*fill=")[^"]*(")', rf'\1{color_palette["primary"]}\2', svg_content)
        
        return svg_content
    
    def generate_emotion_color_test(self, text: str, svg_path: str) -> Dict:
        """Generate all color variations for testing"""
        
        print(f"🎨 Generating emotion-colored glyphs for: '{text[:50]}...'")
        
        # Analyze emotions
        emotion_analysis = self.analyze_text_emotions(text)
        dominant = emotion_analysis["dominant_emotion"]
        
        print(f"😊 Dominant emotion: {dominant.get('path', [dominant['core']])}")
        print(f"🎨 Primary color: {emotion_analysis['color_palette']['primary']}")
        
        # Generate all style variations
        styles = ["solid", "gradient", "emotional_blend", "accent"]
        generated_files = {}
        
        for style in styles:
            try:
                colored_path = self.colorize_svg(svg_path, emotion_analysis, style)
                generated_files[style] = colored_path
                print(f"✅ {style.title()} style: {Path(colored_path).name}")
            except Exception as e:
                print(f"❌ Failed to create {style} style: {e}")
                generated_files[style] = None
        
        return {
            "emotion_analysis": emotion_analysis,
            "generated_files": generated_files,
            "color_palette": emotion_analysis["color_palette"]
        }

# Create singleton instance
color_generator = ColorGlyphGenerator()

def colorize_glyph_by_emotion(text: str, svg_path: str, style: str = "gradient") -> str:
    """Quick function to colorize a glyph based on text emotion"""
    emotion_analysis = color_generator.analyze_text_emotions(text)
    return color_generator.colorize_svg(svg_path, emotion_analysis, style)

def test_emotion_colors(text: str, svg_path: str) -> Dict:
    """Test all emotion color styles on a glyph"""
    return color_generator.generate_emotion_color_test(text, svg_path)

if __name__ == "__main__":
    # Test with different emotional texts
    test_texts = [
        "I felt overwhelming joy and happiness dancing in the sunlight",
        "Deep sadness and melancholy filled my heart",
        "Terrifying fear gripped me in the dark forest",
        "Burning anger and fury consumed my thoughts",
        "Tender love and compassion warmed my soul",
        "Complete surprise and amazement at the discovery"
    ]
    
    print("🎨 Emotion Color Analysis Test")
    print("=" * 50)
    
    for text in test_texts:
        print(f"\n📝 Text: {text}")
        emotion_analysis = color_generator.analyze_text_emotions(text)
        dominant = emotion_analysis["dominant_emotion"]
        
        print(f"😊 Emotion: {dominant.get('path', [dominant['core']])}")
        print(f"🎨 Colors: {emotion_analysis['color_palette']['primary']} → {emotion_analysis['color_palette']['secondary']}") 