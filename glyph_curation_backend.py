#!/usr/bin/env python3
"""
Glyph Curation Backend - Handles generation, selection, and model reinforcement
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import replicate
from dotenv import load_dotenv

# Import our existing modules
from src.utils.model_interface import get_model
from src.generators.archetypal import ArchetypalGenerator

class GlyphCurationBackend:
    """Backend for glyph curation with model reinforcement learning."""
    
    def __init__(self):
        """Initialize the curation backend."""
        load_dotenv()
        
        # Initialize generators
        self.celtic_generator = ArchetypalGenerator(model_name="celtic")
        self.meru_generator = ArchetypalGenerator(model_name="meru")
        
        # Curation data storage
        self.curation_data_path = Path("data/curation")
        self.curation_data_path.mkdir(parents=True, exist_ok=True)
        
        # Model reinforcement data
        self.reinforcement_data_path = Path("data/reinforcement")
        self.reinforcement_data_path.mkdir(parents=True, exist_ok=True)
        
        # Load existing data
        self.curation_history = self.load_curation_history()
        self.reinforcement_data = self.load_reinforcement_data()
    
    def load_curation_history(self) -> List[Dict]:
        """Load existing curation history."""
        history_file = self.curation_data_path / "curation_history.json"
        if history_file.exists():
            with open(history_file, 'r') as f:
                return json.load(f)
        return []
    
    def load_reinforcement_data(self) -> Dict:
        """Load model reinforcement data."""
        reinforcement_file = self.reinforcement_data_path / "reinforcement_data.json"
        if reinforcement_file.exists():
            with open(reinforcement_file, 'r') as f:
                return json.load(f)
        return {
            "celtic": {
                "preferred_styles": {},
                "quality_feedback": {},
                "regeneration_patterns": {},
                "selection_patterns": {}
            },
            "meru": {
                "preferred_styles": {},
                "quality_feedback": {},
                "regeneration_patterns": {},
                "selection_patterns": {}
            }
        }
    
    def save_curation_history(self):
        """Save curation history to file."""
        history_file = self.curation_data_path / "curation_history.json"
        with open(history_file, 'w') as f:
            json.dump(self.curation_history, f, indent=2)
    
    def save_reinforcement_data(self):
        """Save reinforcement data to file."""
        reinforcement_file = self.reinforcement_data_path / "reinforcement_data.json"
        with open(reinforcement_file, 'w') as f:
            json.dump(self.reinforcement_data, f, indent=2)
    
    def generate_glyph_variants(self, glyph_info: Dict) -> Dict:
        """Generate 4 variants for a glyph."""
        try:
            name = glyph_info['name']
            meaning = glyph_info.get('meaning', '')
            interpretation = glyph_info.get('interpretation', '')
            style = glyph_info.get('style', 'celtic_enhanced')
            emotion_hex = glyph_info.get('emotion', '#FFD700')
            
            print(f"🎨 Generating variants for {name}...")
            
            # Generate variants using the appropriate model
            if style.startswith('celtic'):
                generator = self.celtic_generator
                # Use the API-specific method for Celtic
                if hasattr(generator.model, 'generate_glyph_for_api'):
                    # Create the output path
                    name_lower = name.lower().replace(' ', '_')
                    output_path = generator.png_path / f"{name_lower}.png"
                    
                    # Create Celtic prompt
                    if hasattr(generator.model, 'create_celtic_prompt'):
                        prompt = generator.model.create_celtic_prompt(name, style, meaning, interpretation)
                    else:
                        prompt = generator.model.create_archetypal_prompt(name, meaning, interpretation)
                    
                    # Generate variants using API method
                    result = generator.model.generate_glyph_for_api(prompt, output_path)
                    
                    if result['success']:
                        return {
                            'success': True,
                            'variants': result['variants'],
                            'message': result['message']
                        }
                    else:
                        return {
                            'success': False,
                            'error': result.get('error', 'Generation failed')
                        }
                else:
                    # Fallback to regular generation
                    success = generator.generate_celtic_glyph(
                        name=name,
                        style=style,
                        meaning=meaning,
                        interpretation=interpretation,
                        emotion_hex=emotion_hex
                    )
                    
                    if success:
                        # Return the generated variants (they should be in the png directory)
                        name_lower = name.lower().replace(' ', '_')
                        variants = []
                        for i in range(1, 5):  # 4 variants
                            variant_path = generator.png_path / f"{name_lower}_variant_{i}.png"
                            if variant_path.exists():
                                variants.append({"path": str(variant_path), "index": i})
                        
                        return {
                            'success': True,
                            'variants': variants,
                            'message': f'Generated {len(variants)} variants for {name}'
                        }
                    else:
                        return {
                            'success': False,
                            'error': f'Failed to generate {name} variants'
                        }
            else:
                # Use MERU for non-Celtic styles
                generator = self.meru_generator
                success = generator.generate_glyph(
                    name=name,
                    meaning=meaning,
                    interpretation=interpretation,
                    emotion_hex=emotion_hex,
                    style=style
                )
                
                if success:
                    # For MERU, we only get one variant
                    name_lower = name.lower().replace(' ', '_')
                    variant_path = generator.png_path / f"{name_lower}.png"
                    
                    return {
                        'success': True,
                        'variants': [{"path": str(variant_path), "index": 1}],
                        'message': f'Generated {name} variant'
                    }
                else:
                    return {
                        'success': False,
                        'error': f'Failed to generate {name} variant'
                    }
                    
        except Exception as e:
            print(f"❌ Error in generate_glyph_variants: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def record_selection(self, glyph_info: Dict, selected_variant: int, 
                        feedback: Optional[str] = None, regeneration_count: int = 0,
                        custom_feedback: Optional[str] = None):
        """Record user selection for model reinforcement."""
        
        # Create selection record
        selection_record = {
            "timestamp": datetime.now().isoformat(),
            "glyph_info": glyph_info,
            "selected_variant": selected_variant,
            "feedback": feedback,
            "regeneration_count": regeneration_count,
            "custom_feedback": custom_feedback,
            "model_used": "celtic" if glyph_info.get('style', '').startswith('celtic') else "meru"
        }
        
        # Add to curation history
        self.curation_history.append(selection_record)
        self.save_curation_history()
        
        # Update reinforcement data
        self.update_reinforcement_data(selection_record)
        self.save_reinforcement_data()
        
        # Process custom feedback for prompt improvement
        if custom_feedback:
            self.process_custom_feedback(glyph_info, custom_feedback)
        
        print(f"✅ Recorded selection: {glyph_info['name']} - Variant {selected_variant}")
        if custom_feedback:
            print(f"📝 Custom feedback: {custom_feedback}")
    
    def update_reinforcement_data(self, selection_record: Dict):
        """Update reinforcement learning data based on selection."""
        
        model = selection_record["model_used"]
        glyph_info = selection_record["glyph_info"]
        style = glyph_info.get('style', 'default')
        feedback = selection_record.get('feedback')
        
        # Update style preferences
        if style not in self.reinforcement_data[model]["preferred_styles"]:
            self.reinforcement_data[model]["preferred_styles"][style] = 0
        self.reinforcement_data[model]["preferred_styles"][style] += 1
        
        # Update quality feedback
        if feedback:
            if feedback not in self.reinforcement_data[model]["quality_feedback"]:
                self.reinforcement_data[model]["quality_feedback"][feedback] = 0
            self.reinforcement_data[model]["quality_feedback"][feedback] += 1
        
        # Update regeneration patterns
        regeneration_count = selection_record.get('regeneration_count', 0)
        if regeneration_count > 0:
            if regeneration_count not in self.reinforcement_data[model]["regeneration_patterns"]:
                self.reinforcement_data[model]["regeneration_patterns"][regeneration_count] = 0
            self.reinforcement_data[model]["regeneration_patterns"][regeneration_count] += 1
        
        # Update selection patterns
        selected_variant = selection_record["selected_variant"]
        if selected_variant not in self.reinforcement_data[model]["selection_patterns"]:
            self.reinforcement_data[model]["selection_patterns"][selected_variant] = 0
        self.reinforcement_data[model]["selection_patterns"][selected_variant] += 1
    
    def get_reinforcement_insights(self) -> Dict:
        """Get insights from reinforcement learning data."""
        
        insights = {
            "celtic": self.analyze_model_insights("celtic"),
            "meru": self.analyze_model_insights("meru"),
            "recommendations": self.generate_recommendations()
        }
        
        return insights
    
    def analyze_model_insights(self, model: str) -> Dict:
        """Analyze insights for a specific model."""
        
        data = self.reinforcement_data[model]
        
        # Find most preferred styles
        preferred_styles = sorted(
            data["preferred_styles"].items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:3]
        
        # Find most common feedback
        quality_feedback = sorted(
            data["quality_feedback"].items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:3]
        
        # Find most selected variants
        selection_patterns = sorted(
            data["selection_patterns"].items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        # Calculate average regenerations
        total_regenerations = sum(
            count * frequency for count, frequency in data["regeneration_patterns"].items()
        )
        total_selections = sum(data["selection_patterns"].values())
        avg_regenerations = total_regenerations / total_selections if total_selections > 0 else 0
        
        return {
            "preferred_styles": preferred_styles,
            "quality_feedback": quality_feedback,
            "selection_patterns": selection_patterns,
            "avg_regenerations": avg_regenerations,
            "total_selections": total_selections
        }
    
    def generate_recommendations(self) -> List[str]:
        """Generate recommendations based on reinforcement data."""
        
        recommendations = []
        
        # Analyze Celtic model
        celtic_insights = self.analyze_model_insights("celtic")
        if celtic_insights["total_selections"] > 0:
            if celtic_insights["avg_regenerations"] > 2:
                recommendations.append("Consider refining Celtic prompts - high regeneration rate suggests room for improvement")
            
            if celtic_insights["preferred_styles"]:
                best_style = celtic_insights["preferred_styles"][0][0]
                recommendations.append(f"Focus on '{best_style}' style for Celtic glyphs - most preferred by users")
        
        # Analyze MERU model
        meru_insights = self.analyze_model_insights("meru")
        if meru_insights["total_selections"] > 0:
            if meru_insights["avg_regenerations"] > 2:
                recommendations.append("Consider refining MERU prompts - high regeneration rate suggests room for improvement")
        
        # General recommendations
        if not recommendations:
            recommendations.append("Continue collecting user feedback to improve model performance")
        
        return recommendations
    
    def process_custom_feedback(self, glyph_info: Dict, custom_feedback: str):
        """Process custom feedback to improve prompts."""
        
        # Load existing custom feedback data
        custom_feedback_file = self.reinforcement_data_path / "custom_feedback.json"
        if custom_feedback_file.exists():
            with open(custom_feedback_file, 'r') as f:
                custom_feedback_data = json.load(f)
        else:
            custom_feedback_data = {
                "feedback_entries": [],
                "prompt_improvements": {},
                "common_themes": {}
            }
        
        # Add new feedback entry
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "glyph_name": glyph_info['name'],
            "glyph_info": glyph_info,
            "feedback": custom_feedback,
            "model_used": "celtic" if glyph_info.get('style', '').startswith('celtic') else "meru"
        }
        
        custom_feedback_data["feedback_entries"].append(feedback_entry)
        
        # Analyze feedback for common themes
        self.analyze_custom_feedback(custom_feedback_data, custom_feedback)
        
        # Generate prompt improvements
        self.generate_prompt_improvements(custom_feedback_data, glyph_info, custom_feedback)
        
        # Save updated custom feedback data
        with open(custom_feedback_file, 'w') as f:
            json.dump(custom_feedback_data, f, indent=2)
        
        print(f"📝 Processed custom feedback for {glyph_info['name']}")
    
    def analyze_custom_feedback(self, custom_feedback_data: Dict, feedback: str):
        """Analyze custom feedback for common themes."""
        
        # Common improvement themes
        themes = {
            "detail": ["more detail", "intricate", "complex", "detailed", "fine lines"],
            "balance": ["balance", "symmetry", "proportion", "harmony", "centered"],
            "movement": ["dynamic", "flow", "movement", "energy", "rhythm"],
            "style": ["celtic", "tribal", "knotwork", "spiral", "ornament"],
            "contrast": ["contrast", "bold", "strong", "clear", "sharp"],
            "composition": ["composition", "layout", "arrangement", "design", "structure"]
        }
        
        feedback_lower = feedback.lower()
        
        for theme, keywords in themes.items():
            if any(keyword in feedback_lower for keyword in keywords):
                if theme not in custom_feedback_data["common_themes"]:
                    custom_feedback_data["common_themes"][theme] = 0
                custom_feedback_data["common_themes"][theme] += 1
    
    def generate_prompt_improvements(self, custom_feedback_data: Dict, glyph_info: Dict, feedback: str):
        """Generate prompt improvements based on custom feedback."""
        
        style = glyph_info.get('style', 'celtic_enhanced')
        model = "celtic" if style.startswith('celtic') else "meru"
        
        # Create prompt improvement entry
        improvement_entry = {
            "timestamp": datetime.now().isoformat(),
            "original_style": style,
            "feedback": feedback,
            "suggested_improvements": self.suggest_prompt_improvements(feedback, style),
            "glyph_name": glyph_info['name']
        }
        
        if model not in custom_feedback_data["prompt_improvements"]:
            custom_feedback_data["prompt_improvements"][model] = []
        
        custom_feedback_data["prompt_improvements"][model].append(improvement_entry)
    
    def suggest_prompt_improvements(self, feedback: str, style: str) -> List[str]:
        """Suggest specific prompt improvements based on feedback."""
        
        suggestions = []
        feedback_lower = feedback.lower()
        
        # Detail improvements
        if any(word in feedback_lower for word in ["detail", "intricate", "complex"]):
            suggestions.append("Add 'highly detailed' and 'intricate patterns' to prompts")
            suggestions.append("Emphasize 'fine line work' and 'precise ornamentation'")
        
        # Balance improvements
        if any(word in feedback_lower for word in ["balance", "symmetry", "proportion"]):
            suggestions.append("Add 'perfect symmetry' and 'balanced composition' to prompts")
            suggestions.append("Emphasize 'harmonious proportions' and 'centered design'")
        
        # Movement improvements
        if any(word in feedback_lower for word in ["dynamic", "flow", "movement"]):
            suggestions.append("Add 'dynamic movement' and 'flowing lines' to prompts")
            suggestions.append("Emphasize 'rhythmic patterns' and 'energetic composition'")
        
        # Style improvements
        if any(word in feedback_lower for word in ["celtic", "knotwork", "spiral"]):
            suggestions.append("Strengthen Celtic knotwork and spiral motifs in prompts")
            suggestions.append("Add 'traditional Celtic patterns' and 'ancient knotwork'")
        
        # Contrast improvements
        if any(word in feedback_lower for word in ["contrast", "bold", "strong"]):
            suggestions.append("Emphasize 'strong contrast' and 'bold lines' in prompts")
            suggestions.append("Add 'high contrast' and 'sharp definition'")
        
        # Composition improvements
        if any(word in feedback_lower for word in ["composition", "layout", "design"]):
            suggestions.append("Focus on 'strong composition' and 'balanced layout'")
            suggestions.append("Emphasize 'well-structured design' and 'harmonious arrangement'")
        
        return suggestions
    
    def get_custom_feedback_insights(self) -> Dict:
        """Get insights from custom feedback data."""
        
        custom_feedback_file = self.reinforcement_data_path / "custom_feedback.json"
        if not custom_feedback_file.exists():
            return {"message": "No custom feedback data available"}
        
        with open(custom_feedback_file, 'r') as f:
            custom_feedback_data = json.load(f)
        
        insights = {
            "total_feedback_entries": len(custom_feedback_data["feedback_entries"]),
            "common_themes": custom_feedback_data["common_themes"],
            "prompt_improvements": custom_feedback_data["prompt_improvements"],
            "recent_feedback": custom_feedback_data["feedback_entries"][-5:] if custom_feedback_data["feedback_entries"] else []
        }
        
        return insights
    
    def export_curation_data(self) -> Dict:
        """Export complete curation data for analysis."""
        
        return {
            "curation_history": self.curation_history,
            "reinforcement_data": self.reinforcement_data,
            "insights": self.get_reinforcement_insights(),
            "custom_feedback_insights": self.get_custom_feedback_insights(),
            "export_timestamp": datetime.now().isoformat(),
            "total_curated": len(self.curation_history),
            "models_used": {
                "celtic": len([r for r in self.curation_history if r["model_used"] == "celtic"]),
                "meru": len([r for r in self.curation_history if r["model_used"] == "meru"])
            }
        }
    
    def get_curation_progress(self) -> Dict:
        """Get current curation progress."""
        
        total_curated = len(self.curation_history)
        total_target = 108  # Target number of glyphs
        
        return {
            "total_curated": total_curated,
            "total_target": total_target,
            "completion_percentage": round((total_curated / total_target) * 100, 1),
            "remaining": total_target - total_curated,
            "last_curated": self.curation_history[-1] if self.curation_history else None
        }

def main():
    """Test the curation backend."""
    
    backend = GlyphCurationBackend()
    
    print("🎨 Glyph Curation Backend")
    print("=" * 50)
    
    # Test glyph generation
    test_glyph = {
        "name": "Dragon",
        "meaning": "Power and Wisdom",
        "interpretation": "Ancient guardian of knowledge",
        "style": "celtic_enhanced",
        "emotion": "#FF4444"
    }
    
    print(f"\n🧪 Testing glyph generation for: {test_glyph['name']}")
    result = backend.generate_glyph_variants(test_glyph)
    
    if result["success"]:
        print("✅ Variants generated successfully")
        
        # Simulate user selection
        backend.record_selection(
            glyph_info=test_glyph,
            selected_variant=2,
            feedback="composition",
            regeneration_count=1,
            custom_feedback="More intricate spiral patterns and stronger Celtic knotwork"
        )
        
        # Show insights
        insights = backend.get_reinforcement_insights()
        print(f"\n📊 Reinforcement Insights:")
        print(f"Celtic preferred styles: {insights['celtic']['preferred_styles']}")
        print(f"Recommendations: {insights['recommendations']}")
        
        # Show custom feedback insights
        custom_insights = backend.get_custom_feedback_insights()
        print(f"\n📝 Custom Feedback Insights:")
        print(f"Total feedback entries: {custom_insights.get('total_feedback_entries', 0)}")
        print(f"Common themes: {custom_insights.get('common_themes', {})}")
        
    else:
        print(f"❌ Failed to generate variants: {result['error']}")

if __name__ == "__main__":
    main() 