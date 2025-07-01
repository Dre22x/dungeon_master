from tools import _get_item_details, _fetch_index

# --- Magic Item Tools ---
def get_magic_item_details(magic_item_name: str) -> dict:
    """Tool to get details for a specific magic item."""
    return _get_item_details("magic-items", magic_item_name)


# --- Magic Item get_all tools ---
def get_all_magic_items() -> list[dict]:
    """Tool to get all magic items."""
    return _fetch_index("magic-items")['results']

def get_all_magic_schools() -> list[dict]:
    """Tool to get all magic schools."""
    return _fetch_index("magic-schools")['results']
