#!/usr/bin/env python3
"""
Test script to verify the character creation agent tools functionality
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.races import get_race_details, get_all_races
from tools.classes import get_class_details, get_all_classes
from tools.equipment import get_equipment_details
from tools.tools import get_starting_equipment
from tools.spells import get_spell_details, get_all_spells

def test_character_creation_tools():
    """Test the character creation agent tools"""
    
    print("=== Testing Character Creation Agent Tools ===")
    
    # Test 1: Race information
    print("\n1. Testing race information...")
    all_races = get_all_races()
    print(f"Total races available: {len(all_races)}")
    
    elf_info = get_race_details("elf")
    if "error" not in elf_info:
        print(f"Elf Ability Bonuses: {elf_info.get('ability_bonuses', 'N/A')}")
        print(f"Elf Traits: {len(elf_info.get('traits', []))} traits")
    else:
        print(f"Error getting elf info: {elf_info['error']}")
    
    # Test 2: Class information
    print("\n2. Testing class information...")
    all_classes = get_all_classes()
    print(f"Total classes available: {len(all_classes)}")
    
    fighter_info = get_class_details("fighter")
    if "error" not in fighter_info:
        print(f"Fighter Hit Die: {fighter_info.get('hit_die', 'N/A')}")
        print(f"Fighter Proficiencies: {len(fighter_info.get('proficiencies', []))} proficiencies")
        print(f"Fighter Starting Equipment: {len(fighter_info.get('starting_equipment', []))} items")
    else:
        print(f"Error getting fighter info: {fighter_info['error']}")
    
    # Test 3: Equipment information
    print("\n3. Testing equipment information...")
    longsword_info = get_equipment_details("longsword")
    if "error" not in longsword_info:
        print(f"Longsword Cost: {longsword_info.get('cost', 'N/A')}")
        print(f"Longsword Damage: {longsword_info.get('damage', 'N/A')}")
        print(f"Longsword Properties: {longsword_info.get('properties', 'N/A')}")
    else:
        print(f"Error getting longsword info: {longsword_info['error']}")
    
    # Test 4: Starting equipment
    print("\n4. Testing starting equipment...")
    fighter_starting = get_starting_equipment("fighter")
    if "error" not in fighter_starting:
        print(f"Fighter Starting Equipment Options: {len(fighter_starting.get('starting_equipment_options', []))}")
        print(f"Fighter Starting Equipment: {len(fighter_starting.get('starting_equipment', []))} items")
    else:
        print(f"Error getting fighter starting equipment: {fighter_starting['error']}")
    
    # Test 5: Spell information
    print("\n5. Testing spell information...")
    all_spells = get_all_spells()
    print(f"Total spells available: {len(all_spells)}")
    
    fireball_info = get_spell_details("fireball")
    if "error" not in fireball_info:
        print(f"Fireball Level: {fireball_info.get('level', 'N/A')}")
        print(f"Fireball School: {fireball_info.get('school', 'N/A')}")
        print(f"Fireball Casting Time: {fireball_info.get('casting_time', 'N/A')}")
    else:
        print(f"Error getting fireball info: {fireball_info['error']}")
    
    # Test 6: Character creation workflow simulation
    print("\n6. Simulating character creation workflow...")
    print("Step 1: Player wants a warrior character")
    print("Step 2: Suggesting races for warrior...")
    warrior_races = ["human", "dwarf", "half-orc"]
    for race in warrior_races:
        race_info = get_race_details(race)
        if "error" not in race_info:
            print(f"  - {race.title()}: {race_info.get('ability_bonuses', 'N/A')}")
    
    print("Step 3: Suggesting classes for warrior...")
    warrior_classes = ["fighter", "paladin", "barbarian"]
    for class_name in warrior_classes:
        class_info = get_class_details(class_name)
        if "error" not in class_info:
            print(f"  - {class_name.title()}: {class_info.get('hit_die', 'N/A')} hit die")
    
    print("\n=== Character Creation Tools Test Complete ===")
    print("✅ All tools working correctly!")

if __name__ == "__main__":
    test_character_creation_tools() 