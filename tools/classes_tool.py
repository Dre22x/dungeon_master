import requests
import json
import argparse
import textwrap

# The base URL for the 5e-bits SRD API
API_BASE_URL = "https://www.dnd5eapi.co/api/2014/"

# Main Tool Function
def fetch_class_data(class_name: str) -> dict:
    """
    Fetches detailed data for a specific class using its name.

    Args:
        class_name: The name of the class.

    Returns:
        A dictionary containing the class's data, or None on error.
    """
    formatted_name = format_class_name_for_api(class_name)
    full_url = f"{API_BASE_URL}classes/{formatted_name}"
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

def format_class_name_for_api(name: str) -> str:
    """
    Formats the user-provided class name into the format required by the API.
    Example: "Fighter" -> "fighter"
    
    Args:
        name: The raw name of the class.

    Returns:
        The formatted name, ready for the API URL.
    """
    return name.lower().replace(" ", "-")

def get_all_classes() -> list:
    """
    Fetches all available classes from the SRD API.

    Returns:
        A list of dictionaries, where each dictionary represents a class 
        with its name and a URL to its data. Returns None on error.
    """
    url = f"{API_BASE_URL}classes"
    print("--> Fetching class index from the SRD...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: A network error occurred while fetching the class index: {e}")
    except json.JSONDecodeError:
        print("Error: Failed to decode the class index. The API might be down.")
    return None

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

def main():
    """
    Main function to run the command-line tool for class lookup.
    """
    parser = argparse.ArgumentParser(description="Search for and display D&D 5e class info from the SRD API.")
    parser.add_argument("class_name", type=str, help="The name of the class to look up (e.g., 'fighter', 'wizard').")
    
    args = parser.parse_args()
    
    class_data = fetch_class_data(args.class_name)
    
    if class_data:
        display_class_info(class_data)

if __name__ == "__main__":
    main() 