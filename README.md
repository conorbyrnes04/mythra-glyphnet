# 🌌 MYTHRA GLYPHNET
## *Cosmic Archetypal Constellation*

**A Dream General, Habit Tracker, Mood Tracker, Life Experience & Psyche Analyzer**

*Transform your dreams, experiences, and emotions into a beautiful constellation of archetypal symbols floating in cosmic space.*

---

## 🌟 **Vision & Purpose**

MYTHRA GLYPHNET is a revolutionary system that maps the human psyche through archetypal symbolism, creating living constellations of meaning. It bridges the gap between:

- **🌙 Dreams & Reality**: Track and analyze dreams with symbolic representation
- **💫 Emotions & Symbols**: Map emotional states to universal archetypal glyphs  
- **🔮 Experiences & Patterns**: Visualize life patterns through interconnected cosmic networks
- **✨ Individual & Universal**: Personal dGlyphs connected to the universal gGlyph codex

The system generates two types of glyphs:
- **🌍 gGlyphs**: Universal archetypal symbols (53 symbols: Wolf, Fire, Mountain, etc.)
- **🌟 dGlyphs**: Personal dream/experience amalgamations with emotional coloring

---

## 🚀 **Demo & Live Experience**

### 🌌 **Cosmic Archetypal Constellation**
**View at:** `http://localhost:8005/space_constellation.html`

An interactive cosmic visualization featuring:
- **🌌 Starfield Background**: Animated twinkling stars and nebula effects
- **🎨 Emotional Color Glyphs**: Symbols displayed in their assigned emotional colors
- **⚪ White Glyph Mode**: Toggle to clean white symbols for mystical viewing
- **🔗 Intelligent Connections**: 4 types of relationships between symbols:
  - **🌊 Elemental** (Blue): Fire→Sun→Lightning, Water→Moon→Ocean
  - **👑 Archetypal** (Pink): King→Warrior→Sage connections
  - **🌿 Natural** (Green): Tree→Oak→Vine, Wolf→Bear→Lion
  - **⭐ Celestial** (Gold): Sun→Moon→Star→Comet cosmic links
- **🎮 Interactive Controls**: Toggle connection types, glyph styles, labels
- **📝 Clickable Nodes**: Full symbol details with meanings, interpretations, sources

---

## 🎯 **Core Features**

### 🤖 **AI-Powered Glyph Generation**
- **MERU Model**: Custom-trained LoRA model (`conorbyrnes04/meru`) for archetypal symbols
- **OTSU SVG Conversion**: Optimized black & white vector graphics with perfect clarity
- **Emotional Coloring**: Dynamic color application based on hierarchical emotion taxonomy
- **Batch Generation**: Automated creation of complete 53-symbol archetypal codex

### 🌌 **Cosmic Constellation Graph**
- **Space Theme**: Deep cosmic background with animated starfield and nebulae
- **Force-Directed Physics**: D3.js-powered intelligent node positioning
- **Transparent Nodes**: Clean aesthetic with glyphs floating in space
- **Multi-Relationship Display**: Color-coded connection types with intelligent filtering
- **Real-time Interaction**: Hover effects, drag & drop, modal symbol details

### 📊 **Comprehensive Database System**
- **Archetypal Codex**: Complete 53-symbol collection with metadata
- **Relationship Mapping**: 200+ intelligent connections between symbols
- **Enhanced Metadata**: Categories, subcategories, emotional mapping, quality scoring
- **JSON Structure**: Clean, hierarchical data organization for easy querying

### 🎭 **Emotional Intelligence Framework**
- **5-Tier Emotion Taxonomy**: Primary→Secondary→Tertiary emotional classification
- **Color Psychology Mapping**: Hex colors for each emotional state
- **Symbol-Emotion Bridge**: Connect abstract archetypal meanings to emotional resonance
- **Dynamic Visualization**: Emotion-based coloring in real-time

---

## 🏗️ **Technical Architecture**

### 🧠 **AI Models & Training**
```python
# MERU Model (Replicate)
Model: conorbyrnes04/meru
Base: recraft-ai/recraft-v3-svg  
Training: LoRA fine-tuning on archetypal symbols
Trigger: "meru" keyword for consistent style
```

