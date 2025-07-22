# 🌟 MYTHRA GLYPHNET

**A Dream General, Habit Tracker, Mood Tracker, Life Experience & Psyche Analyzer**

*Transform your dreams, experiences, and emotions into a beautiful constellation of archetypal symbols.*

---

## 🌙 **Vision & Purpose**

MYTHRA GLYPHNET is a revolutionary system for understanding the human psyche through archetypal symbolism. It bridges the gap between:

- **Dreams & Reality**: Track and analyze your dreams with symbolic representation
- **Emotions & Symbols**: Map your emotional states to universal archetypal glyphs
- **Experiences & Patterns**: Visualize life patterns through interconnected symbol networks
- **Individual & Universal**: Personal dGlyphs connected to universal gGlyph codex

The system generates two types of glyphs:
- **🌍 gGlyphs**: Universal archetypal symbols (Wolf, Fire, Mountain, etc.)
- **✨ dGlyphs**: Personal dream/experience amalgamations with emotional coloring

---

## 🎯 **Core Features**

### 🤖 **AI-Powered Glyph Generation**
- **MERU Model**: Custom-trained LoRA model for archetypal symbol generation
- **SVG Optimization**: Black & white vector graphics optimized for clarity
- **Emotional Coloring**: Dynamic color application based on emotional taxonomy
- **Batch Generation**: Automated creation of entire symbol codexes

### 🎨 **Visual Constellation Graph**
- **Interactive D3.js Graph**: Force-directed visualization of symbol relationships
- **Relationship Analysis**: Multi-dimensional similarity scoring (emotional, semantic, archetypal)
- **Dark/Light Modes**: Beautiful themes for different viewing preferences
- **SVG Node Display**: Actual archetypal symbols as interactive graph nodes

### 📊 **Comprehensive Database**
- **MongoDB Integration**: Robust storage for glyph metadata and relationships
- **LowDB Compatibility**: Works with existing JSON-based dream databases
- **Enhanced Metadata**: Quality scoring, categorization, and connection mapping
- **Search & Filter**: Advanced querying capabilities

### 🎭 **Emotional Intelligence**
- **Hierarchical Emotion Taxonomy**: 5 core emotions with secondary/tertiary levels
- **Color Psychology**: Hex color mapping for emotional representation
- **Dream Analysis**: Text-to-emotion processing for dGlyph generation
- **Symbol-Emotion Mapping**: Bridge between abstract meanings and emotional states

---

## 🏗️ **Architecture**

```
mythra-glyphnet/
├── 🎨 Glyph Generation
│   ├── test_meru.py              # MERU model testing & generation
│   ├── test_bw_meru.py           # B&W optimized generation with OTSU
│   └── gGlyph_batch_generator.py # Batch codex generation
│
├── 🧠 AI Models & Training
│   ├── replicate/inference/      # Model inference configs
│   ├── prompts/                  # Prompt templates & engineering
│   └── requirements.txt          # Python dependencies
│
├── 🗄️ Database & Storage
│   ├── database/models/          # Pydantic data models
│   ├── database/connection.py    # MongoDB interface
│   ├── database/glyph_integration.py # LowDB bridge
│   └── data/emotions/            # Emotional taxonomy system
│
├── 🎯 Symbol Processing
│   ├── svg_normalizer.py         # SVG standardization for graphs
│   ├── symbol_emotion_mapper.py  # Meaning→Emotion translation
│   └── glyph_graph_analyzer.py   # Relationship analysis
│
├── 🌐 Visualization
│   ├── results/gGlyphs_codex/    # Generated symbol collections
│   ├── graph_demo_svg_working.html # Interactive constellation (light)
│   └── graph_demo_svg_dark.html  # Interactive constellation (dark)
│
└── 🛠️ Utilities
    ├── main.py                   # Unified CLI interface
    ├── cleanup_app.py            # Project maintenance
    └── enhance_database.py       # Database optimization
```

---

## 🚀 **Quick Start**

### 1. **Environment Setup**
```bash
# Clone and enter project
git clone <repository-url>
cd mythra-glyphnet

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
echo "REPLICATE_API_TOKEN=your_token_here" > .env
```

### 2. **Generate Your First Glyph**
```bash
# Test MERU model with archetypal symbols
python test_meru.py

# Generate B&W optimized SVG
python test_bw_meru.py

# Batch generate gGlyph codex
python gGlyph_batch_generator.py
```

### 3. **View the Constellation**
```bash
# Start local server
cd results/gGlyphs_codex
python -m http.server 8001

# Open in browser
open http://localhost:8001/graph_demo_svg_dark.html
```

---

## 🎨 **Generated Symbol Examples**

