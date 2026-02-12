"""Generate markdown files from OverFast API data."""
import json
import os
import time
from pathlib import Path
from typing import Dict, Any, List
from src.ingestion.overfast_client import OverFastClient
from src.utils.config import config


class MarkdownGenerator:
    """Generate markdown documentation for heroes and maps."""
    
    def __init__(self):
        self.client = OverFastClient()
        self.heroes_path = Path(config.DATA_HEROES_PATH)
        self.maps_path = Path(config.DATA_MAPS_PATH)
        self.raw_path = Path(config.DATA_RAW_PATH)
        
        # Ensure directories exist
        self.heroes_path.mkdir(parents=True, exist_ok=True)
        self.maps_path.mkdir(parents=True, exist_ok=True)
        self.raw_path.mkdir(parents=True, exist_ok=True)
    
    def generate_hero_markdown(self, hero_key: str, hero_data: Dict[str, Any]) -> str:
        """Generate markdown content for a hero."""
        md_lines = []
        
        # Header
        md_lines.append(f"# {hero_data.get('name', hero_key)}\n")
        
        # Basic info
        md_lines.append("## Basic Information\n")
        md_lines.append(f"- **Key**: {hero_key}")
        md_lines.append(f"- **Name**: {hero_data.get('name', 'N/A')}")
        md_lines.append(f"- **Role**: {hero_data.get('role', 'N/A')}")
        if 'description' in hero_data:
            md_lines.append(f"- **Description**: {hero_data['description']}")
        md_lines.append("")
        
        # Location
        if 'location' in hero_data:
            md_lines.append(f"- **Location**: {hero_data['location']}")
        md_lines.append("")
        
        # Story
        if 'story' in hero_data and hero_data['story']:
            md_lines.append("## Story\n")
            if isinstance(hero_data['story'], dict):
                summary = hero_data['story'].get('summary', '')
                if summary:
                    md_lines.append(summary)
            else:
                md_lines.append(str(hero_data['story']))
            md_lines.append("")
        
        # Abilities
        if 'abilities' in hero_data and hero_data['abilities']:
            md_lines.append("## Abilities\n")
            for ability in hero_data['abilities']:
                name = ability.get('name', 'Unknown')
                description = ability.get('description', 'No description')
                icon = ability.get('icon', '')
                
                md_lines.append(f"### {name}\n")
                if icon:
                    md_lines.append(f"![{name}]({icon})\n")
                md_lines.append(f"{description}\n")
            md_lines.append("")
        
        # Hitpoints
        if 'hitpoints' in hero_data:
            md_lines.append("## Hitpoints\n")
            hitpoints = hero_data['hitpoints']
            if isinstance(hitpoints, dict):
                for hp_type, value in hitpoints.items():
                    if value:
                        md_lines.append(f"- **{hp_type.title()}**: {value}")
            else:
                md_lines.append(f"- **Total**: {hitpoints}")
            md_lines.append("")
        
        return "\n".join(md_lines)
    
    def generate_map_markdown(self, map_data: Dict[str, Any]) -> str:
        """Generate markdown content for a map."""
        md_lines = []
        
        # Header
        md_lines.append(f"# {map_data.get('name', 'Unknown Map')}\n")
        
        # Basic info
        md_lines.append("## Basic Information\n")
        md_lines.append(f"- **Name**: {map_data.get('name', 'N/A')}")
        
        # Gamemodes
        if 'gamemodes' in map_data and map_data['gamemodes']:
            md_lines.append(f"- **Gamemodes**: {', '.join(map_data['gamemodes'])}")
        
        # Location
        if 'location' in map_data:
            md_lines.append(f"- **Location**: {map_data['location']}")
        
        # Country code
        if 'country_code' in map_data:
            md_lines.append(f"- **Country**: {map_data['country_code']}")
        
        md_lines.append("")
        
        # Screenshot
        if 'screenshot' in map_data:
            md_lines.append(f"![{map_data.get('name', 'Map')} Screenshot]({map_data['screenshot']})\n")
        
        return "\n".join(md_lines)
    
    def save_hero(self, hero_key: str, hero_data: Dict[str, Any]) -> str:
        """Save hero data as markdown and raw JSON."""
        # Save raw JSON
        raw_file = self.raw_path / f"hero_{hero_key}.json"
        with open(raw_file, 'w', encoding='utf-8') as f:
            json.dump(hero_data, f, indent=2, ensure_ascii=False)
        
        # Generate and save markdown
        markdown_content = self.generate_hero_markdown(hero_key, hero_data)
        md_file = self.heroes_path / f"{hero_key}.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        return str(md_file)
    
    def save_map(self, map_data: Dict[str, Any]) -> str:
        """Save map data as markdown and raw JSON."""
        map_name = map_data.get('name', 'unknown')
        # Create safe filename
        safe_name = map_name.lower().replace(' ', '-').replace("'", '').replace(':', '')
        
        # Save raw JSON
        raw_file = self.raw_path / f"map_{safe_name}.json"
        with open(raw_file, 'w', encoding='utf-8') as f:
            json.dump(map_data, f, indent=2, ensure_ascii=False)
        
        # Generate and save markdown
        markdown_content = self.generate_map_markdown(map_data)
        md_file = self.maps_path / f"{safe_name}.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        return str(md_file)
    
    def process_all_heroes(self) -> List[str]:
        """Fetch and process all heroes."""
        print("Fetching heroes list...")
        heroes = self.client.get_heroes()
        print(f"Found {len(heroes)} heroes\n")
        
        processed_files = []
        for i, hero in enumerate(heroes):
            hero_key = hero.get('key')
            hero_name = hero.get('name', hero_key)
            
            print(f"Processing {hero_name}...")
            try:
                hero_details = self.client.get_hero_details(hero_key)
                md_file = self.save_hero(hero_key, hero_details)
                processed_files.append(md_file)
                print(f"  ✓ Saved to {md_file}")
                
                # Rate limiting: wait between requests
                if i < len(heroes) - 1:
                    time.sleep(0.5)
                    
            except Exception as e:
                print(f"  ✗ Error: {e}")
                # Wait longer on rate limit errors
                if "429" in str(e):
                    print("  ⏳ Rate limit hit, waiting 15 seconds...")
                    time.sleep(15)
        
        return processed_files
    
    def process_all_maps(self) -> List[str]:
        """Fetch and process all maps."""
        print("\nFetching maps list...")
        maps = self.client.get_maps()
        print(f"Found {len(maps)} maps\n")
        
        processed_files = []
        for map_data in maps:
            map_name = map_data.get('name', 'Unknown')
            
            print(f"Processing {map_name}...")
            try:
                md_file = self.save_map(map_data)
                processed_files.append(md_file)
                print(f"  ✓ Saved to {md_file}")
            except Exception as e:
                print(f"  ✗ Error: {e}")
        
        return processed_files
    
    def close(self):
        """Close the API client."""
        self.client.close()


def main():
    """Main entry point for data ingestion."""
    generator = MarkdownGenerator()
    
    try:
        # Process heroes
        hero_files = generator.process_all_heroes()
        print(f"\n✓ Generated {len(hero_files)} hero markdown files")
        
        # Process maps
        map_files = generator.process_all_maps()
        print(f"\n✓ Generated {len(map_files)} map markdown files")
        
        print(f"\n✓ Total: {len(hero_files) + len(map_files)} markdown files created")
        
    finally:
        generator.close()


if __name__ == "__main__":
    main()
