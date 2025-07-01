from tools.tools import _get_item_details, _fetch_index, _search_index, _fetch_data_by_url

# --- Equipment Tools ---
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


# --- Equipment get_all tools ---
def get_all_equipment() -> list[dict]:
    """Tool to get all equipment."""
    return _fetch_index("equipment")['results']


def get_all_equipment_categories() -> list[dict]:
    """Tool to get all equipment categories."""
    return _fetch_index("equipment-categories")['results']

def get_equipment_by_category(category: str) -> list:
    """Tool to get equipment by category."""
    return _fetch_index(f"equipment?category={category}")['results']