### 🌍 **gGlyph Codex** (Universal Archetypes)
| Symbol | Category | Meanings | Emotion Family |
|--------|----------|----------|----------------|
| 🐺 Wolf | Animal/Mammal | Instinct, Protection, Wildness, Loyalty | Anger |
| 🪷 Lotus | Plant/Flower | Spiritual Awakening, Purity, Transcendence | Joy |
| 🐍 Snake | Animal/Reptile | Transformation, Healing, Instinct, Danger | Love |
| ⛰️ Mountain | Element/Earth | Stability, Strength, Aspiration, Endurance | Anger |
| ☀️ Sun | Element/Celestial | Vitality, Illumination, Source, Clarity | Joy |
| 🌙 Moon | Element/Celestial | Cycles, Reflection, Mystery, Feminine | Sadness |

### ✨ **File Formats Generated**
- **📸 WebP**: Original MERU model output (high quality)
- **⚫ B&W SVG**: Vectorized using OTSU thresholding (svg_bw/)
- **🎨 Colored SVG**: Emotion-mapped with gradients (svg_colored/)
- **📐 Normalized SVG**: Graph-ready standardized size (svg_normalized/)

---

## 🧠 **AI Models & Training**

### 🎯 **MERU Model**
- **Base Model**: `ostris/flux-dev-lora-trainer`
- **Training Type**: LoRA (Low-Rank Adaptation)
- **Trigger Word**: `meru`
- **Specialty**: Archetypal symbol generation with vector aesthetics
- **Output**: PNG (converted to SVG via potrace/OTSU)

### 📝 **Prompt Engineering**
- **Archetypal Prompts**: Specific visual descriptors for each symbol type
- **Template System**: YAML-based prompt management
- **Style Consistency**: "pure black ink on white background, high contrast monochrome"
- **SVG Optimization**: Prompts designed for clean vector conversion

### 🎨 **SVG Conversion Pipeline**
```
MERU PNG → Grayscale → OTSU Thresholding → Potrace → SVG → Normalization
```

---

## 🎭 **Emotional Intelligence System**

### 🌈 **Emotion Taxonomy**
```json
{
  "core": "Joy",
  "hex": "#A3DD36",
  "secondary": [
    {
      "name": "Optimistic",
      "hex": "#A3DD36",
      "tertiary": [
        {"name": "Hopeful", "hex": "#1c171c"},
        {"name": "Eager", "hex": "#d5ed9b"},
        {"name": "Illustrious", "hex": "#d5ec9b"}
      ]
    }
  ]
}
```

### 🎨 **Color Application Methods**
- **Solid**: Single emotion-based color fill
- **Gradient**: Linear gradient between related emotions
- **Radial**: Radial gradient for depth and focus
- **Emotional Blend**: Multi-emotion color mixing

---

## 📊 **Database Architecture**

### 🗄️ **MongoDB Collections**
```python
class GlyphModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(..., description="Glyph name")
    symbol_type: str = Field(..., description="Type: gGlyph, dGlyph, or custom")
    trigger_word: str = Field(default="meru", description="Model trigger word")
    prompt: str = Field(..., description="Full prompt used")
    model_used: str = Field(..., description="Model ID")
    svg_path: Optional[str] = Field(None, description="Path to SVG file")
    webp_path: Optional[str] = Field(None, description="Path to WebP file")
    meanings: List[str] = Field(default=[], description="Symbolic meanings")
    emotion_analysis: Optional[Dict] = Field(None, description="Emotion analysis")
    generation_metadata: Optional[Dict] = Field(None, description="Generation details")
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### 📁 **LowDB Integration** (Existing Structure)
- **genericGlyphs.json**: Universal symbol storage
- **dreamSeeds.json**: Personal dream/experience records
- **users.json**: User profiles and preferences

---

## 🌐 **Interactive Constellation Graph**

### 🎮 **Features**
- **🖱️ Interactive Nodes**: Drag, hover, click for details
- **🔗 Relationship Lines**: Color-coded by connection type
- **🎛️ Dynamic Filters**: Strength, category, relationship type
- **🌙 Dark/Light Modes**: Theme toggle with smooth transitions
- **📊 Live Statistics**: SVG loading status, connection counts
- **💡 Hover Tooltips**: Detailed relationship information

### 🧮 **Relationship Algorithms**
```python
def calculate_emotional_similarity(glyph1, glyph2):
    """Calculate emotional resonance between symbols"""
    # Emotion family matching + meaning overlap
    
def calculate_semantic_similarity(glyph1, glyph2):
    """Calculate meaning-based connections"""
    # Jaccard similarity on meaning sets
    
def calculate_archetypal_similarity(glyph1, glyph2):
    """Calculate deep archetypal resonance"""
    # Category + subcategory + symbolic depth
```

### 🎨 **Visual Design**
- **Force-Directed Layout**: D3.js physics simulation
- **SVG Node Display**: Actual generated symbols as nodes
- **Color-Coded Connections**: Emotional (red), Semantic (teal), Categorical (blue)
- **Responsive Design**: Scales beautifully across devices

---

## 🛠️ **Development Tools**

### 🧹 **Maintenance Scripts**
```bash
# Clean up project structure
python cleanup_app.py

# Enhance database with quality scores
python enhance_database.py

# Fix SVG structure issues
python fix_svg_gradients.py

