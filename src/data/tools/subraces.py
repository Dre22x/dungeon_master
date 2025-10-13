from .tools import _get_item_details, _fetch_index

# --- Subrace Tools ---
def get_subrace_details(subrace_name: str) -> dict:
    """Tool to get details for a specific character subrace."""
    return _get_item_details("subraces", subrace_name)


# --- Subrace resource lists ---
def get_proficiencies_available_for_subrace(subrace_name: str) -> list:
    """Tool to get proficiencies available for a specific subrace."""
    return _fetch_index(f"subraces/{subrace_name}/proficiencies")['results']

def get_traits_available_for_subrace(subrace_name: str) -> list:
    """Tool to get traits available for a specific subrace."""
    return _fetch_index(f"subraces/{subrace_name}/traits")['results']


# --- Subrace get_all tools ---
def get_all_subraces() -> list[dict]:
    """Tool to get all subraces."""
    return _fetch_index("subraces")['results']
