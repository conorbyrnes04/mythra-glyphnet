#!/usr/bin/env python3
"""
Simple test for web interface and generation system
"""
import requests
import webbrowser
import time

def test_web_interface():
    """Test the web interface and generation system"""
    
    print("🌐 Testing Web Interface and Generation System")
    print("=" * 50)
    
    # Test 1: Check if web server is running
    print("📡 Testing web server...")
    try:
        response = requests.get('http://localhost:8000/')
        if response.status_code == 200:
            print("✅ Web server is running!")
        else:
            print(f"❌ Web server issue: {response.status_code}")
    except Exception as e:
        print(f"❌ Web server error: {e}")
    
    # Test 2: Check if API server is running
    print("\n📡 Testing API server...")
    try:
        response = requests.get('http://localhost:5002/api/health')
        if response.status_code == 200:
            print("✅ API server is running!")
            result = response.json()
            print(f"📊 Status: {result.get('status', 'Unknown')}")
        else:
            print(f"❌ API server issue: {response.status_code}")
    except Exception as e:
        print(f"❌ API server error: {e}")
    
    # Test 3: Test a simple generation
    print("\n🎨 Testing glyph generation...")
    test_glyph = {
        "name": "Star",
        "meaning": "Guidance and Hope",
        "interpretation": "Light in the darkness, celestial wisdom",
        "style": "celtic_enhanced",
        "emotion": "#FFD700"
    }
    
    try:
        response = requests.post(
            'http://localhost:5002/api/regenerate',
            json={
                'glyph_info': test_glyph,
                'custom_feedback': 'Make it more radiant and celestial'
            },
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Generation successful!")
            print(f"📁 Generated {len(result.get('variants', []))} variants")
            print(f"💬 Message: {result.get('message', 'No message')}")
            
            # Show the variant paths
            variants = result.get('variants', [])
            for i, variant in enumerate(variants, 1):
                print(f"   Variant {i}: {variant}")
                
        else:
            print(f"❌ Generation failed: {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Generation error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Web interface test completed!")
    
    # Open the web interface
    print("\n🌐 Opening web interface...")
    try:
        webbrowser.open('http://localhost:8000/glyph_curation_app.html')
        print("✅ Opened glyph curation app in browser!")
    except Exception as e:
        print(f"❌ Could not open browser: {e}")
        print("📝 Please manually open: http://localhost:8000/glyph_curation_app.html")

if __name__ == "__main__":
    test_web_interface() 