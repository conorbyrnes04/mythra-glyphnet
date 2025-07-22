#!/usr/bin/env python3
"""
MYTHRA GLYPHNET - Archetypal Codex Generator
Generate the complete set of 53 archetypal symbols with all SVG variants
"""

import json
import sys
import os
import time
from pathlib import Path
import replicate
from datetime import datetime
import tempfile
import subprocess
import urllib.request
import re
from typing import Dict, List, Tuple, Optional

# Import our existing conversion functions
sys.path.append('.')
from test_bw_meru import convert_to_bw_svg

class ArchetypalCodexGenerator:
    def __init__(self):
        self.base_dir = Path("results/gGlyphs_codex/archetypal_53")
        self.codex_file = Path("results/gGlyphs_codex/archetypal_symbol_codex_complete.json")
        
        # Directories for different formats
        self.webp_dir = self.base_dir / "webp"
        self.svg_bw_dir = self.base_dir / "svg_bw" 
        self.svg_normalized_dir = self.base_dir / "svg_normalized"
        self.svg_colored_dir = self.base_dir / "svg_colored"
        
        # Create directories
        for dir_path in [self.webp_dir, self.svg_bw_dir, self.svg_normalized_dir, self.svg_colored_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # MERU Model
        self.MERU_MODEL = "conorbyrnes04/meru:86bcf689d994c5ebec0c93fe6bf2a15abe067850f78607ebd46c9f0f46418d24"
        
        # Load existing symbols to skip
        self.existing_symbols = self.get_existing_symbols()
        
        print(f"🎨 MYTHRA GLYPHNET - Archetypal Codex Generator")
        print(f"📁 Output directory: {self.base_dir}")
        print(f"🔍 Found {len(self.existing_symbols)} existing symbols")
    
    def get_existing_symbols(self) -> set:
        """Get list of symbols that already exist"""
        existing = set()
        
        # Check webp directory for existing files
        if self.webp_dir.exists():
            for file in self.webp_dir.glob("*.webp"):
                symbol_name = file.stem
                existing.add(symbol_name.lower())
        
        return existing
    
    def load_codex(self) -> List[Dict]:
        """Load the archetypal symbol codex"""
        try:
            with open(self.codex_file, 'r') as f:
                codex = json.load(f)
            print(f"📖 Loaded {len(codex)} symbols from codex")
            return codex
        except Exception as e:
            print(f"❌ Error loading codex: {e}")
            return []
    
    def get_remaining_symbols(self, codex: List[Dict]) -> List[Dict]:
        """Get symbols that haven't been generated yet"""
        remaining = []
        
        for symbol in codex:
            symbol_name = symbol['name'].lower()
            if symbol_name not in self.existing_symbols:
                remaining.append(symbol)
            else:
                print(f"⏭️  Skipping {symbol['name']} (already exists)")
        
        print(f"🎯 {len(remaining)} symbols remaining to generate")
        return remaining
    
    def generate_single_symbol(self, symbol: Dict) -> bool:
        """Generate a single symbol with all variants"""
        symbol_name = symbol['name']
        symbol_lower = symbol_name.lower()
        prompt = symbol['prompt']
        emotion_hex = symbol['emotion_hex']
        
        print(f"\n🎨 Generating {symbol_name}...")
        print(f"📝 Prompt: {prompt[:100]}...")
        
        try:
            # Step 1: Generate WebP with MERU
            print(f"🤖 Calling MERU model...")
            start_time = time.time()
            
            output = replicate.run(
                self.MERU_MODEL,
                input={
                    "prompt": prompt,
                    "guidance": 3.5,
                    "num_outputs": 1,
                    "aspect_ratio": "1:1",
                    "output_format": "webp",
                    "output_quality": 80,
                    "num_inference_steps": 28
                }
            )
            
            generation_time = time.time() - start_time
            print(f"⚡ Generated in {generation_time:.1f}s")
            
            if not output or len(output) == 0:
                print(f"❌ No output received from MERU for {symbol_name}")
                return False
            
            # Step 2: Download WebP
            webp_url = output[0].url
            webp_path = self.webp_dir / f"{symbol_lower}.webp"
            
            print(f"⬇️  Downloading WebP...")
            urllib.request.urlretrieve(webp_url, webp_path)
            print(f"✅ WebP saved: {webp_path}")
            
            # Step 3: Convert to B&W SVG using OTSU method
            print(f"🔄 Converting to B&W SVG...")
            svg_result = convert_to_bw_svg(webp_path, method="otsu")
            
            if svg_result["success"] and Path(svg_result["svg_path"]).exists():
                # Move to our organized directory
                target_svg_path = self.svg_bw_dir / f"{symbol_lower}.svg"
                Path(svg_result["svg_path"]).rename(target_svg_path)
                print(f"✅ B&W SVG saved: {target_svg_path}")
                
                # Step 4: Create normalized version for graph
                normalized_path = self.create_normalized_svg(target_svg_path, symbol_lower)
                
                # Step 5: Create colored version
                colored_path = self.create_colored_svg(target_svg_path, symbol_lower, emotion_hex)
                
                return True
            else:
                error_msg = svg_result.get("error", "Unknown SVG conversion error")
                print(f"❌ Failed to convert {symbol_name} to SVG: {error_msg}")
                return False
                
        except Exception as e:
            print(f"❌ Error generating {symbol_name}: {e}")
            return False
    
    def create_normalized_svg(self, source_svg_path: Path, symbol_name: str) -> Optional[Path]:
        """Create normalized SVG for graph display"""
        try:
            normalized_path = self.svg_normalized_dir / f"{symbol_name}_graph.svg"
            
            with open(source_svg_path, 'r') as f:
                svg_content = f.read()
            
            # Properly normalize by keeping the original viewBox but setting standard dimensions
            normalized_svg = re.sub(
                r'<svg[^>]*>',
                '<svg width="100" height="100" viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg">',
                svg_content,
                count=1
            )
            
            # Clean up XML declarations
            normalized_svg = re.sub(r'<\?xml[^>]*\?>\s*', '', normalized_svg)
            normalized_svg = re.sub(r'<!DOCTYPE[^>]*>\s*', '', normalized_svg)
            
            # Add clean XML declaration
            clean_svg = '<?xml version="1.0" encoding="UTF-8"?>\n' + normalized_svg
            
            with open(normalized_path, 'w') as f:
                f.write(clean_svg)
            
            print(f"✅ Normalized SVG: {normalized_path}")
            return normalized_path
            
        except Exception as e:
            print(f"❌ Error creating normalized SVG for {symbol_name}: {e}")
            return None
    
    def create_colored_svg(self, source_svg_path: Path, symbol_name: str, emotion_hex: str) -> Optional[Path]:
        """Create emotion-colored SVG"""
        try:
            colored_path = self.svg_colored_dir / f"{symbol_name}_colored.svg"
            
            with open(source_svg_path, 'r') as f:
                svg_content = f.read()
            
            # Replace black fill with emotion color
            colored_svg = svg_content.replace('fill="#000000"', f'fill="{emotion_hex}"')
            colored_svg = colored_svg.replace('fill="black"', f'fill="{emotion_hex}"')
            colored_svg = colored_svg.replace('fill="#000"', f'fill="{emotion_hex}"')
            
            with open(colored_path, 'w') as f:
                f.write(colored_svg)
            
            print(f"✅ Colored SVG ({emotion_hex}): {colored_path}")
            return colored_path
            
        except Exception as e:
            print(f"❌ Error creating colored SVG for {symbol_name}: {e}")
            return None
    
    def generate_batch(self, symbols: List[Dict], batch_size: int = 5) -> Dict:
        """Generate symbols in batches with progress tracking"""
        total_symbols = len(symbols)
        successful = []
        failed = []
        
        print(f"\n🚀 Starting batch generation of {total_symbols} symbols")
        print(f"📦 Batch size: {batch_size}")
        
        for i in range(0, total_symbols, batch_size):
            batch = symbols[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (total_symbols + batch_size - 1) // batch_size
            
            print(f"\n🔄 Batch {batch_num}/{total_batches} ({len(batch)} symbols)")
            print("=" * 50)
            
            for j, symbol in enumerate(batch):
                symbol_num = i + j + 1
                print(f"\n[{symbol_num}/{total_symbols}] {symbol['name']}")
                
                success = self.generate_single_symbol(symbol)
                
                if success:
                    successful.append(symbol['name'])
                    print(f"✅ {symbol['name']} completed successfully")
                else:
                    failed.append(symbol['name'])
                    print(f"❌ {symbol['name']} failed")
                
                # Brief pause between symbols to avoid rate limits
                if j < len(batch) - 1:
                    print("⏱️  Pausing 3 seconds...")
                    time.sleep(3)
            
            # Longer pause between batches
            if i + batch_size < total_symbols:
                print(f"\n⏸️  Batch {batch_num} complete. Pausing 10 seconds before next batch...")
                time.sleep(10)
        
        return {
            'successful': successful,
            'failed': failed,
            'total': total_symbols
        }
    
    def create_summary_report(self, results: Dict) -> str:
        """Create a summary report of the generation process"""
        successful = results['successful']
        failed = results['failed']
        total = results['total']
        
        report = f"""
🎨 ARCHETYPAL CODEX GENERATION REPORT
{'=' * 50}

📊 STATISTICS:
  • Total symbols: {total}
  • Successful: {len(successful)} ({len(successful)/total*100:.1f}%)
  • Failed: {len(failed)} ({len(failed)/total*100:.1f}%)

✅ SUCCESSFUL GENERATIONS:
"""
        
        for symbol in successful:
            report += f"  • {symbol}\n"
        
        if failed:
            report += f"\n❌ FAILED GENERATIONS:\n"
            for symbol in failed:
                report += f"  • {symbol}\n"
        
        report += f"""
📁 OUTPUT DIRECTORIES:
  • WebP: {self.webp_dir}
  • B&W SVG: {self.svg_bw_dir}
  • Graph SVG: {self.svg_normalized_dir}
  • Colored SVG: {self.svg_colored_dir}

🎯 NEXT STEPS:
  1. Review failed generations and retry if needed
  2. Update the symbol graph with new symbols
  3. Test the graph display at: http://localhost:8001/archetypal_53/
  
🌟 Generation complete!
"""
        
        # Save report to file
        report_file = self.base_dir / "generation_report.txt"
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(report)
        print(f"📄 Report saved: {report_file}")
        
        return report

def main():
    """Main execution"""
    print("🎨 MYTHRA GLYPHNET - Archetypal Codex Generator")
    print("=" * 60)
    
    # Initialize generator
    generator = ArchetypalCodexGenerator()
    
    # Load codex
    codex = generator.load_codex()
    if not codex:
        print("❌ Failed to load codex. Exiting.")
        return
    
    # Get remaining symbols
    remaining_symbols = generator.get_remaining_symbols(codex)
    
    if not remaining_symbols:
        print("🎉 All symbols already generated!")
        return
    
    # Confirm generation
    print(f"\n🔍 SYMBOLS TO GENERATE:")
    for i, symbol in enumerate(remaining_symbols, 1):
        print(f"  {i:2d}. {symbol['name']} ({symbol['category']}/{symbol['subcategory']})")
    
    confirm = input(f"\n🚀 Generate {len(remaining_symbols)} symbols? (y/N): ").strip().lower()
    if confirm != 'y':
        print("⏹️  Generation cancelled.")
        return
    
    # Generate all symbols
    start_time = time.time()
    results = generator.generate_batch(remaining_symbols, batch_size=3)
    total_time = time.time() - start_time
    
    # Create summary report
    print(f"\n⏱️  Total generation time: {total_time/60:.1f} minutes")
    generator.create_summary_report(results)
    
    print("🎉 Archetypal codex generation complete!")

if __name__ == "__main__":
    main()