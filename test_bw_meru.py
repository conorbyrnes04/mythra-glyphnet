#!/usr/bin/env python3
"""
Enhanced B&W MERU Testing
Optimized for pure black/white SVG conversion
"""
import os
import replicate
from datetime import datetime
from pathlib import Path
import requests
from dotenv import load_dotenv
import subprocess
from PIL import Image, ImageOps
import tempfile
import json
import numpy as np

# Load environment
load_dotenv()

# Import our integration
from database.glyph_integration import glyph_db, add_generated_glyph

# MERU Model Configuration
MERU_MODEL = "conorbyrnes04/meru:86bcf689d994c5ebec0c93fe6bf2a15abe067850f78607ebd46c9f0f46418d24"
TRIGGER_WORD = "meru"

def create_bw_optimized_prompt(symbol: str, style_emphasis: str = "high_contrast") -> str:
    """Create prompts optimized for pure black/white output"""
    
    # Core B&W emphasis
    bw_core = (
        f"{TRIGGER_WORD} {symbol} in pure black ink on white background, "
        f"high contrast monochrome, no colors, no grays, "
        f"stark black and white only, "
        f"clean vector-style line art, "
        f"minimalist symbolic design, "
    )
    
    # Style modifiers
    if style_emphasis == "high_contrast":
        bw_core += (
            f"bold black strokes, sharp edges, "
            f"clear silhouette, maximum contrast, "
            f"binary black and white, "
        )
    elif style_emphasis == "line_art":
        bw_core += (
            f"thin black lines, outline style, "
            f"linear drawing, stroke-based, "
            f"pen and ink aesthetic, "
        )
    elif style_emphasis == "solid_forms":
        bw_core += (
            f"solid black shapes, filled forms, "
            f"strong silhouettes, geometric, "
            f"block printing style, "
        )
    
    # SVG optimization
    bw_core += (
        f"perfect for SVG conversion, "
        f"scalable vector graphics, "
        f"clean paths, no gradients, "
        f"suitable for laser cutting"
    )
    
    return bw_core

# Enhanced B&W prompts
BW_OPTIMIZED_PROMPTS = {
    "elements_solid": [
        create_bw_optimized_prompt("fire spiral", "solid_forms"),
        create_bw_optimized_prompt("water wave", "solid_forms"),
        create_bw_optimized_prompt("earth mountain", "solid_forms"),
        create_bw_optimized_prompt("air vortex", "solid_forms")
    ],
    "elements_line": [
        create_bw_optimized_prompt("fire spiral", "line_art"),
        create_bw_optimized_prompt("water flow", "line_art"),
        create_bw_optimized_prompt("earth crystal", "line_art"),
        create_bw_optimized_prompt("air wind", "line_art")
    ],
    "sacred_contrast": [
        create_bw_optimized_prompt("tree of life", "high_contrast"),
        create_bw_optimized_prompt("ouroboros serpent", "high_contrast"),
        create_bw_optimized_prompt("sacred eye", "high_contrast"),
        create_bw_optimized_prompt("lotus mandala", "high_contrast")
    ]
}

