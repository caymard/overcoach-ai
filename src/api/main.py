"""FastAPI application for Overwatch RAG Team Composer."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import httpx
from typing import List

from src.api.models import (
    TeamCompositionRequest,
    TeamCompositionResponse,
    HeroRecommendation,
    HeroSimple,
    MapSimple,
    HeroCounterRequest,
    HeroCounterResponse,
    HealthResponse,
)
from src.rag.retriever import RAGRetriever
from src.ingestion.overfast_client import OverFastClient
from src.utils.config import config


# Global retriever instance
retriever: RAGRetriever = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management for the FastAPI app."""
    global retriever
    print("Initializing RAG retriever...")
    retriever = RAGRetriever()
    print("✓ RAG retriever initialized")
    print("✓ Overcoach AI is ready to serve requests!")
    yield
    print("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Overcoach AI",
    description="AI-powered team composition coach for Overwatch",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint."""
    return {
        "message": "Overcoach AI - Your Overwatch Team Composition Coach",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint."""
    # Check Ollama connection
    ollama_connected = False
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{config.OLLAMA_BASE_URL}/api/tags", timeout=5.0)
            ollama_connected = response.status_code == 200
    except:
        pass
    
    # Get index stats
    heroes_count = 0
    maps_count = 0
    if retriever:
        try:
            heroes_collection = retriever.chroma_client.get_collection("heroes")
            heroes_count = heroes_collection.count()
        except:
            pass
        
        try:
            maps_collection = retriever.chroma_client.get_collection("maps")
            maps_count = maps_collection.count()
        except:
            pass
    
    return HealthResponse(
        status="healthy" if ollama_connected else "degraded",
        ollama_connected=ollama_connected,
        heroes_indexed=heroes_count,
        maps_indexed=maps_count,
    )


@app.post("/suggest", response_model=TeamCompositionResponse, tags=["Team Composition"])
async def suggest_team_composition(request: TeamCompositionRequest):
    """
    Suggest an optimal team composition based on map, enemy team, and context.
    """
    if not retriever:
        raise HTTPException(status_code=503, detail="RAG retriever not initialized")
    
    try:
        # Prepare context
        context = {
            "map": request.map_name,
            "enemy_team": request.enemy_team,
            "current_team": request.current_team,
            "difficulties": request.difficulties,
        }
        
        # Query RAG
        raw_response = retriever.query_team_composition(context)
        
        # Parse response - extract heroes from "RECOMMENDED TEAM" section
        recommended_team = []
        strategy = ""
        synergies = ""
        alternatives = []
        
        lines = raw_response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect sections
            if "RECOMMENDED TEAM" in line.upper():
                current_section = "team"
                continue
            elif "COUNTER STRATEGY" in line.upper():
                current_section = "strategy"
                continue
            elif "SYNERGIES" in line.upper() or "KEY SYNERGIES" in line.upper():
                current_section = "synergies"
                continue
            elif "ALTERNATIVE" in line.upper():
                current_section = "alternatives"
                continue
            
            # Extract content based on section
            if current_section == "team":
                # Look for pattern: "Role: HeroName - reasoning" or "Role: HeroName – reasoning"
                # Handle both regular dash (-) and em dash (–)
                if ':' in line and ('-' in line or '–' in line):
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        role = parts[0].strip().lower()
                        if role in ['tank', 'damage', 'support']:
                            # Try to split by em dash first, then regular dash
                            hero_parts = None
                            if '–' in parts[1]:
                                hero_parts = parts[1].split('–', 1)
                            elif '-' in parts[1]:
                                hero_parts = parts[1].split('-', 1)
                            
                            if hero_parts:
                                hero_name = hero_parts[0].strip()
                                reasoning = hero_parts[1].strip() if len(hero_parts) > 1 else "Strategic pick"
                                
                                recommended_team.append(HeroRecommendation(
                                    name=hero_name,
                                    role=role,
                                    reasoning=reasoning
                                ))
            
            elif current_section == "strategy":
                if line and not any(x in line.upper() for x in ["COUNTER STRATEGY", "STRATEGY:"]):
                    strategy += line + " "
            
            elif current_section == "synergies":
                if line and not any(x in line.upper() for x in ["SYNERGIES", "KEY SYNERGIES"]):
                    synergies += line + " "
            
            elif current_section == "alternatives":
                # Handle multiple formats:
                # "- HeroName (Role): description" or "- Role: HeroName - description"
                if line.startswith('-'):
                    # Format 1: "- D.Va (Tank): description"
                    if '(' in line and ')' in line:
                        hero_with_role = line.split(':', 1)[0]  # Get "- D.Va (Tank)"
                        hero_name = hero_with_role.split('(')[0].replace('-', '').strip()
                        if hero_name and len(hero_name) < 30:
                            alternatives.append(hero_name)
                    # Format 2: "- Role: HeroName - description"
                    elif ':' in line:
                        parts = line.split(':', 1)
                        if len(parts) == 2:
                            after_role = parts[1].strip()
                            # Split by dash (regular or em dash)
                            if '–' in after_role:
                                hero_desc = after_role.split('–', 1)
                            elif '-' in after_role:
                                hero_desc = after_role.split('-', 1)
                            else:
                                hero_desc = [after_role]
                            
                            hero_name = hero_desc[0].strip()
                            if hero_name and len(hero_name) < 30:
                                alternatives.append(hero_name)
        
        # Fallback if parsing failed
        if not recommended_team:
            recommended_team = [
                HeroRecommendation(
                    name="Parsing failed - see raw_response",
                    role="various",
                    reasoning="Check raw_response field for full recommendation"
                )
            ]
        
        if not strategy.strip():
            strategy = "Check raw_response for detailed strategy"
        
        if not synergies.strip():
            synergies = "Check raw_response for team synergies"
        
        return TeamCompositionResponse(
            recommended_team=recommended_team,
            strategy=strategy.strip(),
            synergies=synergies.strip(),
            alternatives=alternatives,
            raw_response=raw_response,
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating suggestion: {str(e)}")


@app.post("/counter", response_model=HeroCounterResponse, tags=["Hero Information"])
async def get_hero_counters(request: HeroCounterRequest):
    """
    Get information about heroes that counter a specific hero.
    """
    if not retriever:
        raise HTTPException(status_code=503, detail="RAG retriever not initialized")
    
    try:
        query = f"What heroes counter {request.hero_name}? Provide specific counter picks and strategies."
        response = retriever.query_heroes(query, top_k=5)
        
        return HeroCounterResponse(
            hero=request.hero_name,
            counters=response,
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting counters: {str(e)}")


@app.get("/heroes", response_model=List[HeroSimple], tags=["Data"])
async def list_heroes():
    """
    Get list of all available heroes.
    """
    try:
        with OverFastClient() as client:
            heroes = client.get_heroes()
            return [
                HeroSimple(
                    key=hero.get("key", ""),
                    name=hero.get("name", ""),
                    role=hero.get("role", "")
                )
                for hero in heroes
            ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching heroes: {str(e)}")


@app.get("/maps", response_model=List[MapSimple], tags=["Data"])
async def list_maps():
    """
    Get list of all available maps.
    """
    try:
        with OverFastClient() as client:
            maps = client.get_maps()
            return [
                MapSimple(
                    name=map_data.get("name", ""),
                    gamemodes=map_data.get("gamemodes", []),
                    location=map_data.get("location"),
                )
                for map_data in maps
            ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching maps: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
