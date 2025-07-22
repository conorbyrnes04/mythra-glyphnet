import os
import requests
import replicate
import yaml
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Get API token from environment
api_token = os.getenv("REPLICATE_API_TOKEN")
if api_token:
    os.environ["REPLICATE_API_TOKEN"] = api_token
    print(f"✅ API token loaded from .env (ends with: ...{api_token[-8:]})")
else:
    print("❌ REPLICATE_API_TOKEN not found in .env file")
    print("💡 Please add your token to .env file: REPLICATE_API_TOKEN=your_token_here")
    exit(1)

# Model configurations
MODELS = {
    'sumi': {
        'id': 'conorbyrnes04/sumi:d776a9d3c801d49af5b31a9b7553f5d405d33429d39be50e6e749e43726e2222',
        'name': 'SUMI',
        'description': 'Abstract sumi-e calligraphy style (white on black)',
        'default_format': 'png'
    },
    'mythra': {
        'id': 'conorbyrnes04/matrka_glyph_1:bce3b7b3017a5ad64f2b43c8bdaec606a4f64e8a5e0671243a9f53e9c37a7e75',
        'name': 'MYTHRA',
        'description': 'Golden/metallic mystical glyphs',
        'default_format': 'webp'
    },
    'svg': {
        'id': 'recraft-ai/recraft-v3-svg',
        'name': 'SVG',
        'description': 'Scalable vector graphics generation',
        'default_format': 'svg'
    }
}

def load_prompt_templates():
    """Load and parse prompt templates from YAML file"""
    templates = {}
    try:
        yaml_path = "../../prompts/prompt_templates.yaml"
        with open(yaml_path, 'r') as f:
            content = f.read()
        
        # Parse the YAML content by splitting on comments
        sections = content.split('\n# ')
        for section in sections:
            if 'MYTHRA' in section:
                templates['mythra'] = section.strip()
            elif 'SUMI Glyph Generation' in section:
                templates['sumi'] = section.strip()
            elif 'genericGlyph' in section:
                templates['generic'] = section.strip()
        
        print(f"✅ Loaded {len(templates)} prompt templates")
        return templates
    except Exception as e:
        print(f"❌ Error loading templates: {e}")
        return {}

def get_prompt(style, entity, element=None, emotion=None):
    """Generate prompt from templates with parameter substitution"""
    templates = load_prompt_templates()
    style = style.lower()
    
    if style not in templates:
        raise ValueError(f"Unknown style '{style}'. Available: {list(templates.keys())}")
    
    template = templates[style]
    
    if style == 'generic':
        return template.format(subject=entity)
    else:
        return template.format(
            entity=entity or '',
            element=element or '',
            emotion=emotion or ''
        )

