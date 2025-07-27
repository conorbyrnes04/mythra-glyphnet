#!/usr/bin/env python3
"""
Test enhanced Celtic generation with Midjourney-quality prompts
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from src.utils.model_interface import get_model
from src.generators.archetypal import ArchetypalGenerator

def test_enhanced_celtic():
    """Test enhanced Celtic generation."""
    
    print("🎨 Testing Enhanced Celtic Generation")
    print("=" * 50)
    
    # Create generator with Celtic model
    generator = ArchetypalGenerator(model_name="celtic")
    
    # Test different styles
    styles = ["celtic_enhanced", "gold_on_black", "tribal_enhanced"]
    
    for style in styles:
        print(f"\n🖼️ Testing style: {style}")
        
        # Generate a test symbol
        success = generator.generate_celtic_glyph(
            name="Phoenix",
            style=style,
            meaning="rebirth and transformation",
            interpretation="rising from ashes with renewed strength",
            emotion_hex="#FF6600"  # Fire orange
        )
        
        if success:
            print(f"✅ Successfully generated Phoenix with {style} style")
        else:
            print(f"❌ Failed to generate Phoenix with {style} style")
        
        # Only test one style for now to avoid API costs
        break

def test_prompt_quality():
    """Test the enhanced prompts."""
    
    print("\n📝 Testing Enhanced Prompts")
    print("=" * 30)
    
    # Get Celtic model
    celtic_model = get_model("celtic")
    
    # Test different styles
    test_cases = [
        ("Sun", "celtic_enhanced", "cosmic energy and life force", "radiant power illuminating all"),
        ("Moon", "gold_on_black", "mystery and intuition", "silver light in darkness"),
        ("Tree", "tribal_enhanced", "growth and wisdom", "roots deep in earth, branches reaching sky")
    ]
    
    for name, style, meaning, interpretation in test_cases:
        print(f"\n🎯 {name} ({style}):")
        prompt = celtic_model.create_celtic_prompt(
            name=name,
            style=style,
            meaning=meaning,
            interpretation=interpretation
        )
        print(f"   {prompt[:100]}...")

if __name__ == "__main__":
    # Test prompts first
    test_prompt_quality()
    
    # Ask user if they want to test generation
    response = input("\n🤔 Do you want to test actual generation? (y/n): ").strip().lower()
    
    if response == 'y':
        test_enhanced_celtic()
    else:
        print("📝 Prompt testing complete. Run with 'y' to test generation.") 