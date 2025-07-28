"""
Abstract Model Interface
Base class for different AI model interfaces.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Dict, Any
import os
import replicate
from dotenv import load_dotenv

class ModelInterface(ABC):
    """Abstract base class for AI model interfaces."""
    
    def __init__(self, model_id: str):
        """Initialize model interface."""
        load_dotenv()
        self.model_id = model_id
        self._validate_api_key()
    
    @abstractmethod
    def generate_glyph(self, prompt: str, output_path: Path) -> bool:
        """Generate a glyph using the model."""
        pass
    
    @abstractmethod
    def create_archetypal_prompt(self, name: str, meaning: str = "", interpretation: str = "") -> str:
        """Create optimized prompt for archetypal symbol."""
        pass
    
    def _validate_api_key(self):
        """Validate that Replicate API key is available."""
        api_key = os.getenv('REPLICATE_API_TOKEN')
        if not api_key:
            raise ValueError(
                "❌ Replicate API key not found. "
                "Please set REPLICATE_API_TOKEN in your .env file"
            )

class MERUInterface(ModelInterface):
    """MERU Model Interface - Current implementation."""
    
    def __init__(self):
        """Initialize MERU interface."""
        super().__init__("conorbyrnes04/meru:86bcf689d994c5ebec0c93fe6bf2a15abe067850f78607ebd46c9f0f46418d24")
    
    def generate_glyph(self, prompt: str, output_path: Path) -> bool:
        """Generate a glyph using MERU model."""
        try:
            # Add meru trigger word if not present
            if not prompt.lower().startswith('meru'):
                prompt = f"meru {prompt}"
            
            print(f"🎨 Generating glyph with MERU: {prompt}")
            
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
            print(f"❌ Error generating glyph with MERU: {e}")
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

class SDXLInterface(ModelInterface):
    """Stable Diffusion XL Interface - Alternative model."""
    
    def __init__(self):
        """Initialize SDXL interface."""
        super().__init__("stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b")
    
    def generate_glyph(self, prompt: str, output_path: Path) -> bool:
        """Generate a glyph using SDXL model."""
        try:
            print(f"🎨 Generating glyph with SDXL: {prompt}")
            
            # Generate with SDXL
            output = replicate.run(
                self.model_id,
                input={
                    "prompt": prompt,
                    "negative_prompt": "text, watermark, signature, blurry, low quality, distorted",
                    "width": 1024,
                    "height": 1024,
                    "num_outputs": 1,
                    "guidance_scale": 7.5,
                    "num_inference_steps": 50
                }
            )
            
            if not output or len(output) == 0:
                print("❌ SDXL failed to generate output")
                return False
            
            # Download the generated image
            import urllib.request
            urllib.request.urlretrieve(output[0], output_path)
            print(f"📥 Downloaded image to: {output_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error generating glyph with SDXL: {e}")
            return False
    
    def create_archetypal_prompt(self, name: str, meaning: str = "", interpretation: str = "") -> str:
        """Create optimized prompt for archetypal symbol with SDXL."""
        prompt = f"minimalist abstract {name} symbol, "
        
        if meaning:
            prompt += f"representing {meaning}, "
        
        prompt += "black silhouette on white background, "
        prompt += "clean geometric design, bold lines, "
        prompt += "modern icon style, high contrast, "
        prompt += "symbolic representation, vector art style"
        
        return prompt

class MidjourneyInterface(ModelInterface):
    """Midjourney Interface - Another alternative."""
    
    def __init__(self):
        """Initialize Midjourney interface."""
        super().__init__("midjourney/diffusion:436b051ebd8fbb5b83f5acf7423d7ebd1f2204e8a3a73f2d0ed5c14debfe35d")
    
    def generate_glyph(self, prompt: str, output_path: Path) -> bool:
        """Generate a glyph using Midjourney model."""
        try:
            print(f"🎨 Generating glyph with Midjourney: {prompt}")
            
            # Generate with Midjourney
            output = replicate.run(
                self.model_id,
                input={
                    "prompt": prompt,
                    "width": 1024,
                    "height": 1024,
                    "num_outputs": 1
                }
            )
            
            if not output or len(output) == 0:
                print("❌ Midjourney failed to generate output")
                return False
            
            # Download the generated image
            import urllib.request
            urllib.request.urlretrieve(output[0], output_path)
            print(f"📥 Downloaded image to: {output_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error generating glyph with Midjourney: {e}")
            return False
    
    def create_archetypal_prompt(self, name: str, meaning: str = "", interpretation: str = "") -> str:
        """Create optimized prompt for archetypal symbol with Midjourney."""
        prompt = f"minimalist {name} symbol, "
        
        if meaning:
            prompt += f"symbolizing {meaning}, "
        
        prompt += "black and white, geometric design, "
        prompt += "clean lines, modern icon, "
        prompt += "symbolic representation, --ar 1:1"
        
        return prompt

class CelticInterface(ModelInterface):
    """Celtic Style Interface - For Celtic ritual symbols and sacred geometry."""
    
    def __init__(self):
        """Initialize Celtic interface."""
        # Using the dedicated Celtic model
        super().__init__("conorbyrnes04/celtic:a04725c70d2f4adf655e6a6aff9894a5b9ba03acdffb67ea976e777068f5c375")
    
    def generate_glyph(self, prompt: str, output_path: Path) -> bool:
        """Generate a glyph using Celtic style with 4 variants."""
        try:
            print(f"🎨 Generating Celtic glyph: {prompt}")
            
            # Generate 4 variants with Celtic model
            output = replicate.run(
                self.model_id,
                input={
                    "model": "dev",
                    "go_fast": False,
                    "lora_scale": 1,
                    "megapixels": "1",
                    "num_outputs": 4,  # Generate 4 variants
                    "aspect_ratio": "1:1",
                    "output_format": "png",  # Changed to PNG for better quality
                    "guidance_scale": 3,
                    "output_quality": 80,
                    "prompt_strength": 0.8,
                    "extra_lora_scale": 1,
                    "num_inference_steps": 28,
                    "prompt": prompt
                }
            )
            
            if not output or len(output) == 0:
                print("❌ Celtic generation failed to produce output")
                return False
            
            # Save all 4 variants
            variants = []
            for i, variant in enumerate(output):
                # Change extension to .png and use PNG directory
                variant_path = output_path.parent.parent / "png" / f"{output_path.stem}_variant_{i+1}.png"
                import urllib.request
                urllib.request.urlretrieve(variant.url, variant_path)
                variants.append(variant_path)
                print(f"📥 Downloaded Celtic variant {i+1} to: {variant_path}")
            
            # For API usage, don't require interactive selection
            # Just save the first variant as the main output and keep all variants
            import shutil
            shutil.copy2(variants[0], output_path)
            print(f"✅ Generated {len(variants)} variants, using first as default")
            return True
            
        except Exception as e:
            print(f"❌ Error generating Celtic glyph: {e}")
            return False
    
    def generate_glyph_for_api(self, prompt: str, output_path: Path) -> dict:
        """Generate glyph variants for API usage - returns all variants without interactive selection."""
        try:
            print(f"🎨 Generating Celtic glyph for API: {prompt}")
            
            # Generate 4 variants with Celtic model
            output = replicate.run(
                self.model_id,
                input={
                    "model": "dev",
                    "go_fast": False,
                    "lora_scale": 1,
                    "megapixels": "1",
                    "num_outputs": 4,  # Generate 4 variants
                    "aspect_ratio": "1:1",
                    "output_format": "png",  # Changed to PNG for better quality
                    "guidance_scale": 3,
                    "output_quality": 80,
                    "prompt_strength": 0.8,
                    "extra_lora_scale": 1,
                    "num_inference_steps": 28,
                    "prompt": prompt
                }
            )
            
            if not output or len(output) == 0:
                print("❌ Celtic generation failed to produce output")
                return {"success": False, "error": "Generation failed"}
            
            # Save all 4 variants
            variants = []
            for i, variant in enumerate(output):
                # Change extension to .png and use PNG directory
                variant_path = output_path.parent.parent / "png" / f"{output_path.stem}_variant_{i+1}.png"
                import urllib.request
                urllib.request.urlretrieve(variant.url, variant_path)
                variants.append(variant_path)
                print(f"📥 Downloaded Celtic variant {i+1} to: {variant_path}")
            
            # Return all variants for API
            return {
                "success": True,
                "variants": [{"path": str(variant), "index": i+1} for i, variant in enumerate(variants)],
                "message": f"Generated {len(variants)} variants successfully"
            }
            
        except Exception as e:
            print(f"❌ Error generating Celtic glyph: {e}")
            return {"success": False, "error": str(e)}
    
    def _select_best_variant(self, variant_paths: list, final_path: Path) -> Optional[Path]:
        """Let user select the best variant from 4 options."""
        try:
            print(f"\n🎯 Please select the best Celtic glyph variant:")
            print("=" * 50)
            
            for i, variant_path in enumerate(variant_paths):
                print(f"{i+1}. {variant_path.name}")
            
            print("5. Regenerate all variants")
            print("0. Cancel generation")
            
            while True:
                try:
                    choice = input("\nEnter your choice (1-5, 0 to cancel): ").strip()
                    
                    if choice == "0":
                        print("❌ Generation cancelled")
                        return None
                    
                    if choice == "5":
                        print("🔄 Regenerating variants...")
                        return self._regenerate_variants(variant_paths, final_path)
                    
                    choice_num = int(choice)
                    if 1 <= choice_num <= 4:
                        selected_variant = variant_paths[choice_num - 1]
                        
                        # Copy selected variant to final path
                        import shutil
                        shutil.copy2(selected_variant, final_path)
                        
                        # Clean up other variants
                        for variant_path in variant_paths:
                            if variant_path != selected_variant:
                                variant_path.unlink()
                        
                        return final_path
                    else:
                        print("❌ Invalid choice. Please enter 1-5 or 0.")
                        
                except ValueError:
                    print("❌ Invalid input. Please enter a number.")
                except KeyboardInterrupt:
                    print("\n❌ Generation cancelled")
                    return None
                    
        except Exception as e:
            print(f"❌ Error in variant selection: {e}")
            return None
    
    def _regenerate_variants(self, old_variants: list, final_path: Path) -> Optional[Path]:
        """Regenerate variants if user is not satisfied."""
        try:
            # Clean up old variants
            for variant_path in old_variants:
                if variant_path.exists():
                    variant_path.unlink()
            
            # Return a special marker to indicate regeneration is needed
            return Path("__REGENERATE__")
            
        except Exception as e:
            print(f"❌ Error regenerating variants: {e}")
            return None
    
    def create_archetypal_prompt(self, name: str, meaning: str = "", interpretation: str = "") -> str:
        """Create optimized prompt for Celtic archetypal symbol."""
        # Choose between gold_on_black and celtic styles
        style = "celtic"  # You can make this configurable
        
        if style == "gold_on_black":
            prompt = f"Create a mythic glyph in the style of ancient ritual symbols and sacred geometry, featuring {name}. "
            prompt += "Use only bold, hand-drawn golden lines on a pure black background. "
            prompt += "The design should be symmetrical or near-symmetrical, highly abstract but still recognizable, "
            prompt += "and richly ornamented with intricate patterns, geometric and floral motifs. "
            prompt += "Channel the energy of shamanic art, visionary illustrations, and illuminated manuscripts. "
            prompt += "No text, no color except gold, strong silhouette, suitable for tattoo or SVG icon."
        else:  # celtic style
            prompt = f"Create a mythic glyph in the style of ancient Celtic ritual symbols, featuring {name}. "
            prompt += "Use only bold, hand-drawn golden lines on a pure black background. "
            prompt += "Incorporate swirling, spiral patterns, knotwork, and stylized eyes. "
            prompt += "The design should be dynamic, highly abstract yet recognizable, "
            prompt += "rich in tribal and Celtic-inspired ornament, with strong contrast and a sense of ritual power. "
            prompt += "Channel the energy of sacred geometry, illuminated manuscripts, and visionary art. "
            prompt += "No text, no color except gold, strong silhouette, suitable for tattoo or SVG icon."
        
        if meaning:
            prompt += f" The symbol represents {meaning}."
        
        if interpretation:
            prompt += f" {interpretation}"
        
        return prompt
    
    def create_celtic_prompt(self, name: str, style: str = "celtic_enhanced", meaning: str = "", interpretation: str = "") -> str:
        """Create enhanced Celtic prompt with Midjourney-quality aesthetics."""
        
        enhanced_prompts = {
            "celtic_enhanced": f"Create a mythic glyph featuring {name}. Use only bold, hand-drawn golden lines on a pure black background. The design should be highly abstract yet recognizable, with flowing organic forms, intricate swirling patterns, spiral motifs, and stylized eyes. Incorporate dynamic movement, sacred geometry, and tribal ornamentation. Channel the energy of ancient illuminated manuscripts, visionary art, and ritual symbols. The composition should be balanced, with strong contrast between the golden lines and black background. No text, no color except gold, create a powerful silhouette suitable for sacred art and spiritual practice. Make it beautiful, detailed, and evocative like high-quality Midjourney art.",
            
            "gold_on_black": f"Create a mythic glyph in the style of ancient ritual symbols and sacred geometry, featuring {name}. Use only bold, hand-drawn golden lines on a pure black background. The design should be symmetrical or near-symmetrical, highly abstract but still recognizable, and richly ornamented with intricate patterns, geometric and floral motifs. Channel the energy of shamanic art, visionary illustrations, and illuminated manuscripts. Make it beautiful, detailed, and powerful. No text, no color except gold, strong silhouette, suitable for sacred art and spiritual practice. Create flowing, organic forms with dynamic movement and spiritual energy.",
            
            "tribal_enhanced": f"Create a tribal glyph featuring {name}. Use bold golden lines on pure black background. Design should be organic and flowing, with dynamic curves, spiral patterns, and stylized elements. Channel ancient tribal art, shamanic symbols, and ritual ornamentation. Make it abstract yet recognizable, with strong movement and spiritual energy. The composition should be balanced and powerful, with intricate details and flowing forms. No text, no color except gold, create a beautiful and evocative sacred symbol.",
            
            "celtic": f"Create a mythic glyph in the style of ancient Celtic ritual symbols, featuring {name}. Use only bold, hand-drawn golden lines on a pure black background. Incorporate swirling, spiral patterns, knotwork, and stylized eyes. The design should be dynamic, highly abstract yet recognizable, rich in tribal and Celtic-inspired ornament, with strong contrast and a sense of ritual power. Channel the energy of sacred geometry, illuminated manuscripts, and visionary art. No text, no color except gold, strong silhouette, suitable for tattoo or SVG icon."
        }
        
        if style not in enhanced_prompts:
            style = "celtic_enhanced"
        
        prompt = enhanced_prompts[style]
        
        if meaning:
            prompt += f" The symbol represents {meaning}."
        
        if interpretation:
            prompt += f" {interpretation}"
        
        return prompt

class CustomModelInterface(ModelInterface):
    """Custom Model Interface - Example of adding your own model."""
    
    def __init__(self):
        """Initialize Custom model interface."""
        # Replace with your custom model ID
        super().__init__("your-username/your-model:version-id")
    
    def generate_glyph(self, prompt: str, output_path: Path) -> bool:
        """Generate a glyph using Custom model."""
        try:
            print(f"🎨 Generating glyph with Custom Model: {prompt}")
            
            # Customize the generation parameters for your model
            output = replicate.run(
                self.model_id,
                input={
                    "prompt": prompt,
                    "custom_param1": "value1",
                    "custom_param2": "value2"
                }
            )
            
            if not output or len(output) == 0:
                print("❌ Custom Model failed to generate output")
                return False
            
            # Download the generated image
            import urllib.request
            urllib.request.urlretrieve(output[0], output_path)
            print(f"📥 Downloaded image to: {output_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error generating glyph with Custom Model: {e}")
            return False
    
    def create_archetypal_prompt(self, name: str, meaning: str = "", interpretation: str = "") -> str:
        """Create optimized prompt for archetypal symbol with Custom Model."""
        # Customize the prompt format for your model
        prompt = f"custom {name} symbol, "
        
        if meaning:
            prompt += f"meaning {meaning}, "
        
        prompt += "minimalist design, geometric shapes, "
        prompt += "black and white, clean lines"
        
        return prompt

# Model registry for easy switching
MODEL_REGISTRY = {
    "meru": MERUInterface,
    "sdxl": SDXLInterface,
    "midjourney": MidjourneyInterface,
    "celtic": CelticInterface,  # Add Celtic model
    "custom": CustomModelInterface
}

def get_model(model_name: str = "meru") -> ModelInterface:
    """Get a model interface by name."""
    if model_name not in MODEL_REGISTRY:
        available_models = ", ".join(MODEL_REGISTRY.keys())
        raise ValueError(f"❌ Unknown model '{model_name}'. Available models: {available_models}")
    
    return MODEL_REGISTRY[model_name]() 