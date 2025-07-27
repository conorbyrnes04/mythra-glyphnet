#!/usr/bin/env python3
"""
Glyph Generation Script
Simple interface to generate or repair archetypal glyphs.
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.generators.archetypal import ArchetypalGenerator

def main():
    """Main function."""
    print("\n🎨 GLYPH GENERATION TOOL")
    print("=" * 50)
    
    # Model selection
    print("\n🤖 Select AI Model:")
    print("1. MERU (default)")
    print("2. SDXL")
    print("3. Midjourney")
    print("4. Celtic")
    
    model_choice = input("Enter model choice (1-4, default=1): ").strip()
    
    model_map = {
        "1": "meru",
        "2": "sdxl", 
        "3": "midjourney",
        "4": "celtic"
    }
    
    model_name = model_map.get(model_choice, "meru")
    generator = ArchetypalGenerator(model_name=model_name)
    
    print(f"\n✅ Using {model_name.upper()} model")
    generator.list_available_models()
    
    while True:
        print("\n🔧 What would you like to do?")
        action = input("Enter 'generate', 'celtic', 'repair', 'switch', or 'quit': ").strip().lower()
        
        if action == 'quit':
            break
            
        if action == 'switch':
            print("\n🤖 Available Models:")
            generator.list_available_models()
            new_model = input("Enter new model name: ").strip().lower()
            generator.switch_model(new_model)
            continue
            
        if action not in ['generate', 'repair', 'celtic']:
            print("❌ Please enter 'generate', 'celtic', 'repair', 'switch', or 'quit'")
            continue
        
        name = input("\n🎯 Enter glyph name: ").strip()
        if not name:
            continue
        
        if action == 'generate':
            meaning = input("Enter meaning (optional): ").strip()
            interpretation = input("Enter interpretation (optional): ").strip()
            emotion_hex = input("Enter emotion color hex (default #000000): ").strip()
            
            if not emotion_hex:
                emotion_hex = "#000000"
            
            success = generator.generate_glyph(
                name=name,
                meaning=meaning,
                interpretation=interpretation,
                emotion_hex=emotion_hex
            )
        elif action == 'celtic':
            print("\n🎨 Celtic Style Options:")
            generator.list_celtic_styles()
            style = input("Enter style (celtic/gold_on_black, default=celtic): ").strip()
            if not style:
                style = "celtic"
            
            meaning = input("Enter meaning (optional): ").strip()
            interpretation = input("Enter interpretation (optional): ").strip()
            emotion_hex = input("Enter emotion color hex (default #FFD700 for gold): ").strip()
            
            if not emotion_hex:
                emotion_hex = "#FFD700"  # Gold color for Celtic
            
            success = generator.generate_celtic_glyph(
                name=name,
                style=style,
                meaning=meaning,
                interpretation=interpretation,
                emotion_hex=emotion_hex
            )
        else:  # repair
            success = generator.repair_glyph(name)
        
        if success:
            info = generator.get_glyph_info(name)
            if info:
                print("\n📊 Glyph Information:")
                print(f"Name: {info['name']}")
                print(f"Meaning: {info.get('meaning', '')}")
                print(f"Interpretation: {info.get('interpretation', '')}")
                print(f"Emotion Color: {info.get('emotion_hex', '#000000')}")
                print(f"Model Used: {info.get('model_used', 'Unknown')}")
                print(f"Style: {info.get('style', 'default')}")
                print("\nFiles:")
                for key, path in info['files'].items():
                    print(f"- {key}: {path}")
        
        print(f"\n{'✅ Success!' if success else '❌ Failed!'}")

if __name__ == "__main__":
    main() 