"""
SVG Processing Module
Handles all SVG-related operations including conversion, normalization, and color application.
"""

import os
import re
import tempfile
import subprocess
from pathlib import Path
from typing import Optional, Tuple, Union
import numpy as np
from PIL import Image
from scipy import ndimage

class SVGProcessor:
    def __init__(self, output_size: int = 256):
        """Initialize SVG processor with output size configuration."""
        self.output_size = output_size
        
    def convert_to_svg(self, image_path: Union[str, Path], output_path: Union[str, Path]) -> bool:
        """Convert image to SVG using optimized processing pipeline."""
        try:
            # Convert paths to Path objects
            image_path = Path(image_path)
            output_path = Path(output_path)
            
            # Load and preprocess image
            img = self._preprocess_image(image_path)
            if img is None:
                return False
            
            # Convert to binary image
            binary = self._create_binary_image(img)
            if binary is None:
                return False
            
            # Convert to SVG using potrace
            return self._potrace_convert(binary, output_path)
        
        except Exception as e:
            print(f"❌ Error converting to SVG: {e}")
            return False
    
    def apply_color(self, svg_path: Union[str, Path], output_path: Union[str, Path], color_hex: str) -> bool:
        """Apply color to SVG while maintaining shape integrity."""
        try:
            # Convert paths to Path objects
            svg_path = Path(svg_path)
            output_path = Path(output_path)
            
            with open(svg_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract path data
            path_match = re.search(r'<path[^>]*d="([^"]*)"[^>]*>', content)
            if not path_match:
                print(f"❌ Could not extract path data from SVG")
                return False
            
            # Create new SVG with color
            colored_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{self.output_size}" height="{self.output_size}" viewBox="0 0 {self.output_size} {self.output_size}" xmlns="http://www.w3.org/2000/svg">
  <g fill="{color_hex}" stroke="none">
    <path d="{path_match.group(1)}"/>
  </g>
</svg>'''
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(colored_svg)
            
            return True
            
        except Exception as e:
            print(f"❌ Error applying color: {e}")
            return False
    
    def normalize_svg(self, svg_path: Union[str, Path], output_path: Union[str, Path]) -> bool:
        """Normalize SVG for consistent display."""
        try:
            # Convert paths to Path objects
            svg_path = Path(svg_path)
            output_path = Path(output_path)
            
            with open(svg_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract path data
            path_matches = re.findall(r'<path[^>]*d="([^"]*)"[^>]*>', content)
            if not path_matches:
                print(f"❌ No path data found in SVG")
                return False
            
            # Create normalized SVG
            normalized_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{self.output_size}" height="{self.output_size}" viewBox="0 0 {self.output_size} {self.output_size}" xmlns="http://www.w3.org/2000/svg">
  <g fill="#000000" stroke="none">
'''
            
            for path_data in path_matches:
                clean_path = re.sub(r'\s+', ' ', path_data.strip())
                normalized_svg += f'    <path d="{clean_path}"/>\n'
            
            normalized_svg += '''  </g>
</svg>'''
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(normalized_svg)
            
            return True
            
        except Exception as e:
            print(f"❌ Error normalizing SVG: {e}")
            return False
    
    def _preprocess_image(self, image_path: Path) -> Optional[np.ndarray]:
        """Preprocess image for conversion."""
        try:
            # Load and resize image
            img = Image.open(image_path).convert('RGB')
            img = img.resize((512, 512), Image.Resampling.LANCZOS)
            
            # Convert to grayscale array
            img_array = np.array(img)
            gray = np.dot(img_array, [0.299, 0.587, 0.114])
            
            # Enhance contrast
            p2, p98 = np.percentile(gray, (2, 98))
            gray = np.clip((gray - p2) * (255.0 / (p98 - p2)), 0, 255)
            
            return gray
            
        except Exception as e:
            print(f"❌ Error preprocessing image: {e}")
            return None
    
    def _create_binary_image(self, gray: np.ndarray) -> Optional[np.ndarray]:
        """Create binary image using Otsu's method."""
        try:
            # Calculate Otsu's threshold
            hist, bins = np.histogram(gray.flatten(), 256, [0, 256])
            total = gray.size
            
            sum_total = np.sum(np.arange(256) * hist)
            sum_bg = weight_bg = 0
            max_variance = threshold = 0
            
            for i in range(256):
                weight_bg += hist[i]
                if weight_bg == 0:
                    continue
                
                weight_fg = total - weight_bg
                if weight_fg == 0:
                    break
                
                sum_bg += i * hist[i]
                mean_bg = sum_bg / weight_bg
                mean_fg = (sum_total - sum_bg) / weight_fg
                
                variance = weight_bg * weight_fg * (mean_bg - mean_fg) ** 2
                if variance > max_variance:
                    max_variance = variance
                    threshold = i
            
            # Create binary image
            binary = (gray > threshold).astype(np.uint8) * 255
            
            # Clean up binary image
            binary = ndimage.binary_fill_holes(binary).astype(np.uint8) * 255
            binary = ndimage.binary_opening(binary, iterations=1).astype(np.uint8) * 255
            binary = ndimage.binary_closing(binary, iterations=1).astype(np.uint8) * 255
            
            # Invert to make glyph black on white
            binary = 255 - binary
            
            return binary
            
        except Exception as e:
            print(f"❌ Error creating binary image: {e}")
            return None
    
    def _potrace_convert(self, binary: np.ndarray, output_path: Path) -> bool:
        """Convert binary image to SVG using potrace."""
        try:
            # Save as temporary PBM
            temp_pbm = tempfile.NamedTemporaryFile(suffix='.pbm', delete=False)
            Image.fromarray(binary).save(temp_pbm.name, 'PPM')
            
            # Convert using potrace
            cmd = [
                'potrace',
                temp_pbm.name,
                '-s',                # SVG output
                '-k', '0.5',        # Corner threshold
                '-t', '5',          # Optimization tolerance
                '-a', '1',          # Corner alignment
                '-O', '1.0',        # Optimize paths
                '--tight',          # Remove whitespace
                '-o', str(output_path)
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            os.unlink(temp_pbm.name)
            
            # Verify output
            if output_path.exists():
                with open(output_path, 'r') as f:
                    content = f.read()
                if '<path' not in content:
                    print("❌ Generated SVG has no path data")
                    return False
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error in potrace conversion: {e}")
            return False 