import requests
from functools import lru_cache

# Globals
API_BASE_URL = "https://www.dnd5eapi.co/api/2014"
API_BASE_URL_PREFIX = "https://www.dnd5eapi.co"


@lru_cache(maxsize=None)
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

def _search_index(query: str, index: list | dict) -> dict | None:
    """Helper function to search a given index for a matching name or index."""
    query_lower = query.lower()
    # Handle both dict with 'results' key and direct list
    if isinstance(index, dict) and 'results' in index:
        items = index['results']
    elif isinstance(index, list):
        items = index
    else:
        return None
    # Exact match on 'index' field
    for item in items:
        if query_lower == str(item.get('index', '')).lower():
            return item
    # Exact match on 'name' field
    for item in items:
        if query_lower == str(item.get('name', '')).lower():
            return item
    # Partial match on 'name' field
    for item in items:
        if query_lower in str(item.get('name', '')).lower():
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


# --- For the Character Creation Assistant Agent ---
    
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

def get_starting_equipment(class_name: str) -> dict:
    """Tool to get the starting equipment for a specific class."""
    # Get the class details which include starting equipment options
    class_data = _get_item_details("classes", class_name)
    
    if "error" in class_data:
        return class_data
    
    # Extract starting equipment information
    starting_equipment = class_data.get("starting_equipment", [])
    starting_equipment_options = class_data.get("starting_equipment_options", [])
    
    return {
        "class_name": class_name,
        "starting_equipment": starting_equipment,
        "starting_equipment_options": starting_equipment_options,
        "description": f"Starting equipment options for {class_name.title()}"
    }


def get_all_equipments() -> list[dict]:
  """Tool to get all equipment."""
  return _fetch_index("equipment")
