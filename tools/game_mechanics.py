from tools import _get_item_details, _fetch_index

# --- Game Mechanics Tools ---
def get_condition_details(condition_name: str) -> dict:
    """Tool to get details for a specific condition."""
    return _get_item_details("conditions", condition_name)

def get_damage_type_details(damage_type_name: str) -> dict:
    """Tool to get details for a specific damage type."""
    return _get_item_details("damage-types", damage_type_name)


# --- Game Mechanics get_all tools ---
def get_all_conditions() -> list:
    """Tool to get all conditions."""
    return _fetch_index("conditions")['results']

def get_all_damage_types() -> list:
    """Tool to get all damage types."""
    return _fetch_index("damage-types")['results']