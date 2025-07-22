"""
MongoDB Connection and Database Management
MYTHRA GLYPHNET Database Layer
"""
import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GlyphDatabase:
    """MongoDB database manager for glyph data"""
    
    def __init__(self, connection_string: Optional[str] = None, database_name: str = "mythra_glyphnet"):
        """
        Initialize database connection
        
        Args:
            connection_string: MongoDB connection string (defaults to local)
            database_name: Database name
        """
        self.connection_string = connection_string or "mongodb://localhost:27017/"
        self.database_name = database_name
        self.client: Optional[MongoClient] = None
        self.db = None
        
    def connect(self):
        """Establish database connection"""
        try:
            self.client = MongoClient(self.connection_string)
            self.db = self.client[self.database_name]
            
            # Test connection
            self.client.admin.command('ping')
            logger.info(f"✅ Connected to MongoDB: {self.database_name}")
            
            # Create indexes for better performance
            self._create_indexes()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to MongoDB: {e}")
            return False
    
    def _create_indexes(self):
        """Create database indexes for better performance"""
        try:
            # Glyph collection indexes
            glyphs = self.db.glyphs
            glyphs.create_index("name")
            glyphs.create_index("symbol_type")
            glyphs.create_index("model_used")
            glyphs.create_index("created_at")
            glyphs.create_index([("categories", 1), ("elements", 1)])
            
            # Text search index for prompts and descriptions
            glyphs.create_index([
                ("name", "text"),
                ("prompt", "text"),
                ("style_tags", "text"),
                ("categories", "text")
            ])
            
            # Collections indexes
            collections = self.db.collections
            collections.create_index("name")
            collections.create_index("collection_type")
            
            # Sessions indexes
            sessions = self.db.sessions
            sessions.create_index("session_id")
            sessions.create_index("started_at")
            
            logger.info("✅ Database indexes created")
            
        except Exception as e:
            logger.warning(f"⚠️ Index creation warning: {e}")
    
    def disconnect(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            logger.info("📤 Disconnected from MongoDB")
    
    # === GLYPH OPERATIONS ===
    
    async def save_glyph(self, glyph_data: Dict[str, Any]) -> str:
        """Save a new glyph to database"""
        try:
            glyph_data['created_at'] = datetime.utcnow()
            glyph_data['updated_at'] = datetime.utcnow()
            
            result = self.db.glyphs.insert_one(glyph_data)
            logger.info(f"✅ Saved glyph: {glyph_data.get('name')}")
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"❌ Failed to save glyph: {e}")
            raise
    
    async def get_glyph(self, glyph_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a glyph by ID"""
        try:
            from bson import ObjectId
            glyph = self.db.glyphs.find_one({"_id": ObjectId(glyph_id)})
            return glyph
            
        except Exception as e:
            logger.error(f"❌ Failed to get glyph {glyph_id}: {e}")
            return None
    
    async def search_glyphs(self, 
                          query: Optional[str] = None,
                          symbol_type: Optional[str] = None,
                          categories: Optional[List[str]] = None,
                          limit: int = 50) -> List[Dict[str, Any]]:
        """Search glyphs with filters"""
        try:
            filter_dict = {}
            
            # Text search
            if query:
                filter_dict["$text"] = {"$search": query}
            
            # Type filter
            if symbol_type:
                filter_dict["symbol_type"] = symbol_type
            
            # Categories filter
            if categories:
                filter_dict["categories"] = {"$in": categories}
            
            cursor = self.db.glyphs.find(filter_dict).limit(limit)
            results = list(cursor)
            
            logger.info(f"🔍 Found {len(results)} glyphs")
            return results
            
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            return []
    
    async def update_glyph_usage(self, glyph_id: str):
        """Update glyph usage statistics"""
        try:
            from bson import ObjectId
            self.db.glyphs.update_one(
                {"_id": ObjectId(glyph_id)},
                {
                    "$inc": {"usage_count": 1},
                    "$set": {"last_used": datetime.utcnow()}
                }
            )
            logger.info(f"📊 Updated usage for glyph {glyph_id}")
            
        except Exception as e:
            logger.error(f"❌ Failed to update usage: {e}")
    
    # === COLLECTION OPERATIONS ===
    
    async def create_collection(self, name: str, description: str, collection_type: str) -> str:
        """Create a new glyph collection"""
        try:
            collection_data = {
                "name": name,
                "description": description,
                "collection_type": collection_type,
                "glyph_ids": [],
                "tags": [],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            result = self.db.collections.insert_one(collection_data)
            logger.info(f"✅ Created collection: {name}")
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"❌ Failed to create collection: {e}")
            raise
    
    async def add_glyph_to_collection(self, collection_id: str, glyph_id: str):
        """Add a glyph to a collection"""
        try:
            from bson import ObjectId
            self.db.collections.update_one(
                {"_id": ObjectId(collection_id)},
                {
                    "$addToSet": {"glyph_ids": glyph_id},
                    "$set": {"updated_at": datetime.utcnow()}
                }
            )
            logger.info(f"📁 Added glyph {glyph_id} to collection {collection_id}")
            
        except Exception as e:
            logger.error(f"❌ Failed to add glyph to collection: {e}")
    
    # === SESSION OPERATIONS ===
    
    async def create_session(self, session_id: str, user_id: Optional[str] = None) -> str:
        """Create a new user session"""
        try:
            session_data = {
                "session_id": session_id,
                "user_id": user_id,
                "dream_text": None,
                "generated_glyphs": [],
                "selected_glyph": None,
                "session_duration": None,
                "glyph_interactions": [],
                "started_at": datetime.utcnow(),
                "ended_at": None
            }
            
            result = self.db.sessions.insert_one(session_data)
            logger.info(f"🎯 Created session: {session_id}")
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"❌ Failed to create session: {e}")
            raise
    
    # === ANALYTICS ===
    
    async def get_glyph_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            stats = {
                "total_glyphs": self.db.glyphs.count_documents({}),
                "gglyphs": self.db.glyphs.count_documents({"symbol_type": "gGlyph"}),
                "dglyphs": self.db.glyphs.count_documents({"symbol_type": "dGlyph"}),
                "total_collections": self.db.collections.count_documents({}),
                "total_sessions": self.db.sessions.count_documents({}),
                "most_used_glyphs": list(
                    self.db.glyphs.find({}, {"name": 1, "usage_count": 1})
                    .sort("usage_count", -1).limit(10)
                )
            }
            
            logger.info("📊 Generated database statistics")
            return stats
            
        except Exception as e:
            logger.error(f"❌ Failed to get stats: {e}")
            return {}

# Singleton instance
db = GlyphDatabase()

# Helper functions
def initialize_database(connection_string: Optional[str] = None) -> bool:
    """Initialize database connection"""
    global db
    if connection_string:
        db.connection_string = connection_string
    return db.connect()

def get_database() -> GlyphDatabase:
    """Get database instance"""
    return db 