def convert_to_bw_svg(webp_path: Path, svg_path: Path = None, method: str = "aggressive") -> dict:
    """Enhanced B&W SVG conversion with multiple methods"""
    
    if svg_path is None:
        svg_path = webp_path.parent / f"{webp_path.stem}_bw.svg"
    
    print(f"🔄 Converting to B&W SVG: {webp_path.name} (method: {method})")
    
    try:
        # Check if potrace is available
        subprocess.run(['potrace', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {
            "success": False, 
            "error": "Potrace not found. Install with: brew install potrace"
        }
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Enhanced B&W preprocessing
            with Image.open(webp_path) as img:
                print(f"📊 Original mode: {img.mode}, size: {img.size}")
                
                # Force RGB conversion
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Create white background for transparency
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'RGBA':
                        background.paste(img, mask=img.split()[-1])
                    elif img.mode == 'LA':
                        background.paste(img.convert('RGB'), mask=img.split()[-1])
                    else:
                        background.paste(img.convert('RGB'))
                    img = background
                
                # Convert to grayscale first
                img_gray = ImageOps.grayscale(img)
                
                if method == "aggressive":
                    # Aggressive B&W conversion
                    # Increase contrast dramatically
                    img_gray = ImageOps.autocontrast(img_gray, cutoff=5)
                    
                    # Use adaptive threshold
                    img_array = np.array(img_gray)
                    threshold = np.mean(img_array) * 0.75  # Aggressive threshold
                    
                    # Create pure B&W
                    img_bw = img_gray.point(lambda x: 0 if x < threshold else 255, '1')
                    
                elif method == "otsu":
                    # Otsu's method for optimal threshold
                    img_array = np.array(img_gray)
                    
                    # Calculate histogram
                    hist, bins = np.histogram(img_array.flatten(), 256, [0, 256])
                    hist = hist.astype(float)
                    
                    # Find optimal threshold using Otsu's method
                    total_pixels = img_array.size
                    sum_total = np.sum(bins[:-1] * hist)
                    
                    sum_bg = 0
                    weight_bg = 0
                    max_variance = 0
                    optimal_threshold = 0
                    
                    for i in range(256):
                        weight_bg += hist[i]
                        if weight_bg == 0:
                            continue
                        
                        weight_fg = total_pixels - weight_bg
                        if weight_fg == 0:
                            break
                        
                        sum_bg += i * hist[i]
                        mean_bg = sum_bg / weight_bg
                        mean_fg = (sum_total - sum_bg) / weight_fg
                        
                        variance = weight_bg * weight_fg * (mean_bg - mean_fg) ** 2
                        if variance > max_variance:
                            max_variance = variance
                            optimal_threshold = i
                    
                    img_bw = img_gray.point(lambda x: 0 if x < optimal_threshold else 255, '1')
                    print(f"📊 Otsu threshold: {optimal_threshold}")
                    
                else:  # "simple"
                    # Simple 50% threshold
                    img_bw = img_gray.point(lambda x: 0 if x < 128 else 255, '1')
                
                # Save processed image
                temp_bmp = temp_path / "processed.bmp"
                img_bw.save(temp_bmp, 'BMP')
                
                print(f"📊 Processed to pure B&W using {method} method")
            
            # Enhanced potrace command for B&W
            cmd = [
                'potrace',
                str(temp_bmp),
                '-s',  # SVG output
                '-o', str(svg_path),
                '--tight',           # Tight bounding box
                '--turnpolicy', 'minority',  # Better curves
                '--alphamax', '0.0',        # No curve smoothing (sharper)
                '--opttolerance', '0.1',    # Less optimization (preserve detail)
                '--unit', '1',              # Use pixels
                '--cleartext',              # Readable SVG
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Post-process SVG to ensure pure black
            if svg_path.exists():
                with open(svg_path, 'r') as f:
                    svg_content = f.read()
                
                # Force all fills to pure black
                svg_content = svg_content.replace('fill="#', 'fill="#000000" data-original="#')
                svg_content = svg_content.replace('stroke="#', 'stroke="#000000" data-original="#')
                
                # Add style to ensure B&W
                if '<svg' in svg_content and 'style=' not in svg_content:
                    svg_content = svg_content.replace('<svg', 
                        '<svg style="fill: black; stroke: black;"')
                
                with open(svg_path, 'w') as f:
                    f.write(svg_content)
                
                print(f"✅ B&W SVG created: {svg_path}")
            
            return {
                "success": True,
                "webp_path": str(webp_path),
                "svg_path": str(svg_path),
                "method": method,
                "file_size": svg_path.stat().st_size,
                "bw_optimized": True
            }
            
    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "error": f"Potrace conversion failed: {e.stderr}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"B&W SVG conversion failed: {str(e)}"
        }

def generate_bw_meru_glyph(prompt: str) -> dict:
    """Generate MERU glyph optimized for B&W conversion using OTSU method"""
    
    print(f"🎨 Generating B&W optimized: {prompt}")
    
    try:
        output = replicate.run(
            MERU_MODEL,
            input={
                "prompt": prompt,
                "model": "dev",
                "go_fast": False,
                "lora_scale": 1.2,  # Slightly higher for more style
                "megapixels": "1",
                "num_outputs": 1,
                "aspect_ratio": "1:1",
                "output_format": "webp",
                "guidance_scale": 6,  # Higher guidance for more prompt adherence
                "output_quality": 95,  # Higher quality
                "prompt_strength": 0.9,  # Stronger prompt influence
                "extra_lora_scale": 1,
                "num_inference_steps": 35  # More steps for better quality
            }
        )
        
        # Get file data
        if output and len(output) > 0:
            if hasattr(output[0], 'url'):
                image_url = str(output[0].url)
                image_data = output[0].read()
            else:
                image_url = str(output[0])
                response = requests.get(image_url)
                response.raise_for_status()
                image_data = response.content
        else:
            raise Exception("No output generated")
        
        # Save WebP
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = prompt.replace("meru", "").strip().split()[:3]
        name = "_".join(name).replace(" ", "_")
        
        webp_file = Path("results/glyphs") / f"bw_{name}_{timestamp}.webp"
        webp_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(webp_file, 'wb') as f:
            f.write(image_data)
        
        print(f"✅ B&W optimized WebP saved: {webp_file}")
        
        # Convert to SVG using OTSU method only
        svg_file = webp_file.parent / f"bw_{name}_{timestamp}.svg"  # No method suffix
        result = convert_to_bw_svg(webp_file, svg_file, "otsu")
        
        if result["success"]:
            print(f"✅ OTSU B&W SVG created: {svg_file}")
            
            # Add to database
            try:
                from database.glyph_integration import add_generated_glyph
                
                glyph_id = add_generated_glyph(
                    name=name,
                    prompt=prompt,
                    model=MERU_MODEL,
                    file_path=str(svg_file),  # Use SVG as primary file
                    metadata={
                        "webp_path": str(webp_file),
                        "svg_path": str(svg_file),
                        "svg_method": "otsu",
                        "bw_optimized": True,
                        "generation_time": datetime.now().isoformat(),
                        "original_url": image_url,
                        "svg_conversion": result
                    }
                )
                print(f"📚 Added to database: {glyph_id}")
                
            except Exception as e:
                print(f"⚠️  Database save failed: {e}")
                glyph_id = None
            
            return {
                "success": True,
                "webp_path": str(webp_file),
                "svg_path": str(svg_file),
                "svg_result": result,
                "prompt": prompt,
                "image_url": image_url,
                "glyph_id": glyph_id
            }
        else:
            print(f"❌ OTSU conversion failed: {result.get('error', 'Unknown error')}")
            return {
                "success": False,
                "error": f"SVG conversion failed: {result.get('error', 'Unknown error')}"
            }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def test_bw_category(category: str, max_tests: int = 2):
    """Test a category of B&W optimized prompts"""
    print(f"\n🎭 Testing B&W {category.upper()} category:")
    print("=" * 60)
    
    prompts = BW_OPTIMIZED_PROMPTS.get(category, [])
    results = []
    
    for i, prompt in enumerate(prompts[:max_tests]):
        print(f"\n[{i+1}/{min(max_tests, len(prompts))}]")
        result = generate_bw_meru_glyph(prompt, )
        results.append(result)
        
        if result["success"]:
            print(f"🎯 Success! Generated {result['methods_tried']} SVG variants")
            if result['best_svg']:
                print(f"🏆 Best: {result['best_svg']['method']} method")
        else:
            print(f"💥 Failed: {result['error']}")
    
    return results

def interactive_bw_test():
    """Interactive B&W testing mode"""
    print("🎮 Interactive B&W MERU Testing")
    print("=" * 40)
    
    while True:
        print("\nB&W Optimization Options:")
        print("1. Test elements (solid forms)")
        print("2. Test elements (line art)")  
        print("3. Test sacred symbols (high contrast)")
        print("4. Custom B&W prompt")
        print("5. Compare all methods")
        print("6. Exit")
        
        choice = input("\nChoose option (1-6): ").strip()
        
        if choice == "1":
            test_bw_category("elements_solid", max_tests=2)
        elif choice == "2":
            test_bw_category("elements_line", max_tests=2)
        elif choice == "3":
            test_bw_category("sacred_contrast", max_tests=2)
        elif choice == "4":
            custom_symbol = input("Enter symbol (e.g., 'dragon', 'moon'): ").strip()
            style = input("Choose style (high_contrast/line_art/solid_forms): ").strip()
            if style not in ["high_contrast", "line_art", "solid_forms"]:
                style = "high_contrast"
            
            custom_prompt = create_bw_optimized_prompt(custom_symbol, style)
            print(f"\n📝 Generated prompt: {custom_prompt[:100]}...")
            
            result = generate_bw_meru_glyph(custom_prompt, )
            if result["success"]:
                print(f"🎉 Custom B&W glyph created with {result['methods_tried']} variants!")
        elif choice == "5":
            # Test all categories briefly
            for cat in BW_OPTIMIZED_PROMPTS.keys():
                test_bw_category(cat, max_tests=1)
        elif choice == "6":
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "test-all":
            # Test all categories
            for category in BW_OPTIMIZED_PROMPTS.keys():
                test_bw_category(category, max_tests=1)
        elif sys.argv[1] == "single":
            # Test single prompt
            if len(sys.argv) > 2:
                symbol = sys.argv[2]
                style = sys.argv[3] if len(sys.argv) > 3 else "high_contrast"
                prompt = create_bw_optimized_prompt(symbol, style)
                generate_bw_meru_glyph(prompt, )
            else:
                print("Usage: python test_bw_meru.py single <symbol> [style]")
        else:
            print("Usage: python test_bw_meru.py [test-all|single <symbol> [style]]")
    else:
        # Default to interactive mode
        interactive_bw_test()
