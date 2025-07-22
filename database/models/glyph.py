"""
MongoDB Models for MYTHRA GLYPHNET
Glyph and Symbol Data Management
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class GlyphModel(BaseModel):
    """Core glyph data model for MongoDB storage"""
    
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    
    # Core Identity
    name: str = Field(..., description="Glyph name (e.g., 'fire_element', 'sacred_tree')")
    symbol_type: str = Field(..., description="Type: gGlyph, dGlyph, or custom")
    trigger_word: str = Field(default="meru", description="Model trigger word used")
    
    # Generation Info
    prompt: str = Field(..., description="Full prompt used for generation")
    model_used: str = Field(..., description="Model ID (e.g., 'conorbyrnes04/meru')")
    model_version: str = Field(..., description="Specific model version/hash")
    generation_params: Dict[str, Any] = Field(default={}, description="Generation parameters")
    
    # File Paths & Storage
    svg_path: Optional[str] = Field(None, description="Path to SVG file")
    png_path: Optional[str] = Field(None, description="Path to PNG file")
    original_path: Optional[str] = Field(None, description="Original generated file path")
    thumbnail_path: Optional[str] = Field(None, description="Thumbnail image path")
    
    # Visual Properties
    primary_color: Optional[str] = Field(None, description="Dominant color (hex)")
    style_tags: List[str] = Field(default=[], description="Style descriptors")
    complexity_score: Optional[float] = Field(None, description="Visual complexity (0-1)")
    
    # Semantic Data
    categories: List[str] = Field(default=[], description="Categories (elements, nature, concepts)")
    elements: List[str] = Field(default=[], description="Elements represented")
    emotions: List[str] = Field(default=[], description="Emotional associations")
    concepts: List[str] = Field(default=[], description="Abstract concepts")
    
    # Usage & Context
    usage_count: int = Field(default=0, description="Times this glyph was used")
    last_used: Optional[datetime] = Field(None, description="Last usage timestamp")
    user_ratings: List[Dict[str, Any]] = Field(default=[], description="User feedback")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str = Field(default="system", description="Creator identifier")
    
    # Quality Metrics
    generation_time: Optional[float] = Field(None, description="Generation time in seconds")
    file_size_bytes: Optional[int] = Field(None, description="File size in bytes")
    image_dimensions: Optional[Dict[str, int]] = Field(None, description="Width/height")
    
    # Relationships
    similar_glyphs: List[str] = Field(default=[], description="IDs of similar glyphs")
    parent_glyph: Optional[str] = Field(None, description="Parent glyph ID if variation")
    variations: List[str] = Field(default=[], description="Variation glyph IDs")
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class GlyphCollection(BaseModel):
    """Collection/set of related glyphs"""
    
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(..., description="Collection name")
    description: str = Field(..., description="Collection description")
    glyph_ids: List[str] = Field(default=[], description="List of glyph IDs")
    collection_type: str = Field(..., description="Type: codex, user_set, generated_set")
    tags: List[str] = Field(default=[], description="Collection tags")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UserSession(BaseModel):
    """User interaction session with glyphs"""
    
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    session_id: str = Field(..., description="Unique session identifier")
    user_id: Optional[str] = Field(None, description="User identifier if logged in")
    
    # Session Data
    dream_text: Optional[str] = Field(None, description="User's dream/experience text")
    generated_glyphs: List[str] = Field(default=[], description="Glyphs generated this session")
    selected_glyph: Optional[str] = Field(None, description="Final selected glyph")
    
    # Interaction Metrics
    session_duration: Optional[float] = Field(None, description="Session length in seconds")
    glyph_interactions: List[Dict[str, Any]] = Field(default=[], description="User interactions")
    
    # Timestamps
    started_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime] = Field(None)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str} 