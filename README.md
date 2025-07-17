
# MYTHRA Glyph Generator

This project uses Replicate to generate sacred dream glyphs from symbolic prompts using a fine-tuned LoRA model called `matrka_glyph_1`.

## 🔮 What It Does

Given symbolic input—such as an entity, an emotion, and an element—the model produces black-and-white glyphs in a sacred, trance-inspired visual style.

Example:
Entity: Falcon
Emotion: Insight
Element: Wind

yaml
Copy
Edit

Output: A stylized dream glyph rendered as black ink on parchment.

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/conorbyrnes04/mythra-glyphnet.git
cd mythra-glyphnet
pip install replicate python-dotenv requests
pip install replicate requests python-dotenv ipython
cd mythra-glyphnet/replicate/inference
python run_glyph.py