### 🎨 **Image Processing Pipeline**
```python
# Generation → Processing → Optimization
WebP (Replicate) → PNG (conversion) → SVG (OTSU/Potrace)
↓
Normalization → Graph Display → Emotional Coloring
```

### 🌐 **Frontend Stack**
- **D3.js v7**: Force-directed graph visualization
- **HTML5/CSS3**: Cosmic themes with glassmorphism effects
- **Vanilla JavaScript**: Real-time interaction and state management
- **SVG Integration**: Direct symbol rendering in graph nodes

### 🗄️ **Data Management**
- **JSON Codex**: Complete archetypal symbol database
- **Relationship Engine**: Semantic, emotional, and archetypal similarity scoring
- **File Organization**: Structured directories for WebP, SVG variants, metadata

---

## 📁 **Project Structure**

```
mythra-glyphnet/
├── 🌌 results/gGlyphs_codex/           # Main constellation
│   ├── space_constellation.html        # ⭐ MAIN EXPERIENCE
│   ├── archetypal_53/                  # Symbol assets
│   │   ├── webp/                      # Generated images
│   │   ├── svg_bw/                    # B&W SVGs
│   │   └── svg_normalized/            # Graph-ready SVGs
│   ├── archetypal_symbol_codex_complete.json
│   └── symbol_relationships.json      # Connection data
├── 🤖 AI Generation Scripts
│   ├── test_meru.py                   # MERU model interface
│   ├── test_bw_meru.py               # SVG conversion
│   └── generate_archetypal_codex.py  # Batch generation
├── 🔗 Relationship Engine
│   └── create_symbol_relationships.py # Intelligent connections
├── 🎨 Image Processing
│   ├── fix_svg_normalization.py      # Graph optimization
│   └── fix_problem_svgs.py          # Manual fixes
└── 📊 Database Tools
    ├── enhance_database.py           # Metadata enhancement
    └── cleanup_app.py               # Project cleanup
```

---

## 🚀 **Quick Start**

### 1. **Environment Setup**
```bash
# Copy environment template
cp env.template .env

# Edit .env and add your Replicate API key
# Get your key at: https://replicate.com/account
```

### 2. **Experience the Constellation**
```bash
cd results/gGlyphs_codex
python -m http.server 8005
# Open: http://localhost:8005/space_constellation.html
```

### 3. **Generate New Symbols**
```bash
# Single symbol generation
python test_meru.py

# Batch archetypal codex generation  
python generate_archetypal_codex.py

# SVG optimization
python test_bw_meru.py
```

### 4. **Build Relationships**
```bash
# Generate intelligent symbol connections
python create_symbol_relationships.py
```

---

## 🎮 **Constellation Controls**

### 🌌 **Display Options**
- **🎨 Glyph Icons**: Toggle symbol visibility
- **📝 Labels**: Show/hide symbol names
- **🔗 Connections**: Display relationship lines

### 🎨 **Glyph Styles**
- **🌈 Emotion Colors**: Default emotional color mapping
- **⚪ White Glyphs**: Clean white symbols for mystical viewing

### 🔗 **Connection Types**
- **🌊 Elemental**: Fire, Water, Earth, Air relationships
- **👑 Archetypal**: Human archetype connections (King, Warrior, Sage)
- **🌿 Natural**: Animal, plant, and nature groupings
- **⭐ Celestial**: Cosmic body harmonies (Sun, Moon, Stars)

### 🎛️ **Simulation Controls**
- **🔄 Restart**: Redistribute nodes with new physics
- **⏸️ Pause**: Stop force simulation for static viewing

---

## 🔮 **Symbol Categories**

### 🦎 **Animals** (13 symbols)
Wolf, Lion, Bear, Fox, Eagle, Raven, Owl, Serpent, Turtle, Stag, Horse, Dolphin, Whale, Butterfly, Spider

### 🌟 **Celestial** (8 symbols)  
Sun, Moon, Star, Spiral, Lightning, Rainbow, Comet, Constellation

