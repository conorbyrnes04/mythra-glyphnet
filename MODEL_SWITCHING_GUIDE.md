# 🤖 Model Switching Guide

## Overview
The glyph generation system now supports easy switching between different AI models and styles. This allows you to experiment with different models and artistic styles to find the best results for your glyphs.

## 🚀 Quick Start

### 1. Using the CLI Tool
```bash
python scripts/generate_glyph.py
```
- Choose your model (1-4)
- Use 'generate', 'celtic', or 'repair' commands
- Use 'switch' command to change models during runtime

### 2. Programmatic Usage
```python
from src.generators.archetypal import ArchetypalGenerator

# Start with Celtic model
generator = ArchetypalGenerator(model_name="celtic")

# Generate Celtic style glyph
generator.generate_celtic_glyph(
    name="dragon", 
    style="celtic",
    meaning="Power and protection"
)

# Switch to MERU
generator.switch_model("meru")

# Generate with new model
generator.generate_glyph(name="eagle", meaning="Freedom and power")
```

## 📋 Available Models

### 1. MERU (Default)
- **Model ID**: `conorbyrnes04/meru:86bcf689d994c5ebec0c93fe6bf2a15abe067850f78607ebd46c9f0f46418d24`
- **Best for**: Abstract, symbolic glyphs
- **Prompt Style**: "meru A minimalist, abstract symbol..."
- **Strengths**: Good at geometric, symbolic representations

### 2. SDXL (Stable Diffusion XL)
- **Model ID**: `stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b`
- **Best for**: Detailed, realistic glyphs
- **Prompt Style**: "minimalist abstract symbol..."
- **Strengths**: High quality, detailed outputs

### 3. Midjourney
- **Model ID**: `midjourney/diffusion:436b051ebd8fbb5b83f5acf7423d7ebd1f2204e8a3a73f2d0ed5c14debfe35d`
- **Best for**: Artistic, stylized glyphs
- **Prompt Style**: "minimalist symbol, --ar 1:1"
- **Strengths**: Artistic quality, unique styles

### 4. Celtic (NEW!)
- **Model ID**: Uses MERU with Celtic-specific prompts
- **Best for**: Celtic ritual symbols and sacred geometry
- **Styles Available**:
  - **celtic**: Celtic ritual symbols with knotwork and spirals
  - **gold_on_black**: Ancient ritual symbols with sacred geometry
- **Strengths**: Rich ornamentation, ritual power, golden aesthetics

## 🎨 Celtic Styles

### Celtic Style
- **Description**: Celtic ritual symbols with knotwork and spirals
- **Features**: Swirling patterns, knotwork, stylized eyes
- **Best for**: Traditional Celtic symbols, tribal designs
- **Color**: Golden lines on black background

### Gold on Black Style
- **Description**: Ancient ritual symbols with sacred geometry
- **Features**: Symmetrical patterns, geometric motifs, floral elements
- **Best for**: Sacred geometry, shamanic art, illuminated manuscripts
- **Color**: Golden lines on black background

## 🔧 Adding Custom Models

### Step 1: Create Model Interface
```python
class MyCustomModel(ModelInterface):
    def __init__(self):
        super().__init__("your-username/your-model:version")
    
    def generate_glyph(self, prompt: str, output_path: Path) -> bool:
        # Your custom generation logic
        pass
    
    def create_archetypal_prompt(self, name: str, meaning: str = "") -> str:
        # Your custom prompt formatting
        return f"custom {name} symbol..."
```

### Step 2: Register Model
```python
# In model_interface.py
MODEL_REGISTRY = {
    "meru": MERUInterface,
    "sdxl": SDXLInterface,
    "midjourney": MidjourneyInterface,
    "celtic": CelticInterface,
    "mycustom": MyCustomModel  # Add your model
}
```

### Step 3: Use Your Model
```python
generator = ArchetypalGenerator(model_name="mycustom")
```

## 🎯 Model Comparison

| Model | Best For | Speed | Quality | Cost | Special Features |
|-------|----------|-------|---------|------|------------------|
| MERU | Abstract symbols | Fast | Good | Low | Geometric designs |
| SDXL | Detailed glyphs | Medium | High | Medium | Realistic details |
| Midjourney | Artistic style | Slow | Very High | High | Unique artistry |
| Celtic | Ritual symbols | Fast | Good | Low | Golden aesthetics, 2 styles |

## 💡 Tips for Model Selection

### Choose MERU when:
- You want abstract, geometric symbols
- Speed is important
- Cost is a concern
- Working with archetypal concepts

### Choose SDXL when:
- You need detailed, realistic glyphs
- Quality is paramount
- You have time to wait
- Working with complex symbols

### Choose Midjourney when:
- You want artistic, stylized results
- Quality is the top priority
- You have budget for premium models
- Creating unique, creative symbols

### Choose Celtic when:
- You want ritual, sacred symbols
- Golden aesthetics are desired
- Working with Celtic or tribal themes
- Need rich ornamentation and patterns

## 🔄 Runtime Model Switching

You can switch models during runtime:

```python
generator = ArchetypalGenerator(model_name="meru")

# Generate with MERU
generator.generate_glyph(name="dragon", meaning="Power")

# Switch to Celtic
generator.switch_model("celtic")

# Generate Celtic style
generator.generate_celtic_glyph(
    name="phoenix", 
    style="celtic",
    meaning="Rebirth"
)

# Switch to gold_on_black style
generator.generate_celtic_glyph(
    name="eagle", 
    style="gold_on_black",
    meaning="Freedom"
)
```

## 📊 Metadata Tracking

Each generated glyph includes model and style information:

```json
{
  "name": "celtic_dragon",
  "meaning": "Power and protection",
  "model_used": "CelticInterface",
  "style": "celtic_celtic",
  "emotion_hex": "#FFD700",
  "files": {
    "webp": "assets/glyphs/archetypal/webp/celtic_dragon.webp",
    "svg": "assets/glyphs/archetypal/svg/celtic_dragon.svg",
    "colored": "assets/glyphs/archetypal/colored/celtic_dragon_colored.svg"
  }
}
```

## 🧪 Testing Models

Use the CLI tool to test different models:

```bash
python scripts/generate_glyph.py
```

This will let you:
- Choose between 4 different models
- Generate regular or Celtic-style glyphs
- Switch models during your session
- Compare results from different models

## 🎨 Prompt Optimization

Each model has optimized prompts:

- **MERU**: Uses "meru" trigger word and specific archetypal language
- **SDXL**: Uses detailed descriptions with negative prompts
- **Midjourney**: Uses Midjourney-specific syntax and parameters
- **Celtic**: Uses ritual and sacred geometry language with golden aesthetics

## 🔧 Troubleshooting

### Model Not Found
```
❌ Unknown model 'invalid_model'. Available models: meru, sdxl, midjourney, celtic
```
Solution: Check the model name spelling or add your model to the registry.

### API Errors
```
❌ Error generating glyph with SDXL: Invalid version or not permitted
```
Solution: Check your Replicate API key and model permissions.

### Generation Failures
```
❌ Celtic generation failed to produce output
```
Solution: Try adjusting prompt parameters or switch to a different model.

### Style Issues
```
❌ Unknown Celtic style 'invalid_style'
```
Solution: Use 'celtic' or 'gold_on_black' for Celtic styles.

## 🚀 Future Enhancements

- Model performance tracking
- Automatic model selection based on glyph type
- Batch generation with multiple models
- Model-specific prompt optimization
- Cost tracking and budgeting
- Additional Celtic style variations
- Style transfer between models 