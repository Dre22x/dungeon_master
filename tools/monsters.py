import textwrap
from tools import _get_item_details, _fetch_index

# --- Monster Tools ---
def get_monster_details(monster_name: str) -> dict:
    """Tool to get the full SRD stat block for any monster."""
    return _get_item_details("monsters", monster_name)

def get_monster_by_challenge_rating(challenge_rating: str) -> dict:
    """Tool to get a monster by challenge rating."""
    return _fetch_index(f"monsters?challenge_rating={challenge_rating}")['results']


# --- Monster get_all tools ---
def get_all_monsters() -> list:
    """Tool to get all monsters."""
    return _fetch_index("monsters")['results']


# --- Display Monster Info ---
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
