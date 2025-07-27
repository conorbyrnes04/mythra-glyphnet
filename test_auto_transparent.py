#!/usr/bin/env python3
"""
Test script for automatic transparent PNG generation
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent))

from src.generators.archetypal import ArchetypalGenerator

def test_auto_transparent():
    """Test automatic transparent PNG generation."""
    print("🎨 Testing Automatic Transparent PNG Generation")
    print("=" * 55)
    
    try:
        # Initialize Celtic generator
        print("\n1️⃣ Initializing Celtic generator...")
        generator = ArchetypalGenerator(model_name="celtic")
        generator.list_available_models()
        
        # Test automatic transparent generation
        print("\n2️⃣ Testing automatic transparent generation...")
        success = generator.generate_celtic_glyph(
            name="celtic_auto_transparent_mask",
            style="celtic",
            meaning="a ritual mask with geometric patterns",
            interpretation="Testing automatic transparent PNG generation",
            emotion_hex="#FFD700"  # Gold
        )
        
        if success:
            print("✅ Automatic transparent generation successful!")
            
            # Get glyph info
            info = generator.get_glyph_info("celtic_auto_transparent_mask")
            if info:
                print("\n📊 Auto Transparent Glyph Info:")
                print(f"Name: {info['name']}")
                print(f"Style: {info.get('style', 'default')}")
                print(f"Model Used: {info.get('model_used', 'Unknown')}")
                print(f"Emotion Color: {info.get('emotion_hex', '#000000')}")
                print(f"PNG File: {info['files'].get('png', 'Not found')}")
                
                # Check if the file is actually transparent
                png_path = Path(info['files'].get('png', ''))
                if png_path.exists():
                    try:
                        from PIL import Image
                        img = Image.open(png_path)
                        print(f"📊 Image mode: {img.mode}")
                        print(f"📊 Has transparency: {'Yes' if img.mode == 'RGBA' else 'No'}")
                    except Exception as e:
                        print(f"❌ Error checking transparency: {e}")
        else:
            print("❌ Automatic transparent generation failed!")
        
        print("\n🎉 Automatic transparent test completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_auto_transparent() 