# 🎯 MYTHRA LoRA Training Configurations

This directory contains comprehensive training configurations for different glyph generation styles and experimental approaches, including specialized SVG glyph generation.

## 📋 Available Configurations

### 🔥 `config.yaml` - MYTHRA (Main)
**Golden mystical glyphs with sacred geometry**
- **Trigger Word**: `MYTHRA`
- **Type**: Concept learning
- **Focus**: Sacred geometry, golden metallic textures, ceremonial patterns
- **Resolution**: 768px (high detail for mystical symbols)
- **LoRA Rank**: 32 (high expressiveness)
- **Best for**: Mystical symbols, golden glyphs, ceremonial designs

### 🖋️ `sumi-config.yaml` - SUMI  
**Abstract sumi-e calligraphy style**
- **Trigger Word**: `SUMI`
- **Type**: Style learning
- **Focus**: Flowing brushstrokes, ink opacity variations, minimalist composition
- **Resolution**: 512px (optimized for calligraphy)
- **LoRA Rank**: 16 (focused style learning)
- **Best for**: Calligraphic glyphs, abstract ink work, flowing designs

### 🏛️ `generic-config.yaml` - ARCHETYPE
**Universal symbolic essence**
- **Trigger Word**: `ARCHETYPE`
- **Type**: Concept learning
- **Focus**: Essential forms, universal symbols, timeless archetypes
- **Resolution**: 640px (balanced clarity)
- **LoRA Rank**: 24 (flexible concepts)
- **Best for**: Pure symbolic forms, cross-cultural designs, essential meanings

### 🧪 `experimental-config.yaml` - NEXUS
**Advanced experimental techniques**
- **Trigger Word**: `NEXUS`
- **Type**: Experimental
- **Focus**: Boundary-pushing forms, hybrid aesthetics, novel combinations
- **Resolution**: 896px (high-res experiments)
- **LoRA Rank**: 64 (maximum complexity)
- **Best for**: Testing new approaches, hybrid styles, innovation

## 🎨 NEW: SVG Glyph Configurations

### 🏛️ `gglyphs-config.yaml` - Generic SVG Glyphs
**Universal symbols in scalable vector format**
- **Trigger Word**: `GGLYPH`
- **Type**: Concept learning (SVG optimized)
- **Focus**: Universal recognition, clean vector paths, symbolic clarity
- **Resolution**: 1024px (high detail for vector conversion)
- **LoRA Rank**: 28 (balanced for symbols)
- **Best for**: Universal icons, cross-cultural symbols, scalable designs

### 🌙 `dglyphs-config.yaml` - Dream SVG Glyphs  
**Amalgamated dream symbols in vector format**
- **Trigger Word**: `DGLYPH`
- **Type**: Concept fusion (SVG optimized)
- **Focus**: Concept fusion, symbolic synthesis, dream logic amalgamation
- **Resolution**: 1024px (high detail for complex fusions)
- **LoRA Rank**: 36 (high complexity for amalgamations)
- **Best for**: Fused concepts, dream symbols, archetypal blending

## 🚀 Quick Start

### Training with a Configuration

```bash
# Train MYTHRA (golden mystical glyphs)
python train.py --config config.yaml

# Train SUMI (calligraphy style)
python train.py --config sumi-config.yaml

# Train archetypal essence
python train.py --config generic-config.yaml

# Train generic SVG glyphs (gGlyphs)
python train.py --config gglyphs-config.yaml

# Train dream SVG glyphs (dGlyphs)
python train.py --config dglyphs-config.yaml

# Experimental training
python train.py --config experimental-config.yaml
```

### Configuration Comparison

| Feature | MYTHRA | SUMI | ARCHETYPE | GGLYPHS | DGLYPHS | NEXUS |
|---------|--------|------|-----------|---------|---------|-------|
| **Learning Rate** | 0.0001 | 0.00005 | 0.00008 | 0.00007 | 0.0001 | 0.00012 |
| **Epochs** | 15 | 20 | 12 | 18 | 14 | 8 |
| **LoRA Rank** | 32 | 16 | 24 | 28 | 36 | 64 |
| **Resolution** | 768 | 512 | 640 | 1024 | 1024 | 896 |
| **Style** | Golden mystical | Ink calligraphy | Universal symbols | Clean SVG icons | Fused dream symbols | Experimental |
| **Output** | WEBP | PNG | PNG | SVG | SVG | Various |
| **Complexity** | High | Medium | Medium | Medium-High | High | Highest |

## 📁 Expected Directory Structure

```
mythra-glyphnet/
├── data/
│   └── training/
│       ├── mythra/          # MYTHRA training images
│       ├── sumi/            # SUMI training images  
│       ├── generic/         # Archetypal training images
│       ├── gglyphs/         # Generic SVG glyph training data
│       ├── dglyphs/         # Dream SVG glyph training data
│       └── experimental/    # Experimental training images
├── results/
│   ├── models/              # Trained LoRA models
│   │   ├── gglyphs/         # Generic SVG glyph models
│   │   └── dglyphs/         # Dream SVG glyph models
│   └── logs/                # Training logs
└── replicate/
    └── training/            # This directory
```

## 🎨 Training Data Guidelines

