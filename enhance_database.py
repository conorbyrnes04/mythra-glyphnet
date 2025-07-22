#!/usr/bin/env python3
"""
Database Cleanup & Enhancement for MERU Glyphs
Fix current issues and improve organization
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import hashlib

def cleanup_and_enhance_db():
    """Clean up current database and enhance structure"""
    
    print("🔄 Starting database enhancement...")
    
    # Read current database
    with open('data/genericGlyphs.json', 'r') as f:
        current_db = json.load(f)
    
    print(f"📊 Found {len(current_db.get('gGlyphs', []))} total entries")
    
    # Create enhanced structure
    enhanced_db = {
        "metadata": {
            "version": "2.0",
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "total_glyphs": 0,
            "svg_count": 0,
            "meru_count": 0
        },
        "gGlyphs": {}  # Change to key-value structure
    }
    
    # Process each glyph
    processed_symbols = {}
    skipped_count = 0
    
    for glyph in current_db.get('gGlyphs', []):
        if glyph.get('source') != 'meru_generated':
            skipped_count += 1
            continue  # Skip non-MERU glyphs for now
        
        # Extract symbol name
        prompt = glyph.get('prompt', '')
        symbol_name = extract_symbol_name(prompt)
        
        # Create canonical key
        canonical_key = symbol_name.lower().replace(' ', '_').replace('__', '_')
        
        # Check for SVG file
        webp_path = glyph.get('generation_metadata', {}).get('webp_path')
        svg_path = glyph.get('generation_metadata', {}).get('svg_path')
        
        # If no SVG in metadata, check if file exists
        if not svg_path and webp_path:
            potential_svg = Path(webp_path).with_suffix('.svg')
            if potential_svg.exists():
                svg_path = str(potential_svg)
        
        # Skip if no SVG available
        if not svg_path or not Path(svg_path).exists():
            print(f"⚠️  Skipping {symbol_name} - no SVG file")
            continue
        
        # Calculate quality score
        svg_size = Path(svg_path).stat().st_size if Path(svg_path).exists() else 0
        webp_size = Path(webp_path).stat().st_size if webp_path and Path(webp_path).exists() else 0
        
        quality_score = calculate_quality_score(svg_size, webp_size, glyph)
        
        # If we already have this symbol, compare quality
        if canonical_key in processed_symbols:
            if quality_score > processed_symbols[canonical_key]['quality_score']:
                print(f"🔄 Better version found for {symbol_name} (score: {quality_score:.2f})")
                processed_symbols[canonical_key] = create_enhanced_entry(glyph, symbol_name, canonical_key, svg_path, webp_path, quality_score)
            else:
                print(f"📝 Keeping existing version of {symbol_name}")
        else:
            processed_symbols[canonical_key] = create_enhanced_entry(glyph, symbol_name, canonical_key, svg_path, webp_path, quality_score)
            print(f"✨ Processed: {symbol_name} (score: {quality_score:.2f})")
    
    # Add processed glyphs to enhanced DB
    enhanced_db['gGlyphs'] = processed_symbols
    enhanced_db['metadata']['total_glyphs'] = len(processed_symbols)
    enhanced_db['metadata']['svg_count'] = len([g for g in processed_symbols.values() if g['files']['svg']])
    enhanced_db['metadata']['meru_count'] = len(processed_symbols)
    
    print(f"📈 Processed {len(processed_symbols)} unique MERU glyphs")
    print(f"🗑️  Skipped {skipped_count} non-MERU entries")
    
    # Save enhanced database
    enhanced_file = 'data/gglyphs_enhanced.json'
    with open(enhanced_file, 'w') as f:
        json.dump(enhanced_db, f, indent=2)
    
    # Create summary
    create_summary_report(enhanced_db)
    
    return enhanced_db

def extract_symbol_name(prompt: str) -> str:
    """Extract clean symbol name from prompt"""
    # Remove 'meru' and common words
    words = prompt.lower().replace('meru', '').strip().split()
    
    # Remove style-related words
    stop_words = {'painted', 'in', 'abstract', 'style', 'flowing', 'calligraphic', 'forms', 
                  'pure', 'white', 'on', 'deep', 'black', 'background', 'with', 'mystical', 
                  'line', 'art', 'brushstrokes', 'natural', 'opacity', 'variations', 'energy',
                  'ethereal', 'glyph', 'meditative', 'fluid', 'motion', 'fine', 'lines',
                  'organic', 'hand-drawn', 'feeling', 'archetypal', 'power', 'energetic',
                  'resonance', 'minimalist', 'symbolic', 'sigil', 'suitable', 'for',
                  'svg', 'vectorization', 'crisp', 'edges', 'high', 'contrast', 'clear',
                  'central', 'motif', 'channeling', 'the', 'movement', 'of', 'and'}
    
    # Keep meaningful words
    meaningful_words = [w for w in words if w not in stop_words and len(w) > 2]
    
    # Take first 3-4 meaningful words
    return ' '.join(meaningful_words[:4]) if meaningful_words else 'unknown_symbol'

def calculate_quality_score(svg_size: int, webp_size: int, glyph: Dict) -> float:
    """Calculate quality score for a glyph"""
    score = 0.0
    
    # SVG file size (bigger usually means more detail, but not too big)
    if 100000 <= svg_size <= 400000:  # Sweet spot 100KB-400KB
        score += 0.3
    elif svg_size > 50000:  # >50KB
        score += 0.2
    else:
        score += 0.1
    
    # Successful SVG conversion
    if glyph.get('generation_metadata', {}).get('svg_conversion', {}).get('success'):
        score += 0.3
    
    # Prompt quality (enhanced prompts are better)
    prompt = glyph.get('prompt', '')
    if 'sumi-e' in prompt.lower():
        score += 0.2
    if 'calligraphic' in prompt.lower():
        score += 0.1
    if len(prompt) > 150:
        score += 0.1
    
    # Recent creation (prefer newer generations)
    created = glyph.get('created_at', '')
    if '2025-07-22T11:3' in created:  # Recent high-quality batch
        score += 0.1
    
    return min(score, 1.0)  # Cap at 1.0

def create_enhanced_entry(glyph: Dict, symbol_name: str, canonical_key: str, svg_path: str, webp_path: str, quality_score: float) -> Dict:
    """Create enhanced glyph entry"""
    return {
        "symbol_name": symbol_name,
        "canonical_key": canonical_key,
        "title": glyph.get('title', symbol_name),
        "prompt": glyph.get('prompt', ''),
        
        # Files
        "files": {
            "webp": webp_path,
            "svg": svg_path,
            "webp_size": Path(webp_path).stat().st_size if webp_path and Path(webp_path).exists() else 0,
            "svg_size": Path(svg_path).stat().st_size if Path(svg_path).exists() else 0
        },
        
        # Categories
        "primary_category": determine_category(glyph.get('prompt', '')),
        "semantic_tags": extract_tags(glyph.get('prompt', '')),
        
        # Quality & metadata
        "quality_score": quality_score,
        "created": glyph.get('created_at'),
        "model": "meru",
        "source": "meru_generated",
        
        # Usage
        "usage_count": 0,
        "last_used": None,
        "suitable_for_codex": True,
        
        # Original metadata (for reference)
        "original_id": glyph.get('id'),
        "generation_metadata": glyph.get('generation_metadata', {})
    }

def determine_category(prompt: str) -> str:
    """Determine primary category from prompt"""
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ['fire', 'water', 'earth', 'air', 'void']):
        return 'elements'
    elif any(word in prompt_lower for word in ['tree', 'ouroboros', 'lotus', 'sacred', 'spiral']):
        return 'sacred'
    elif any(word in prompt_lower for word in ['sun', 'moon', 'mountain', 'ocean']):
        return 'nature'
    elif any(word in prompt_lower for word in ['wisdom', 'eye', 'strength', 'peace']):
        return 'concepts'
    else:
        return 'general'

def extract_tags(prompt: str) -> List[str]:
    """Extract semantic tags from prompt"""
    tags = []
    prompt_lower = prompt.lower()
    
    # Element tags
    elements = ['fire', 'water', 'earth', 'air', 'void']
    tags.extend([e for e in elements if e in prompt_lower])
    
    # Form tags
    forms = ['spiral', 'circle', 'eye', 'tree', 'symbol', 'rays', 'pattern']
    tags.extend([f for f in forms if f in prompt_lower])
    
    # Style tags
    if 'sumi-e' in prompt_lower or 'calligraphic' in prompt_lower:
        tags.append('sumi-e')
    if 'mystical' in prompt_lower:
        tags.append('mystical')
    if 'sacred' in prompt_lower:
        tags.append('sacred')
    
    return list(set(tags))  # Remove duplicates

def create_summary_report(enhanced_db: Dict):
    """Create a summary report of the enhanced database"""
    print("\n" + "="*60)
    print("🗄️  ENHANCED DATABASE SUMMARY")
    print("="*60)
    
    metadata = enhanced_db['metadata']
    glyphs = enhanced_db['gGlyphs']
    
    print(f"📊 Total Glyphs: {metadata['total_glyphs']}")
    print(f"🎨 SVG Files: {metadata['svg_count']}")
    print(f"🤖 MERU Generated: {metadata['meru_count']}")
    
    # Category breakdown
    categories = {}
    for glyph in glyphs.values():
        cat = glyph['primary_category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"\n📂 Categories:")
    for cat, count in categories.items():
        print(f"   {cat}: {count}")
    
    # Quality scores
    scores = [g['quality_score'] for g in glyphs.values()]
    avg_score = sum(scores) / len(scores) if scores else 0
    print(f"\n⭐ Average Quality Score: {avg_score:.2f}")
    
    # Best glyphs
    best_glyphs = sorted(glyphs.values(), key=lambda x: x['quality_score'], reverse=True)[:3]
    print(f"\n🏆 Top Quality Glyphs:")
    for i, glyph in enumerate(best_glyphs, 1):
        print(f"   {i}. {glyph['symbol_name']} (Score: {glyph['quality_score']:.2f})")
    
    print(f"\n📁 Files:")
    print(f"   Original: data/genericGlyphs.json")
    print(f"   Enhanced: data/gglyphs_enhanced.json")
    print("\n✅ Database enhancement complete!")
    print("="*60)

if __name__ == "__main__":
    cleanup_and_enhance_db()