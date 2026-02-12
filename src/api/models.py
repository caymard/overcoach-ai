"""Pydantic models for API requests and responses."""
from typing import List, Optional
from pydantic import BaseModel, Field


class TeamCompositionRequest(BaseModel):
    """Request model for team composition suggestions."""
    
    map_name: str = Field(..., description="Name of the Overwatch map")
    enemy_team: List[str] = Field(
        default=[],
        description="List of enemy hero names"
    )
    current_team: List[str] = Field(
        default=[],
        description="List of current team hero names"
    )
    difficulties: Optional[str] = Field(
        default="",
        description="Description of difficulties or challenges faced"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "map_name": "King's Row",
                "enemy_team": ["Reinhardt", "Bastion", "Mercy", "Widowmaker"],
                "current_team": [],
                "difficulties": "Enemy has strong bunker defense with Bastion"
            }
        }


class HeroRecommendation(BaseModel):
    """Model for a single hero recommendation."""
    
    name: str = Field(..., description="Hero name")
    role: str = Field(..., description="Hero role (tank, damage, support)")
    reasoning: str = Field(..., description="Why this hero is recommended")


class TeamCompositionResponse(BaseModel):
    """Response model for team composition suggestions."""
    
    recommended_team: List[HeroRecommendation] = Field(
        ...,
        description="List of recommended heroes"
    )
    strategy: str = Field(..., description="Overall strategy and counter-play")
    synergies: str = Field(..., description="Key team synergies")
    alternatives: Optional[List[str]] = Field(
        default=[],
        description="Alternative hero options"
    )
    raw_response: str = Field(..., description="Full LLM response")


class HeroSimple(BaseModel):
    """Simple hero information."""
    
    key: str
    name: str
    role: str


class MapSimple(BaseModel):
    """Simple map information."""
    
    name: str
    gamemodes: List[str] = []
    location: Optional[str] = None


class HeroCounterRequest(BaseModel):
    """Request for hero counter information."""
    
    hero_name: str = Field(..., description="Name of the hero to counter")
    
    class Config:
        json_schema_extra = {
            "example": {
                "hero_name": "Bastion"
            }
        }


class HeroCounterResponse(BaseModel):
    """Response with hero counter suggestions."""
    
    hero: str = Field(..., description="The hero being countered")
    counters: str = Field(..., description="Counter suggestions and strategies")


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str
    ollama_connected: bool
    heroes_indexed: int
    maps_indexed: int
