import requests
import json
import argparse
import textwrap
from functools import lru_cache

# ==============================================================================
#  CORE CONFIGURATION & HELPERS
# ==============================================================================

API_BASE_URL = "https://www.dnd5eapi.co/api/2014"
API_BASE_URL_PREFIX = "https://www.dnd5eapi.co"


@lru_cache(maxsize=None) # Simple and powerful cache for indices
def _fetch_index(category: str) -> list:
    """
    A cached helper function to fetch the index for a given API category.
    The lru_cache decorator ensures we only download each index once.
    """
    url = f"{API_BASE_URL}/{category}"
    print(f"[Toolkit] Fetching and caching index for '{category}'...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"FATAL ERROR: Could not fetch index for '{category}': {e}")
        return []

def _search_index(query: str, index: list) -> dict | None:
    """Helper function to search a given index for a matching name."""
    query_lower = query.lower()
    for item in index['results']:
        if query_lower == item.get('name', '').lower(): # Exact match first
            return item
    for item in index['results']:
        if query_lower in item.get('name', '').lower(): # Partial match second
            return item
    return None

def _fetch_data_by_url(item_url: str) -> dict | None:
    """Helper function to fetch detailed data from a specific item URL."""
    if not item_url:
        return None
    full_url = f"{API_BASE_URL_PREFIX}{item_url}"
    try:
        response = requests.get(full_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Could not fetch data from {full_url}: {e}")
        return None

def _get_item_details(category: str, name: str) -> dict:
    """Generic function to get details for any item by category and name."""
    index = _fetch_index(category)
    if not index:
        return {"error": f"Could not retrieve index for {category}."}
    
    found_item = _search_index(name, index)
    if not found_item:
        return {"error": f"Item '{name}' not found in category '{category}'."}
        
    return _fetch_data_by_url(found_item.get('url'))


# ==============================================================================
#  PUBLIC TOOL FUNCTIONS (One for each API category)
# ==============================================================================

# --- For the Rules Lawyer Agent ---

def get_monster_stats(monster_name: str) -> dict:
    """Tool to get the full SRD stat block for any monster."""
    return _get_item_details("monsters", monster_name)

def get_spell_description(spell_name: str) -> dict:
    """Tool to get the full SRD description of a spell."""
    return _get_item_details("spells", spell_name)

# --- For the Character Creation Assistant Agent ---

def get_race_info(race_name: str) -> dict:
    """Tool to get details for a specific character race."""
    return _get_item_details("races", race_name)

def get_class_info(class_name: str) -> dict:
    """Tool to get details for a specific character class."""
    return _get_item_details("classes", class_name)

def get_background_info(background_name: str) -> dict:
    """Tool to get details for a specific character background."""
    return _get_item_details("backgrounds", background_name)
    
def get_equipment_details(equipment_name: str) -> dict:
    """Tool to get details for a specific piece of equipment."""
    # Note: The equipment API is nested, so we search all categories.
    index = _fetch_index("equipment")
    all_equipment = []
    for category in index:
        all_equipment.extend(category.get('equipment', []))
    
    found_item = _search_index(equipment_name, all_equipment)
    if not found_item:
        return {"error": f"Equipment '{equipment_name}' not found."}
    return _fetch_data_by_url(found_item.get('url'))

# --- General Knowledge Tools ---

def get_ability_score_details(score_name: str) -> dict:
    """Tool to get details about an ability score (e.g., Strength)."""
    return _get_item_details("ability-scores", score_name)

def get_skill_details(skill_name: str) -> dict:
    """Tool to get details about a specific skill (e.g., Athletics)."""
    return _get_item_details("skills", skill_name)

def get_proficiency_details(proficiency_name: str) -> dict:
    """Tool to get details about a proficiency (e.g., 'all armor', 'longswords')."""
    return _get_item_details("proficiencies", proficiency_name)

def get_language_details(language_name: str) -> dict:
    """Tool to get details about a specific language."""
    return _get_item_details("languages", language_name)


# ==============================================================================
#  EXAMPLE USAGE (for testing the script from the command line)
# ==============================================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A comprehensive toolkit for the D&D 5e SRD API.")
    parser.add_argument("category", help="The category of information to fetch.", choices=[
        'monster', 'spell', 'race', 'class', 'background', 'equipment', 'skill', 'language'
    ])
    parser.add_argument("name", help="The name of the item to look up.")
    
    args = parser.parse_args()
    
    result = None
    if args.category == 'monster':
        result = get_monster_stats(args.name)
    elif args.category == 'spell':
        result = get_spell_description(args.name)
    elif args.category == 'race':
        result = get_race_info(args.name)
    elif args.category == 'class':
        result = get_class_info(args.name)
    elif args.category == 'background':
        result = get_background_info(args.name)
    elif args.category == 'equipment':
        result = get_equipment_details(args.name)
    elif args.category == 'skill':
        result = get_skill_details(args.name)
    elif args.category == 'language':
        result = get_language_details(args.name)
    elif args.category == 'ability_score':
        result = get_ability_score_details(args.name)
        
    if result:
        # Pretty print the JSON result
        print(json.dumps(result, indent=2))

