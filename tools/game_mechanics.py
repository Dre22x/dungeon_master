from tools import _get_item_details, _fetch_index
import random
from typing import Dict, List, Optional

# Combat state storage
_combat_state: Dict[str, dict] = {}

# Combat result storage for agent handoff
_combat_results: Dict[str, dict] = {}

# NPC Combat Classification System
NPC_COMBAT_CLASSES = {
    "weak": {
        "description": "Commoners, children, elderly, unarmed civilians",
        "monster_mapping": ["commoner", "peasant", "child"],
        "hp_range": (4, 8),
        "ac_range": (10, 12),
        "damage_range": (1, 3)
    },
    "medium": {
        "description": "Guards, bandits, trained fighters, armed civilians",
        "monster_mapping": ["guard", "bandit", "thug", "scout"],
        "hp_range": (8, 16),
        "ac_range": (12, 15),
        "damage_range": (3, 8)
    },
    "strong": {
        "description": "Veterans, elite guards, experienced fighters, minor villains",
        "monster_mapping": ["veteran", "knight", "berserker", "assassin"],
        "hp_range": (16, 30),
        "ac_range": (15, 18),
        "damage_range": (8, 15)
    }
}

# --- Game Mechanics Tools ---
def get_condition_details(condition_name: str) -> dict:
    """Tool to get details for a specific condition."""
    return _get_item_details("conditions", condition_name)

def get_damage_type_details(damage_type_name: str) -> dict:
    """Tool to get details for a specific damage type."""
    return _get_item_details("damage-types", damage_type_name)

