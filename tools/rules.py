from tools import _get_item_details, _fetch_index

# --- Rules Tools ---
def get_rules_details(rule_name: str) -> dict:
    """Tool to get details for a specific rule."""
    return _get_item_details("rules", rule_name)

def get_rules_by_section(section_name: str) -> dict:
    """Tool to get details for a specific rule section."""
    return _get_item_details("rules", section_name)

# --- Rules get_all tools ---

def get_all_rules() -> list:
    """Tool to get all rules."""
    return _fetch_index("rules")['results']

def get_all_rules_sections() -> list:
    """Tool to get all rules sections."""
    return _fetch_index("rules")['results']

if __name__ == "__main__":
    print(get_rules_by_section("spellcasting"))