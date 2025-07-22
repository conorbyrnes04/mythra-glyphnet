"""
Glyph Database Integration
Bridge between Python (MERU generation) and existing LowDB structure
"""
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import subprocess
import logging

logger = logging.getLogger(__name__)

class GlyphIntegration:
    """Integration layer between Python generation and existing LowDB"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # File paths for existing structure
        self.gglyphs_file = self.data_dir / "genericGlyphs.json"
        self.dreams_file = self.data_dir / "dreamSeeds.json"  
        self.users_file = self.data_dir / "users.json"
        
        # New enhanced paths
        self.meru_glyphs_dir = Path("results/glyphs")
        self.meru_metadata_dir = Path("results/metadata")
        
        self._ensure_files_exist()
    
    def _ensure_files_exist(self):
        """Ensure all required JSON files exist with proper structure"""
        
        # Generic glyphs structure
        if not self.gglyphs_file.exists():
            gglyphs_data = {"gGlyphs": []}
            with open(self.gglyphs_file, 'w') as f:
                json.dump(gglyphs_data, f, indent=2)
        
        # Dream seeds structure  
        if not self.dreams_file.exists():
            dreams_data = {"dGlyphs": []}
            with open(self.dreams_file, 'w') as f:
                json.dump(dreams_data, f, indent=2)
        
        # Users structure
        if not self.users_file.exists():
            users_data = {"users": []}
            with open(self.users_file, 'w') as f:
                json.dump(users_data, f, indent=2)
    
    def add_meru_glyph(self, 
                      name: str,
                      prompt: str, 
                      model_used: str,
                      file_path: str,
                      metadata: Optional[Dict] = None) -> str:
        """Add a MERU-generated glyph to the database"""
        
        try:
            # Read current gGlyphs
            with open(self.gglyphs_file, 'r') as f:
                data = json.load(f)
            
            # Create enhanced glyph entry
            glyph_id = f"meru_{int(datetime.now().timestamp())}"
            
            glyph_entry = {
                "id": glyph_id,
                "title": name,
                "svg": file_path,
                
                # Enhanced fields for MERU integration
                "source": "meru_generated",
                "prompt": prompt,
                "model": model_used,
                "created_at": datetime.now().isoformat(),
                "file_type": "svg" if file_path.endswith('.svg') else "png",
                
                # Metadata from generation
                "generation_metadata": metadata or {},
                
                # Usage tracking (compatible with existing structure)
                "usage_count": 0,
                "last_used": None,
                
                # Categories for filtering
                "categories": self._extract_categories_from_prompt(prompt),
                "style_tags": ["meru", "vector", "mystical"]
            }
            
            # Add to gGlyphs array
            data["gGlyphs"].append(glyph_entry)
            
            # Save back to file
            with open(self.gglyphs_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"✅ Added MERU glyph: {name} ({glyph_id})")
            return glyph_id
            
        except Exception as e:
            logger.error(f"❌ Failed to add MERU glyph: {e}")
            raise
    
    def _extract_categories_from_prompt(self, prompt: str) -> List[str]:
        """Extract categories from generation prompt"""
        categories = []
        
        # Common element keywords
        elements = ["fire", "water", "earth", "air", "spirit"]
        nature = ["tree", "mountain", "river", "sun", "moon", "star"]
        concepts = ["wisdom", "strength", "peace", "sacred", "mystical"]
        
        prompt_lower = prompt.lower()
        
        for element in elements:
            if element in prompt_lower:
                categories.append("elements")
                break
                
        for item in nature:
            if item in prompt_lower:
                categories.append("nature")
                break
                
        for concept in concepts:
            if concept in prompt_lower:
                categories.append("concepts")
                break
        
        if not categories:
            categories.append("general")
            
        return categories
    
    def get_all_glyphs(self) -> List[Dict]:
        """Get all gGlyphs with enhanced metadata"""
        try:
            with open(self.gglyphs_file, 'r') as f:
                data = json.load(f)
            return data.get("gGlyphs", [])
        except Exception as e:
            logger.error(f"❌ Failed to read glyphs: {e}")
            return []
    
    def search_glyphs(self, 
                     query: Optional[str] = None,
                     category: Optional[str] = None,
                     source: Optional[str] = None) -> List[Dict]:
        """Search glyphs with filters"""
        glyphs = self.get_all_glyphs()
        filtered = []
        
        for glyph in glyphs:
            # Text search in title and prompt
            if query:
                searchable_text = f"{glyph.get('title', '')} {glyph.get('prompt', '')}".lower()
                if query.lower() not in searchable_text:
                    continue
            
            # Category filter
            if category:
                glyph_categories = glyph.get('categories', [])
                if category not in glyph_categories:
                    continue
            
            # Source filter (meru_generated, manual, etc.)
            if source:
                if glyph.get('source') != source:
                    continue
            
            filtered.append(glyph)
        
        return filtered
    
    def update_glyph_usage(self, glyph_id: str):
        """Update usage statistics for a glyph"""
        try:
            with open(self.gglyphs_file, 'r') as f:
                data = json.load(f)
            
            # Find and update the glyph
            for glyph in data["gGlyphs"]:
                if glyph["id"] == glyph_id:
                    glyph["usage_count"] = glyph.get("usage_count", 0) + 1
                    glyph["last_used"] = datetime.now().isoformat()
                    break
            
            # Save back
            with open(self.gglyphs_file, 'w') as f:
                json.dump(data, f, indent=2)
                
            logger.info(f"📊 Updated usage for glyph: {glyph_id}")
            
        except Exception as e:
            logger.error(f"❌ Failed to update usage: {e}")
    
    def create_dream_entry(self, 
                          user_id: str,
                          dream_text: str,
                          selected_glyph_id: str,
                          emotion_data: Optional[Dict] = None,
                          context_data: Optional[Dict] = None) -> str:
        """Create a new dream entry linking to a gGlyph"""
        
        try:
            with open(self.dreams_file, 'r') as f:
                data = json.load(f)
            
            dream_id = f"dream_{int(datetime.now().timestamp())}"
            
            dream_entry = {
                "id": dream_id,
                "user_id": user_id,
                "created_at": datetime.now().isoformat(),
                
                # Dream content
                "transcript": dream_text,
                "selected_glyph": selected_glyph_id,
                
                # Analysis data
                "emotions": emotion_data or {},
                "context": context_data or {},
                
                # Future: AI interpretation fields
                "core_themes": [],
                "symbolic_meanings": [],
                "interpretation": None
            }
            
            data["dGlyphs"].append(dream_entry)
            
            with open(self.dreams_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            # Update glyph usage
            self.update_glyph_usage(selected_glyph_id)
            
            logger.info(f"✅ Created dream entry: {dream_id}")
            return dream_id
            
        except Exception as e:
            logger.error(f"❌ Failed to create dream entry: {e}")
            raise
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            glyphs = self.get_all_glyphs()
            
            with open(self.dreams_file, 'r') as f:
                dreams_data = json.load(f)
            dreams = dreams_data.get("dGlyphs", [])
            
            with open(self.users_file, 'r') as f:
                users_data = json.load(f)
            users = users_data.get("users", [])
            
            # Calculate stats
            meru_glyphs = [g for g in glyphs if g.get("source") == "meru_generated"]
            total_usage = sum(g.get("usage_count", 0) for g in glyphs)
            
            stats = {
                "total_glyphs": len(glyphs),
                "meru_glyphs": len(meru_glyphs),
                "total_dreams": len(dreams),
                "total_users": len(users),
                "total_usage": total_usage,
                "categories": self._get_category_stats(glyphs),
                "most_used": sorted(glyphs, key=lambda x: x.get("usage_count", 0), reverse=True)[:5]
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Failed to get stats: {e}")
            return {}
    
    def _get_category_stats(self, glyphs: List[Dict]) -> Dict[str, int]:
        """Get glyph count by category"""
        category_counts = {}
        
        for glyph in glyphs:
            categories = glyph.get("categories", ["general"])
            for category in categories:
                category_counts[category] = category_counts.get(category, 0) + 1
        
        return category_counts
    
    def run_node_command(self, command: str) -> str:
        """Run Node.js commands for compatibility with existing structure"""
        try:
            result = subprocess.run(
                ["node", "-e", command],
                capture_output=True,
                text=True,
                cwd="."
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                logger.error(f"Node command failed: {result.stderr}")
                return ""
                
        except Exception as e:
            logger.error(f"Failed to run Node command: {e}")
            return ""

# Singleton instance
glyph_db = GlyphIntegration()

# Helper functions
def add_generated_glyph(name: str, prompt: str, model: str, file_path: str, metadata: Dict = None) -> str:
    """Helper to add a MERU-generated glyph"""
    return glyph_db.add_meru_glyph(name, prompt, model, file_path, metadata)

def search_glyphs(**kwargs) -> List[Dict]:
    """Helper to search glyphs"""
    return glyph_db.search_glyphs(**kwargs)

def get_database_stats() -> Dict:
    """Helper to get database statistics"""
    return glyph_db.get_stats() 