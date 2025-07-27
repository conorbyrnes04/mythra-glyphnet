"""
Archetypal Glyph Generator
Handles generation and processing of archetypal glyphs.
"""

import json
from pathlib import Path
from typing import Dict, Optional
from PIL import Image
import numpy as np

from ..utils.model_interface import get_model
from ..processors.svg import SVGProcessor

def convert_to_transparent(input_path: Path, output_path: Path = None, threshold: int = 30):
    """Convert PNG with black background to transparent background."""
    try:
        # Load the image
        img = Image.open(input_path)
        
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Convert to numpy array for processing
        data = np.array(img)
        
        # Create a mask for black pixels (background)
        # Check if R, G, B are all below threshold (black)
        black_mask = np.all(data[:, :, :3] <= threshold, axis=2)
        
        # Set alpha channel to 0 for black pixels (transparent)
        data[black_mask, 3] = 0
        
        # Convert back to PIL Image
        transparent_img = Image.fromarray(data)
        
        # Save with transparent background
        if output_path is None:
            output_path = input_path
        
        transparent_img.save(output_path, 'PNG')
        
        print(f"✅ Converted to transparent background: {output_path.name}")
        return output_path
        
    except Exception as e:
        print(f"❌ Error converting to transparent: {e}")
        return None

class ArchetypalGenerator:
    def __init__(self, base_path: Path = Path("assets/glyphs/archetypal"), model_name: str = "meru"):
        """Initialize archetypal glyph generator."""
        self.base_path = base_path
        self.png_path = base_path / "png"  # Changed to PNG directory
        self.svg_path = base_path / "svg"
        self.colored_path = base_path / "colored"
        self.metadata_path = Path("assets/metadata")
        
        # Ensure directories exist
        self.png_path.mkdir(parents=True, exist_ok=True)  # Changed to PNG
        self.svg_path.mkdir(parents=True, exist_ok=True)
        self.colored_path.mkdir(parents=True, exist_ok=True)
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize components with flexible model selection
        self.model = get_model(model_name)
        self.svg_processor = SVGProcessor()
        
        print(f"🎨 Archetypal Glyph Generator initialized with {model_name.upper()} model")
    
    def generate_glyph(self, name: str, meaning: str = "", interpretation: str = "", 
                      emotion_hex: str = "#000000", style: str = None) -> bool:
        """Generate a complete archetypal glyph with all variants."""
        try:
            name_lower = name.lower().replace(' ', '_')
            
            # Generate paths - use PNG instead of WebP
            png_file = self.png_path / f"{name_lower}.png"  # Changed to PNG
            svg_file = self.svg_path / f"{name_lower}.svg"
            colored_file = self.colored_path / f"{name_lower}_colored.svg"
            metadata_file = self.metadata_path / f"{name_lower}.json"
            
            # Create prompt based on model type
            if hasattr(self.model, 'create_celtic_prompt') and style:
                prompt = self.model.create_celtic_prompt(name, style, meaning, interpretation)
            else:
                prompt = self.model.create_archetypal_prompt(name, meaning, interpretation)
            
            if not self.model.generate_glyph(prompt, png_file):
                return False
            
            # Convert to transparent background
            print(f"🎨 Converting to transparent background...")
            transparent_file = convert_to_transparent(png_file)
            
            if transparent_file:
                # Use the transparent version
                png_file = transparent_file
                print(f"✅ Using transparent PNG for better force graph display")
            else:
                print(f"⚠️ Using original PNG (transparency conversion failed)")
            
            # Create a simple colored version (optional)
            colored_file = png_file  # Use PNG as colored version too
            
            # Save metadata
            metadata = {
                "name": name,
                "meaning": meaning,
                "interpretation": interpretation,
                "emotion_hex": emotion_hex,
                "model_used": self.model.__class__.__name__,
                "style": style if style else "default",
                "files": {
                    "png": str(png_file),  # Changed to PNG
                    "svg": str(svg_file),
                    "colored": str(colored_file)
                }
            }
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"✅ Successfully generated {name} glyph")
            return True
            
        except Exception as e:
            print(f"❌ Error generating {name} glyph: {e}")
            return False
    
    def generate_celtic_glyph(self, name: str, style: str = "celtic", meaning: str = "", 
                            interpretation: str = "", emotion_hex: str = "#FFD700") -> bool:
        """Generate a Celtic-style glyph with specific style."""
        try:
            name_lower = name.lower().replace(' ', '_')
            
            # Generate paths - use PNG instead of WebP
            png_file = self.png_path / f"{name_lower}.png"  # Changed to PNG
            svg_file = self.svg_path / f"{name_lower}.svg"
            colored_file = self.colored_path / f"{name_lower}_colored.svg"
            metadata_file = self.metadata_path / f"{name_lower}.json"
            
            # Create Celtic prompt
            if hasattr(self.model, 'create_celtic_prompt'):
                prompt = self.model.create_celtic_prompt(name, style, meaning, interpretation)
            else:
                # Fallback to regular prompt if Celtic interface not available
                prompt = self.model.create_archetypal_prompt(name, meaning, interpretation)
            
            if not self.model.generate_glyph(prompt, png_file):
                return False
            
            # Convert to transparent background
            print(f"🎨 Converting to transparent background...")
            transparent_file = convert_to_transparent(png_file)
            
            if transparent_file:
                # Use the transparent version
                png_file = transparent_file
                print(f"✅ Using transparent PNG for better force graph display")
            else:
                print(f"⚠️ Using original PNG (transparency conversion failed)")
            
            # Create a simple colored version (optional)
            # For now, we'll skip this since PNGs work better
            colored_file = png_file  # Use PNG as colored version too
            
            # Save metadata
            metadata = {
                "name": name,
                "meaning": meaning,
                "interpretation": interpretation,
                "emotion_hex": emotion_hex,
                "model_used": self.model.__class__.__name__,
                "style": f"celtic_{style}",
                "files": {
                    "png": str(png_file),  # Changed to PNG
                    "svg": str(svg_file),
                    "colored": str(colored_file)
                }
            }
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"✅ Successfully generated Celtic {name} glyph")
            return True
            
        except Exception as e:
            print(f"❌ Error generating Celtic {name} glyph: {e}")
            return False
    
    def repair_glyph(self, name: str) -> bool:
        """Repair existing glyph's SVG and colored versions."""
        try:
            name_lower = name.lower().replace(' ', '_')
            
            # Get file paths
            png_file = self.png_path / f"{name_lower}.png"  # Changed to PNG
            svg_file = self.svg_path / f"{name_lower}.svg"
            colored_file = self.colored_path / f"{name_lower}_colored.svg"
            metadata_file = self.metadata_path / f"{name_lower}.json"
            
            if not png_file.exists():
                print(f"❌ PNG file not found for {name}")
                return False
            
            # Load metadata for color information
            if metadata_file.exists():
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                emotion_hex = metadata.get('emotion_hex', '#000000')
            else:
                emotion_hex = '#000000'
            
            # For PNG files, we don't need SVG conversion
            print(f"✅ PNG file exists and is ready for use: {png_file}")
            
            # Create a simple colored version (optional)
            colored_file = png_file  # Use PNG as colored version too
            
            print(f"✅ Successfully repaired {name} glyph")
            return True
            
        except Exception as e:
            print(f"❌ Error repairing {name} glyph: {e}")
            return False
    
    def get_glyph_info(self, name: str) -> Optional[Dict]:
        """Get information about a glyph."""
        try:
            name_lower = name.lower().replace(' ', '_')
            metadata_file = self.metadata_path / f"{name_lower}.json"
            
            if not metadata_file.exists():
                return None
            
            with open(metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception:
            return None
    
    def switch_model(self, model_name: str):
        """Switch to a different AI model."""
        try:
            self.model = get_model(model_name)
            print(f"🔄 Switched to {model_name.upper()} model")
        except Exception as e:
            print(f"❌ Error switching model: {e}")
    
    def list_available_models(self):
        """List all available models."""
        from ..utils.model_interface import MODEL_REGISTRY
        print("\n🤖 Available Models:")
        for name, model_class in MODEL_REGISTRY.items():
            print(f"  - {name}: {model_class.__name__}")
        print(f"  Current model: {self.model.__class__.__name__}")
    
    def list_celtic_styles(self):
        """List available Celtic styles."""
        print("\n🎨 Available Celtic Styles:")
        print("  - celtic: Celtic ritual symbols with knotwork and spirals")
        print("  - gold_on_black: Ancient ritual symbols with sacred geometry") 