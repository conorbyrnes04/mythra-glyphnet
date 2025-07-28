#!/usr/bin/env python3
"""
Test script for the new non-interactive generation system
"""
import requests
import json

def test_new_generation():
    """Test the new non-interactive generation system"""
    
    print("🧪 Testing New Generation System")
    print("=" * 50)
    
    # Test data
    test_glyph = {
        "name": "Star",
        "meaning": "Guidance and Hope",
        "interpretation": "Light in the darkness, celestial wisdom",
        "style": "celtic_enhanced",
        "emotion": "#FFD700"
    }
    
    print(f"🎨 Testing generation for: {test_glyph['name']}")
    print(f"📝 Style: {test_glyph['style']}")
    print(f"💭 Custom feedback: Make it more radiant and celestial")
    
    try:
        # Test the regeneration endpoint
        response = requests.post(
            'http://localhost:5002/api/regenerate',
            json={
                'glyph_info': test_glyph,
                'custom_feedback': 'Make it more radiant and celestial'
            },
            headers={'Content-Type': 'application/json'},
            timeout=120  # 2 minute timeout for generation
        )
        
        print(f"\n📡 API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Generation successful!")
            print(f"💬 Message: {result.get('message', 'No message')}")
            
            variants = result.get('variants', [])
            print(f"📁 Generated {len(variants)} variants:")
            
            for i, variant in enumerate(variants, 1):
                print(f"   Variant {i}: {variant}")
                
            # Test selection
            if variants:
                print(f"\n📝 Testing selection of variant 1...")
                selection_response = requests.post(
                    'http://localhost:5002/api/select',
                    json={
                        'glyph_info': test_glyph,
                        'selected_variant': 1,
                        'feedback': 'Perfect celestial design',
                        'regeneration_count': 1,
                        'custom_feedback': 'The radiant design is exactly what I wanted'
                    },
                    headers={'Content-Type': 'application/json'}
                )
                
                if selection_response.status_code == 200:
                    selection_result = selection_response.json()
                    print(f"✅ Selection recorded: {selection_result.get('message', 'No message')}")
                else:
                    print(f"❌ Selection failed: {selection_response.status_code}")
                    
        else:
            print(f"❌ Generation failed: {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏰ Generation timed out (this is normal for first generation)")
    except Exception as e:
        print(f"❌ Error during test: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Test completed!")

if __name__ == "__main__":
    test_new_generation() 