#!/usr/bin/env python3
"""
Test the API regeneration endpoint
"""

import requests
import json

def test_api_regeneration():
    """Test the API regeneration endpoint."""
    
    print("🧪 Testing API Regeneration Endpoint")
    print("=" * 50)
    
    # Test data
    test_data = {
        "glyph_info": {
            "name": "Dragon",
            "meaning": "Power and Wisdom",
            "interpretation": "Ancient guardian of knowledge",
            "style": "celtic_enhanced",
            "emotion": "#FF4444"
        },
        "custom_feedback": "Make the dragon more dynamic with flowing movement"
    }
    
    print(f"🎨 Testing regeneration for: {test_data['glyph_info']['name']}")
    print(f"📝 Custom feedback: {test_data['custom_feedback']}")
    
    try:
        # Call the API
        response = requests.post(
            'http://localhost:5002/api/regenerate',
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"📡 API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API call successful!")
            print(f"📄 Message: {result.get('message', 'No message')}")
            print(f"🖼️ Variants returned: {len(result.get('variants', []))}")
            
            for i, variant in enumerate(result.get('variants', []), 1):
                print(f"  Variant {i}: {variant}")
                
            print(f"📝 Feedback recorded: {result.get('feedback_recorded', False)}")
            
        else:
            print(f"❌ API call failed with status {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing API: {str(e)}")

if __name__ == "__main__":
    test_api_regeneration() 