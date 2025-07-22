#!/usr/bin/env python3
"""
SVG Normalizer for Graph Display
Standardize gGlyph SVGs for consistent graph node sizing
"""
import re
import xml.etree.ElementTree as ET
from pathlib import Path
import json

class SVGNormalizer:
    """Normalize SVG glyphs for graph visualization"""
    
    def __init__(self, target_size=100, padding=10):
        self.target_size = target_size  # Target canvas size
        self.padding = padding  # Internal padding
        self.content_size = target_size - (padding * 2)  # Actual content area
    
    def parse_viewbox(self, svg_content):
        """Extract viewBox dimensions from SVG"""
        viewbox_match = re.search(r'viewBox="([^"]+)"', svg_content)
        if viewbox_match:
            values = viewbox_match.group(1).split()
            return {
                "x": float(values[0]),
                "y": float(values[1]), 
                "width": float(values[2]),
                "height": float(values[3])
            }
        return None
    
    def calculate_content_bounds(self, svg_content):
        """Calculate actual content bounds from path data"""
        
        # Extract all path data
        paths = re.findall(r'd="([^"]+)"', svg_content)
        
        if not paths:
            return None
        
        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')
        
        for path_data in paths:
            # Simple coordinate extraction (basic implementation)
            # Extract numbers that could be coordinates
            coords = re.findall(r'-?\d+\.?\d*', path_data)
            
            for i in range(0, len(coords)-1, 2):
                try:
                    x, y = float(coords[i]), float(coords[i+1])
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)
                except (ValueError, IndexError):
                    continue
        
        if min_x == float('inf'):
            return None
        
        return {
            "x": min_x,
            "y": min_y,
            "width": max_x - min_x,
            "height": max_y - min_y
        }
    
    def normalize_svg(self, svg_content, glyph_name):
        """Normalize SVG to standard size and centering"""
        
        print(f"🔧 Normalizing SVG: {glyph_name}")
        
        # Get current viewBox
        viewbox = self.parse_viewbox(svg_content)
        if not viewbox:
            print(f"   ⚠️  No viewBox found, using default")
            viewbox = {"x": 0, "y": 0, "width": 1000, "height": 1000}
        
        # Calculate scale to fit content in target size with padding
        scale_x = self.content_size / viewbox["width"]
        scale_y = self.content_size / viewbox["height"]
        scale = min(scale_x, scale_y)  # Maintain aspect ratio
        
        # Calculate centered position
        scaled_width = viewbox["width"] * scale
        scaled_height = viewbox["height"] * scale
        offset_x = (self.target_size - scaled_width) / 2
        offset_y = (self.target_size - scaled_height) / 2
        
        print(f"   📐 Original: {viewbox['width']:.0f}x{viewbox['height']:.0f}")
        print(f"   📐 Scale: {scale:.3f}, Offset: ({offset_x:.1f}, {offset_y:.1f})")
        
        # Create normalized SVG
        normalized_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{self.target_size}" height="{self.target_size}" 
     viewBox="0 0 {self.target_size} {self.target_size}" 
     xmlns="http://www.w3.org/2000/svg">
'''
        
        # Extract defs if present
        defs_match = re.search(r'(<defs>.*?</defs>)', svg_content, re.DOTALL)
        if defs_match:
            normalized_svg += f"  {defs_match.group(1)}\n"
        
        # Extract the main content (g elements and paths)
        content_pattern = r'<g[^>]*transform="([^"]*)"[^>]*>(.*?)</g>'
        content_match = re.search(content_pattern, svg_content, re.DOTALL)
        
        if content_match:
            original_transform = content_match.group(1)
            content = content_match.group(2)
            
            # Create new transform that centers and scales the content
            new_transform = f"translate({offset_x}, {offset_y}) scale({scale}) {original_transform}"
            
            # Get fill attribute
            fill_match = re.search(r'fill="([^"]*)"', svg_content)
            fill = fill_match.group(1) if fill_match else "url(#emotionGradient)"
            
            normalized_svg += f'''  <g transform="{new_transform}" fill="{fill}" stroke="none">
{content}
  </g>
