#!/usr/bin/env python3
"""
gGlyph Batch Generator
Generate comprehensive gGlyph codex with multiple formats for each symbol
"""
import json
import sys
import os
from pathlib import Path
from datetime import datetime
import replicate
from dotenv import load_dotenv

# Add emotion processor to path
sys.path.append('data/emotions')

# Import our existing functions
from test_bw_meru import convert_to_bw_svg
from test_emotion_coloring import analyze_emotion_colors, colorize_svg_gradient

# Load environment
load_dotenv()

class GGlyphBatchGenerator:
    """Generate batches of gGlyphs for the symbol codex"""
    
    def __init__(self, codex_dir="results/gGlyphs_codex"):
        self.codex_dir = Path(codex_dir)
        self.webp_dir = self.codex_dir / "webp"
        self.svg_bw_dir = self.codex_dir / "svg_bw" 
        self.svg_colored_dir = self.codex_dir / "svg_colored"
        self.metadata_dir = self.codex_dir / "metadata"
        
        # MERU model for generation
        self.meru_model = "conorbyrnes04/meru:86bcf689d994c5ebec0c93fe6bf2a15abe067850f78607ebd46c9f0f46418d24"
        
        # Create progress tracking
        self.progress_file = self.metadata_dir / "generation_progress.json"
        self.load_progress()
    
    def load_progress(self):
        """Load generation progress to resume if interrupted"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                self.progress = json.load(f)
        else:
            self.progress = {"completed": [], "failed": [], "current_batch": None}
    
    def save_progress(self):
        """Save current progress"""
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)
    
    def generate_meru_webp(self, prompt, symbol_name):
        """Generate WebP using MERU model"""
        
        print(f"🎨 Generating MERU WebP for {symbol_name}...")
        
        try:
            output = replicate.run(
                self.meru_model,
                input={
                    "prompt": prompt,
                    "model": "dev",
                    "go_fast": False,
                    "lora_scale": 1,
                    "megapixels": "1",
                    "num_outputs": 1,
                    "aspect_ratio": "1:1",
                    "output_format": "webp",
                    "guidance_scale": 3,
                    "output_quality": 90,
                    "prompt_strength": 0.8,
                    "extra_lora_scale": 1,
                    "num_inference_steps": 28
                }
            )
            
            if output and len(output) > 0:
                # Download and save WebP
                webp_filename = f"{symbol_name.lower()}.webp"
                webp_path = self.webp_dir / webp_filename
                
                with open(webp_path, 'wb') as f:
                    f.write(output[0].read())
                
                print(f"✅ WebP saved: {webp_filename}")
                return str(webp_path)
            else:
                print(f"❌ No output from MERU for {symbol_name}")
                return None
                
        except Exception as e:
            print(f"❌ MERU generation failed for {symbol_name}: {e}")
            return None
    
    def create_bw_svg(self, webp_path, symbol_name):
        """Convert WebP to B&W SVG using OTSU method"""
        
        print(f"🔄 Converting to B&W SVG: {symbol_name}")
        
        try:
            # Ensure webp_path is a Path object
            webp_path = Path(webp_path)
            
            # Use our existing OTSU conversion
            svg_result = convert_to_bw_svg(webp_path, method="otsu")
            
            if svg_result and svg_result.get("success"):
                # Move to codex directory with proper naming
                original_svg = Path(svg_result["svg_path"])
                new_svg_path = self.svg_bw_dir / f"{symbol_name.lower()}.svg"
                
                # Copy to codex directory
                with open(original_svg, 'r') as f:
                    svg_content = f.read()
                
                with open(new_svg_path, 'w') as f:
                    f.write(svg_content)
                
                print(f"✅ B&W SVG saved: {symbol_name.lower()}.svg")
                return str(new_svg_path)
            else:
                print(f"❌ SVG conversion failed for {symbol_name}")
                return None
                
        except Exception as e:
            print(f"❌ SVG conversion error for {symbol_name}: {e}")
            return None
    
    def create_colored_svg(self, bw_svg_path, symbol_name, meanings):
        """Create colored SVG based on symbol meanings"""
        
        print(f"🎨 Creating colored SVG: {symbol_name}")
        
        try:
            # Create emotion text from meanings for color analysis
            emotion_text = f"I feel {', '.join(meanings[:3]).lower()} energy"
            
            # Analyze emotions to get colors
            emotion_analysis = analyze_emotion_colors(emotion_text)
            
            # Read B&W SVG
            with open(bw_svg_path, 'r') as f:
                svg_content = f.read()
            
            # Apply gradient coloring
            colored_svg = colorize_svg_gradient(svg_content, emotion_analysis['color_palette'])
            
            # Save colored version
            colored_svg_path = self.svg_colored_dir / f"{symbol_name.lower()}_colored.svg"
            
            with open(colored_svg_path, 'w') as f:
                f.write(colored_svg)
            
            print(f"✅ Colored SVG saved: {symbol_name.lower()}_colored.svg")
            print(f"   Color: {emotion_analysis['color_palette']['primary']}")
            
            return {
                "path": str(colored_svg_path),
                "emotion_analysis": emotion_analysis
            }
            
        except Exception as e:
            print(f"❌ Colored SVG creation failed for {symbol_name}: {e}")
            return None
    
    def generate_symbol_set(self, symbol_data):
        """Generate complete set for one symbol (WebP + B&W SVG + Colored SVG)"""
        
        symbol_name = symbol_data["name"]
        
        print(f"\n🔥 Generating gGlyph: {symbol_name}")
        print("=" * 50)
        
        # Check if already completed
        if symbol_name in self.progress["completed"]:
            print(f"⏭️  {symbol_name} already completed, skipping...")
            return self.load_symbol_metadata(symbol_name)
        
        # Update current progress
        self.progress["current_batch"] = symbol_name
        self.save_progress()
        
        # Step 1: Generate WebP with MERU
        webp_path = self.generate_meru_webp(symbol_data["prompt"], symbol_name)
        if not webp_path:
            self.progress["failed"].append(symbol_name)
            self.save_progress()
            return None
        
        # Step 2: Create B&W SVG
        bw_svg_path = self.create_bw_svg(webp_path, symbol_name)
        if not bw_svg_path:
            self.progress["failed"].append(symbol_name)
            self.save_progress()
            return None
        
        # Step 3: Create Colored SVG
        colored_result = self.create_colored_svg(bw_svg_path, symbol_name, symbol_data["meanings"])
        if not colored_result:
            print("⚠️  Colored SVG failed, but continuing with B&W version")
            colored_result = {"path": None, "emotion_analysis": None}
        
        # Create metadata
        metadata = {
            "name": symbol_name,
            "category": symbol_data["category"],
            "subcategory": symbol_data["subcategory"],
            "meanings": symbol_data["meanings"],
            "prompt": symbol_data["prompt"],
            "files": {
                "webp": webp_path,
                "svg_bw": bw_svg_path,
                "svg_colored": colored_result["path"]
            },
            "emotion_analysis": colored_result["emotion_analysis"],
            "generated": datetime.now().isoformat(),
            "model": "meru",
            "version": "1.0"
        }
        
        # Save individual metadata
        metadata_file = self.metadata_dir / f"{symbol_name.lower()}_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Mark as completed
        self.progress["completed"].append(symbol_name)
        self.progress["current_batch"] = None
        self.save_progress()
        
        print(f"🎉 {symbol_name} generation complete!")
        print(f"   WebP: {Path(webp_path).name}")
        print(f"   B&W SVG: {Path(bw_svg_path).name}")
        if colored_result["path"]:
            print(f"   Colored SVG: {Path(colored_result['path']).name}")
        
        return metadata
    
    def load_symbol_metadata(self, symbol_name):
        """Load existing symbol metadata"""
        metadata_file = self.metadata_dir / f"{symbol_name.lower()}_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                return json.load(f)
        return None
    
    def batch_generate_from_json(self, json_file):
        """Generate complete gGlyph set from JSON symbol definitions"""
        
        print("🚀 gGlyph Batch Generator")
        print("=" * 60)
        
        # Load symbol definitions
        with open(json_file, 'r') as f:
            symbols = json.load(f)
        
        print(f"📊 Loading {len(symbols)} symbol definitions")
        print(f"📁 Output directory: {self.codex_dir}")
        print()
        
        # Process each symbol
        generated_metadata = []
        
        for i, symbol_data in enumerate(symbols, 1):
            print(f"\n📍 Progress: {i}/{len(symbols)}")
            
            try:
                metadata = self.generate_symbol_set(symbol_data)
                if metadata:
                    generated_metadata.append(metadata)
                
                # Brief pause between generations
                import time
                time.sleep(2)
                
            except KeyboardInterrupt:
                print(f"\n⏹️  Generation interrupted. Progress saved.")
                break
            except Exception as e:
                print(f"❌ Unexpected error for {symbol_data['name']}: {e}")
                self.progress["failed"].append(symbol_data["name"])
                self.save_progress()
                continue
        
        # Create master codex file
        codex_file = self.codex_dir / "gGlyph_codex.json"
        with open(codex_file, 'w') as f:
            json.dump({
                "codex_version": "1.0",
                "generated": datetime.now().isoformat(),
                "total_symbols": len(generated_metadata),
                "symbols": generated_metadata
            }, f, indent=2)
        
        # Final report
        print(f"\n🎉 BATCH GENERATION COMPLETE!")
        print("=" * 60)
        print(f"✅ Successfully generated: {len(self.progress['completed'])} symbols")
        print(f"❌ Failed: {len(self.progress['failed'])} symbols")
        if self.progress['failed']:
            print(f"   Failed symbols: {', '.join(self.progress['failed'])}")
        print(f"📄 Master codex: {codex_file}")
        print(f"📁 Files organized in: {self.codex_dir}")
        
        return generated_metadata

def main():
    """Main execution"""
    
    # Initialize generator
    generator = GGlyphBatchGenerator()
    
    # Run batch generation
    test_symbols_file = "results/gGlyphs_codex/test_symbols.json"
    
    if not Path(test_symbols_file).exists():
        print(f"❌ Symbol definitions not found: {test_symbols_file}")
        return
    
    generator.batch_generate_from_json(test_symbols_file)

if __name__ == "__main__":
    main() 