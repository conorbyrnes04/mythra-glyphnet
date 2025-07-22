#!/usr/bin/env python3
"""
Symbol Emotion Mapper
Maps gGlyph symbol meanings to appropriate emotions for coloring
"""
import sys
import random
sys.path.append('data/emotions')

from emotion_processor import emotion_processor

class SymbolEmotionMapper:
    """Map symbol meanings to emotions for coloring"""
    
    def __init__(self):
        self.symbol_emotion_map = {
            # Animal symbols -> appropriate emotions
            "instinct": ["intuitive", "primal", "natural"],
            "protection": ["caring", "defensive", "strong"],
            "wildness": ["free", "untamed", "fierce"],
            "loyalty": ["devoted", "faithful", "steadfast"],
            "transformation": ["changing", "evolving", "metamorphosis"],
            "healing": ["compassionate", "nurturing", "restorative"],
            "danger": ["fearful", "threatening", "alarming"],
            
            # Element symbols -> emotions
            "stability": ["grounded", "secure", "steady"],
            "strength": ["powerful", "resilient", "determined"],
            "aspiration": ["hopeful", "ambitious", "reaching"],
            "endurance": ["persistent", "lasting", "durable"],
            "vitality": ["energetic", "alive", "vibrant"],
            "illumination": ["enlightened", "clear", "bright"],
            "source": ["originating", "pure", "fundamental"],
            "clarity": ["clear", "focused", "understanding"],
            "cycles": ["rhythmic", "periodic", "changing"],
            "reflection": ["contemplative", "thoughtful", "introspective"],
            "mystery": ["enigmatic", "hidden", "secretive"],
            "feminine": ["gentle", "nurturing", "receptive"],
            "flow": ["fluid", "adaptable", "moving"],
            "emotion": ["feeling", "expressive", "sensitive"],
            "adaptability": ["flexible", "adjusting", "responsive"],
            "depth": ["profound", "deep", "complex"],
            
            # Object/Tool symbols -> emotions
            "access": ["opening", "unlocking", "discovering"],
            "discovery": ["curious", "exploring", "finding"],
            "unlocking": ["revealing", "opening", "freeing"],
            "potential": ["hopeful", "promising", "possible"],
            "growth": ["developing", "expanding", "flourishing"],
            "connection": ["bonding", "linking", "relating"],
            "life": ["vibrant", "living", "energetic"],
            
            # Archetype symbols -> emotions
            "unconscious": ["hidden", "mysterious", "deep"],
            "hidden aspects": ["secretive", "concealed", "inner"],
            
            # Spiritual symbols
            "spiritual awakening": ["enlightened", "awakening", "transcendent"],
            "purity": ["clean", "innocent", "clear"],
            "transcendence": ["elevated", "higher", "beyond"]
        }
        
        # Direct emotion mappings for stronger associations
        self.meaning_to_core_emotion = {
            # Positive/Growth meanings -> Joy
            "growth": "Joy",
            "vitality": "Joy", 
            "life": "Joy",
            "spiritual awakening": "Joy",
            "illumination": "Joy",
            "discovery": "Joy",
            "potential": "Joy",
            
            # Protective/Caring meanings -> Love
            "protection": "Love",
            "loyalty": "Love",
            "healing": "Love",
            "connection": "Love",
            "nurturing": "Love",
            
            # Challenging/Intense meanings -> Anger (for intensity)
            "wildness": "Anger",
            "strength": "Anger",
            "instinct": "Anger",
            "power": "Anger",
            
            # Mysterious/Unknown meanings -> Surprise
            "mystery": "Surprise",
            "transcendence": "Surprise",
            "hidden aspects": "Surprise",
            "unconscious": "Surprise",
            
            # Threatening meanings -> Fear
            "danger": "Fear",
            "shadow": "Fear",
            
            # Reflective/Contemplative meanings -> Sadness (for depth)
            "reflection": "Sadness",
            "depth": "Sadness",
            "cycles": "Sadness"
        }
    
    def map_meanings_to_emotion(self, meanings):
        """Map symbol meanings to the best emotion from taxonomy"""
        
        print(f"🔍 Mapping meanings: {meanings}")
        
        # Check for direct core emotion mappings first
        core_emotions = []
        for meaning in meanings:
            meaning_lower = meaning.lower()
            if meaning_lower in self.meaning_to_core_emotion:
                core_emotion = self.meaning_to_core_emotion[meaning_lower]
                core_emotions.append(core_emotion)
                print(f"   📍 {meaning} -> {core_emotion} (direct mapping)")
        
        if core_emotions:
            # Use the first mapped core emotion
            chosen_core = core_emotions[0]
            
            # Get a specific emotion from that family
            available_emotions = [
                emotion for emotion in emotion_processor.emotion_index.values() 
                if emotion["core"] == chosen_core
            ]
            
            if available_emotions:
                # Prefer secondary/tertiary emotions for more specific colors
                tertiary = [e for e in available_emotions if e["level"] == "tertiary"]
                secondary = [e for e in available_emotions if e["level"] == "secondary"]
                
                if tertiary:
                    chosen_emotion = random.choice(tertiary)
                elif secondary:
                    chosen_emotion = random.choice(secondary)
                else:
                    chosen_emotion = available_emotions[0]
                
                print(f"   🎨 Final emotion: {chosen_emotion['path']} ({chosen_emotion['hex']})")
                return chosen_emotion
        
        # Fallback: try to find emotions that contain meaning words
        for meaning in meanings:
            meaning_lower = meaning.lower()
            for emotion_key, emotion_data in emotion_processor.emotion_index.items():
                if meaning_lower in emotion_key or emotion_key in meaning_lower:
                    print(f"   🎨 Found match: {meaning} -> {emotion_data['path']} ({emotion_data['hex']})")
                    return emotion_data
        
        # Default to a meaningful emotion instead of neutral
        print(f"   🎨 No match found, using default Joy emotion")
        joy_emotions = [e for e in emotion_processor.emotion_index.values() if e["core"] == "Joy"]
        return joy_emotions[0] if joy_emotions else {"core": "Neutral", "hex": "#808080"}
    
    def create_symbol_emotion_text(self, meanings):
        """Create emotion-rich text for better analysis"""
        
        mapped_emotion = self.map_meanings_to_emotion(meanings)
        
        # Create rich emotional text
        emotion_words = []
        
        # Add the mapped emotion
        if "path" in mapped_emotion:
            emotion_words.extend(mapped_emotion["path"])
        else:
            emotion_words.append(mapped_emotion["core"])
        
        # Add meaning-based emotional descriptors
        for meaning in meanings[:2]:  # Use first 2 meanings
            meaning_lower = meaning.lower()
            if meaning_lower in self.symbol_emotion_map:
                descriptors = self.symbol_emotion_map[meaning_lower]
                emotion_words.extend(descriptors[:2])  # Add 2 descriptors
        
        # Create emotional narrative
        emotion_text = f"I feel deeply {', '.join(emotion_words[:5])} and {mapped_emotion['core'].lower()}"
        
        print(f"   📝 Generated emotion text: {emotion_text}")
        return emotion_text, mapped_emotion

# Create singleton
symbol_mapper = SymbolEmotionMapper()

def get_symbol_emotion(meanings):
    """Get emotion mapping for symbol meanings"""
    return symbol_mapper.create_symbol_emotion_text(meanings)

if __name__ == "__main__":
    # Test with different symbol meanings
    test_cases = [
        ["Instinct", "Protection", "Wildness", "Loyalty"],  # Wolf
        ["Spiritual Awakening", "Purity", "Transcendence"],  # Lotus
        ["Transformation", "Healing", "Instinct", "Danger"],  # Snake
        ["Stability", "Strength", "Aspiration", "Endurance"],  # Mountain
        ["Vitality", "Illumination", "Source", "Clarity"]  # Sun
    ]
    
    print("🧪 Testing Symbol Emotion Mapping")
    print("=" * 50)
    
    for meanings in test_cases:
        print(f"\n🔍 Testing: {meanings}")
        emotion_text, mapped_emotion = get_symbol_emotion(meanings)
        print(f"   Color: {mapped_emotion['hex']}")
        print() 