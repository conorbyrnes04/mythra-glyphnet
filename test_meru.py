#!/usr/bin/env python3
"""
MERU Model Testing & Integration
Test the new MERU model and save results to integrated database
"""
import os
import replicate
from datetime import datetime
from pathlib import Path
import requests
from dotenv import load_dotenv
import yaml
import subprocess
from PIL import Image, ImageOps
import tempfile
import json

# Load environment
load_dotenv()

# Import our integration
from database.glyph_integration import glyph_db, add_generated_glyph

# MERU Model Configuration
MERU_MODEL = "conorbyrnes04/meru:86bcf689d994c5ebec0c93fe6bf2a15abe067850f78607ebd46c9f0f46418d24"
TRIGGER_WORD = "meru"

# Test prompt categories
TEST_PROMPTS = {
    "elements": [
        f"{TRIGGER_WORD} fire element with flowing energy in mystical line art style",
        f"{TRIGGER_WORD} water spirit symbol with flowing curves",
        f"{TRIGGER_WORD} earth mountain wisdom in sacred geometry",
        f"{TRIGGER_WORD} air wind patterns in circular form"
    ],
    "sacred": [
        f"{TRIGGER_WORD} sacred tree of life symbol",
        f"{TRIGGER_WORD} serpent in ouroboros circle",
        f"{TRIGGER_WORD} lotus flower geometric pattern",
        f"{TRIGGER_WORD} spiral galaxy energy form"
    ],
    "nature": [
        f"{TRIGGER_WORD} sun rays with mystical energy",
        f"{TRIGGER_WORD} crescent moon with stars",
        f"{TRIGGER_WORD} mountain peak in minimalist style",
        f"{TRIGGER_WORD} ocean wave pattern"
    ],
    "concepts": [
        f"{TRIGGER_WORD} wisdom eye symbol",
        f"{TRIGGER_WORD} strength pillar geometric",
        f"{TRIGGER_WORD} peace dove in line art",
        f"{TRIGGER_WORD} transformation butterfly"
    ]
}

