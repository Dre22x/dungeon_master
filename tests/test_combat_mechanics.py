#!/usr/bin/env python3
"""
Test script to verify the combat mechanics system functionality
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.game_mechanics import calculate_hp, start_combat, get_combat_state, update_combat_participant_hp, end_combat
from tools.character_data import create_character_data
from firestore.db_utils import create_campaign, save_character_to_campaign

def test_combat_mechanics():
    """Test the combat mechanics system"""
    
    print("=== Testing Combat Mechanics System ===")
    
    # Test 1: HP Calculation
    print("\n1. Testing HP calculation...")
    
    # Create test character data
    test_character = {
        'name': 'Test Fighter',
        'class': 'fighter',
        'level': 1,
        'ability_scores': {
            'Strength': 16,
            'Dexterity': 14,
            'Constitution': 15,
            'Intelligence': 10,
            'Wisdom': 12,
            'Charisma': 8
        }
    }
    
    hp = calculate_hp(test_character)
    print(f"Fighter HP (Level 1, CON 15): {hp}")
    
    # Test higher level character
    test_character['level'] = 3
    hp = calculate_hp(test_character)
    print(f"Fighter HP (Level 3, CON 15): {hp}")
    
    # Test wizard
    test_wizard = {
        'name': 'Test Wizard',
        'class': 'wizard',
        'level': 1,
        'ability_scores': {
            'Strength': 8,
            'Dexterity': 14,
            'Constitution': 12,
            'Intelligence': 16,
            'Wisdom': 10,
            'Charisma': 8
        }
    }
    
    hp = calculate_hp(test_wizard)
    print(f"Wizard HP (Level 1, CON 12): {hp}")
    
    # Test 2: Character Creation with HP
    print("\n2. Testing character creation with HP...")
    
    character_data = create_character_data(
        name="Thorin Ironfist",
        race="Dwarf",
        char_class="Fighter",
        level=1,
        background="Soldier",
        alignment="Lawful Good",
        ability_scores={"Strength": 16, "Dexterity": 14, "Constitution": 15, "Intelligence": 10, "Wisdom": 12, "Charisma": 8},
        skills=["Athletics", "Intimidation", "Perception", "Survival"],
        proficiencies=["All armor", "Shields", "Simple weapons", "Martial weapons"],
        equipment=["Longsword", "Shield", "Chain mail", "Crossbow, light", "20 bolts", "Explorer's pack"]
    )
    
    print(f"Character HP: {character_data.get('hit_points', 'Not calculated')}")
    print(f"Max HP: {character_data.get('max_hit_points', 'Not set')}")
    
    # Test 3: Combat State Management
    print("\n3. Testing combat state management...")
    
    # Create a test campaign
    campaign_id = "test_combat_campaign"
    create_result = create_campaign(campaign_id)
    print(f"Campaign creation: {create_result}")
    
    # Save test character
    save_result = save_character_to_campaign(campaign_id, character_data)
    print(f"Character save: {save_result}")
    
    # Test combat initialization with API monster
    print("\n4. Testing combat initialization with API monster...")
    combat_start = start_combat(campaign_id, ["Thorin Ironfist"], ["goblin"])
    print(f"Combat start: {combat_start}")
    
    # Test combat state retrieval
    print("\n5. Testing combat state retrieval...")
    combat_state = get_combat_state(campaign_id)
    if 'error' not in combat_state:
        print(f"Combat participants: {list(combat_state['characters'].keys())}")
        print(f"Monsters: {list(combat_state['monsters'].keys())}")
        print(f"Turn order: {combat_state['turn_order']}")
        print(f"Current round: {combat_state['round']}")
        
        # Check character HP
        thorin = combat_state['characters']['Thorin Ironfist']
        print(f"Thorin HP: {thorin.get('hit_points', 'Not set')}")
        
        # Check monster HP from API
        goblin = combat_state['monsters']['goblin']
        print(f"Goblin HP: {goblin.get('current_hit_points', 'Not set')}")
        print(f"Goblin AC: {goblin.get('armor_class', 'Not set')}")
    else:
        print(f"Error getting combat state: {combat_state['error']}")
    
    # Test HP updates
    print("\n6. Testing HP updates...")
    
    # Damage the goblin
    damage_result = update_combat_participant_hp(campaign_id, "goblin", 3)
    print(f"Goblin damage: {damage_result}")
    
    # Check updated state
    updated_state = get_combat_state(campaign_id)
    if 'error' not in updated_state:
        goblin = updated_state['monsters']['goblin']
        print(f"Goblin current HP: {goblin.get('current_hit_points', 'Not set')}")
    
    # Test death
    print("\n7. Testing death...")
    death_result = update_combat_participant_hp(campaign_id, "goblin", 0)
    print(f"Goblin death: {death_result}")
    
    # Test combat end
    print("\n8. Testing combat end...")
    combat_end = end_combat(campaign_id)
    print(f"Combat end: {combat_end}")
    
    # Test combat state after end
    final_state = get_combat_state(campaign_id)
    print(f"Final combat state: {final_state}")
    
    print("\n=== Combat Mechanics Test Complete ===")

if __name__ == "__main__":
    test_combat_mechanics() 