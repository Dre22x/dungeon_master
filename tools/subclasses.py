import textwrap
from tools import _get_item_details, _fetch_index

# --- Subclass Tools ---
def get_subclass_details(subclass_name: str) -> dict:
    """Tool to get details for a specific character subclass."""
    return _get_item_details("subclasses", subclass_name)


# --- Class resource lists ---
def get_features_available_for_subclass(subclass_name: str) -> list:
    """Tool to get features available for a specific character subclass."""
    return _fetch_index(f"subclasses/{subclass_name}/features")['results']


# --- Class levels ---
def get_all_level_resources_for_subclass(subclass_name: str) -> list:
    """Tool to get all level resources for a specific character subclass."""
    return _fetch_index(f"subclasses/{subclass_name}/levels")

def get_level_resources_for_subclass_at_level(subclass_name: str, level: str) -> list:
    """Tool to get level resources for a specific character subclass at a specific level."""
    return _fetch_index(f"subclasses/{subclass_name}/levels/{level}")

def get_features_of_spell_level_for_subclass(subclass_name: str, level: str) -> list:
    """Tool to get features of spell level for a specific character subclass at a specific level."""
    return _fetch_index(f"subclasses/{subclass_name}/levels/{level}/features")['results']


# --- Class get_all tools ---
def get_all_subclasses() -> list:
  """Tool to get all subclasses."""
  return _fetch_index("subclasses")


# --- Display Class Info ---
def display_class_info(data: dict):
    """
    Displays the fetched class data in a clean, readable format.

    Args:
        data: A dictionary containing the class's information.
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
    class_name = data.get('name', 'N/A').upper()
    hit_die = data.get('hit_die', 'N/A')
    print("="*60)
    print(f" {class_name} ".center(60, "="))
    print(f" Hit Die: d{hit_die} ".center(60))
    print("="*60)

    # --- Core Info ---
    print(f"Proficiency Choices: {data.get('proficiency_choices', [])}")
    print(f"Proficiencies: {', '.join([prof.get('name', '') for prof in data.get('proficiencies', [])])}")
    print(f"Saving Throw Proficiencies: {', '.join([save.get('name', '') for save in data.get('saving_throws', [])])}")
    print("-" * 60)

    # --- Starting Equipment ---
    if 'starting_equipment' in data and data['starting_equipment']:
        print("STARTING EQUIPMENT:")
        for item in data['starting_equipment']:
            if 'equipment' in item:
                print(f"  - {item['equipment'].get('name', 'N/A')}")
            elif 'equipment_option' in item:
                print(f"  - Choose from: {item['equipment_option'].get('choose', 0)} items")
        print("-" * 60)

    # --- Class Levels ---
    if 'class_levels' in data and data['class_levels']:
        print("CLASS FEATURES BY LEVEL:")
        for level_data in data['class_levels']:
            level = level_data.get('level', 'N/A')
            print(f"\nLevel {level}:")
            
            # Display features for this level
            for feature in level_data.get('features', []):
                print(f"  - {feature.get('name', 'N/A')}")
                if 'desc' in feature and feature['desc']:
                    print_wrapped(f"    {feature['desc']}", indent=4)
        print("-" * 60)

    # --- Spellcasting ---
    if 'spellcasting' in data and data['spellcasting']:
        print("SPELLCASTING:")
        spellcasting = data['spellcasting']
        print_wrapped(spellcasting.get('info', []), indent=2)
        print("-" * 60)

    # --- Subclasses ---
    if 'subclasses' in data and data['subclasses']:
        print("SUBCLASSES:")
        for subclass in data['subclasses']:
            print(f"  - {subclass.get('name', 'N/A')}")
        print("-" * 60)

    print("="*60)
