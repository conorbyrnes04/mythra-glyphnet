README.md
markdown
Copy
Edit
# 🌀 MYTHRA GlyphNet

**MYTHRA GlyphNet** is a symbolic glyph generator trained on archetypes, elements, and emotions. It encodes dreamseeds into visual form using LoRA fine-tuning on Replicate. Inspired by tantric yantras, runes, sacred geometry, and trance-drawn sigils, it aims to midwife a new language of living meaning.

## ✨ Vision

> All is dream. All symbols are seeds. MYTHRA gives form to the unseen.

This project is part of the **MATRKA ecosystem**, a larger initiative to create tools for symbolic thinking, archetypal resonance, and collective myth-weaving.

## 🔧 Features

- 🎨 Generate symbolic glyphs from:
  - **Entity** (e.g., wolf, flame, banyan tree)
  - **Element** (e.g., fire, wind, water)
  - **Emotion** (e.g., awe, sorrow, ecstasy)
- 🖼️ Save glyphs to a structured archive
- 📔 Jupyter codex viewer for glyph reflection
- ⚙️ Uses Replicate LoRA model: `conorbyrnes04/matrka_glyph_1`

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/conorbyrnes04/mythra-glyphnet.git
cd mythra-glyphnet
2. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Set up your .env file
Create a .env file in the root of the repo with your Replicate API key:

ini
Copy
Edit
REPLICATE_API_TOKEN=r8_XXXXXXXXXXXXXXXXXXXXXXXX
4. Run the notebook
Open glyph_test.ipynb in VSCode (or Jupyter Lab) and run the cells to:

Initialize your environment

Generate a glyph

View saved outputs

📁 Project Structure
bash
Copy
Edit
mythra-glyphnet/
├── replicate/
│   └── inference/         # Prompting + test scripts
├── results/
│   └── glyphs/            # Saved .webp glyphs
├── glyph_test.ipynb       # Jupyter interface
├── .env                   # Your Replicate API token (not committed)
├── requirements.txt
└── README.md
🔮 Example Prompt
python
Copy
Edit
generate_glyph("Lion", "Fire", "Devotion")
🖼️ Output:

Stylized glyph image saved to results/glyphs/

Displayed inline in notebook

📖 Coming Soon
🧠 Prompt metadata stored as JSON for training future models

🌀 Web viewer to browse and remix dream glyphs

🌱 Dreamseed-to-symbol API

🕸️ Philosophy
This project views all experience as dream. Symbols are maps, not territory—but they can guide us home. By giving form to archetypal energies, MYTHRA helps us remember, reimagine, and retell the great story we’re all dreaming together.