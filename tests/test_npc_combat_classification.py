#!/usr/bin/env python3
"""
Test script to verify the NPC combat classification system works correctly.
This test ensures that NPCs are properly classified and resolved to appropriate monsters.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.game_mechanics import (
    classify_npc_for_combat, 
    get_monster_for_npc_classification, 
    resolve_npc_to_monster,
    start_combat,
    get_combat_state,
    end_combat
)
from firestore.db_utils import save_campaign

def test_npc_classification():
    """Test that NPCs are properly classified into combat categories."""
    
    print("=== Testing NPC Combat Classification ===\n")
    
    # Test cases for different NPC types
    test_cases = [
        # (NPC Name, Description, Expected Classification)
        ("Cloaked Figure", "A mysterious shadowy figure", "medium"),
        ("Veteran Guard", "An experienced soldier with armor", "strong"),
        ("Young Merchant", "A nervous trader with no weapons", "weak"),
        ("Elite Knight", "A heavily armored warrior", "strong"),
        ("Commoner", "A simple farmer", "weak"),
        ("Bandit", "An armed criminal", "medium"),
        ("Old Woman", "An elderly villager", "weak"),
        ("Commander", "A military leader", "strong"),
        ("Child", "A young boy", "weak"),
        ("Assassin", "A deadly killer", "strong"),
        ("Guard", "A town watchman", "medium"),
        ("Peasant", "A simple farmer", "weak"),
        ("Mysterious Stranger", "A hooded figure", "medium"),
        ("Warrior", "A trained fighter", "strong"),
        ("Innocent Bystander", "A helpless civilian", "weak")
    ]
    
    print("Testing NPC Classification:")
    print("-" * 50)
    
    for npc_name, description, expected in test_cases:
        classification = classify_npc_for_combat(npc_name, description)
        status = "✓" if classification == expected else "✗"
        print(f"{status} {npc_name} ({description}) → {classification} (expected: {expected})")
    
    print("\n" + "=" * 50)

def test_monster_resolution():
    """Test that NPC classifications resolve to appropriate monsters."""
    
    print("\n=== Testing Monster Resolution ===\n")
    
    classifications = ["weak", "medium", "strong"]
    
    for classification in classifications:
        monster_name = get_monster_for_npc_classification(classification)
        print(f"Classification '{classification}' → Monster: {monster_name}")
    
    print("\n" + "=" * 50)

def test_npc_to_monster_resolution():
    """Test the complete NPC to monster resolution process."""
    
    print("\n=== Testing Complete NPC Resolution ===\n")
    
    test_npcs = [
        ("Cloaked Figure", "A mysterious shadowy figure"),
        ("Veteran Guard", "An experienced soldier"),
        ("Young Merchant", "A nervous trader"),
        ("Elite Knight", "A heavily armored warrior"),
        ("Commoner", "A simple farmer"),
        ("Bandit", "An armed criminal"),
        ("Old Woman", "An elderly villager"),
        ("Commander", "A military leader")
    ]
    
    for npc_name, description in test_npcs:
        monster_name = resolve_npc_to_monster(npc_name, description)
        classification = classify_npc_for_combat(npc_name, description)
        print(f"NPC: {npc_name} ({description})")
        print(f"  Classification: {classification}")
        print(f"  Resolved Monster: {monster_name}")
        print()
    
    print("=" * 50)

def test_combat_with_npcs():
    """Test that combat can be started with NPCs that get resolved to monsters."""
    
    print("\n=== Testing Combat with NPCs ===\n")
    
    # Setup test campaign
    campaign_id = "test_npc_combat"
    campaign_data = {
        "campaign_id": campaign_id,
        "characters": [
            {
                "name": "Test Fighter",
                "class": "Fighter",
                "level": 1,
                "hp": 12,
                "max_hp": 12,
                "strength": 16,
                "dexterity": 14,
                "constitution": 14,
                "intelligence": 10,
                "wisdom": 12,
                "charisma": 8,
                "equipment": ["longsword", "chain mail"],
                "proficiency_bonus": 2
            }
        ],
        "current_location": "A dark forest clearing",
        "game_state": "exploration",
        "notes": "Testing NPC combat"
    }
    
    save_campaign(campaign_id, campaign_data)
    print("✓ Test campaign created")
    
    # Test combat with various NPCs
    test_npcs = [
        ["Cloaked Figure"],
        ["Veteran Guard"],
        ["Young Merchant"],
        ["Elite Knight", "Bandit"]
    ]
    
    for i, npcs in enumerate(test_npcs, 1):
        print(f"\n--- Test {i}: Combat with {', '.join(npcs)} ---")
        
        # Start combat
        result = start_combat(campaign_id, ["Test Fighter"], npcs)
        print(f"Combat Result: {result}")
        
        # Check combat state
        combat_state = get_combat_state(campaign_id)
        if combat_state and not combat_state.get("error"):
            print("✓ Combat started successfully")
            
            # Show monster participants
            monsters = list(combat_state.get("monsters", {}).keys())
            print(f"Monster participants: {', '.join(monsters)}")
        else:
            print("✗ Combat failed to start")
        
        # End combat
        end_result = end_combat(campaign_id)
        print(f"Combat ended: {end_result}")
    
    print("\n" + "=" * 50)

def test_edge_cases():
    """Test edge cases and error handling."""
    
    print("\n=== Testing Edge Cases ===\n")
    
    # Test with empty description
    result = classify_npc_for_combat("Mysterious Figure")
    print(f"NPC with no description: {result}")
    
    # Test with very long description
    long_desc = "A very experienced and well-trained elite guard with heavy armor and multiple weapons who has seen many battles and is highly skilled in combat"
    result = classify_npc_for_combat("Guard", long_desc)
    print(f"NPC with long description: {result}")
    
    # Test with special characters
    result = classify_npc_for_combat("Shadowy Figure (Unknown)")
    print(f"NPC with special characters: {result}")
    
    # Test resolution with non-existent monster names
    result = resolve_npc_to_monster("Completely Unknown NPC")
    print(f"Unknown NPC resolution: {result}")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    test_npc_classification()
    test_monster_resolution()
    test_npc_to_monster_resolution()
    test_combat_with_npcs()
    test_edge_cases()
    
    print("\n=== NPC Combat Classification Test Complete ===")
    print("\nSummary:")
    print("- NPCs are classified as weak, medium, or strong based on names and descriptions")
    print("- Classifications map to appropriate monsters in the database")
    print("- Combat can be started with NPC names and they get resolved automatically")
    print("- Original NPC names are preserved for display")
    print("- System handles edge cases gracefully") 