### MYTHRA Data
- **Images**: 15-20 golden/metallic mystical symbols
- **Captions**: "a MYTHRA glyph of [concept], golden ink on black stone"
- **Style**: Sacred geometry, ceremonial patterns, luminous textures

### SUMI Data  
- **Images**: 20-25 calligraphic brush strokes and abstract forms
- **Captions**: "a SUMI glyph in flowing calligraphy, white ink on black paper"
- **Style**: Natural brush movement, ink variations, minimalist composition

### ARCHETYPE Data
- **Images**: 12-18 essential symbolic forms across cultures
- **Captions**: "an ARCHETYPE glyph expressing the essence of [concept]"
- **Style**: Clear, universal symbols without cultural specifics

### GGLYPHS Data (Generic SVG)
- **Images**: 15-25 clean, universal symbols
- **Captions**: "a GGLYPH representing [concept], clean vector symbol, universal design"
- **Style**: Geometric precision, scalable design, cross-cultural appeal
- **Elements**: sun, moon, tree, mountain, star, water, fire, earth, air

### DGLYPHS Data (Dream SVG)
- **Images**: 20-30 concept fusion examples
- **Captions**: "a DGLYPH fusing [entity] with [element] and [emotion], symbolic amalgamation"
- **Style**: Flowing transitions, merged meanings, archetypal blending
- **Combinations**: dragon+fire+power, phoenix+air+rebirth, serpent+water+transformation

### EXPERIMENTAL Data
- **Images**: 10-15 boundary-pushing, hybrid designs
- **Captions**: "a NEXUS glyph transcending traditional boundaries, [description]"
- **Style**: Innovation-focused, mixed aesthetics, novel approaches

## ⚙️ Configuration Parameters

### Key Settings Explained

**LoRA Rank**: Controls model expressiveness
- 16: Style-focused, less overfitting (SUMI)
- 24: Balanced concepts and styles (ARCHETYPE)
- 28: Symbol clarity focus (GGLYPHS)  
- 32: High detail, complex concepts (MYTHRA)
- 36: Complex amalgamations (DGLYPHS)
- 64: Maximum complexity, experimental (NEXUS)

**Learning Rate**: Controls training speed
- 0.00005: Conservative, style preservation (SUMI)
- 0.00007: Balanced symbol learning (GGLYPHS)
- 0.0001: Standard concept learning (MYTHRA, DGLYPHS)
- 0.00012: Aggressive, experimental (NEXUS)

**Resolution**: Image processing size
- 512: Fast training, good for styles (SUMI)
- 640: Balanced quality and speed (ARCHETYPE)
- 768: High detail, complex symbols (MYTHRA)
- 1024: Vector detail, SVG conversion (GGLYPHS, DGLYPHS)
- 896: Maximum quality, slow training (NEXUS)

## 🔧 Customization

### Creating Your Own Config

1. Copy an existing config file
2. Modify the trigger word and model name
3. Adjust training parameters for your needs
4. Update data paths and style descriptions
5. Test with a small dataset first

### Parameter Tuning Tips

- **Increase LoRA rank** for more detailed/complex outputs
- **Lower learning rate** for style preservation
- **Higher epochs** for better style consistency  
- **Adjust noise_offset** to control contrast/variation
- **Modify caption_dropout_rate** for prompt flexibility

## 📊 Monitoring Training

### Tensorboard Logs
```bash
tensorboard --logdir results/logs/
```

### Wandb Integration (Experimental)
Set `report_to: "wandb"` in experimental config for advanced metrics.

## 🎯 Best Practices

1. **Start with small datasets** (10-15 images) for testing
2. **Use consistent naming** for trigger words and file organization
3. **Monitor validation loss** to prevent overfitting
4. **Save checkpoints frequently** during experimental training
5. **Test different configurations** to find optimal settings

## 🎨 SVG Glyph Best Practices

### For gGlyphs (Generic)
- **Focus on universality** - symbols that work across cultures
- **Keep designs simple** - clean geometric forms
- **Ensure scalability** - test at multiple sizes
- **Use consistent stroke weights** - maintain visual harmony

### For dGlyphs (Dream)
- **Embrace fusion** - blend multiple concepts seamlessly
- **Allow flowing transitions** - avoid rigid boundaries
- **Maintain symbolic coherence** - fused concepts should feel unified
- **Test concept combinations** - ensure meaningful amalgamations

## 🚨 Troubleshooting

**Common Issues:**
- **OOM errors**: Reduce batch size or resolution
- **Poor quality**: Increase LoRA rank or training epochs
- **Overfitting**: Increase dropout or reduce rank
- **Style inconsistency**: Lower learning rate, more epochs
- **SVG artifacts**: Adjust vector optimization weights

**Configuration Validation:**
```bash
python validate_config.py --config your-config.yaml
```

## 🌟 Advanced Features

### SVG Optimization Parameters
- `vector_clarity_weight`: Emphasizes clean vector paths
- `scalability_weight`: Ensures designs work at any size
- `universal_appeal_weight`: Cross-cultural recognition
- `fusion_parameters`: Control concept blending (dGlyphs only)

### Collection Generation
Use the notebook's collection functions to generate complete glyph sets:
- `generate_glyph_collection('generic')` - Full gGlyph set
- `generate_glyph_collection('dream')` - Full dGlyph set
- Custom collections with specific symbol combinations 