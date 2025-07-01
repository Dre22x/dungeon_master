from tools import _get_item_details, _fetch_index

# --- Weapon Tools ---
def get_weapon_property_details(weapon_property_name: str) -> dict:
    """Tool to get details for a specific weapon property."""
    return _get_item_details("weapon-properties", weapon_property_name)


# --- Weapon get_all tools ---
def get_all_weapon_properties() -> list[dict]:
    """Tool to get all weapon properties."""
    result = _fetch_index("weapon-properties")
    return result.get('results', []) if isinstance(result, dict) else result
