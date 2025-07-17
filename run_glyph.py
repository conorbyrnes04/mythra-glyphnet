## 🐍 `run_glyph.py` (Replicate Script)


import os
import replicate
from dotenv import load_dotenv

# Load API key
load_dotenv()
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
if not REPLICATE_API_TOKEN:
    raise Exception("Missing REPLICATE_API_TOKEN in .env file or environment.")

# Input parameters
entity = "Falcon"
element = "Wind"
emotion = "Insight"

prompt = f"""
Generate a [MYTHRA] glyph that symbolizes the essence of a dreamseed formed from:
- Entity: {entity}
- Element: {element}
- Emotion: {emotion}

This [MYTHRA] glyph should:
– Appear etched in luminous ink, not sketched  
– Be precise yet full of life—like a living sigil carved in trance  
– Use flowing lines, spirals, sacred symmetry, and energetic centers  
– Rendered in glowing metalic or gold ink on a black background
"""

# Run the model
output = replicate.run(
    "conorbyrnes04/matrka_glyph_1:bce3b7b3017a5ad64f2b43c8bdaec606a4f64e8a5e0671243a9f53e9c37a7e75",
    input={
        "prompt": prompt,
        "model": "dev",
        "go_fast": False,
        "lora_scale": 1,
        "megapixels": "1",
        "num_outputs": 1,
        "aspect_ratio": "1:1",
        "output_format": "webp",
        "guidance_scale": 3,
        "output_quality": 80,
        "prompt_strength": 0.8,
        "extra_lora_scale": 1,
        "num_inference_steps": 28
    }
)

# Save result
output_url = output[0]
filename = f"results/glyphs/{entity.lower()}_{element.lower()}_{emotion.lower()}.webp"

print(f"🌀 Downloading image from: {output_url}")

import requests
response = requests.get(output_url)
with open(filename, "wb") as f:
    f.write(response.content)

print(f"✅ Glyph saved to {filename}")