def generate_glyph(entity, element=None, emotion=None, style='sumi', model=None, output_format=None):
    """
    Generate a glyph using specified model and prompt template.
    
    Args:
        entity: The main subject (e.g., 'horse', 'dragon')
        element: Optional element (e.g., 'fire', 'water', 'air')
        emotion: Optional emotion (e.g., 'joy', 'concentration', 'peace')
        style: Template style ('sumi', 'mythra', or 'generic')
        model: Model to use ('sumi', 'mythra', or 'svg') - defaults to style if not specified
        output_format: File format ('png', 'webp', or 'svg') - defaults to model's preferred format
    """
    # Determine model to use
    model_key = model or style
    if model_key not in MODELS:
        print(f"❌ Unknown model '{model_key}'. Available: {list(MODELS.keys())}")
        return None
    
    model_config = MODELS[model_key]
    model_id = model_config['id']
    model_name = model_config['name']
    
    # Determine output format
    if output_format is None:
        output_format = model_config['default_format']
    
    # Generate filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    parts = [entity.lower()]
    if element: parts.append(element.lower())
    if emotion: parts.append(emotion.lower())
    filename = '_'.join(parts) + f'_{timestamp}.{output_format}'
    
    # Create output directory
    output_dir = "../../results/glyphs"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    try:
        # Get prompt from template
        prompt = get_prompt(style, entity, element, emotion)
        
        print(f"🎨 Generating {entity} with {model_name} model...")
        print(f"📝 Using {style} prompt template")
        print(f"💾 Output format: {output_format}")
        
        # Generate glyph
        if model_key == 'svg':
            # SVG-specific parameters
            output = replicate.run(
                model_id,
                input={
                    "prompt": prompt,
                    "output_format": output_format,
                    "style": "vector_art",
                    "size": "1024x1024"
                }
            )
        else:
            # Standard model parameters
            output = replicate.run(
                model_id,
                input={
                    "prompt": prompt,
                    "output_format": output_format,
                    "model": "dev",
                    "go_fast": False,
                    "lora_scale": 1,
                    "megapixels": "1",
                    "num_outputs": 1,
                    "aspect_ratio": "1:1",
                    "guidance_scale": 3,
                    "output_quality": 80,
                    "prompt_strength": 0.8,
                    "extra_lora_scale": 1,
                    "num_inference_steps": 28
                }
            )
        
        # Download and save
        img_url = output[0] if isinstance(output, list) else output
        img_data = requests.get(img_url).content
        
        with open(filepath, "wb") as f:
            f.write(img_data)
        
        print(f"🌱 Saved {model_name} glyph: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"❌ Error generating glyph: {e}")
        return None

def generate_svg_glyph(entity, element=None, emotion=None, glyph_type='generic'):
    """
    Generate SVG glyphs for gGlyphs (generic) or dGlyphs (dream amalgamations)
    
    Args:
        entity: Core symbol/concept (e.g., 'dragon', 'tree', 'sun')
        element: Elemental association (e.g., 'fire', 'water', 'earth', 'air')
        emotion: Emotional quality (e.g., 'power', 'peace', 'wisdom')
        glyph_type: 'generic' for gGlyphs, 'dream' for dGlyphs
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if glyph_type == 'generic':
        # gGlyphs: Clean, universal symbols
        trigger = "GGLYPH"
        parts = [f"g{entity.lower()}"]
        
        if element and emotion:
            prompt = f"a {trigger} representing {entity} with {element} and {emotion}, clean vector symbol, universal design, minimalist SVG, scalable icon"
            parts.extend([element.lower(), emotion.lower()])
        elif element:
            prompt = f"a {trigger} representing {entity} with {element}, clean vector symbol, universal design, minimalist SVG, scalable icon"
            parts.append(element.lower())
        elif emotion:
            prompt = f"a {trigger} representing {entity} with {emotion}, clean vector symbol, universal design, minimalist SVG, scalable icon"
            parts.append(emotion.lower())
        else:
            prompt = f"a {trigger} representing {entity}, clean vector symbol, universal design, minimalist SVG, scalable icon"
            
    elif glyph_type == 'dream':
        # dGlyphs: Amalgamated dream symbols
        trigger = "DGLYPH"
        parts = [f"d{entity.lower()}"]
        
        if element and emotion:
            prompt = f"a {trigger} fusing {entity} with {element} and {emotion}, symbolic amalgamation, dream synthesis, flowing vector paths, merged concepts"
            parts.extend([element.lower(), emotion.lower()])
        elif element:
            prompt = f"a {trigger} blending {entity} with {element}, symbolic fusion, dream synthesis, flowing vector paths"
            parts.append(element.lower())
        elif emotion:
            prompt = f"a {trigger} expressing {entity} through {emotion}, dream symbol, emotional synthesis, flowing vector paths"
            parts.append(emotion.lower())
        else:
            prompt = f"a {trigger} of {entity}, dream symbol synthesis, archetypal fusion, flowing vector paths"
    
    else:
        raise ValueError(f"Unknown glyph_type '{glyph_type}'. Use 'generic' or 'dream'")
    
    # Generate filename
    filename = '_'.join(parts) + f'_{timestamp}.svg'
    output_dir = f"../../results/glyphs/{glyph_type}"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    try:
        print(f"🎨 Generating {glyph_type} SVG glyph: {entity}")
        print(f"📝 Prompt: {prompt}")
        
        # Generate SVG using the SVG model
        output = replicate.run(
            MODELS['svg']['id'],
            input={
                'prompt': prompt,
                'output_format': 'svg',
                'style': 'vector_art',
                'size': '1024x1024'
            }
        )
        
        # Download and save
        svg_url = output[0] if isinstance(output, list) else output
        svg_data = requests.get(svg_url).content
        
        with open(filepath, 'wb') as f:
            f.write(svg_data)
        
        print(f'🌱 Saved {glyph_type.upper()} SVG glyph: {filepath}')
        return filepath
        
    except Exception as e:
        print(f'❌ Error generating {glyph_type} SVG glyph: {e}')
        return None

def list_models():
    """Display available models and their descriptions"""
    print("📦 Available Models:")
    for key, config in MODELS.items():
        print(f"  • {key}: {config['name']} - {config['description']} (default: {config['default_format']})")

if __name__ == "__main__":
    # Show available models
    list_models()
    print()
    
    # Example configurations - modify these as needed
    
    print("🎨 Standard Model Examples:")
    print("="*50)
    
    # SUMI model examples
    print("🖋️ SUMI Model Examples:")
    # generate_glyph("dragon", style="sumi", model="sumi")
    # generate_glyph("horse", "air", "concentration", style="sumi", model="sumi")
    
    # MYTHRA model examples  
    print("🔥 MYTHRA Model Examples:")
    # generate_glyph("phoenix", "fire", "rebirth", style="mythra", model="mythra")
    # generate_glyph("wolf", "moon", "wisdom", style="mythra", model="mythra")
    
    print("\n🎯 SVG Glyph Examples:")
    print("="*50)
    
    # SVG gGlyph examples
    print("🏛️ Generic SVG Glyph (gGlyph) Examples:")
    # generate_svg_glyph("sun", "fire", "energy", glyph_type="generic")
    # generate_svg_glyph("tree", "earth", "growth", glyph_type="generic")
    # generate_svg_glyph("moon", glyph_type="generic")
    
    # SVG dGlyph examples
    print("🌙 Dream SVG Glyph (dGlyph) Examples:")
    # generate_svg_glyph("dragon", "fire", "power", glyph_type="dream")
    # generate_svg_glyph("phoenix", "air", "rebirth", glyph_type="dream")
    # generate_svg_glyph("serpent", "water", "transformation", glyph_type="dream")
    
    # Quick test - uncomment to run
    print("\n🚀 Quick Test:")
    print("Generating a test SVG glyph...")
    generate_svg_glyph("tree", "earth", "growth", glyph_type="generic")