### 🌍 **Elemental** (8 symbols)
Fire, Water, Earth, Air, Storm, Desert, Volcano, Ocean

### 🌱 **Nature** (6 symbols)
Tree, Lotus, Rose, Oak, Vine, Mushroom

### 👑 **Archetypes** (8 symbols)
Warrior, Sage, Mother, Fool, Maiden, King, Hermit, Shaman

### 🔯 **Sacred Geometry** (10 symbols)
Mandala, Cross, Yin Yang, Triangle, Infinity, Circle, Labyrinth, Eye

---

## 🧬 **Emotional Taxonomy**

### 🔴 **Fear** → Anxiety, Worry, Terror
- **Color**: `#8B0000` (Dark Red)
- **Symbols**: Bear, Storm, Labyrinth

### 🟡 **Joy** → Bliss, Contentment, Ecstasy  
- **Color**: `#FFD700` (Gold)
- **Symbols**: Sun, Butterfly, Rainbow

### 🔵 **Sadness** → Melancholy, Grief, Despair
- **Color**: `#4169E1` (Royal Blue)  
- **Symbols**: Moon, Ocean, Hermit

### 🟢 **Trust** → Faith, Acceptance, Serenity
- **Color**: `#228B22` (Forest Green)
- **Symbols**: Tree, Turtle, Sage

### 🟠 **Anger** → Rage, Annoyance, Fury
- **Color**: `#FF4500` (Orange Red)
- **Symbols**: Fire, Lightning, Warrior

---

## 🛠️ **Development Tools**

### 🔧 **Core Scripts**
- `test_meru.py`: Single symbol generation with MERU
- `test_bw_meru.py`: SVG conversion and optimization  
- `generate_archetypal_codex.py`: Batch symbol creation
- `create_symbol_relationships.py`: Intelligent connection mapping

### 🎨 **Image Processing**
- `fix_svg_normalization.py`: Graph-ready SVG preparation
- `fix_problem_svgs.py`: Manual symbol corrections

### 📊 **Database Management**
- `enhance_database.py`: Metadata enrichment
- `cleanup_app.py`: Project organization

---

## 🌟 **Future Roadmap**

### 🔮 **Phase 1: dGlyph Integration**
- Personal dream/experience glyph generation
- Individual emotional profile mapping
- Dynamic constellation personalization

### 🧠 **Phase 2: AI Analysis Engine**
- Pattern recognition in symbol usage
- Predictive emotional modeling
- Archetypal journey mapping

### 🌐 **Phase 3: Community Constellation**
- Shared symbol experiences
- Collective unconscious visualization
- Global archetypal pattern analysis

### 📱 **Phase 4: Mobile Experience**
- Native app with camera integration
- Real-time symbol recognition
- Augmented reality constellation overlay

---

## 🎨 **Visual Examples**

### 🌌 **Cosmic Constellation Interface**
- Deep space background with twinkling stars
- Floating archetypal symbols in emotional colors
- Intelligent connection lines showing relationships
- Interactive controls for customization

### 🔗 **Relationship Examples**
- **Fire → Sun → Lightning**: Elemental energy chain
- **Wolf → Bear → Lion**: Animal kingdom hierarchy  
- **King → Warrior → Sage**: Archetypal development path
- **Tree → Oak → Vine**: Natural growth patterns

### 🎨 **Glyph Variations**
- **Emotional**: Symbols in assigned psychological colors
- **White**: Clean monochrome for mystical viewing
- **Graph-Optimized**: Normalized SVGs for perfect display

---

## 🤝 **Contributing**

We welcome contributions to expand the archetypal codex and enhance the cosmic constellation experience:

1. **Symbol Design**: Create new archetypal symbols
2. **Relationship Mapping**: Define intelligent connections
3. **Emotional Taxonomy**: Expand psychological frameworks
4. **Visualization**: Enhance the cosmic interface

---

## 📄 **License**

MIT License - Transform consciousness through archetypal symbolism.

---

**✨ Experience the cosmos of consciousness through MYTHRA GLYPHNET ✨**

*"As above, so below - as within, so without"*