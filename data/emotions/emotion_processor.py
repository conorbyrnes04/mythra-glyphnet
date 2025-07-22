#!/usr/bin/env python3
"""
Emotion Processor for dGlyph Generation
Load and process emotions_colors.json for dream glyph creation
"""
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import random

class EmotionProcessor:
    """Process emotions for dGlyph generation"""
    
    def __init__(self, emotions_file: str = "data/emotions/emotions_colors.json"):
        self.emotions_file = Path(emotions_file)
        self.emotions_data = self.load_emotions()
        self.emotion_index = self._build_emotion_index()
    
    def load_emotions(self) -> List[Dict]:
        """Load emotions from JSON file"""
        try:
            with open(self.emotions_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Failed to load emotions: {e}")
            return []
    
    def _build_emotion_index(self) -> Dict[str, Dict]:
        """Build searchable index of all emotions"""
        index = {}
        
        for core_emotion in self.emotions_data:
            core_name = core_emotion["core"]
            
            # Add core emotion
            index[core_name.lower()] = {
                "level": "core",
                "core": core_name,
                "hex": core_emotion["hex"],
                "path": [core_name]
            }
            
            # Add secondary emotions
            for secondary in core_emotion.get("secondary", []):
                sec_name = secondary["name"]
                index[sec_name.lower()] = {
                    "level": "secondary",
                    "core": core_name,
                    "secondary": sec_name,
                    "hex": secondary["hex"],
                    "path": [core_name, sec_name]
                }
                
                # Add tertiary emotions
                for tertiary in secondary.get("tertiary", []):
                    ter_name = tertiary["name"]
                    index[ter_name.lower()] = {
                        "level": "tertiary",
                        "core": core_name,
                        "secondary": sec_name,
                        "tertiary": ter_name,
                        "hex": tertiary["hex"],
                        "path": [core_name, sec_name, ter_name]
                    }
        
        return index
    
    def find_emotion(self, emotion_word: str) -> Optional[Dict]:
        """Find emotion by name (case insensitive)"""
        return self.emotion_index.get(emotion_word.lower())
    
    def get_emotion_family(self, emotion_word: str) -> List[Dict]:
        """Get all emotions in the same family"""
        emotion = self.find_emotion(emotion_word)
        if not emotion:
            return []
        
        core_name = emotion["core"]
        family = []
        
        for emotion_key, emotion_data in self.emotion_index.items():
            if emotion_data["core"] == core_name:
                family.append(emotion_data)
        
        return family
    
    def analyze_emotion_text(self, text: str) -> List[Dict]:
        """Analyze text for emotional content"""
        words = text.lower().split()
        found_emotions = []
        
        for word in words:
            # Remove punctuation
            clean_word = ''.join(c for c in word if c.isalpha())
            emotion = self.find_emotion(clean_word)
            if emotion:
                found_emotions.append(emotion)
        
        return found_emotions
    
    def get_dominant_emotion(self, emotions: List[Dict]) -> Optional[Dict]:
        """Get the most specific/dominant emotion"""
        if not emotions:
            return None
        
        # Prioritize tertiary > secondary > core
        tertiary = [e for e in emotions if e["level"] == "tertiary"]
        if tertiary:
            return tertiary[0]
        
        secondary = [e for e in emotions if e["level"] == "secondary"]
        if secondary:
            return secondary[0]
        
        return emotions[0]
    
    def get_emotion_descriptors(self, emotion: Dict) -> Dict[str, List[str]]:
        """Get symbolic descriptors for an emotion"""
        
        core_emotion = emotion["core"]
        
        # Emotion-symbol mappings
        emotion_mappings = {
            "Joy": {
                "symbols": ["sun", "flame", "spiral", "ascending_forms", "radiating_star"],
                "movements": ["dancing", "radiating", "ascending", "flowing_upward", "bursting"],
                "qualities": ["jubilant", "euphoric", "illuminated", "triumphant", "bright"]
            },
            "Love": {
                "symbols": ["heart", "embracing_forms", "unity_circle", "intertwining_patterns", "flowing_together"],
                "movements": ["embracing", "unifying", "gentle_flowing", "tender_radiating", "merging"],
                "qualities": ["compassionate", "tender", "enamored", "passionate", "warm"]
            },
            "Fear": {
                "symbols": ["jagged_forms", "protective_shells", "retreat_patterns", "barrier_shapes", "sharp_edges"],
                "movements": ["recoiling", "contracting", "sharp_edges", "defensive_posturing", "withdrawing"],
                "qualities": ["terrified", "overwhelmed", "paralyzed", "helpless", "anxious"]
            },
            "Anger": {
                "symbols": ["lightning", "sharp_triangles", "explosive_forms", "piercing_lines", "striking_patterns"],
                "movements": ["striking", "piercing", "explosive", "aggressive_thrust", "cutting"],
                "qualities": ["furious", "hostile", "enraged", "agitated", "intense"]
            },
            "Sadness": {
                "symbols": ["downward_flows", "teardrop_forms", "heavy_curves", "sinking_shapes", "melting_forms"],
                "movements": ["flowing_downward", "heavy_settling", "gentle_weeping", "melting", "drooping"],
                "qualities": ["melancholic", "sorrowful", "lonely", "disappointed", "heavy"]
            },
            "Surprise": {
                "symbols": ["burst_patterns", "radiating_lines", "opening_forms", "expansion_shapes", "sudden_star"],
                "movements": ["sudden_expansion", "radiating_outward", "opening_revelation", "explosive_awareness", "blooming"],
                "qualities": ["astonished", "bewildered", "awe-struck", "speechless", "amazed"]
            }
        }
        
        return emotion_mappings.get(core_emotion, {
            "symbols": ["neutral_form"],
            "movements": ["gentle_flow"],
            "qualities": ["calm"]
        })
    
    def create_dglyph_prompt(self, 
                           dream_text: str, 
                           base_symbols: List[str] = None,
                           style_emphasis: str = "emotional_abstract") -> str:
        """Create a dGlyph prompt based on dream emotional analysis"""
        
        # Analyze emotions in dream text
        emotions = self.analyze_emotion_text(dream_text)
        dominant_emotion = self.get_dominant_emotion(emotions)
        
        if not dominant_emotion:
            # Default neutral emotion
            dominant_emotion = {
                "core": "Neutral",
                "level": "core",
                "hex": "#808080"
            }
        
        # Get emotion descriptors
        descriptors = self.get_emotion_descriptors(dominant_emotion)
        
        # Select random elements for variety
        symbol = random.choice(descriptors["symbols"])
        movement = random.choice(descriptors["movements"])
        quality = random.choice(descriptors["qualities"])
        
        # Include base symbols from dream content
        if base_symbols:
            symbol_fusion = f"fusion of {symbol} with {', '.join(base_symbols[:2])}"
        else:
            symbol_fusion = symbol
        
        # Get emotion path for context
        emotion_path = " → ".join(dominant_emotion.get("path", [dominant_emotion["core"]]))
        
        # Create enhanced prompt
        prompt = f"""
        meru archetypal dGlyph symbol of {symbol_fusion}, 
        expressing {quality} {dominant_emotion["core"].lower()} energy,
        {movement} with emotional resonance,
        dream-specific symbolic fusion,
        pure black ink on white background,
        high contrast monochrome, no colors, no grays,
        emotionally charged abstract form,
        personal dream archetype with {quality} essence,
        perfect for SVG conversion,
        unique dreamer's symbol
        """.strip().replace('\n        ', ' ')
        
        return {
            "prompt": prompt,
            "emotion_analysis": {
                "dominant_emotion": dominant_emotion,
                "emotion_path": emotion_path,
                "all_emotions": emotions,
                "symbolic_elements": {
                    "symbol": symbol,
                    "movement": movement,
                    "quality": quality
                }
            }
        }
    
    def get_emotion_stats(self) -> Dict:
        """Get statistics about the emotion system"""
        total_emotions = len(self.emotion_index)
        core_count = len([e for e in self.emotion_index.values() if e["level"] == "core"])
        secondary_count = len([e for e in self.emotion_index.values() if e["level"] == "secondary"])
        tertiary_count = len([e for e in self.emotion_index.values() if e["level"] == "tertiary"])
        
        return {
            "total_emotions": total_emotions,
            "core_emotions": core_count,
            "secondary_emotions": secondary_count,
            "tertiary_emotions": tertiary_count,
            "emotion_families": core_count
        }

# Singleton instance
emotion_processor = EmotionProcessor()

# Helper functions for easy access
def analyze_dream_emotions(dream_text: str) -> List[Dict]:
    """Analyze dream text for emotions"""
    return emotion_processor.analyze_emotion_text(dream_text)

def create_dream_glyph_prompt(dream_text: str, base_symbols: List[str] = None) -> Dict:
    """Create dGlyph prompt from dream text"""
    return emotion_processor.create_dglyph_prompt(dream_text, base_symbols)

def get_emotion_info(emotion_word: str) -> Optional[Dict]:
    """Get information about a specific emotion"""
    return emotion_processor.find_emotion(emotion_word)

if __name__ == "__main__":
    # Test the system
    stats = emotion_processor.get_emotion_stats()
    print("📊 Emotion System Stats:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Test emotion analysis
    test_dream = "I felt terrified and overwhelmed as I was falling through dark water"
    result = create_dream_glyph_prompt(test_dream, ["water", "falling", "darkness"])
    
    print(f"\n🌙 Test Dream Analysis:")
    print(f"Dream: {test_dream}")
    print(f"Emotion: {result['emotion_analysis']['emotion_path']}")
    print(f"Prompt: {result['prompt'][:100]}...")
