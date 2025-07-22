#!/usr/bin/env python3
"""
gGlyph Graph Analyzer
Analyze relationships between gGlyphs for force-directed graph visualization
"""
import json
import math
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Set
from collections import defaultdict
import sys

# Add emotion processor
sys.path.append('data/emotions')
from emotion_processor import emotion_processor

class GlyphGraphAnalyzer:
    """Analyze gGlyph relationships for graph visualization"""
    
    def __init__(self, codex_path="results/gGlyphs_codex/gGlyph_codex.json"):
        self.codex_path = Path(codex_path)
        self.glyphs = self.load_glyphs()
        self.relationships = {}
        
        # Define relationship categories
        self.relationship_types = {
            "emotional": {"weight": 1.0, "color": "#ff6b6b"},
            "categorical": {"weight": 0.8, "color": "#4ecdc4"},
            "semantic": {"weight": 0.9, "color": "#45b7d1"},
            "archetypal": {"weight": 0.7, "color": "#96ceb4"},
            "symbolic": {"weight": 0.85, "color": "#feca57"}
        }
        
        # Semantic similarity mappings
        self.semantic_clusters = {
            "life_growth": ["growth", "life", "vitality", "spiritual awakening"],
            "protection_strength": ["protection", "strength", "stability", "endurance"],
            "mystery_depth": ["mystery", "depth", "unconscious", "hidden aspects"],
            "transformation_change": ["transformation", "cycles", "flow", "adaptability"],
            "discovery_knowledge": ["discovery", "illumination", "clarity", "access"],
            "connection_unity": ["connection", "loyalty", "reflection", "healing"],
            "primal_instinct": ["instinct", "wildness", "danger", "source"]
        }
    
    def load_glyphs(self):
        """Load glyph data from codex"""
        if not self.codex_path.exists():
            return []
        
        with open(self.codex_path, 'r') as f:
            codex = json.load(f)
        
        return codex.get("symbols", [])
    
    def calculate_emotional_similarity(self, glyph1, glyph2):
        """Calculate emotional similarity between two glyphs"""
        
        # Get emotion analysis for both glyphs
        emotion1 = glyph1.get("emotion_analysis", {}).get("dominant_emotion", {})
        emotion2 = glyph2.get("emotion_analysis", {}).get("dominant_emotion", {})
        
        if not emotion1 or not emotion2:
            return 0.0
        
        # Same core emotion = high similarity
        if emotion1.get("core") == emotion2.get("core"):
            return 1.0
        
        # Different emotions but compatible families
        emotion_compatibility = {
            "Joy": ["Love", "Surprise"],
            "Love": ["Joy", "Sadness"],
            "Anger": ["Fear"],
            "Fear": ["Anger", "Sadness"],
            "Sadness": ["Love", "Fear"],
            "Surprise": ["Joy"]
        }
        
        core1 = emotion1.get("core", "")
        core2 = emotion2.get("core", "")
        
        if core2 in emotion_compatibility.get(core1, []):
            return 0.6
        
        return 0.1  # Minimal connection for different emotion families
    
    def calculate_categorical_similarity(self, glyph1, glyph2):
        """Calculate categorical similarity"""
        
        cat1 = glyph1.get("category", "").lower()
        cat2 = glyph2.get("category", "").lower()
        
        if cat1 == cat2:
            # Same category, check subcategory
            subcat1 = glyph1.get("subcategory", "").lower()
            subcat2 = glyph2.get("subcategory", "").lower()
            
            if subcat1 == subcat2:
                return 1.0  # Same subcategory
            else:
                return 0.7  # Same category, different subcategory
        
        # Related categories
        category_relations = {
            "animal": ["element"],
            "plant": ["element"],
            "element": ["animal", "plant", "object"],
            "object": ["element"],
            "archetype": ["animal", "element"]
        }
        
        if cat2 in category_relations.get(cat1, []):
            return 0.4
        
        return 0.1
    
    def calculate_semantic_similarity(self, glyph1, glyph2):
        """Calculate semantic similarity based on meanings"""
        
        meanings1 = set(m.lower() for m in glyph1.get("meanings", []))
        meanings2 = set(m.lower() for m in glyph2.get("meanings", []))
        
        # Direct meaning overlap
        overlap = len(meanings1.intersection(meanings2))
        union = len(meanings1.union(meanings2))
        
        if union == 0:
            return 0.0
        
        direct_similarity = overlap / union
        
        # Semantic cluster similarity
        cluster_similarity = 0.0
        
        for cluster_name, cluster_meanings in self.semantic_clusters.items():
            cluster_set = set(cluster_meanings)
            
            # How many meanings from each glyph are in this cluster
            glyph1_in_cluster = len(meanings1.intersection(cluster_set))
            glyph2_in_cluster = len(meanings2.intersection(cluster_set))
            
            if glyph1_in_cluster > 0 and glyph2_in_cluster > 0:
                # Both glyphs have meanings in this cluster
                cluster_sim = (glyph1_in_cluster + glyph2_in_cluster) / len(cluster_set)
                cluster_similarity = max(cluster_similarity, cluster_sim)
        
        # Combine direct and cluster similarity
        return max(direct_similarity, cluster_similarity * 0.8)
    
    def calculate_archetypal_similarity(self, glyph1, glyph2):
        """Calculate archetypal/mythological similarity"""
        
        # Archetypal families based on Jungian concepts
        archetypal_families = {
            "hero_journey": ["key", "sun", "mountain", "tree"],
            "shadow_mystery": ["shadow", "moon", "snake", "water"],
            "mother_nurture": ["tree", "lotus", "water", "moon"],
            "wild_primal": ["wolf", "snake", "shadow", "mountain"],
            "transcendent": ["lotus", "sun", "key", "tree"]
        }
        
        name1 = glyph1.get("name", "").lower()
        name2 = glyph2.get("name", "").lower()
        
        for family, members in archetypal_families.items():
            if name1 in members and name2 in members:
                return 0.9
        
        return 0.1
    
    def calculate_symbolic_similarity(self, glyph1, glyph2):
        """Calculate symbolic representation similarity"""
        
        # Symbolic attribute mapping
        symbolic_attributes = {
            "vertical_energy": ["tree", "mountain", "sun", "key"],
            "horizontal_flow": ["water", "snake", "moon"],
            "circular_unity": ["sun", "moon", "lotus"],
            "organic_form": ["tree", "lotus", "snake", "wolf"],
            "geometric_form": ["key", "mountain", "sun"],
            "transformative": ["snake", "lotus", "shadow", "water"]
        }
        
        name1 = glyph1.get("name", "").lower()
        name2 = glyph2.get("name", "").lower()
        
        shared_attributes = 0
        total_attributes = 0
        
        for attribute, symbols in symbolic_attributes.items():
            in1 = name1 in symbols
            in2 = name2 in symbols
            
            if in1 or in2:
                total_attributes += 1
                if in1 and in2:
                    shared_attributes += 1
        
        if total_attributes == 0:
            return 0.0
        
        return shared_attributes / total_attributes
    
    def calculate_all_relationships(self):
        """Calculate all pairwise relationships between glyphs"""
        
        print("🔗 Calculating gGlyph relationships...")
        
        relationships = []
        
        for i, glyph1 in enumerate(self.glyphs):
            for j, glyph2 in enumerate(self.glyphs):
                if i >= j:  # Only calculate each pair once
                    continue
                
                # Calculate different types of similarity
                emotional_sim = self.calculate_emotional_similarity(glyph1, glyph2)
                categorical_sim = self.calculate_categorical_similarity(glyph1, glyph2)
                semantic_sim = self.calculate_semantic_similarity(glyph1, glyph2)
                archetypal_sim = self.calculate_archetypal_similarity(glyph1, glyph2)
                symbolic_sim = self.calculate_symbolic_similarity(glyph1, glyph2)
                
                # Calculate weighted overall similarity
                weights = self.relationship_types
                overall_similarity = (
                    emotional_sim * weights["emotional"]["weight"] +
                    categorical_sim * weights["categorical"]["weight"] +
                    semantic_sim * weights["semantic"]["weight"] +
                    archetypal_sim * weights["archetypal"]["weight"] +
                    symbolic_sim * weights["symbolic"]["weight"]
                ) / sum(w["weight"] for w in weights.values())
                
                # Only include relationships above threshold
                if overall_similarity > 0.2:
                    relationship = {
                        "source": glyph1["name"],
                        "target": glyph2["name"],
                        "overall_similarity": round(overall_similarity, 3),
                        "similarities": {
                            "emotional": round(emotional_sim, 3),
                            "categorical": round(categorical_sim, 3),
                            "semantic": round(semantic_sim, 3),
                            "archetypal": round(archetypal_sim, 3),
                            "symbolic": round(symbolic_sim, 3)
                        },
                        "strength": self.categorize_relationship_strength(overall_similarity)
                    }
                    
                    relationships.append(relationship)
        
        print(f"   📊 Found {len(relationships)} significant relationships")
        
        return relationships
    
    def categorize_relationship_strength(self, similarity):
        """Categorize relationship strength for visualization"""
        if similarity >= 0.8:
            return "very_strong"
        elif similarity >= 0.6:
            return "strong"
        elif similarity >= 0.4:
            return "medium"
        else:
            return "weak"
    
    def prepare_graph_data(self):
        """Prepare data structure for D3.js force-directed graph"""
        
        relationships = self.calculate_all_relationships()
        
        # Create nodes
        nodes = []
        for glyph in self.glyphs:
            # Get color info
            color_info = {}
            metadata_file = Path(f"results/gGlyphs_codex/metadata/{glyph['name'].lower()}_metadata.json")
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                color_info = metadata.get("color_info", {})
            
            node = {
                "id": glyph["name"],
                "name": glyph["name"],
                "category": glyph["category"],
                "subcategory": glyph["subcategory"],
                "meanings": glyph["meanings"],
                "color": color_info.get("primary_color", "#808080"),
                "emotion_family": color_info.get("emotion_family", "Neutral"),
                "svg_path": glyph["files"]["svg_colored"],
                "group": self.assign_group(glyph),
                "size": 10  # Base size, can be adjusted based on connections
            }
            nodes.append(node)
        
        # Create links
        links = []
        for rel in relationships:
            link = {
                "source": rel["source"],
                "target": rel["target"],
                "value": rel["overall_similarity"],
                "strength": rel["strength"],
                "similarities": rel["similarities"]
            }
            links.append(link)
        
        # Calculate node sizes based on connections
        connection_counts = defaultdict(int)
        for link in links:
            connection_counts[link["source"]] += 1
            connection_counts[link["target"]] += 1
        
        # Update node sizes
        for node in nodes:
            connections = connection_counts[node["id"]]
            node["size"] = 8 + min(connections * 2, 12)  # Size 8-20 based on connections
            node["connections"] = connections
        
        graph_data = {
            "nodes": nodes,
            "links": links,
            "metadata": {
                "total_nodes": len(nodes),
                "total_links": len(links),
                "relationship_types": self.relationship_types,
                "generated": "2025-07-22T13:30:00Z"
            }
        }
        
        return graph_data
    
    def assign_group(self, glyph):
        """Assign group number for graph clustering"""
        category_groups = {
            "Animal": 1,
            "Plant": 2,
            "Element": 3,
            "Object": 4,
            "Archetype": 5
        }
        return category_groups.get(glyph["category"], 0)
    
    def save_graph_data(self, output_path="results/gGlyphs_codex/graph_data.json"):
        """Save graph data for D3.js visualization"""
        
        graph_data = self.prepare_graph_data()
        
        with open(output_path, 'w') as f:
            json.dump(graph_data, f, indent=2)
        
        print(f"📊 Graph data saved: {output_path}")
        return graph_data
    
    def generate_relationship_report(self):
        """Generate a detailed relationship report"""
        
        relationships = self.calculate_all_relationships()
        
        print("\n🔗 gGlyph Relationship Analysis")
        print("=" * 60)
        
        # Group by strength
        by_strength = defaultdict(list)
        for rel in relationships:
            by_strength[rel["strength"]].append(rel)
        
        for strength in ["very_strong", "strong", "medium", "weak"]:
            if strength in by_strength:
                print(f"\n{strength.upper().replace('_', ' ')} Relationships ({len(by_strength[strength])}):")
                print("-" * 40)
                
                for rel in sorted(by_strength[strength], key=lambda x: x["overall_similarity"], reverse=True):
                    print(f"   {rel['source']} ↔ {rel['target']} ({rel['overall_similarity']:.3f})")
                    
                    # Show top similarity type
                    sims = rel["similarities"]
                    top_sim = max(sims.items(), key=lambda x: x[1])
                    print(f"      Primary: {top_sim[0]} ({top_sim[1]:.3f})")

def main():
    """Main execution"""
    
    print("🌐 gGlyph Graph Analysis System")
    print("=" * 50)
    
    analyzer = GlyphGraphAnalyzer()
    
    if not analyzer.glyphs:
        print("❌ No glyphs found in codex!")
        return
    
    print(f"📚 Loaded {len(analyzer.glyphs)} glyphs")
    
    # Generate graph data
    graph_data = analyzer.save_graph_data()
    
    # Generate relationship report
    analyzer.generate_relationship_report()
    
    print(f"\n🎯 Graph Visualization Ready!")
    print(f"   Nodes: {len(graph_data['nodes'])}")
    print(f"   Links: {len(graph_data['links'])}")
    print(f"   Data: results/gGlyphs_codex/graph_data.json")

if __name__ == "__main__":
    main() 