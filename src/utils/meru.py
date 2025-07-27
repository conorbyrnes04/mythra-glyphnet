"""
MERU Model Interface
Handles interaction with the MERU model for glyph generation.
"""

import os
import replicate
from pathlib import Path
from typing import Optional, List
from dotenv import load_dotenv

class MERUInterface:
    def __init__(self):
        """Initialize MERU interface."""
        load_dotenv()
        self.model_id = "conorbyrnes04/meru:86bcf689d994c5ebec0c93fe6bf2a15abe067850f78607ebd46c9f0f46418d24"
        self._validate_api_key()
    
    def generate_glyph(self, prompt: str, output_path: Path) -> bool:
        """Generate a glyph using MERU model."""
        try:
            # Add meru trigger word if not present
            if not prompt.lower().startswith('meru'):
                prompt = f"meru {prompt}"
            
            print(f"🎨 Generating glyph with prompt: {prompt}")
            
            # Generate with MERU
            output = replicate.run(
                self.model_id,
                input={"prompt": prompt}
            )
            
            if not output or len(output) == 0:
                print("❌ MERU failed to generate output")
                return False
            
            # Download the generated image
            import urllib.request
            urllib.request.urlretrieve(output[0].url, output_path)
            print(f"📥 Downloaded image to: {output_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error generating glyph: {e}")
            return False
    
    def create_archetypal_prompt(self, name: str, meaning: str = "", interpretation: str = "") -> str:
        """Create optimized prompt for archetypal symbol."""
        prompt = f"A minimalist, abstract {name} symbol. "
        
        if meaning:
            prompt += f"Represents {meaning}. "
        
        prompt += "Clean vector-style black silhouette on white background. "
        prompt += "Simple geometric forms, bold lines, easily recognizable. "
        prompt += "Modern icon design, high contrast, no details or textures. "
        prompt += "Suitable for symbolic representation."
        
        return prompt
    
    def _validate_api_key(self):
        """Validate that Replicate API key is available."""
        api_key = os.getenv('REPLICATE_API_TOKEN')
        if not api_key:
            raise ValueError(
                "❌ Replicate API key not found. "
                "Please set REPLICATE_API_TOKEN in your .env file"
            ) 