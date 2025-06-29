import requests
import json
import argparse
import textwrap

# The base URL for the 5e-bits SRD API
API_BASE_URL = "https://www.dnd5eapi.co/api/2014/"

# Main Tool Function
def fetch_race_data(race_name: str) -> dict:
    """
    Fetches detailed data for a specific race using its name.

    Args:
        race_name: The name of the race.

    Returns:
        A dictionary containing the race's data, or None on error.
    """
    formatted_name = format_race_name_for_api(race_name)
    full_url = f"{API_BASE_URL}races/{formatted_name}"
    print(f"--> Fetching details from: {full_url}\n")
    try:
        response = requests.get(full_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"A network error occurred: {req_err}")
    return None

def format_race_name_for_api(name: str) -> str:
    """
    Formats the user-provided race name into the format required by the API.
    Example: "High Elf" -> "high-elf"
    
    Args:
        name: The raw name of the race.

    Returns:
        The formatted name, ready for the API URL.
    """
    return name.lower().replace(" ", "-")

def get_all_races() -> list:
    """
    Fetches all available races from the SRD API.

    Returns:
        A list of dictionaries, where each dictionary represents a race 
        with its name and a URL to its data. Returns None on error.
    """
    url = f"{API_BASE_URL}races"
    print("--> Fetching race index from the SRD...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: A network error occurred while fetching the race index: {e}")
    except json.JSONDecodeError:
        print("Error: Failed to decode the race index. The API might be down.")
    return None

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

def main():
    """
    Main function to run the command-line tool for race lookup.
    """
    parser = argparse.ArgumentParser(description="Search for and display D&D 5e race info from the SRD API.")
    parser.add_argument("race_name", type=str, help="The name of the race to look up (e.g., 'elf', 'dwarf').")
    
    args = parser.parse_args()
    
    race_data = fetch_race_data(args.race_name)
    
    if race_data:
        display_race_info(race_data)

if __name__ == "__main__":
    main() 