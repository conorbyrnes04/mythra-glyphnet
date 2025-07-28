#!/usr/bin/env python3
"""
Test script for generation and selection system
"""
import requests
import json
import time

def test_generation_and_selection():
    """Test the full generation and selection workflow"""
    
    # Test data for a new glyph
    test_glyph = {
        "name": "Eagle",
        "meaning": "Freedom and Vision",
        "interpretation": "Soaring above the mundane with keen sight",
        "style": "celtic_enhanced",
        "emotion": "#4A90E2"
    }
    
    print("🦅 Testing Eagle glyph generation and selection...")
    print("=" * 60)
    
    # Test 1: Generate variants
    print("📡 Testing variant generation...")
    try:
        response = requests.post(
            'http://localhost:5002/api/regenerate',
            json={
                'glyph_info': test_glyph,
                'custom_feedback': 'Make it more majestic with spread wings'
            },
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Generation successful!")
            print(f"📁 Generated variants: {result.get('variants', [])}")
            print(f"💬 Message: {result.get('message', 'No message')}")
        else:
            print(f"❌ Generation failed: {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during generation: {e}")
    
    print("\n" + "=" * 60)
    
    # Test 2: Record selection
    print("📝 Testing selection recording...")
    try:
        response = requests.post(
            'http://localhost:5002/api/select',
            json={
                'glyph_info': test_glyph,
                'selected_variant': 2,
                'feedback': 'Great dynamic movement',
                'regeneration_count': 1,
                'custom_feedback': 'The spread wings look perfect'
            },
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Selection recorded successfully!")
            print(f"📊 Result: {result.get('message', 'No message')}")
        else:
            print(f"❌ Selection recording failed: {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during selection: {e}")
    
    print("\n" + "=" * 60)
    
    # Test 3: Get insights
    print("🧠 Testing insights retrieval...")
    try:
        response = requests.get('http://localhost:5002/api/insights')
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Insights retrieved successfully!")
            print(f"📈 Total selections: {result.get('total_selections', 0)}")
            print(f"🔄 Total regenerations: {result.get('total_regenerations', 0)}")
            print(f"🎨 Preferred styles: {result.get('preferred_styles', [])}")
        else:
            print(f"❌ Insights retrieval failed: {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during insights retrieval: {e}")
    
    print("\n" + "=" * 60)
    
    # Test 4: Get progress
    print("📊 Testing progress tracking...")
    try:
        response = requests.get('http://localhost:5002/api/progress')
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Progress retrieved successfully!")
            print(f"🎯 Total glyphs: {result.get('total_glyphs', 0)}")
            print(f"✅ Completed: {result.get('completed', 0)}")
            print(f"📈 Progress: {result.get('progress_percentage', 0)}%")
        else:
            print(f"❌ Progress retrieval failed: {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during progress retrieval: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Testing completed!")

def test_multiple_glyphs():
    """Test generation with multiple different glyphs"""
    
    test_glyphs = [
        {
            "name": "Wolf",
            "meaning": "Loyalty and Instinct",
            "interpretation": "Wild spirit with pack mentality",
            "style": "celtic_enhanced",
            "emotion": "#8B4513"
        },
        {
            "name": "Moon",
            "meaning": "Intuition and Mystery",
            "interpretation": "Cycles of change and hidden wisdom",
            "style": "celtic_enhanced",
            "emotion": "#C0C0C0"
        },
        {
            "name": "Tree",
            "meaning": "Growth and Wisdom",
            "interpretation": "Rooted in earth, reaching for sky",
            "style": "celtic_enhanced",
            "emotion": "#228B22"
        }
    ]
    
    print("🌳 Testing multiple glyph generation...")
    print("=" * 60)
    
    for i, glyph in enumerate(test_glyphs, 1):
        print(f"\n🌿 Testing glyph {i}: {glyph['name']}")
        print("-" * 40)
        
        try:
            response = requests.post(
                'http://localhost:5002/api/regenerate',
                json={
                    'glyph_info': glyph,
                    'custom_feedback': f'Make {glyph["name"].lower()} more {glyph["meaning"].lower()}'
                },
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {glyph['name']} generation successful!")
                print(f"📁 Variants: {len(result.get('variants', []))}")
                
                # Simulate selection
                selection_response = requests.post(
                    'http://localhost:5002/api/select',
                    json={
                        'glyph_info': glyph,
                        'selected_variant': 1,
                        'feedback': f'Perfect {glyph["meaning"].lower()} representation',
                        'regeneration_count': 0,
                        'custom_feedback': f'Great {glyph["name"].lower()} design'
                    },
                    headers={'Content-Type': 'application/json'}
                )
                
                if selection_response.status_code == 200:
                    print(f"✅ {glyph['name']} selection recorded!")
                else:
                    print(f"❌ {glyph['name']} selection failed")
                    
            else:
                print(f"❌ {glyph['name']} generation failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error with {glyph['name']}: {e}")
        
        time.sleep(2)  # Brief pause between tests
    
    print("\n" + "=" * 60)
    print("🎉 Multiple glyph testing completed!")

if __name__ == "__main__":
    print("🚀 Starting Generation and Selection Tests")
    print("=" * 60)
    
    # Test single glyph workflow
    test_generation_and_selection()
    
    print("\n" + "=" * 60)
    
    # Test multiple glyphs
    test_multiple_glyphs()
    
    print("\n🎯 All tests completed!") 