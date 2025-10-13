from .tools import _get_item_details, _fetch_index, _search_index, _fetch_data_by_url

# --- Equipment Tools ---
def get_equipment_details(equipment_name: str) -> dict:
    """Tool to get details for a specific piece of equipment."""
    index = _fetch_index("equipment")
    all_equipment = index.get('results', []) if isinstance(index, dict) else index
    found_item = _search_index(equipment_name, all_equipment)
    if not found_item:
        return {"error": f"Equipment '{equipment_name}' not found."}
    return _fetch_data_by_url(found_item.get('url'))


# --- Equipment get_all tools ---
def get_all_equipment() -> list[dict]:
    """Tool to get all equipment."""
    result = _fetch_index("equipment")
    return result.get('results', []) if isinstance(result, dict) else result


def get_all_equipment_categories() -> list[dict]:
    """Tool to get all equipment categories."""
    result = _fetch_index("equipment-categories")
    return result.get('results', []) if isinstance(result, dict) else result

def get_equipment_by_category(category: str) -> list:
    """Tool to get equipment by category."""
    result = _fetch_index(f"equipment?category={category}")
    return result.get('results', []) if isinstance(result, dict) else result