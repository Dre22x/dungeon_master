import textwrap
from tools import _get_item_details, _fetch_index

# --- Race Tools ---
def get_race_details(race_name: str) -> dict:
    """Tool to get details for a specific character race."""
    return _get_item_details("races", race_name)


# --- Race resource lists ---
def get_subraces_available_for_race(race_name: str) -> list:
    """Tool to get subraces available for a specific race."""
    return _fetch_index(f"races/{race_name}/subraces")['results']

def get_proficiencies_available_for_race(race_name: str) -> list:
    """Tool to get proficiencies available for a specific race."""
    return _fetch_index(f"races/{race_name}/proficiencies")['results']

def get_traits_available_for_race(race_name: str) -> list:
    """Tool to get traits available for a specific race."""
    return _fetch_index(f"races/{race_name}/traits")['results']


# --- Race get_all tools ---
def get_all_races() -> list:
    """Tool to get all races."""
    return _fetch_index("races")['results']


# --- Display Race Info ---
def display_race_info(data: dict):
    """
    Displays the fetched race data in a clean, readable format.

    Args:
        data: A dictionary containing the race's information.
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
    race_name = data.get('name', 'N/A').upper()
    size = data.get('size', 'N/A')
    speed = data.get('speed', 'N/A')
    print("="*60)
    print(f" {race_name} ".center(60, "="))
    print(f" Size: {size} | Speed: {speed} ".center(60))
    print("="*60)

    # --- Ability Score Bonuses ---
    if 'ability_bonuses' in data and data['ability_bonuses']:
        print("ABILITY SCORE BONUSES:")
        for bonus in data['ability_bonuses']:
            ability = bonus.get('ability_score', {}).get('name', 'N/A')
            bonus_value = bonus.get('bonus', 0)
            print(f"  - {ability}: +{bonus_value}")
        print("-" * 60)

    # --- Age ---
    if 'age' in data and data['age']:
        print("AGE:")
        print_wrapped(data['age'], indent=2)
        print("-" * 60)

    # --- Alignment ---
    if 'alignment' in data and data['alignment']:
        print("ALIGNMENT:")
        print_wrapped(data['alignment'], indent=2)
        print("-" * 60)

    # --- Size Description ---
    if 'size_description' in data and data['size_description']:
        print("SIZE DESCRIPTION:")
        print_wrapped(data['size_description'], indent=2)
        print("-" * 60)

    # --- Starting Proficiencies ---
    if 'starting_proficiencies' in data and data['starting_proficiencies']:
        print("STARTING PROFICIENCIES:")
        for prof in data['starting_proficiencies']:
            print(f"  - {prof.get('name', 'N/A')}")
        print("-" * 60)

    # --- Starting Proficiency Options ---
    if 'starting_proficiency_options' in data and data['starting_proficiency_options']:
        print("STARTING PROFICIENCY OPTIONS:")
        for option in data['starting_proficiency_options']:
            choose = option.get('choose', 0)
            from_list = option.get('from', {}).get('options', [])
            print(f"  - Choose {choose} from:")
            for item in from_list:
                if 'item' in item:
                    print(f"    * {item['item'].get('name', 'N/A')}")
        print("-" * 60)

    # --- Languages ---
    if 'languages' in data and data['languages']:
        print("LANGUAGES:")
        for lang in data['languages']:
            print(f"  - {lang.get('name', 'N/A')}")
        print("-" * 60)

    # --- Language Options ---
    if 'language_options' in data and data['language_options']:
        print("LANGUAGE OPTIONS:")
        choose = data['language_options'].get('choose', 0)
        from_list = data['language_options'].get('from', {}).get('options', [])
        print(f"  - Choose {choose} additional languages from:")
        for item in from_list:
            if 'item' in item:
                print(f"    * {item['item'].get('name', 'N/A')}")
        print("-" * 60)

    # --- Traits ---
    if 'traits' in data and data['traits']:
        print("RACIAL TRAITS:")
        for trait in data['traits']:
            print(f"  - {trait.get('name', 'N/A')}")
            if 'desc' in trait and trait['desc']:
                print_wrapped(trait['desc'], indent=4)
        print("-" * 60)

    # --- Subraces ---
    if 'subraces' in data and data['subraces']:
        print("SUBRACES:")
        for subrace in data['subraces']:
            print(f"  - {subrace.get('name', 'N/A')}")
        print("-" * 60)

    print("="*60)