def calculate_hp(character_data: dict) -> int:
    """
    Calculate hit points for a character based on class, level, and constitution.
    
    Args:
        character_data: dict - Character data including class, level, and ability scores
    
    Returns:
        int - Calculated hit points
    """
    char_class = character_data.get('class', '').lower()
    level = character_data.get('level', 1)
    ability_scores = character_data.get('ability_scores', {})
    
    # Get constitution modifier
    constitution = ability_scores.get('Constitution', ability_scores.get('CON', 10))
    con_modifier = (constitution - 10) // 2
    
    # Class hit dice
    hit_dice = {
        'fighter': 10,
        'paladin': 10,
        'ranger': 10,
        'barbarian': 12,
        'wizard': 6,
        'sorcerer': 6,
        'warlock': 8,
        'cleric': 8,
        'druid': 8,
        'monk': 8,
        'rogue': 8,
        'bard': 8
    }
    
    # Get hit die for class
    die_size = hit_dice.get(char_class, 8)
    
    # Calculate HP: First level is max HP, subsequent levels are average + 1
    if level == 1:
        # First level: max HP
        hp = die_size + con_modifier
    else:
        # Subsequent levels: average HP (half die size + 1) + con modifier
        average_hp_per_level = (die_size // 2) + 1
        hp = die_size + con_modifier + (average_hp_per_level + con_modifier) * (level - 1)
    
    return max(1, hp)  # Minimum 1 HP

def start_combat(campaign_id: str, characters: List[str], monsters: List[str]) -> str:
    """
    Start a combat encounter and save participant information to memory.
    
    Args:
        campaign_id: str - The campaign ID
        characters: List[str] - List of character names participating in combat
        monsters: List[str] - List of monster names participating in combat
    
    Returns:
        str - Status message about combat initialization
    """
    from firestore.db_utils import load_character_from_campaign
    from tools.monsters import get_monster_details
    
    # Initialize combat state
    combat_data = {
        'campaign_id': campaign_id,
        'characters': {},
        'monsters': {},
        'turn_order': [],
        'current_turn': 0,
        'round': 1,
        'status': 'active'
    }
    
    # Load character data and calculate HP
    for char_name in characters:
        char_data = load_character_from_campaign(campaign_id, char_name)
        if 'error' not in char_data:
            # Calculate HP if not already present
            if 'hit_points' not in char_data:
                char_data['hit_points'] = calculate_hp(char_data)
                char_data['max_hit_points'] = char_data['hit_points']
            else:
                char_data['max_hit_points'] = char_data['hit_points']
            
            combat_data['characters'][char_name] = char_data
        else:
            return f"Error loading character {char_name}: {char_data['error']}"
    
    # Load monster data from API, with NPC resolution
    resolved_monsters = []
    for monster_name in monsters:
        # Try to resolve NPC names to appropriate monsters
        resolved_monster = resolve_npc_to_monster(monster_name)
        resolved_monsters.append(resolved_monster)
        
        monster_data = get_monster_details(resolved_monster)
        if 'error' not in monster_data:
            # Ensure monster has current HP tracking
            if 'hit_points' in monster_data:
                monster_data['current_hit_points'] = monster_data['hit_points']
                monster_data['max_hit_points'] = monster_data['hit_points']
            else:
                monster_data['current_hit_points'] = 10  # Default HP
                monster_data['max_hit_points'] = 10
            
            # Store with original name for display, but resolved monster data
            combat_data['monsters'][monster_name] = monster_data
        else:
            return f"Error loading monster {resolved_monster} (resolved from {monster_name}): {monster_data['error']}"
    
    # Generate turn order (simplified - characters first, then monsters)
    all_participants = list(combat_data['characters'].keys()) + list(combat_data['monsters'].keys())
    combat_data['turn_order'] = all_participants
    
    # Store combat state
    _combat_state[campaign_id] = combat_data
    
    # Create participant summary
    char_summary = ", ".join(characters) if characters else "None"
    monster_summary = ", ".join(monsters) if monsters else "None"
    
    # Add resolution info if any NPCs were resolved
    resolution_info = ""
    if resolved_monsters != monsters:
        resolution_info = f" (NPCs resolved to: {', '.join(resolved_monsters)})"
    
    return f"Combat started! Characters: {char_summary}. Monsters: {monster_summary}. Total participants: {len(all_participants)}{resolution_info}"

def get_combat_state(campaign_id: str) -> dict:
    """
    Get the current combat state for a campaign.
    
    Args:
        campaign_id: str - The campaign ID
    
    Returns:
        dict - Current combat state or error message
    """
    if campaign_id not in _combat_state:
        return {"error": f"No active combat found for campaign {campaign_id}"}
    
    return _combat_state[campaign_id]

def update_combat_participant_hp(campaign_id: str, participant_name: str, new_hp: int) -> str:
    """
    Update the hit points of a combat participant.
    
    Args:
        campaign_id: str - The campaign ID
        participant_name: str - Name of the participant
        new_hp: int - New hit point value
    
    Returns:
        str - Status message about the update
    """
    if campaign_id not in _combat_state:
        return f"Error: No active combat found for campaign {campaign_id}. Please ensure combat has been initiated with start_combat() before updating HP."
    
    combat_data = _combat_state[campaign_id]
    
    # Check if participant is a character
    if participant_name in combat_data['characters']:
        combat_data['characters'][participant_name]['hit_points'] = max(0, new_hp)
        participant_type = "character"
    # Check if participant is a monster
    elif participant_name in combat_data['monsters']:
        combat_data['monsters'][participant_name]['current_hit_points'] = max(0, new_hp)
        participant_type = "monster"
    else:
        return f"Error: Participant {participant_name} not found in combat"
    
    # Check for death
    if new_hp <= 0:
        return f"{participant_name} ({participant_type}) has been reduced to 0 HP and is unconscious/dead."
    else:
        return f"{participant_name} ({participant_type}) HP updated to {new_hp}."

def end_combat(campaign_id: str) -> str:
    """
    End the combat encounter and clear combat state.
    
    Args:
        campaign_id: str - The campaign ID
    
    Returns:
        str - Status message about combat ending
    """
    if campaign_id not in _combat_state:
        return f"Error: No active combat found for campaign {campaign_id}"
    
    combat_data = _combat_state[campaign_id]
    
    # Count survivors and casualties
    characters_alive = sum(1 for char in combat_data['characters'].values() if char.get('hit_points', 0) > 0)
    characters_dead = len(combat_data['characters']) - characters_alive
    
    monsters_alive = sum(1 for monster in combat_data['monsters'].values() if monster.get('current_hit_points', 0) > 0)
    monsters_dead = len(combat_data['monsters']) - monsters_alive
    
    # Clear combat state
    del _combat_state[campaign_id]
    
    return f"Combat ended. Characters: {characters_alive} alive, {characters_dead} dead. Monsters: {monsters_alive} alive, {monsters_dead} dead."

def get_next_turn(campaign_id: str) -> str:
    """
    Get the next participant in the turn order.
    
    Args:
        campaign_id: str - The campaign ID
    
    Returns:
        str - Name of the next participant or status message
    """
    if campaign_id not in _combat_state:
        return f"Error: No active combat found for campaign {campaign_id}"
    
    combat_data = _combat_state[campaign_id]
    turn_order = combat_data['turn_order']
    current_turn = combat_data['current_turn']
    
    if not turn_order:
        return "Error: No participants in combat"
    
    # Get next participant
    next_participant = turn_order[current_turn]
    
    # Check if participant is still alive
    if next_participant in combat_data['characters']:
        hp = combat_data['characters'][next_participant].get('hit_points', 0)
    else:
        hp = combat_data['monsters'][next_participant].get('current_hit_points', 0)
    
    if hp <= 0:
        # Skip dead participants
        combat_data['current_turn'] = (current_turn + 1) % len(turn_order)
        return get_next_turn(campaign_id)  # Recursive call to get next alive participant
    
    return f"Next turn: {next_participant} (HP: {hp})"

def advance_turn(campaign_id: str) -> str:
    """
    Advance to the next turn in combat.
    
    Args:
        campaign_id: str - The campaign ID
    
    Returns:
        str - Status message about turn advancement
    """
    if campaign_id not in _combat_state:
        return f"Error: No active combat found for campaign {campaign_id}. Please ensure combat has been initiated with start_combat() before calling advance_turn()."
    
    combat_data = _combat_state[campaign_id]
    turn_order = combat_data['turn_order']
    
    # Advance turn
    combat_data['current_turn'] = (combat_data['current_turn'] + 1) % len(turn_order)
    
    # Check if we've completed a round
    if combat_data['current_turn'] == 0:
        combat_data['round'] += 1
        return f"Round {combat_data['round']} begins. {get_next_turn(campaign_id)}"
    else:
        return f"Turn advanced. {get_next_turn(campaign_id)}"

# --- Game Mechanics get_all tools ---
def get_all_conditions() -> list[dict]:
    """Tool to get all conditions."""
    result = _fetch_index("conditions")
    return result.get('results', []) if isinstance(result, dict) else result

def get_all_damage_types() -> list[dict]:
    """Tool to get all damage types."""
    result = _fetch_index("damage-types")
    return result.get('results', []) if isinstance(result, dict) else result

def classify_npc_for_combat(npc_name: str, npc_description: str = "") -> str:
    """
    Classify an NPC into a combat category based on their name and description.
    
    Args:
        npc_name: str - The name of the NPC
        npc_description: str - Optional description of the NPC
    
    Returns:
        str - Combat classification: "weak", "medium", or "strong"
    """
    # Convert to lowercase for easier matching
    name_lower = npc_name.lower()
    desc_lower = npc_description.lower()
    combined_text = f"{name_lower} {desc_lower}"
    
    # Strong indicators
    strong_keywords = [
        "veteran", "elite", "knight", "paladin", "warrior", "fighter", "berserker",
        "assassin", "rogue", "wizard", "sorcerer", "warlock", "cleric", "druid",
        "commander", "captain", "leader", "boss", "villain", "enemy", "foe",
        "armored", "heavily armed", "well-equipped", "experienced", "trained",
        "guardian", "protector", "champion", "hero", "adventurer"
    ]
    
    # Medium indicators
    medium_keywords = [
        "guard", "soldier", "bandit", "thug", "scout", "hunter", "ranger",
        "mercenary", "fighter", "warrior", "armed", "weapon", "sword", "axe",
        "bow", "crossbow", "spear", "shield", "armor", "leather", "chain",
        "trained", "skilled", "experienced", "professional", "soldier"
    ]
    
    # Weak indicators
    weak_keywords = [
        "commoner", "peasant", "farmer", "merchant", "trader", "child", "elderly",
        "old", "young", "unarmed", "defenseless", "helpless", "innocent",
        "civilian", "villager", "townsfolk", "citizen", "resident", "worker",
        "laborer", "servant", "maid", "cook", "blacksmith", "carpenter"
    ]
    
    # Check for strong indicators first
    for keyword in strong_keywords:
        if keyword in combined_text:
            return "strong"
    
    # Check for medium indicators
    for keyword in medium_keywords:
        if keyword in combined_text:
            return "medium"
    
    # Check for weak indicators
    for keyword in weak_keywords:
        if keyword in combined_text:
            return "weak"
    
    # Default classification based on context clues
    if any(word in combined_text for word in ["figure", "person", "individual", "someone"]):
        # Generic person - likely medium unless context suggests otherwise
        if any(word in combined_text for word in ["cloaked", "hooded", "mysterious", "shadowy"]):
            return "medium"  # Mysterious figures are often medium threat
        else:
            return "weak"  # Generic person is likely weak
    
    # Default to medium for unknown NPCs
    return "medium"

def get_monster_for_npc_classification(classification: str) -> str:
    """
    Get an appropriate monster name for an NPC classification.
    
    Args:
        classification: str - The combat classification ("weak", "medium", "strong")
    
    Returns:
        str - A monster name that matches the classification
    """
    if classification not in NPC_COMBAT_CLASSES:
        return "commoner"  # Default fallback
    
    monster_options = NPC_COMBAT_CLASSES[classification]["monster_mapping"]
    
    # Try to find an available monster from the options
    from tools.monsters import get_monster_details
    
    for monster_name in monster_options:
        monster_data = get_monster_details(monster_name)
        if 'error' not in monster_data:
            return monster_name
    
    # If none of the preferred monsters are available, try common alternatives
    fallback_monsters = {
        "weak": ["commoner", "peasant"],
        "medium": ["guard", "bandit"],
        "strong": ["veteran", "knight"]
    }
    
    for monster_name in fallback_monsters.get(classification, ["commoner"]):
        monster_data = get_monster_details(monster_name)
        if 'error' not in monster_data:
            return monster_name
    
    # Ultimate fallback
    return "commoner"

def resolve_npc_to_monster(npc_name: str, npc_description: str = "") -> str:
    """
    Resolve an NPC name to an appropriate monster for combat.
    
    Args:
        npc_name: str - The name of the NPC
        npc_description: str - Optional description of the NPC
    
    Returns:
        str - The resolved monster name
    """
    classification = classify_npc_for_combat(npc_name, npc_description)
    return get_monster_for_npc_classification(classification)

def create_combat_result(campaign_id: str, action_type: str, attacker: str, target: str, 
                        attack_roll: int, attack_bonus: int, target_ac: int, 
                        hit: bool, damage: int = 0, damage_type: str = "", 
                        critical: bool = False, target_hp_before: int = 0, 
                        target_hp_after: int = 0, target_status: str = "alive",
                        additional_effects: Optional[dict] = None) -> str:
    """
    Create a structured combat result for handoff between agents.
    
    Args:
        campaign_id: str - The campaign ID
        action_type: str - Type of action (attack, spell, etc.)
        attacker: str - Name of the attacker
        target: str - Name of the target
        attack_roll: int - The attack roll result
        attack_bonus: int - The attack bonus
        target_ac: int - The target's armor class
        hit: bool - Whether the attack hit
        damage: int - Damage dealt (if hit)
        damage_type: str - Type of damage
        critical: bool - Whether it was a critical hit
        target_hp_before: int - Target's HP before the attack
        target_hp_after: int - Target's HP after the attack
        target_status: str - Target's status (alive, unconscious, dead)
        additional_effects: Optional[dict] - Any additional effects or conditions (defaults to empty dict if None)
    
    Returns:
        str - Success message
    """
    combat_result = {
        'campaign_id': campaign_id,
        'timestamp': 'now',  # Would be actual timestamp in production
        'action_type': action_type,
        'attacker': attacker,
        'target': target,
        'attack_roll': attack_roll,
        'attack_bonus': attack_bonus,
        'total_attack': attack_roll + attack_bonus,
        'target_ac': target_ac,
        'hit': hit,
        'damage': damage,
        'damage_type': damage_type,
        'critical': critical,
        'target_hp_before': target_hp_before,
        'target_hp_after': target_hp_after,
        'target_status': target_status,
        'additional_effects': additional_effects or {},
        'mechanical_summary': f"Attack: {attack_roll} + {attack_bonus} = {attack_roll + attack_bonus} vs AC {target_ac} ({'HIT' if hit else 'MISS'})"
    }
    
    if hit and damage > 0:
        combat_result['mechanical_summary'] += f" | Damage: {damage} {damage_type} | Target HP: {target_hp_after}/{target_hp_before}"
    
    if critical:
        combat_result['mechanical_summary'] += " | CRITICAL HIT!"
    
    _combat_results[campaign_id] = combat_result
    
    return f"Combat result created for {campaign_id}: {action_type} by {attacker} against {target}"

def get_combat_result(campaign_id: str) -> dict:
    """
    Get the most recent combat result for a campaign.
    
    Args:
        campaign_id: str - The campaign ID
    
    Returns:
        dict - The combat result or error message
    """
    if campaign_id not in _combat_results:
        return {"error": f"No combat result found for campaign {campaign_id}"}
    
    return _combat_results[campaign_id]

def clear_combat_result(campaign_id: str) -> str:
    """
    Clear the combat result for a campaign after it has been processed.
    
    Args:
        campaign_id: str - The campaign ID
    
    Returns:
        str - Success message
    """
    if campaign_id in _combat_results:
        del _combat_results[campaign_id]
        return f"Combat result cleared for campaign {campaign_id}"
    else:
        return f"No combat result to clear for campaign {campaign_id}"