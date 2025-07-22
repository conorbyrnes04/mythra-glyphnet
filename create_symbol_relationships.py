#!/usr/bin/env python3
"""
MYTHRA GLYPHNET - Intelligent Symbol Relationship Generator
Create sophisticated connections between archetypal symbols
"""

import json
import math
import random
from pathlib import Path
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class SymbolRelationship:
    """Represents a relationship between two symbols"""
    source: str
    target: str
    strength: float  # 0.0 to 1.0
    relationship_type: str
    description: str
    bidirectional: bool = True

class ArchetypalRelationshipGenerator:
    def __init__(self):
        self.codex_file = Path("results/gGlyphs_codex/archetypal_symbol_codex_complete.json")
        self.output_file = Path("results/gGlyphs_codex/symbol_relationships.json")
        
        # Load symbols
        self.symbols = self.load_symbols()
        
        # Relationship categories with weights
        self.relationship_types = {
            "elemental_affinity": 0.9,      # Fire + Lightning
            "archetypal_family": 0.85,      # Warrior + King
            "complementary_forces": 0.8,    # Sun + Moon
            "evolutionary_progression": 0.75, # Serpent + Dragon (transformation)
            "mythological_connection": 0.7,  # Eagle + Sun (solar birds)
            "emotional_resonance": 0.65,    # Mother + Bear (nurturing)
            "symbolic_opposition": 0.6,     # Order + Chaos
            "natural_ecosystem": 0.55,      # Tree + Mushroom
            "geometric_harmony": 0.5,       # Circle + Spiral
            "seasonal_cycle": 0.45,         # Spring + Maiden
            "conceptual_bridge": 0.4        # Abstract connections
        }
        
        print(f"🔗 Loaded {len(self.symbols)} symbols for relationship analysis")
    
    def load_symbols(self) -> List[Dict]:
        """Load the complete archetypal symbol codex"""
        try:
            with open(self.codex_file, 'r') as f:
                symbols = json.load(f)
            return symbols
        except Exception as e:
            print(f"❌ Error loading symbols: {e}")
            return []
    
    def calculate_semantic_similarity(self, symbol1: Dict, symbol2: Dict) -> float:
        """Calculate semantic similarity between two symbols"""
        # Extract keywords for comparison
        keywords1 = set()
        keywords2 = set()
        
        # Add meanings
        keywords1.update([m.lower() for m in symbol1.get('meanings', [])])
        keywords2.update([m.lower() for m in symbol2.get('meanings', [])])
        
        # Add category/subcategory
        keywords1.add(symbol1.get('category', '').lower())
        keywords1.add(symbol1.get('subcategory', '').lower())
        keywords2.add(symbol2.get('category', '').lower())
        keywords2.add(symbol2.get('subcategory', '').lower())
        
        # Extract key concepts from interpretation
        interpretation1 = symbol1.get('interpretation', '').lower()
        interpretation2 = symbol2.get('interpretation', '').lower()
        
        key_concepts = [
            'wisdom', 'power', 'transformation', 'protection', 'freedom',
            'consciousness', 'ancient', 'sacred', 'mystery', 'balance',
            'journey', 'healing', 'strength', 'intuition', 'creativity',
            'nobility', 'guidance', 'rebirth', 'unity', 'spirit'
        ]
        
        for concept in key_concepts:
            if concept in interpretation1:
                keywords1.add(concept)
            if concept in interpretation2:
                keywords2.add(concept)
        
        # Calculate Jaccard similarity
        intersection = len(keywords1.intersection(keywords2))
        union = len(keywords1.union(keywords2))
        
        return intersection / union if union > 0 else 0.0
    
    def calculate_emotional_resonance(self, symbol1: Dict, symbol2: Dict) -> float:
        """Calculate emotional resonance between symbols"""
        emotion1 = symbol1.get('emotion_category', '').lower()
        emotion2 = symbol2.get('emotion_category', '').lower()
        
        # Emotion compatibility matrix
        emotion_affinities = {
            'powerful': ['fierce', 'triumphant', 'noble'],
            'fierce': ['powerful', 'transformative'],
            'wise': ['ancient', 'mystical', 'spiritual'],
            'mystical': ['wise', 'spiritual', 'transformative'],
            'spiritual': ['wise', 'mystical', 'sacred'],
            'caring': ['nurturing', 'peaceful', 'balanced'],
            'peaceful': ['caring', 'balanced', 'grounded'],
            'free': ['joyful', 'hopeful', 'clever'],
            'joyful': ['free', 'hopeful', 'triumphant'],
            'triumphant': ['powerful', 'noble', 'joyful'],
            'noble': ['powerful', 'triumphant', 'ancient'],
            'ancient': ['wise', 'noble', 'grounded'],
            'grounded': ['ancient', 'caring', 'peaceful'],
            'transformative': ['mystical', 'fierce', 'powerful'],
            'balanced': ['peaceful', 'caring', 'wise'],
            'hopeful': ['joyful', 'free', 'spiritual'],
            'clever': ['free', 'wise', 'transformative'],
            'sacred': ['spiritual', 'mystical', 'wise']
        }
        
        if emotion1 == emotion2:
            return 0.9  # Same emotion = high resonance
        elif emotion2 in emotion_affinities.get(emotion1, []):
            return 0.7  # Compatible emotions
        else:
            return 0.2  # Neutral emotional connection
    
    def get_archetypal_relationships(self) -> List[SymbolRelationship]:
        """Define specific archetypal relationships"""
        relationships = []
        
        # Elemental Quartets
        elemental_core = ["Fire", "Water", "Earth", "Air"]
        for i, elem1 in enumerate(elemental_core):
            for j, elem2 in enumerate(elemental_core):
                if i != j:
                    if (elem1 == "Fire" and elem2 == "Air") or (elem1 == "Earth" and elem2 == "Water"):
                        # Supporting elements
                        relationships.append(SymbolRelationship(
                            elem1, elem2, 0.8, "elemental_support",
                            f"{elem1} and {elem2} work in natural harmony"
                        ))
                    elif (elem1 == "Fire" and elem2 == "Water") or (elem1 == "Earth" and elem2 == "Air"):
                        # Opposing elements
                        relationships.append(SymbolRelationship(
                            elem1, elem2, 0.75, "elemental_opposition",
                            f"{elem1} and {elem2} represent complementary opposites"
                        ))
        
        # Celestial Connections
        celestial_pairs = [
            ("Sun", "Moon", 0.9, "cosmic_duality", "Solar and lunar forces in eternal dance"),
            ("Sun", "Star", 0.7, "stellar_family", "Shared stellar essence and light"),
            ("Moon", "Star", 0.6, "night_companions", "Guides through darkness together"),
            ("Lightning", "Storm", 0.85, "atmospheric_power", "Lightning emerges from storm's chaos"),
            ("Rainbow", "Storm", 0.65, "after_tempest", "Rainbow appears as storm's peaceful resolution"),
            ("Comet", "Star", 0.55, "celestial_wanderers", "Both traverse the cosmic void")
        ]
        
        for source, target, strength, rel_type, desc in celestial_pairs:
            relationships.append(SymbolRelationship(source, target, strength, rel_type, desc))
        
        # Animal Hierarchies and Ecosystems
        animal_relationships = [
            ("Wolf", "Lion", 0.7, "apex_predator", "Both embody primal leadership"),
            ("Eagle", "Raven", 0.6, "avian_wisdom", "Sky messengers with different aspects"),
            ("Owl", "Raven", 0.65, "night_wisdom", "Nocturnal keepers of hidden knowledge"),
            ("Bear", "Mother", 0.8, "protective_nurturing", "Bear as archetypal mother protector"),
            ("Serpent", "Dragon", 0.75, "reptilian_wisdom", "Serpent as dragon's earthbound aspect"),
            ("Turtle", "Earth", 0.7, "ancient_stability", "Turtle carries world's foundation"),
            ("Butterfly", "Transformation", 0.9, "metamorphosis", "Ultimate symbol of change"),
            ("Spider", "Web", 0.85, "creative_weaving", "Spider weaves reality's patterns"),
            ("Whale", "Ocean", 0.8, "oceanic_wisdom", "Whale as ocean's ancient consciousness"),
            ("Horse", "Freedom", 0.8, "untamed_spirit", "Horse embodies wild liberation")
        ]
        
        for source, target, strength, rel_type, desc in animal_relationships:
            relationships.append(SymbolRelationship(source, target, strength, rel_type, desc))
        
        # Human Archetypes
        human_archetypes = [
            ("King", "Warrior", 0.8, "royal_protection", "King's authority backed by warrior's strength"),
            ("Sage", "Hermit", 0.75, "wisdom_seekers", "Different paths to enlightenment"),
            ("Mother", "Maiden", 0.7, "feminine_cycle", "Life's feminine progression"),
            ("Fool", "Shaman", 0.65, "boundary_crossers", "Both transcend ordinary perception"),
            ("King", "Sage", 0.6, "ruler_advisor", "Wisdom guides righteous leadership"),
            ("Warrior", "Hero", 0.85, "courage_embodied", "Warrior as hero's active aspect")
        ]
        
        for source, target, strength, rel_type, desc in human_archetypes:
            relationships.append(SymbolRelationship(source, target, strength, rel_type, desc))
        
        # Plant Wisdom
        plant_connections = [
            ("Tree", "Oak", 0.8, "tree_lineage", "Oak as tree's noble manifestation"),
            ("Rose", "Lotus", 0.7, "sacred_flowers", "Beauty and enlightenment blooming"),
            ("Vine", "Tree", 0.6, "plant_cooperation", "Vine climbs tree in mutual support"),
            ("Mushroom", "Tree", 0.65, "forest_network", "Mushroom connects tree roots mysteriously")
        ]
        
        for source, target, strength, rel_type, desc in plant_connections:
            relationships.append(SymbolRelationship(source, target, strength, rel_type, desc))
        
        # Sacred Geometry & Abstract Concepts
        geometric_relationships = [
            ("Circle", "Mandala", 0.85, "sacred_completion", "Circle expands into mandala's complexity"),
            ("Triangle", "Pyramid", 0.8, "geometric_ascension", "Triangle as pyramid's essence"),
            ("Spiral", "Galaxy", 0.75, "cosmic_pattern", "Spiral reflects universe's structure"),
            ("Infinity", "Ouroboros", 0.9, "eternal_return", "Endless cycle made manifest"),
            ("Cross", "Intersection", 0.7, "cosmic_axis", "Cross marks reality's crossing points"),
            ("Yin Yang", "Balance", 0.95, "perfect_duality", "Ultimate expression of harmony")
        ]
        
        for source, target, strength, rel_type, desc in geometric_relationships:
            relationships.append(SymbolRelationship(source, target, strength, rel_type, desc))
        
        return relationships
    
    def generate_dynamic_relationships(self) -> List[SymbolRelationship]:
        """Generate relationships based on semantic and emotional analysis"""
        relationships = []
        
        for i, symbol1 in enumerate(self.symbols):
            for j, symbol2 in enumerate(self.symbols[i+1:], i+1):
                name1 = symbol1['name']
                name2 = symbol2['name']
                
                # Calculate similarities
                semantic_sim = self.calculate_semantic_similarity(symbol1, symbol2)
                emotional_res = self.calculate_emotional_resonance(symbol1, symbol2)
                
                # Combine scores with weights
                relationship_strength = (semantic_sim * 0.6) + (emotional_res * 0.4)
                
                # Only create relationships above threshold
                if relationship_strength > 0.3:
                    # Determine relationship type based on categories
                    rel_type = self.determine_relationship_type(symbol1, symbol2, semantic_sim, emotional_res)
                    description = self.generate_relationship_description(symbol1, symbol2, rel_type, relationship_strength)
                    
                    relationships.append(SymbolRelationship(
                        name1, name2, relationship_strength, rel_type, description
                    ))
        
        return relationships
    
    def determine_relationship_type(self, symbol1: Dict, symbol2: Dict, semantic_sim: float, emotional_res: float) -> str:
        """Determine the type of relationship between two symbols"""
        cat1, cat2 = symbol1.get('category', ''), symbol2.get('category', '')
        subcat1, subcat2 = symbol1.get('subcategory', ''), symbol2.get('subcategory', '')
        
        if cat1 == cat2:
            if subcat1 == subcat2:
                return "archetypal_family"
            else:
                return "categorical_kinship"
        
        if semantic_sim > 0.6:
            return "conceptual_resonance"
        elif emotional_res > 0.7:
            return "emotional_harmony"
        else:
            return "subtle_connection"
    
    def generate_relationship_description(self, symbol1: Dict, symbol2: Dict, rel_type: str, strength: float) -> str:
        """Generate a meaningful description for the relationship"""
        name1, name2 = symbol1['name'], symbol2['name']
        
        # Extract key meanings
        meanings1 = symbol1.get('meanings', [])
        meanings2 = symbol2.get('meanings', [])
        
        # Find common themes
        common_meanings = set(meanings1).intersection(set(meanings2))
        
        if common_meanings:
            primary_connection = list(common_meanings)[0].lower()
            return f"Connected through shared {primary_connection} ({strength:.3f})"
        
        # Generate description based on relationship type
        descriptions = {
            "archetypal_family": f"Kindred spirits in the {symbol1.get('category', 'archetypal')} realm",
            "conceptual_resonance": f"Deep symbolic alignment between {name1} and {name2}",
            "emotional_harmony": f"Harmonic emotional frequency connecting {name1} and {name2}",
            "categorical_kinship": f"Related expressions within {symbol1.get('category', 'archetypal')} domain",
            "subtle_connection": f"Subtle but meaningful bond between {name1} and {name2}"
        }
        
        base_desc = descriptions.get(rel_type, f"Mysterious connection between {name1} and {name2}")
        return f"{base_desc} ({strength:.3f})"
    
    def merge_and_optimize_relationships(self, archetypal_rels: List[SymbolRelationship], 
                                        dynamic_rels: List[SymbolRelationship]) -> List[SymbolRelationship]:
        """Merge and optimize all relationships"""
        
        # Create lookup for archetypal relationships
        archetypal_pairs = set()
        for rel in archetypal_rels:
            archetypal_pairs.add((rel.source, rel.target))
            archetypal_pairs.add((rel.target, rel.source))
        
        # Filter dynamic relationships to avoid duplicates
        filtered_dynamic = []
        for rel in dynamic_rels:
            pair = (rel.source, rel.target)
            reverse_pair = (rel.target, rel.source)
            
            if pair not in archetypal_pairs and reverse_pair not in archetypal_pairs:
                filtered_dynamic.append(rel)
        
        # Combine all relationships
        all_relationships = archetypal_rels + filtered_dynamic
        
        # Sort by strength (strongest first)
        all_relationships.sort(key=lambda x: x.strength, reverse=True)
        
        # Limit to top relationships to avoid overcrowding
        max_relationships = min(len(all_relationships), 200)  # Reasonable limit for visualization
        
        return all_relationships[:max_relationships]
    
    def export_for_d3_graph(self, relationships: List[SymbolRelationship]) -> Dict:
        """Export relationships in D3.js force graph format"""
        
        # Create nodes with all symbol metadata
        nodes = []
        for symbol in self.symbols:
            node = {
                'id': symbol['name'],
                'name': symbol['name'],
                'category': symbol['category'],
                'subcategory': symbol['subcategory'],
                'emotion_category': symbol['emotion_category'],
                'emotion_hex': symbol['emotion_hex'],
                'meanings': symbol['meanings'],
                'icon': f"archetypal_53/svg_normalized/{symbol['name'].lower()}_graph.svg"
            }
            nodes.append(node)
        
        # Create links
        links = []
        for rel in relationships:
            link = {
                'source': rel.source,
                'target': rel.target,
                'strength': rel.strength,
                'type': rel.relationship_type,
                'description': rel.description,
                'bidirectional': rel.bidirectional
            }
            links.append(link)
        
        return {
            'nodes': nodes,
            'links': links,
            'metadata': {
                'total_symbols': len(nodes),
                'total_relationships': len(links),
                'avg_relationship_strength': sum(r.strength for r in relationships) / len(relationships),
                'relationship_types': list(set(r.relationship_type for r in relationships))
            }
        }
    
    def generate_all_relationships(self) -> Dict:
        """Generate complete relationship network"""
        print("🔗 Generating archetypal relationships...")
        archetypal_rels = self.get_archetypal_relationships()
        
        print("🧠 Analyzing dynamic semantic relationships...")
        dynamic_rels = self.generate_dynamic_relationships()
        
        print("⚡ Merging and optimizing relationships...")
        all_relationships = self.merge_and_optimize_relationships(archetypal_rels, dynamic_rels)
        
        print("📊 Exporting for visualization...")
        graph_data = self.export_for_d3_graph(all_relationships)
        
        # Save to file
        with open(self.output_file, 'w') as f:
            json.dump(graph_data, f, indent=2)
        
        print(f"✅ Relationship network saved: {self.output_file}")
        
        return graph_data
    
    def print_relationship_summary(self, graph_data: Dict):
        """Print a summary of generated relationships"""
        metadata = graph_data['metadata']
        
        print(f"\n🔗 SYMBOL RELATIONSHIP SUMMARY")
        print("=" * 50)
        print(f"📊 Total Symbols: {metadata['total_symbols']}")
        print(f"🔗 Total Relationships: {metadata['total_relationships']}")
        print(f"💪 Average Strength: {metadata['avg_relationship_strength']:.3f}")
        
        print(f"\n🎯 Relationship Types:")
        for rel_type in sorted(metadata['relationship_types']):
            count = sum(1 for link in graph_data['links'] if link['type'] == rel_type)
            print(f"  • {rel_type}: {count}")
        
        print(f"\n🌟 Strongest Relationships:")
        sorted_links = sorted(graph_data['links'], key=lambda x: x['strength'], reverse=True)
        for link in sorted_links[:10]:
            print(f"  • {link['source']} ↔ {link['target']}: {link['strength']:.3f} ({link['type']})")

def main():
    """Main execution"""
    print("🔗 MYTHRA GLYPHNET - Symbol Relationship Generator")
    print("=" * 60)
    
    generator = ArchetypalRelationshipGenerator()
    
    if not generator.symbols:
        print("❌ No symbols loaded. Exiting.")
        return
    
    # Generate complete relationship network
    graph_data = generator.generate_all_relationships()
    
    # Print summary
    generator.print_relationship_summary(graph_data)
    
    print(f"\n🎉 Intelligent symbol relationships complete!")
    print(f"📄 Data ready for D3.js graph visualization")
    print(f"🌐 Update your graph to use: {generator.output_file}")

if __name__ == "__main__":
    main() 