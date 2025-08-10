import textwrap
from tools import _get_item_details, _fetch_index

# --- Spell Tools ---
def get_spell_details(spell_name: str) -> dict:
    """Tool to get details for a specific spell."""
    return _get_item_details("spells", spell_name)

def get_spells_by_level(level: str) -> list:
    """Tool to get spells by level."""
    return _fetch_index(f"spells?level={level}")['results']

def get_spells_by_school(school: str) -> list:
    """Tool to get spells by school."""
    return _fetch_index(f"spells?school={school}")['results']

def get_spells_by_level_and_school(level: str, school: str) -> list:
    """Tool to get spells by level and school."""
    return _fetch_index(f"spells?level={level}&school={school}")['results']


# --- Spell get_all tools ---
def get_all_spells() -> list[dict]:
    """Tool to get all spells."""
    return _fetch_index("spells")['results']


# --- Display Spell Info ---
def display_spell_info(data: dict):
    """
    Displays the fetched spell data in a clean, readable format.

    Args:
        data: A dictionary containing the spell's information.
    """
    if not data:
        return

    # Helper function for pretty printing with wrapping
    def print_wrapped(text, indent=0, subsequent_indent=0):
        prefix = ' ' * indent
        sub_prefix = ' ' * subsequent_indent if subsequent_indent > 0 else prefix
        wrapper = textwrap.TextWrapper(initial_indent=prefix, width=80, subsequent_indent=sub_prefix)
        # The description is often a list of strings, join them first.
        if isinstance(text, list):
            text = "\n\n".join(text)
        print(wrapper.fill(text))

    # --- Header ---
    spell_name = data.get('name', 'N/A').upper()
    level = data.get('level_text', 'N/A')
    school = data.get('school', {}).get('name', 'N/A')
    print("="*60)
    print(f" {spell_name} ".center(60, "="))
    print(f" {level} {school} ".center(60))
    print("="*60)

    # --- Core Info ---
    print(f"Casting Time: {data.get('casting_time', 'N/A')}")
    print(f"Range: {data.get('range', 'N/A')}")
    
    components = ", ".join(data.get('components', []))
    if 'material' in data and data['material']:
         components += f" ( {data.get('material')} )"
    print(f"Components: {components}")
    
    print(f"Duration: {data.get('duration', 'N/A')}")
    print("-" * 60)

    # --- Description ---
    print_wrapped(data.get('desc', ['No description available.']))
    
    # --- Higher Level Casting ---
    if 'higher_level' in data and data['higher_level']:
        print("-" * 60)
        print_wrapped("At Higher Levels:", indent=0)
        print_wrapped(data['higher_level'], indent=2)

    print("="*60)

