#!/usr/bin/env python3
"""
MYTHRA GLYPHNET - Fix Problem SVGs
Fix Earth and Shaman SVGs with unusual dimensions
"""

import re
from pathlib import Path

def fix_problem_svg(symbol_name: str):
    """Fix a single problematic SVG"""
    
    print(f"🔧 Fixing {symbol_name}...")
    
    # Paths
    svg_path = Path(f"results/gGlyphs_codex/archetypal_53/svg_normalized/{symbol_name.lower()}_graph.svg")
    
    # Read the problematic SVG
    with open(svg_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract all path data
    path_matches = re.findall(r'<path[^>]*d="([^"]*)"[^>]*>', content)
    
    if not path_matches:
        print(f"❌ No paths found in {symbol_name}")
        return False
    
    # Create a simple, normalized SVG
    fixed_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="256" height="256" viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg">
  <g fill="#000000" stroke="none">
'''
    
    # Add all paths with minimal scaling
    for path_data in path_matches:
        # Clean up the path data a bit
        clean_path = re.sub(r'\s+', ' ', path_data.strip())
        fixed_svg += f'    <path d="{clean_path}" transform="scale(0.3) translate(100, 100)"/>\n'
    
    fixed_svg += '''  </g>
</svg>'''
    
    # Write the fixed SVG
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(fixed_svg)
    
    print(f"✅ Fixed {symbol_name}")
    return True

def main():
    """Fix the problematic SVGs"""
    print("🔧 MYTHRA GLYPHNET - Problem SVG Fix")
    print("=" * 40)
    
    problem_symbols = ["Earth", "Shaman"]
    
    for symbol in problem_symbols:
        fix_problem_svg(symbol)
    
    print("\n🎉 Problem SVGs fixed!")
    print("🌟 Test them at: http://localhost:8003/test_svg_display.html")

if __name__ == "__main__":
    main() 