</svg>'''
        else:
            # Fallback: just wrap all paths
            paths = re.findall(r'<path[^>]*d="[^"]*"[^>]*/?>', svg_content)
            
            fill_match = re.search(r'fill="([^"]*)"', svg_content)
            fill = fill_match.group(1) if fill_match else "url(#emotionGradient)"
            
            normalized_svg += f'  <g transform="translate({offset_x}, {offset_y}) scale({scale})" fill="{fill}" stroke="none">\n'
            
            for path in paths:
                normalized_svg += f"    {path}\n"
            
            normalized_svg += "  </g>\n</svg>"
        
        return normalized_svg
    
    def normalize_glyph_set(self, input_dir="results/gGlyphs_codex/svg_colored", 
                           output_dir="results/gGlyphs_codex/svg_normalized"):
        """Normalize all colored SVGs for graph display"""
        
        print("🎯 Normalizing gGlyph SVGs for Graph Display")
        print("=" * 50)
        
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        svg_files = list(input_path.glob("*_colored.svg"))
        
        if not svg_files:
            print("❌ No colored SVG files found!")
            return
        
        print(f"📊 Found {len(svg_files)} SVGs to normalize")
        print(f"🎯 Target size: {self.target_size}x{self.target_size}px")
        print()
        
        normalized_count = 0
        
        for svg_file in svg_files:
            try:
                # Read original SVG
                with open(svg_file, 'r') as f:
                    svg_content = f.read()
                
                # Extract glyph name
                glyph_name = svg_file.stem.replace('_colored', '')
                
                # Normalize
                normalized_svg = self.normalize_svg(svg_content, glyph_name)
                
                # Save normalized version
                output_file = output_path / f"{glyph_name}_graph.svg"
                with open(output_file, 'w') as f:
                    f.write(normalized_svg)
                
                print(f"   ✅ Saved: {output_file.name}")
                normalized_count += 1
                
            except Exception as e:
                print(f"   ❌ Failed to normalize {svg_file.name}: {e}")
        
        print(f"\n🎉 Normalized {normalized_count}/{len(svg_files)} SVGs")
        
        # Update graph data with normalized paths
        self.update_graph_data_paths(output_path)
        
        return normalized_count
    
    def update_graph_data_paths(self, normalized_dir):
        """Update graph data to use normalized SVG paths"""
        
        graph_data_file = Path("results/gGlyphs_codex/graph_data.json")
        
        if not graph_data_file.exists():
            return
        
        with open(graph_data_file, 'r') as f:
            graph_data = json.load(f)
        
        # Update SVG paths to normalized versions
        for node in graph_data["nodes"]:
            glyph_name = node["name"].lower()
            normalized_path = str(normalized_dir / f"{glyph_name}_graph.svg")
            node["svg_path_normalized"] = normalized_path
            node["svg_size"] = self.target_size
        
        # Save updated graph data
        with open(graph_data_file, 'w') as f:
            json.dump(graph_data, f, indent=2)
        
        print(f"📊 Updated graph data with normalized SVG paths")
    
    def create_size_comparison(self):
        """Create a comparison showing original vs normalized sizes"""
        
        comparison_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="800" height="400" viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="800" height="400" fill="#f8f9fa"/>
  
  <!-- Title -->
  <text x="400" y="30" text-anchor="middle" font-family="Arial" font-size="20" font-weight="bold">
    gGlyph SVG Normalization for Graph Display
  </text>
  
  <!-- Before section -->
  <text x="200" y="70" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">
    Before: Inconsistent Sizes
  </text>
  <rect x="50" y="80" width="300" height="120" fill="none" stroke="#ddd" stroke-width="2"/>
  
  <!-- After section -->
  <text x="600" y="70" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">
    After: Normalized {self.target_size}x{self.target_size}px
  </text>
  <rect x="450" y="80" width="300" height="120" fill="none" stroke="#ddd" stroke-width="2"/>
  
  <!-- Grid showing normalized nodes -->
  <text x="400" y="240" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">
    Graph Node Grid (All Same Visual Weight)
  </text>
  
  <!-- Node grid -->
  <g transform="translate(250, 260)">
    <!-- Grid background -->
    <rect width="300" height="120" fill="#f0f0f0" stroke="#ccc"/>
    
    <!-- Sample normalized nodes -->
    <circle cx="60" cy="30" r="15" fill="#ff6b6b" opacity="0.8"/>
    <circle cx="150" cy="30" r="15" fill="#4ecdc4" opacity="0.8"/>
    <circle cx="240" cy="30" r="15" fill="#45b7d1" opacity="0.8"/>
    
    <circle cx="60" cy="60" r="15" fill="#96ceb4" opacity="0.8"/>
    <circle cx="150" cy="60" r="15" fill="#feca57" opacity="0.8"/>
    <circle cx="240" cy="60" r="15" fill="#ff9ff3" opacity="0.8"/>
    
    <circle cx="60" cy="90" r="15" fill="#54a0ff" opacity="0.8"/>
    <circle cx="150" cy="90" r="15" fill="#5f27cd" opacity="0.8"/>
    <circle cx="240" cy="90" r="15" fill="#00d2d3" opacity="0.8"/>
    
    <!-- Connection lines -->
    <line x1="75" y1="30" x2="135" y2="30" stroke="#999" stroke-width="1"/>
    <line x1="165" y1="30" x2="225" y2="30" stroke="#999" stroke-width="1"/>
    <line x1="60" y1="45" x2="60" y2="75" stroke="#999" stroke-width="1"/>
    <line x1="150" y1="45" x2="150" y2="75" stroke="#999" stroke-width="1"/>
  </g>
  
  <!-- Technical specs -->
  <text x="50" y="220" font-family="Arial" font-size="12" fill="#666">
    • Consistent {self.target_size}x{self.target_size}px canvas
  </text>
  <text x="50" y="205" font-family="Arial" font-size="12" fill="#666">
    • {self.padding}px internal padding
  </text>
</svg>'''
        
        with open("results/gGlyphs_codex/normalization_guide.svg", 'w') as f:
            f.write(comparison_svg)
        
        print("📋 Created normalization guide: results/gGlyphs_codex/normalization_guide.svg")

def main():
    """Main execution"""
    
    # Create normalizer with 100px target (good for graph nodes)
    normalizer = SVGNormalizer(target_size=100, padding=10)
    
    # Normalize all glyphs
    normalized_count = normalizer.normalize_glyph_set()
    
    # Create comparison guide
    normalizer.create_size_comparison()
    
    print(f"\n🎯 SVG Normalization Complete!")
    print(f"   Normalized: {normalized_count} glyphs")
    print(f"   Target size: 100x100px (optimal for graph nodes)")
    print(f"   Output: results/gGlyphs_codex/svg_normalized/")

if __name__ == "__main__":
    main() 