def convert_to_svg(webp_path: Path, svg_path: Path = None) -> dict:
    """Convert WebP/PNG to SVG using OTSU method (optimized default)"""
    
    if svg_path is None:
        svg_path = webp_path.parent / f"{webp_path.stem}.svg"
    
    print(f"🔄 Converting to SVG: {webp_path.name} (OTSU method)")
    
    try:
        # Check if potrace is available
        subprocess.run(['potrace', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {
            "success": False, 
            "error": "Potrace not found. Install with: brew install potrace"
        }
    
    try:
        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Preprocess image for better SVG conversion
            with Image.open(webp_path) as img:
                # Convert to RGB if needed
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'RGBA':
                        background.paste(img, mask=img.split()[-1])
                    else:
                        background.paste(img)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Enhance contrast and convert to B&W
                img = ImageOps.autocontrast(img)
                img_gray = ImageOps.grayscale(img)
                img_bw = img_gray.point(lambda x: 0 if x < 128 else 255, '1')
                
                # Save as BMP for potrace
                temp_bmp = temp_path / "temp.bmp"
                img_bw.save(temp_bmp, 'BMP')
            
            # Run potrace to convert to SVG
            cmd = [
                'potrace',
                str(temp_bmp),
                '-s',  # SVG output
                '-o', str(svg_path),
                '--tight',  # Tight bounding box
                '--turnpolicy', 'minority',
                '--alphamax', '1.0',
                '--opttolerance', '0.2'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            print(f"✅ SVG created: {svg_path}")
            
            return {
                "success": True,
                "webp_path": str(webp_path),
                "svg_path": str(svg_path),
                "file_size": svg_path.stat().st_size
            }
            
    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "error": f"Potrace conversion failed: {e.stderr}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"SVG conversion error: {str(e)}"
        }

def test_meru_model(prompt: str, save_to_db: bool = True) -> dict:
    """Test MERU model with a single prompt"""
    print(f"🎨 Generating: {prompt}")
    
    try:
        # Generate with MERU using correct schema
        output = replicate.run(
            MERU_MODEL,
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
                "output_quality": 80,
                "prompt_strength": 0.8,
                "extra_lora_scale": 1,
                "num_inference_steps": 28
            }
        )
        
        # Handle new output format with FileOutput objects
        if output and len(output) > 0:
            # Check if output has url property (FileOutput) or is direct URL
            if hasattr(output[0], 'url'):
                image_url = str(output[0].url)  # url is a property, not method
                image_data = output[0].read()
            else:
                # Fallback: treat as URL string
                image_url = str(output[0])
                response = requests.get(image_url)
                response.raise_for_status()
                image_data = response.content
        else:
            raise Exception("No output generated")
        
        # Extract name from prompt (first few words after trigger)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name_parts = prompt.replace(TRIGGER_WORD, "").strip().split()[:3]
        name = "_".join(name_parts).replace(" ", "_")
        
        filename = f"meru_{name}_{timestamp}.webp"
        filepath = Path("results/glyphs") / filename
        
        # Ensure directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Save image data directly
        with open(filepath, 'wb') as f:
            f.write(image_data)
        
        print(f"✅ Saved: {filepath}")
        
        # Convert to SVG
        svg_result = convert_to_svg(filepath)
        svg_path = None
        
        if svg_result["success"]:
            svg_path = svg_result["svg_path"]
            print(f"🎨 SVG created: {svg_path}")
        else:
            print(f"⚠️  SVG conversion failed: {svg_result['error']}")
        
        # Enhanced metadata with SVG info
        metadata = {
            "original_url": image_url,
            "generation_time": datetime.now().isoformat(),
            "model_version": MERU_MODEL,
            "webp_path": str(filepath),
            "svg_path": svg_path,
            "svg_conversion": svg_result,
            "parameters": {
                "model": "dev",
                "go_fast": False,
                "lora_scale": 1,
                "megapixels": "1",
                "aspect_ratio": "1:1",
                "output_format": "webp",
                "guidance_scale": 3,
                "output_quality": 80,
                "prompt_strength": 0.8,
                "extra_lora_scale": 1,
                "num_inference_steps": 28
            }
        }
        
        result = {
            "success": True,
            "prompt": prompt,
            "filepath": str(filepath),
            "url": image_url,
            "metadata": metadata,
            "name": name
        }
        
        # Add to database if requested
        if save_to_db:
            try:
                glyph_id = add_generated_glyph(
                    name=name,
                    prompt=prompt,
                    model=MERU_MODEL,
                    file_path=str(filepath),
                    metadata=metadata
                )
                result["glyph_id"] = glyph_id
                print(f"📚 Added to database: {glyph_id}")
            except Exception as e:
                print(f"⚠️  Database save failed: {e}")
                result["db_error"] = str(e)
        
        return result
        
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        return {
            "success": False,
            "prompt": prompt,
            "error": str(e)
        }

def test_category(category: str, max_tests: int = 2):
    """Test a specific category of prompts"""
    print(f"\n🎭 Testing {category.upper()} category:")
    print("=" * 50)
    
    prompts = TEST_PROMPTS.get(category, [])
    results = []
    
    for i, prompt in enumerate(prompts[:max_tests]):
        print(f"\n[{i+1}/{min(max_tests, len(prompts))}]")
        result = test_meru_model(prompt)
        results.append(result)
        
        if result["success"]:
            print(f"🎯 Success!")
        else:
            print(f"💥 Failed: {result['error']}")
    
    return results

def run_full_test_suite():
    """Run comprehensive MERU testing"""
    print("🚀 MERU Model Testing Suite")
    print("=" * 60)
    
    all_results = {}
    
    # Test each category
    for category in TEST_PROMPTS.keys():
        category_results = test_category(category, max_tests=1)  # 1 per category for speed
        all_results[category] = category_results
    
    # Save test results
    test_log = {
        "timestamp": datetime.now().isoformat(),
        "model": MERU_MODEL,
        "trigger_word": TRIGGER_WORD,
        "results": all_results
    }
    
    log_file = Path("results/logs") / f"meru_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, 'w') as f:
        json.dump(test_log, f, indent=2)
    
    print(f"\n📊 Test results saved: {log_file}")
    
    return all_results

def quick_test():
    """Quick single test"""
    print("⚡ Quick MERU Test")
    prompt = f"{TRIGGER_WORD} sacred fire symbol in mystical line art style"
    result = test_meru_model(prompt)
    return result

def show_database_stats():
    """Show current database statistics"""
    print("\n📊 Database Statistics:")
    print("=" * 30)
    
    stats = glyph_db.get_stats()
    
    print(f"Total Glyphs: {stats.get('total_glyphs', 0)}")
    print(f"MERU Glyphs: {stats.get('meru_glyphs', 0)}")
    print(f"Total Dreams: {stats.get('total_dreams', 0)}")
    print(f"Total Usage: {stats.get('total_usage', 0)}")
    
    print("\nCategories:")
    for category, count in stats.get('categories', {}).items():
        print(f"  {category}: {count}")
    
    print("\nMost Used Glyphs:")
    for glyph in stats.get('most_used', [])[:3]:
        print(f"  {glyph.get('title', 'Unknown')}: {glyph.get('usage_count', 0)} uses")

def interactive_test():
    """Interactive testing mode"""
    print("🎮 Interactive MERU Testing")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Quick test")
        print("2. Full test suite")
        print("3. Custom prompt")
        print("4. Show database stats")
        print("5. Exit")
        
        choice = input("\nChoose option (1-5): ").strip()
        
        if choice == "1":
            quick_test()
        elif choice == "2":
            run_full_test_suite()
        elif choice == "3":
            custom_prompt = input(f"Enter prompt ('{TRIGGER_WORD}' will be added): ")
            if not custom_prompt.startswith(TRIGGER_WORD):
                custom_prompt = f"{TRIGGER_WORD} {custom_prompt}"
            test_meru_model(custom_prompt)
        elif choice == "4":
            show_database_stats()
        elif choice == "5":
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    import sys
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "quick":
            quick_test()
        elif sys.argv[1] == "full":
            run_full_test_suite()
        elif sys.argv[1] == "stats":
            show_database_stats()
        elif sys.argv[1] == "interactive":
            interactive_test()
        else:
            print("Usage: python test_meru.py [quick|full|stats|interactive]")
    else:
        # Default to interactive mode
        interactive_test() 