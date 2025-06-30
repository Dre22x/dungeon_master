from tools import _get_item_details, _fetch_index

# --- Trait Tools ---
def get_trait_details(trait_name: str) -> dict:
    """Tool to get details for a specific character trait."""
    return _get_item_details("traits", trait_name)


# --- Trait get_all tools ---
def get_all_traits() -> list:
    """Tool to get all traits."""
    return _fetch_index("traits")['results']