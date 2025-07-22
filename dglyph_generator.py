#!/usr/bin/env python3
"""
dGlyph Generator - Dream-specific glyph creation with emotion integration
"""
from data.emotions.emotion_processor import create_dream_glyph_prompt, analyze_dream_emotions
from test_bw_meru import generate_bw_meru_glyph
from datetime import datetime
from pathlib import Path
import json

def generate_dream_glyph(dream_text: str, 
                        dreamer_id: str = "anonymous",
                        base_symbols: list = None) -> dict:
    """Generate a personalized dGlyph from dream text"""
    
    print(f"🌙 Generating dGlyph for dream analysis...")
    print(f"📝 Dream: {dream_text[:100]}...")
    
    # Analyze emotions and create prompt
    dream_prompt_data = create_dream_glyph_prompt(dream_text, base_symbols)
    prompt = dream_prompt_data["prompt"]
    emotion_analysis = dream_prompt_data["emotion_analysis"]
    
    print(f"😊 Detected emotion: {emotion_analysis['emotion_path']}")
    print(f"🎨 Symbolic elements: {emotion_analysis['symbolic_elements']}")
    
    # Generate the glyph using MERU
    result = generate_bw_meru_glyph(prompt)
    
    if result["success"]:
        # Enhanced metadata for dGlyph
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Rename files to indicate dGlyph
        original_svg = Path(result["svg_path"])
        original_webp = Path(result["webp_path"])
        
        dglyph_svg = original_svg.parent / f"dglyph_{dreamer_id}_{timestamp}.svg"
        dglyph_webp = original_webp.parent / f"dglyph_{dreamer_id}_{timestamp}.webp"
        
        # Move files
        original_svg.rename(dglyph_svg)
        original_webp.rename(dglyph_webp)
        
        print(f"✅ dGlyph generated: {dglyph_svg}")
        
        # Create dGlyph metadata
        dglyph_metadata = {
            "type": "dGlyph",
            "dreamer_id": dreamer_id,
            "dream_text": dream_text,
            "base_symbols": base_symbols or [],
            "emotion_analysis": emotion_analysis,
            "generated_prompt": prompt,
            "files": {
                "svg": str(dglyph_svg),
                "webp": str(dglyph_webp)
            },
            "created": datetime.now().isoformat(),
            "model": "meru_emotional"
        }
        
        # Save dGlyph record
        save_dglyph_record(dglyph_metadata)
        
        return {
            "success": True,
            "dglyph_metadata": dglyph_metadata,
            "svg_path": str(dglyph_svg),
            "webp_path": str(dglyph_webp),
            "emotion_analysis": emotion_analysis
        }
    else:
        print(f"❌ dGlyph generation failed: {result['error']}")
        return {
            "success": False,
            "error": result["error"],
            "emotion_analysis": emotion_analysis
        }

def save_dglyph_record(dglyph_metadata: dict):
    """Save dGlyph record to database"""
    
    # Load existing dGlyphs
    dglyph_file = Path("data/dreamSeeds.json")
    
    try:
        with open(dglyph_file, 'r') as f:
            data = json.load(f)
    except:
        data = {"dGlyphs": []}
    
    # Add new dGlyph
    data["dGlyphs"].append(dglyph_metadata)
    
    # Save back
    with open(dglyph_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"📚 dGlyph saved to database")

def interactive_dglyph_creation():
    """Interactive dGlyph creation mode"""
    
    print("🌙 Interactive dGlyph Generator")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Create dGlyph from dream text")
        print("2. Test emotion analysis only")
        print("3. View recent dGlyphs")
        print("4. Exit")
        
        choice = input("\nChoose option (1-4): ").strip()
        
        if choice == "1":
            print("\n📝 Enter your dream:")
            dream_text = input("Dream description: ").strip()
            
            if not dream_text:
                print("❌ Please enter a dream description!")
                continue
            
            # Optional dreamer ID
            dreamer_id = input("Dreamer ID (optional, press Enter for anonymous): ").strip()
            if not dreamer_id:
                dreamer_id = "anonymous"
            
            # Optional base symbols
            symbols_input = input("Base symbols (comma-separated, optional): ").strip()
            base_symbols = [s.strip() for s in symbols_input.split(",")] if symbols_input else None
            
            # Generate dGlyph
            result = generate_dream_glyph(dream_text, dreamer_id, base_symbols)
            
            if result["success"]:
                print(f"\n🎉 dGlyph created successfully!")
                print(f"   SVG: {result['svg_path']}")
                print(f"   Emotion: {result['emotion_analysis']['emotion_path']}")
                
        elif choice == "2":
            dream_text = input("Enter dream text to analyze: ").strip()
            if dream_text:
                emotions = analyze_dream_emotions(dream_text)
                print(f"\n😊 Found emotions:")
                for emotion in emotions:
                    print(f"   {emotion['path']} ({emotion['level']})")
                    
        elif choice == "3":
            try:
                with open("data/dreamSeeds.json", 'r') as f:
                    data = json.load(f)
                
                dglyphs = data.get("dGlyphs", [])
                print(f"\n�� Recent dGlyphs ({len(dglyphs)} total):")
                
                for i, dglyph in enumerate(dglyphs[-5:], 1):  # Show last 5
                    emotion_path = dglyph.get("emotion_analysis", {}).get("emotion_path", "Unknown")
                    created = dglyph.get("created", "Unknown")[:10]  # Date only
                    print(f"   {i}. {emotion_path} ({created})")
                    
            except Exception as e:
                print(f"❌ Error loading dGlyphs: {e}")
                
        elif choice == "4":
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    interactive_dglyph_creation()
