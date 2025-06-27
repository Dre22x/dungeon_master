import requests
import json
import argparse
import textwrap

# The base URL for the 5e-bits SRD API
API_BASE_URL = "https://www.dnd5eapi.co/api/2014/"

# Main Tool Function
def fetch_monster_data(monster_name: str) -> dict:
    """
    Fetches data for a specific monster from the 5e SRD API. This data includes everything from the monster's stats to its actions.

    Args:
        monster_name: The name of the monster.

    Returns:
        A dictionary containing the monster's data if found, otherwise None.
    """
    # Construct the full URL for the API endpoint.
    formatted_name = format_monster_name_for_api(monster_name)
    url = f"{API_BASE_URL}monsters/{formatted_name}"
    print(f"--> Contacting API at: {url}\n")
    
    try:
        response = requests.get(url)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print(f"Error: Monster '{monster_name}' not found in the SRD. Please check the spelling.")
        else:
            print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"A network error occurred: {req_err}")
    except json.JSONDecodeError:
        print("Error: Failed to decode the response from the server. The API might be down or returned invalid data.")
        
    return None

def get_all_monsters():
    """
    Fetches all monsters from the 5e SRD API.

    Returns:
        A list of dictionaries, each containing a monster's data.
    """
    url = f"{API_BASE_URL}monsters"
    response = requests.get(url)
    return response.json()

def format_monster_name_for_api(name: str) -> str:
    """
    Formats the user-provided monster name into the format required by the API.
    Example: "Dire Wolf" -> "dire-wolf"
    
    Args:
        name: The raw name of the monster.

    Returns:
        The formatted name, ready for the API URL.
    """
    return name.lower().replace(" ", "-")

def display_monster_info(data: dict):
    """
    Displays the fetched monster data in a clean, readable format.

    Args:
        data: A dictionary containing the monster's statistics.
    """
    if not data:
        return

    # Helper function for pretty printing with wrapping
    def print_wrapped(text, indent=0):
        prefix = ' ' * indent
        wrapper = textwrap.TextWrapper(initial_indent=prefix, width=80, subsequent_indent=prefix)
        print(wrapper.fill(text))

    # --- Basic Info ---
    print("="*50)
    print(f" {data.get('name', 'N/A').upper()} ".center(50, "="))
    print("="*50)
    print(f"Size: {data.get('size')} | Type: {data.get('type')} | Alignment: {data.get('alignment')}")
    print("-" * 50)

    # --- Core Stats ---
    print(f"Armor Class: {data.get('armor_class')}")
    print(f"Hit Points: {data.get('hit_points')} ({data.get('hit_dice')})")
    speed_str = ", ".join([f"{k}: {v}" for k, v in data.get('speed', {}).items()])
    print(f"Speed: {speed_str}")
    print("-" * 50)
    
    # --- Ability Scores ---
    print("STR {:>2} | DEX {:>2} | CON {:>2} | INT {:>2} | WIS {:>2} | CHA {:>2}".format(
        data.get('strength', 0), data.get('dexterity', 0), data.get('constitution', 0),
        data.get('intelligence', 0), data.get('wisdom', 0), data.get('charisma', 0)
    ))
    print("-" * 50)

    # --- Actions ---
    print("ACTIONS")
    for action in data.get('actions', []):
        print(f"  - {action.get('name')}:")
        print_wrapped(action.get('desc', 'No description available.'), indent=4)
        if 'attack_bonus' in action:
            print_wrapped(f"Attack Bonus: +{action['attack_bonus']}", indent=4)
        if 'damage' in action:
            dmg_str = ", ".join([f"{d.get('damage_dice')} {d.get('damage_type', '')}" for d in action.get('damage', [])])
            print_wrapped(f"Damage: {dmg_str}", indent=4)
        print("") # Newline for spacing

    print("="*80)

def main():
    """
    Main function to run the command-line tool.
    """
    # Set up argparse to handle command-line arguments.
    parser = argparse.ArgumentParser(description="Fetch D&D 5e monster stats from the SRD API.")
    parser.add_argument("monster_name", type=str, help="The name of the monster to look up (e.g., 'goblin', 'dire wolf').")
    
    args = parser.parse_args()
    
    # Process the input and run the main logic.
    monster_data = fetch_monster_data(args.monster_name)
    
    if monster_data:
        display_monster_info(monster_data)

if __name__ == "__main__":
    main()

