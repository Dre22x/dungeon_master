import requests
import json
import argparse
import textwrap

# The base URL for the 5e-bits SRD API
API_BASE_URL = "https://www.dnd5eapi.co/api/2014/"

# Main Tool Function
def fetch_spell_data(spell_name: str) -> dict:
    """
    Fetches detailed data for a specific spell using its name.

    Args:
        spell_name: The name of the spell.

    Returns:
        A dictionary containing the spell's data, or None on error.
    """
    formatted_name = format_spell_name_for_api(spell_name)
    full_url = f"{API_BASE_URL}spells/{formatted_name}"
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

def format_spell_name_for_api(name: str) -> str:
    """
    Formats the user-provided spell name into the format required by the API.
    Example: "Magic Missile" -> "magic-missile"
    
    Args:
        name: The raw name of the spell.

    Returns:
        The formatted name, ready for the API URL.
    """
    return name.lower().replace(" ", "-")

def get_all_spells() -> list:
    """
    Fetches all available spells from the SRD API.

    Returns:
        A list of dictionaries, where each dictionary represents a spell 
        with its name and a URL to its data. Returns None on error.
    """
    url = f"{API_BASE_URL}spells"
    print("--> Fetching spell index from the SRD...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: A network error occurred while fetching the spell index: {e}")
    except json.JSONDecodeError:
        print("Error: Failed to decode the spell index. The API might be down.")
    return None

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

def main():
    """
    Main function to run the command-line tool for spell lookup.
    """
    parser = argparse.ArgumentParser(description="Search for and display D&D 5e spell info from the SRD API.")
    parser.add_argument("spell_name", type=str, help="The name of the spell to look up (e.g., 'fireball', 'mage armor').")
    
    args = parser.parse_args()
    
    all_spells = get_all_spells()
    print(json.dumps(all_spells, indent=4))

if __name__ == "__main__":
    main()