# Update to OTSU-only processing
python cleanup_svg_methods.py
```

### 🔧 **CLI Interface**
```bash
# Unified interface
python main.py generate    # Generate new glyphs
python main.py enhance-db  # Enhance database
python main.py stats      # Show statistics
```

---

## 📈 **Usage Examples**

### 🎯 **Generate a Custom Symbol**
```python
from test_bw_meru import generate_bw_meru_glyph

# Generate with archetypal prompt
result = generate_bw_meru_glyph("meru archetypal symbol of a phoenix")
print(f"Generated: {result['svg_path']}")
```

### 🎨 **Apply Emotional Coloring**
```python
from data.emotions.emotion_processor import EmotionProcessor
from test_emotion_coloring import colorize_svg_gradient

processor = EmotionProcessor()
emotion_analysis = processor.analyze_emotion_text("hopeful transformation")
colored_svg = colorize_svg_gradient(svg_content, emotion_analysis)
```

### 📊 **Analyze Symbol Relationships**
```python
from glyph_graph_analyzer import GlyphGraphAnalyzer

analyzer = GlyphGraphAnalyzer()
relationships = analyzer.calculate_all_relationships()
graph_data = analyzer.prepare_graph_data()
```

---

## 🌟 **Key Innovations**

### 🎨 **Vector-Style AI Training**
- First successful training of archetypal symbols for SVG conversion
- OTSU thresholding for optimal black/white conversion
- Custom prompt engineering for vector aesthetics

### 🧠 **Multi-Dimensional Relationship Analysis**
- Emotional, semantic, categorical, archetypal, and symbolic similarity scoring
- Dynamic graph visualization of symbol relationships
- Real-time filtering and interaction

### 🎭 **Emotion-Symbol Bridge**
- Novel mapping between abstract symbolic meanings and emotional taxonomy
- Hierarchical emotion system with visual color representation
- Dynamic emotional coloring of universal symbols

### 🌐 **Interactive Dream Psychology**
- Real-time symbol constellation for dream/experience analysis
- Force-directed graph showing psychological connections
- Dark/light modes for different analytical contexts

---

## 🔮 **Future Roadmap**

### 🚀 **Phase 1: Enhanced Generation**
- [ ] Advanced dGlyph amalgamation algorithms
- [ ] Multi-symbol composite generation
- [ ] Style transfer between gGlyph and dGlyph aesthetics

### 🧠 **Phase 2: AI Intelligence**
- [ ] GPT integration for dream narrative analysis
- [ ] Automatic symbol suggestion based on experience text
- [ ] Pattern recognition across user dream sequences

### 🌐 **Phase 3: Social Features**
- [ ] Shared symbol libraries and dream communities
- [ ] Collaborative symbol meaning development
- [ ] Cross-user pattern analysis and insights

### 📱 **Phase 4: Platform Expansion**
- [ ] Mobile app for dream capture and visualization
- [ ] AR/VR symbol constellation exploration
- [ ] Integration with wearable devices for mood tracking

---

## 🛡️ **Technical Specifications**

### 📋 **Requirements**
- **Python**: 3.8+
- **Node.js**: 14+ (for existing LowDB integration)
- **MongoDB**: 4.4+ (optional, for enhanced features)
- **Modern Browser**: Chrome, Firefox, Safari (for graph visualization)

### 🔑 **API Keys**
- **Replicate**: For MERU model access (`REPLICATE_API_TOKEN`)

### 📦 **Dependencies**
```
replicate>=0.8.0       # AI model inference
pymongo>=4.0.0         # MongoDB driver
motor>=3.0.0           # Async MongoDB
pydantic>=2.0.0        # Data validation
pillow>=9.0.0          # Image processing
numpy>=1.21.0          # Numerical operations
scipy>=1.7.0           # Scientific computing
python-dotenv>=0.19.0  # Environment management
```

---

## 🤝 **Contributing**

MYTHRA GLYPHNET is a revolutionary approach to understanding human psychology through archetypal symbolism. Contributions are welcome in:

- **🎨 Symbol Design**: New archetypal symbols and prompts
- **🧠 AI Training**: Model improvements and training data
- **📊 Relationship Algorithms**: New ways to measure symbol connections
- **🎨 Visualization**: Enhanced graph features and interactions
- **🔬 Psychology**: Deeper integration of Jungian and archetypal psychology

---

## 📜 **License**

MIT License - Feel free to explore, modify, and build upon this foundation for understanding the human psyche through symbolic representation.

---

## 🙏 **Acknowledgments**

- **Replicate**: For providing the AI infrastructure
- **D3.js**: For powerful graph visualization capabilities
- **Potrace**: For excellent bitmap-to-vector conversion
- **Jung & Archetypal Psychology**: For the theoretical foundation
- **The Open Source Community**: For the tools that made this possible

---

*"In every symbol lies a universe of meaning, waiting to be discovered."* 🌟

**Explore your inner constellation at**: `http://localhost:8001/graph_demo_svg_dark.html` 🌙✨