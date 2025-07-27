#!/usr/bin/env python3
"""
Simple test for glyph regeneration with custom feedback
"""

from glyph_curation_backend import GlyphCurationBackend

def test_regeneration():
    """Test the regeneration functionality."""
    
    print("🧪 Testing Glyph Regeneration with Custom Feedback")
    print("=" * 50)
    
    # Initialize backend
    backend = GlyphCurationBackend()
    
    # Test glyph
    test_glyph = {
        "name": "Dragon",
        "meaning": "Power and Wisdom",
        "interpretation": "Ancient guardian of knowledge",
        "style": "celtic_enhanced",
        "emotion": "#FF4444"
    }
    
    print(f"🎨 Testing regeneration for: {test_glyph['name']}")
    
    # Test with custom feedback
    custom_feedback = "More intricate spiral patterns and stronger Celtic knotwork"
    
    print(f"📝 Custom feedback: {custom_feedback}")
    
    # Generate variants
    result = backend.generate_glyph_variants(test_glyph)
    
    if result['success']:
        print("✅ Variants generated successfully")
        
        # Record selection with custom feedback
        backend.record_selection(
            glyph_info=test_glyph,
            selected_variant=2,
            feedback="composition",
            regeneration_count=1,
            custom_feedback=custom_feedback
        )
        
        print("✅ Selection recorded with custom feedback")
        
        # Show insights
        insights = backend.get_reinforcement_insights()
        custom_insights = backend.get_custom_feedback_insights()
        
        print(f"\n📊 Reinforcement Insights:")
        print(f"Celtic preferred styles: {insights['celtic']['preferred_styles']}")
        print(f"Recommendations: {insights['recommendations']}")
        
        print(f"\n📝 Custom Feedback Insights:")
        print(f"Total feedback entries: {custom_insights.get('total_feedback_entries', 0)}")
        print(f"Common themes: {custom_insights.get('common_themes', {})}")
        
        if custom_insights.get('prompt_improvements'):
            print(f"Prompt improvements: {custom_insights['prompt_improvements']}")
        
    else:
        print(f"❌ Failed to generate variants: {result['error']}")

if __name__ == "__main__":
    test_regeneration() 